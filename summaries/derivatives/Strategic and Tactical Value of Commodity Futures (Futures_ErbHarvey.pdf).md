# The Strategic and Tactical Value of Commodity Futures — Detailed Quantitative Research Notes

| Field | Detail |
|------|--------|
| **Authors** | Claude B. Erb, CFA (TCW); Campbell R. Harvey (Duke) |
| **Outlet** | *Financial Analysts Journal* 62(2), March/April 2006, pp. 69–97 (working paper: NBER WP 11222, 2005) |
| **Main sample** | 12 GSCI constituents plus GSCI and sectors, Dec 1982–May 2004 (monthly); GSCI back to Dec 1969; the 36-contract evidence cites Gorton–Rouwenhorst 1959–2004 |
| **Source file** | `Finance/Futures_ErbHarvey.pdf` |

---

## Thesis

History shows equity-like returns for commodity portfolios: GSCI 12.24% compound return vs 11.20% for the S&P 500 over Dec 1969–May 2004, with monthly correlation −0.03, and a 50/50 mix at 12.54% with 11.86% volatility. But the typical *individual* commodity future has had a geometric excess return of about zero. The gap between the two is explained mostly by the **diversification return** of rebalanced portfolios, plus weighting choices that happened to overweight winners (energy). Forward-looking expectations should therefore be built from components:
- a fairly reliable diversification return;
- uncertain spot and roll returns;
- optional tactical tilts (momentum, term structure) whose persistence is not guaranteed.

## Stylized facts

**Individual contracts.**
- Of Gorton–Rouwenhorst's 36 futures (1959–2004), 18 had positive and 18 negative geometric excess returns.
- The mean is −0.51% (cross-sectional SD 30.10%) and the median +0.03%. The average |t| is 0.8, and the only significant one is corn, *negative* (t = −2.25).
- Yet the rebalanced equal-weight (EW) portfolio earned about 4.5% excess, which is significant.

**Equal weighting is not "the asset class".**
- EW portfolios in the literature change composition over time, and futures have zero net market cap, so there is no natural market portfolio.
- Equity analogy: from 1970 to 2004 the EW Wilshire 5000 returned 20.3% vs 11.4% for cap-weighted.
- Indices are strategies: GSCI (production-weighted, unrebalanced, energy-heavy; about 28–29% crude by 2004 vs >50% cattle in the early 1970s), DJ-AIGCI (liquidity plus production, annual rebalance) and CRB (historically geometric equal-weight).
- Common window Jan 1991–May 2004: GSCI 6.81% (volatility 17.53%), DJ-AIGCI 7.83% (11.71%), CRB 3.64% (8.30%).
- **Backfill:** GSCI returned 15.3% over 1969–91 (backfilled) but only 7.0% over 1991–2004 (S&P 10.4%).

**Table 4 (Dec 1982–May 2004, geometric excess):**

| | Geom | σ | t | Sharpe |
|---|---:|---:|---:|---:|
| GSCI | 4.49% | 16.97% | 1.22 | 0.26 |
| Energy / Nonenergy | 7.06 / −0.12 | 31.23 / 9.87 | 1.05 / −0.06 | |
| Heating oil / Copper / Live cattle | 5.53 / 6.17 / 5.07 | | 0.79 / 1.11 / 1.68 | |
| Gold / Silver / Corn / Wheat / Coffee | −5.68 / −8.09 / −5.63 / −5.39 / −6.36 | | | |
| EW rebalanced (12) / buy-and-hold EW | 1.01 / 0.70 | 10.05 / 10.61 | | 0.10 / 0.07 |
| Average of the 12 | −1.71 | 25.16 | | |
| S&P 500 / Lehman Agg | 7.35 / 3.45 | 15.30 / 4.65 | 2.22 / 3.43 | 0.48 / 0.74 |

- Only 4 of the 12 had positive excess returns.
- Till's difficult-to-store group (heating oil, copper, live cattle, live hogs) averaged +3.5%, vs −4.3% for the rest.

**Heterogeneity (Table 5).**
- Average pairwise correlation is 0.09 (average absolute correlation 0.11). Average correlation with the GSCI is 0.20, and heating oil's average with the other 11 is 0.03.
- GSCI–energy correlation is 0.91. Within-group correlations are high (gold–silver 0.66, corn–soybeans 0.70).
- This is a "heterogeneous market of commodity futures", not a single asset class.

## Theories of the premium, and what the data say

- **CAPM** (Dusak; Kaplan–Lummer): zero expected excess return. But futures are not capital assets (Black 1976), and beta is a weak guide anyway.
- **Keynesian normal backwardation:** implies long positions earn a premium in every market, which is contradicted by the many negative individual returns (Kolb 1992: "normal backwardation is not normal"). Significant *portfolio* returns do not prove it, because rebalancing alone generates return.
- **Hedging pressure** (Cootner; Bessembinder 1992; de Roon et al. 2000): premia accrue to longs in backwardated markets (producers hedging) and shorts in contangoed ones (consumers hedging). This is more flexible, but hard to measure in practice.
- **Theory of storage:** $F=S(1+r-c)$ in the paper's example ($S=100$, $r=10\%$: $F=110$ when convenience yield $c=0$, $105$ at $c=5\%$, $95$ at $c=15\%$). Scarce inventories give a high convenience yield and backwardation, but the theory says nothing about *future* convenience yields.

## Return decomposition and the role of roll

- **Individual contract:** total return = cash + excess, and excess = spot + roll.
- **Portfolio:** total return = cash + weighted-average excess + diversification return.
- **Roll example (30 May 2004):** oil July 2004 at \$40.95 vs July 2005 at \$36.65 gives an 11.7% one-year roll yield if the curve is unchanged. Gold gives −1.4% (always in contango). Oil was backwardated about 66% of the time historically.
- **Cross-section (Table 6):** regressing compound excess returns on roll returns across the 12 commodities gives slope 1.20 (t = 10.97), intercept 0.89% (t = 1.84), adjusted $R^2 = 91.6\%$.
  - Positive-roll names averaged +4.22% excess vs −4.67% for negative-roll names, a gap of about 9 pp: 7.5 pp from roll and 1.4 pp from spot.
  - Corn illustrates the split: spot +1.57%, roll −7.19%.
- **Time series:** Spot drives volatility. Average spot SD is 26.76% vs 9.14% for roll, and corr(spot, roll) = −0.29.
- **Significance:** No individual commodity or sector has a significant average excess or spot return. On GSCI risk/return it would take about 57 years of data to reach significance, and about 78 years for energy.
- **Authors' own caution:** do not extrapolate roll returns; a risk-averse investor might assume future roll of zero or less.

## Inflation and other factors

- **GSCI vs unexpected inflation (1969–2003, annual):** GSCI excess = 0.083 + 6.50·ΔInflation, $R^2=0.43$. Unexpected inflation is proxied by the year-over-year change in inflation (its autocorrelation is 0.13).
- **Table 7 (1982–2003):**
  - GSCI ΔInflation beta 10.88 (t = 2.98), adjusted $R^2$ 28%.
  - Significant positive betas: energy (18.80), livestock, industrial metals (17.44), heating oil, cattle, copper.
  - Precious metals, gold and silver have significantly *negative* inflation-level betas.
  - The EW basket's beta is insignificant (3.88, t = 1.74).
- **Roll and inflation:** Average roll return explains 67% of the cross-section of unexpected-inflation betas. Hard-to-store, high-roll contracts were the better hedges, so inflation-hedging ability depends on portfolio composition.
- **CPI mismatch:** Energy is only about 4% of the CPI and food about 14%, so commodity futures are structurally poor CPI hedges.
- **Other factors:** No Fama–French five-factor exposure is significant. The GSCI has a significant negative beta to the trade-weighted dollar.

## Diversification return ("turning water into wine")

- **Definition:** portfolio geometric return minus the weighted-average constituent geometric return.
- **Table 8 example (heating oil + S&P 500, 1993–2003, annual rebalancing):**
  - Constituent geometric excess returns: 8.21% and 6.76%, averaging 7.49%.
  - The rebalanced 50/50 portfolio earned 10.95%, a diversification return of 3.46 pp. This equals half the variance reduction ($\tfrac12(11.44-4.52)$).
  - The unrebalanced portfolio gets a larger variance reduction (3.57) but a covariance drag of −3.48 (−2.51 from heating oil, −0.97 from the S&P), so its net diversification return is about zero.
- **Monthly example (heating oil + copper, 1982–2004, Table 9):** The rebalanced portfolio earned 7.86% vs a 5.85% weighted average (diversification return +2.01%). Buy-and-hold earned 5.86% (−0.03%).
- **Closed form** for an EW rebalanced portfolio with $K$ assets, average variance $\bar\sigma^2$ and average correlation $\bar\rho$ (serially uncorrelated returns):

$$\text{DR}\approx\tfrac12\Big(1-\tfrac1K\Big)\bar\sigma^2(1-\bar\rho).$$

  - Table 10: $K=30$, $\sigma=30\%$ gives 4.35% at $\rho=0$ and 3.05% at $\rho=0.3$. $\sigma=40\%$ gives about 5–7.7%.
  - Implied for the literature: Bodie–Rosansky (σ ≈ 40%, ρ ≈ 0.1) about 7%, i.e. nearly all of their 8.52%. Gorton–Rouwenhorst (σ ≈ 30%) 3.0–4.5%, i.e. nearly all of their 4.52%. De Chiara–Raab measured 2.8% for the DJ-AIGCI over 1991–2001.
- **General identity:** portfolio geometric return = weighted arithmetic return + impact of not rebalancing (covariance of weights with returns) − variance/2. A simulation (40 zero-mean assets, 45 years) gives 4.3% rebalanced vs 3.8% unrebalanced, and unrebalanced portfolios have lower return/risk ratios.

## Strategic allocation

- **Persistence:** Excess returns for Dec 1982–Sep 1993 vs Oct 1993–May 2004 have correlation 0.03 across GSCI, sectors and commodities. Only energy and industrial metals were positive in both halves. Rolling GSCI excess and roll returns trended down.
- **Building-block forecast:** about 3% diversification return (DJ-AIGCI-like) plus 0% spot and 0% roll gives about 3% expected excess. Reaching 5% requires a 2% bet on spot plus roll.
- **Forward-looking frontier:** stocks 5% excess, bonds 2%, 1969–2004 covariances. At 60/40 volatility (about 10.1%), a 3% commodity expectation implies an 18% allocation (60% stocks / 22% bonds); a 1% expectation implies 3%. The allocation is essentially a bet on the expected return.
- **Liability-hedging credit (Sharpe–Tint):** Relative to 10-year Treasuries it was mostly negative over 1982–2004, while many commodities had positive credits vs TIPS after 1997. The evidence on liability hedging is inconclusive.

## Tactical results (historical, as reported)

| Strategy | Excess (compound ann.) | Sharpe |
|---|---:|---:|
| GSCI long if trailing 12m excess > 0 (monthly returns, 1969–2004) | 13.47% (t 2.98) vs −5.49% when trailing < 0 | — |
| Best-4 momentum / worst-4 / long–short (1982–2004) | 7.0% / −3.4% / 10.8% | 0.45 / −0.21 / 0.55 |
| Individual-commodity trend following (long if 12m > 0, else short) | 6.54% | 0.85 |
| GSCI long if backwardated / long if contango (Jul 1992–May 2004) | 11.25% / −5.01% | 0.60 / −0.29 |
| GSCI long backwardated, short contango | 8.18% | 0.45 (vs long-only 2.68%, 0.15) |
| Long top-6 / short bottom-6 by nearby/next-nearby ratio (1982–2004) | 3.65% (σ 7.79%) | 0.47 |

- The GSCI momentum effect was strongest in 1969–82 (17.49%) but still present in 1982–2004 (11.34%, t = 2.10).
- The authors explicitly decline to claim persistence. Many long-only investors will not accept TAA exposure anyway.

## Assessment

- **Most durable contribution:** the accounting.
  - Separating the *average asset's* premium (about zero) from the *portfolio's* return (largely the rebalancing/variance-reduction term).
  - A closed-form diversification return, and the covariance-drag identity for unrebalanced portfolios.
  - This reframes the Bodie–Rosansky / Gorton–Rouwenhorst "equity-like premium" result: most of it can be mechanical.
  - The critique of backfilled index histories and composition drift is also important.
- **Caveats:**
  - The diversification return is not a risk premium. It is a volatility-harvesting term that assumes stable volatilities and correlations and no serial correlation. It is large only for high-volatility, low-correlation assets, and it drops sharply if commodity correlations rise, as they did during post-2004 financialization and in 2008.
  - The 12-commodity universe is small. The TAA tests are in-sample, cost-free and single-period, with arbitrary lookbacks, and the long–short term-structure test has only 6-versus-6 names.
  - The 91.6% cross-sectional $R^2$ is a 12-point regression of long-run averages, and excess ≈ spot + roll makes the roll–excess link partly mechanical when spot returns average near zero.
- **Later evidence:** The tactical signals (carry/basis and time-series momentum) held up in larger samples (Gorton–Hayashi–Rouwenhorst, Koijen et al., Moskowitz–Ooi–Pedersen), while long-only index returns after 2004 were poor, consistent with the paper's warning.
- **Practical use for a PM:**
  - Budget roughly 0–3% expected excess for a long-only diversified sleeve, and rebalance it deliberately.
  - Treat carry and momentum as separate risk-budgeted strategies.
  - Model commodities as a block-factor structure (energy, metals, grains, softs, livestock) rather than one beta.
  - Choose index weights knowing that the weighting scheme *is* the bet.
