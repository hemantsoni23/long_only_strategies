# Liquidity as an Investment Style — Ibbotson, Chen, Kim & Hu (2013)

| Field | Detail |
|------|--------|
| **Authors** | Roger G. Ibbotson (Yale SOM; chairman/CIO, Zebra Capital); Zhiwu Chen (Yale SOM); Daniel Y.-J. Kim (Zebra Capital); Wendy Y. Hu (Permal) |
| **Journal** | *Financial Analysts Journal* 69(3), May/June 2013, pp. 30–44 |
| **Sample** | NYSE/Amex/NASDAQ (CRSP + Compustat); selection years 1971–2010, performance years 1972–2011 |
| **Liquidity metric** | Annual share turnover (sum of 12 monthly volume/shares outstanding); NASDAQ volume deflated per Anderson–Dyl |
| **Source file** | `Finance/AbnormalReturnLiquidity_IbbotsonChenKimHu_2013.pdf` (Drive id `0B-6kBz0I0dMsNnQyYk1HTVBkcEU`) |

---

## Claim

Stock liquidity, measured by turnover, should be treated as an investment style on a par with size, value/growth and momentum. The test is Sharpe's (1992) four criteria for a benchmark style: (1) identifiable before the fact, (2) not easily beaten, (3) a viable alternative, (4) low in cost. The authors argue that turnover meets all four. Their motivation is that the literature since Amihud–Mendelson (1986) finds an illiquidity premium, yet liquidity is rarely used as a control (Subrahmanyam 2010). They do not claim turnover is the best liquidity measure, only that it is simple and works (cf. Idzorek–Xiong–Ibbotson 2012 on mutual funds).

## Design

**Universe (Appendix A).**
- Exclusions: REITs, warrants, ADRs, ETFs, Americus Trust components and closed-end funds.
- Requirements: all 12 months of volume, return, earnings, shares and price data in the selection year.
- Size filters: year-end price at least \$2, market cap within the largest 3,500 and above \$5m.
- Resulting sample: about 1,600–1,900 names per year until 1982, then about 3,500 from 1983. The average is 2,969 stocks a year, or about 742 per quartile.

**Sorting variables (all measured in the selection year).**
- Turnover.
- Year-end market cap.
- Trailing E/P, using the four most recent quarters of EPS, the latest quarter ending at least two months before formation.
- 12-month return.

**Portfolios.** Quartiles are formed each December. Portfolios are **equal-weighted**, bought at the start of the performance year and held passively. Delisted stocks go to cash for the rest of the year.

**Factor tests.**
- LMH = the low-turnover quartile minus the high-turnover quartile (equal-weighted, dollar-neutral).
- LMH and the low-liquidity long portfolio are regressed on the CAPM, FF3 and FF3+WML. The right-hand-side factors are Ken French's, which use B/M for value rather than E/P.
- A Daniel–Titman (1998) characteristic-versus-covariance double sort.
- Year-to-year migration matrices.

## Results

**Single sorts (Table 1, EW, 1972–2011).**

| Style | Q1 geo / arith / SD | Q4 geo / arith / SD |
|---|---|---|
| Size (Q1 micro) | 13.04 / 16.42 / 27.29 | 10.98 / 12.61 / 18.35 |
| Value, E/P (Q1 value) | 16.13 / 18.59 / 23.31 | 7.62 / 11.56 / 29.42 |
| Momentum (Q1 winners) | 12.85 / 15.37 / 23.46 | 7.18 / 11.16 / 29.49 |
| Liquidity (Q1 low) | **14.50 / 16.38 / 20.41** | 7.24 / 11.04 / 28.48 |
| Universe (EW) | 12.15 / 14.46 / 22.39 | |

- Liquidity is monotone across quartiles: 14.50, 13.97, 11.91, 7.24.
- Momentum is not monotone at the top: Q2 earns 14.25 against 12.85 for Q1.
- Returns and risk run in opposite directions for liquidity: the low-turnover quartile has the highest return and the lowest SD. The authors attribute this to trading costs, not risk.
- Low liquidity beats micro-cap and high momentum on cumulative wealth and trails only high value (Figure 1).

**Double sorts (geometric means, %).**

| | Low liq | Mid-low | Mid-high | High liq |
|---|---|---|---|---|
| Micro | 15.36 | 16.21 | 9.94 | **1.32** |
| Large | 11.53 | 11.66 | 11.19 | 8.37 |
| High value (high E/P) | **18.43** | 16.69 | 15.97 | 9.98 |
| High growth | 9.99 | 12.32 | 8.39 | **2.24** |
| Winners | 16.03 | 15.18 | 12.97 | 8.53 |
| Losers | 10.30 | 9.62 | 7.52 | **3.03** |

- **Size.** The liquidity spread is present in every size quartile. It falls from micro (about 14 percentage points) to large (3.16 pp). The size effect disappears within the high-turnover quartile.
- **Value.** Within value and growth the liquidity spread is about 8 pp. The best cell is high value / low liquidity at 18.43%; the worst is high growth / high liquidity at 2.24%.
- **Momentum.** Winners / low liquidity earn 16.03%; losers / high liquidity earn 3.03%.
- **Where the spread comes from.** Much of it is the collapse of the high-turnover column, not a rise in the low-turnover column. In the micro row, mid-low liquidity (16.21%) beats low liquidity (15.36%).

**Factor regressions (Table 5, monthly, N = 480, t-statistics in parentheses).**

| | α (%/mo) | β_MKT | SMB | HML | WML | adj. R² |
|---|---|---|---|---|---|---|
| LMH, CAPM | 0.66 (4.52) | −0.66 | | | | 48.0 |
| LMH, FF3 | 0.44 (3.93) | −0.47 | −0.39 | 0.54 | | 70.4 |
| LMH, 4F | 0.31 (2.80) | −0.45 | −0.39 | 0.58 | 0.14 (5.54) | 72.2 |
| Low-liq long, CAPM | 0.45 (3.97) | 0.75 | | | | 67.4 |
| Low-liq long, FF3 | 0.16 (2.41) | 0.73 | 0.56 | 0.44 | | 88.2 |
| Low-liq long, 4F | 0.16 (2.30) | 0.74 | 0.56 | 0.44 | 0.00 | 88.2 |

The four-factor alpha of LMH is about 3.7% a year; for the long-only portfolio it is about 1.9% a year. Correlations of LMH with the other factors (Table 6): MKT −0.694, SMB −0.503, HML +0.594, WML +0.139. It is the most negatively market-correlated factor in the set.

**Combined-style longs (Table 7).** The regressions cover micro/low-liq, high-value/low-liq and winners/low-liq.
- CAPM alphas are 0.54, 0.75 and 0.55 %/mo, with betas of 0.71–0.84.
- High-value/low-liq keeps a four-factor alpha of 0.44 %/mo (t = 4.88).
- The two borderline cases are four-factor alphas: micro/low-liq 0.20 (t = 1.85) and winners/low-liq 0.14 (t = 1.52).

**Characteristic vs covariance (Table 8, Figure 3).** Stocks are sorted independently on turnover and on $\beta_{LMH}$, estimated from 12 selection-year monthly returns in excess of the universe. Returns line up with the turnover columns but vary weakly and non-monotonically across the $\beta$ rows. The decisive off-diagonal cells:
- low turnover but high-turnover-like covariance ($\beta_{LMH}$ low): 13.49%;
- high turnover but low-turnover-like covariance ($\beta_{LMH}$ high): 6.43%.

So the characteristic, not the loading, prices returns, in parallel with Daniel–Titman on value. A 12-month beta is noisy, which biases this test in favour of the characteristic.

**Stability and migration (Tables 9–10).**
- Share of stocks staying in the same quartile next year: liquidity 62.93% (low-liquidity quartile 77.28%, high 71.33%), size 78.73%, value 51.63%, momentum 29.03%.
- The authors use this persistence, rather than measured trading costs, to argue "low in cost". For net-of-cost evidence they defer to Idzorek–Xiong–Ibbotson (2012).
- Mean arithmetic returns by migration cell are large: low→high liquidity +109.43%, low→low +9.81%, high→low −5.89%, high→high +14.41%.
- The authors state that migration is not known ex ante. The migration table shows that liquidity changes coincide with repricing (cf. Fama–French 2007, "Migration"); it is not a trading rule.

## Assessment

**Convincing.**
- The turnover–return relation is large, monotone across quartiles, and holds within every size, value and momentum quartile over 40 years.
- It leaves significant alpha against FF3/4F, both long–short and long-only.
- The characteristic-over-covariance result is clean.
- Lower volatility and lower beta for low-turnover stocks rule out a simple risk-premium story.

**Fragile or missing.**
- *Weighting and benchmarks.* Portfolios are equal-weighted, and micro-caps dominate the extreme cells. LMH is an EW quartile spread regressed on value-weighted French factors, which inflates the apparent alpha relative to a like-for-like benchmark. The large-cap row (3.16 pp) is the relevant number for capacity.
- *Short-leg concentration.* The spread is concentrated in high-turnover losers and growth stocks (1–3% a year). High turnover proxies for disagreement/speculation, idiosyncratic volatility and lottery demand (Baker–Stein, Ang et al., Bali et al.). The paper never controls for volatility or beta, so its overlap with low-volatility/BAB effects is untested. The lower SD and beta of low-turnover portfolios suggest the overlap is substantial.
- *Turnover over time.* Turnover is not normalized for the secular rise in trading volume. It is ranked cross-sectionally each year, which mitigates the problem, but the measure's meaning shifts over 1971–2011.
- *Cost evidence.* Nothing on trading costs, capacity or implementation is shown here. "Low cost" rests only on quartile persistence.
- *Value definition.* Value is E/P in the sorts but B/M in the regressions.
- *Conflict of interest.* Two authors are at Zebra Capital, which manages liquidity-style strategies.

**Practical relevance.**
- Low turnover, or turnover residualized on size, is a cheap, persistent characteristic that combines additively with value and momentum and carries negative market beta as a long–short factor.
- For a quant PM, the useful questions are how much survives controls for idiosyncratic volatility, beta and short interest, and whether it survives value-weighting in large caps.
- The characteristic-versus-covariance result argues for using turnover as a signal. Treating an Amihud or Pástor–Stambaugh loading as a substitute would miss it.

## Relation to literature

- **Amihud–Mendelson (1986), Brennan–Subrahmanyam (1996), Amihud (2002):** other liquidity measures.
- **Haugen–Baker (1996), Datar–Naik–Radcliffe (1998):** earlier turnover–return evidence.
- **Pástor–Stambaugh (2003); Lou–Sadka (2011):** liquidity risk versus liquidity level. This paper is about level.
- **Daniel–Titman (1998):** the characteristics-versus-covariances methodology.
- **Fama–French (2007):** migration.
- **Idzorek–Xiong–Ibbotson (2012):** the companion mutual-fund evidence, net of costs.
