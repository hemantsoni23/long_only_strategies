# Do Momentum Strategies Work?

**Stanley G. Eakins, Stanley R. Stansell · 2004 · Journal of Investing (Fall 2004), pp. 65–71 · Source file `Finance/AbnormalReturnsInvestmentsMomentum_Eakins_2004.pdf` · Data: monthly index values of 19 sectors (18 S&P 1500 Super Composite sectors / industry groups / industries + Wilshire REIT), Dec-1995 – Dec-2001 (73 months); supported by Rydex Global Advisors**

## Claim
A long-only rotation into the best-performing sector(s) over the past $L$ months gave a higher Sharpe ratio than the Dow, S&P 500 and Wilshire 5000 over 1995–2001. The best rule was 6-month lookback with 1-month hold (6L1H). The authors themselves show that the result depends on the Internet bubble, and that the "best" $L/H$ changes once that sector is dropped.

## Method
- **Universe:** energy, materials, staples, health care, financials, IT, utilities, transportation, retailing, banks, tech hardware, energy equipment, biotech, **Internet software & services**, consumer discretionary, communications equipment, metals & mining, capital goods, Wilshire REIT. The paper calls these "sector funds", but the data are index values: no fund fees, no tracking error.
- **Rule $L$L$H$H:** rank sectors on compounded return over the past $L$ months, buy the top-ranked sector (later the top $k$, equal-weighted, $k=1..18$), and hold for $H$ months. Seven rules: 1L1H, 3L1H, 6L1H, 12L1H, 3L3H, 6L3H, 6L6H. There is no skip month between ranking and holding.
- **Benchmarks:** equal-weighted 19-sector basket rebalanced monthly, S&P 500, Dow, Wilshire 5000.
- **Metric:** only the Sharpe ratio, $(R_p-R_f)/\sigma_p$, with annualised return, the 3-month T-bill as $R_f$, and SD of monthly returns (annualised). There are no significance tests, no factor alphas and no transaction costs. Beta-based measures are explicitly rejected because the portfolios are undiversified.

## Results
**Sector returns, Dec-1995 to Dec-2001 (Exhibit 1):** the Internet sector returned 727.8% cumulative (42.1% p.a., about twice any other sector). Next came retailing at 21.2% p.a. and biotech at 21.1%; the worst was metals & mining at −2.8%. The average sector returned 12.5% p.a., vs S&P 500 10.9%, Dow 11.8% and Wilshire 5000 9.5%.

**Single-sector strategies (Exhibit 2):**

| | EW 19 | Wilshire | S&P | Dow | 1L1H | 3L1H | 6L1H | 12L1H | 3L3H | 6L3H | 6L6H |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Ann. return % | 15.7 | 9.5 | 10.9 | 11.8 | 27.6 | 46.3 | **76.2** | 55.3 | 23.4 | 72.5 | 67.1 |
| Ann. SD % | 18.9 | 17.3 | 16.8 | 17.0 | 59.2 | 58.6 | 59.2 | 63.5 | 51.8 | 59.9 | 60.7 |
| Sharpe | 0.83 | 0.27 | 0.36 | 0.41 | 0.47 | 0.71 | **1.20** | 0.79 | 0.36 | 1.13 | 1.03 |

- Cumulative return of 6L1H: 2914%, vs 86.4% for the S&P 500. 9L1H (not tabulated) has Sharpe 0.94.
- Ranking of lookbacks: 6 months > 12 months > 3 months > 1 month. The 6-month rules dominate at every holding period.
- Volatility runs at about 3.5× the index level (SD ≈ 52–64%).

**By year (Exhibit 3):**
- The S&P beat every momentum rule in 1996. In 1998 every momentum rule beat it by a wide margin, because the models held the Internet sector every month that year (6L1H Sharpe 6.98).
- The best rule beats the S&P in 4 of 6 years.
- In the 2000–2001 bust, most rules have negative Sharpe ratios comparable to or less negative than the S&P (e.g. 6L1H −0.15 in 2000 vs S&P −0.92), because they rotated out of Internet.

**Top-$k$ sectors (Exhibits 4–5):**
- Short lookbacks (1L1H, 3L1H, 3L3H) improve with 2 sectors.
- Long lookbacks (6L1H, 12L1H, 6L3H, 6L6H) are best with 1 sector. Adding the second sector cuts return faster than SD, so the Sharpe ratio falls; beyond 2 sectors it is roughly flat.
- The reason: long lookbacks kept selecting the Internet sector in 1997–1999 (in 31 of the 73 months), and any diversification dilutes it.

**Internet sector removed (Exhibit 6, full-period Sharpe):**

| 1L1H | 3L1H | 6L1H | 12L1H | 3L3H | 6L3H | 6L6H |
|---|---|---|---|---|---|---|
| 0.10 | 0.18 | 0.18 | 0.03 | **0.63** | 0.43 | 0.02 |

- Sharpe ratios collapse: 6L1H falls from 1.20 to 0.18 (return 10.5% at SD 30.9%).
- The best rule becomes 3L3H, the only one that improves (+0.28). Short lookbacks now do better than long ones.
- The authors note that benchmarks cannot be compared directly here, since they contain Internet stocks.

## Critical assessment
- **Essentially one bubble episode.** Six years and 73 overlapping-ranking months, with most of the profit from holding one sector through 1997–1999. There is no statistical inference; with ~60% annual vol, a Sharpe gap of 0.8 over 6 years is not distinguishable from noise.
- **Data mining over $L/H$.** The optimum moves from 6L1H to 3L3H when one sector is removed, which the authors acknowledge undermines any recommended rule.
- **Inconsistencies in the paper:**
  - The equal-weighted 19-sector basket's reported Sharpe of 0.83 equals return/SD with no T-bill subtracted (15.7/18.9). It is inconsistent with the other Sharpe ratios; with $R_f$ subtracted it would be much lower. Even at face value it beats 5 of the 7 momentum rules, so the claim that "most" strategies beat the benchmarks holds only against the cap-weighted indices.
  - Full-period benchmark Sharpes differ between Exhibits 2 and 3 (Dow 0.41 vs 0.35; Wilshire 0.27 vs 0.24).
  - Exhibit 6's text says "January 1, 1995"; the sample starts Dec-1995.
  - Exhibit 3 omits 6L3H, and Exhibit 6 mislabels it "6L3M".
- **Not modelled:** trading costs, fund loads or redemption fees, taxes, and the survivorship and backfill of the sector index menu. Using an ex-post-selected sector list that includes Internet (a sector that was tiny in 1995) adds look-ahead flavour.

## Practical relevance for a quant PM
- It illustrates why concentrated top-1 sector rotation is a vol-and-luck machine rather than a factor. Use broader industry momentum (e.g. Moskowitz–Grinblatt), top-$k$ with $k$ well above 1, or risk-scaled weights, and evaluate across multiple bubbles and busts.
- The one robust takeaway is qualitative: intermediate lookbacks of 3–12 months, and fast exits during reversals, helped avoid the 2000–01 drawdown.
- Use it as a cautionary example for backtests dominated by a single asset: always rerun excluding the top contributor.
