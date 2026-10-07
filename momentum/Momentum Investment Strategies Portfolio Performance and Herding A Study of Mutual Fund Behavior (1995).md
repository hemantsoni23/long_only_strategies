# Momentum Investment Strategies, Portfolio Performance, and Herding: A Study of Mutual Fund Behavior

**Mark Grinblatt, Sheridan Titman, Russ Wermers · 1995 · *American Economic Review* 85(5), 1088–1105 · Source file `Finance/AbnormalReturnsInvestmentsMomentum_GrinblattTitmanWermers_1995.pdf` (JSTOR image scan; text obtained by OCR) · CDA quarterly holdings of 274 funds alive on 31 Dec 1974, of which 155 survive to Dec 1984 and are used for momentum/performance; all 274 used for stock-level herding. NYSE/AMEX stocks with CRSP returns; OTC and fixed-income holdings treated as missing.**

## Claim
Holdings data show that most mutual funds are **momentum investors**: 77% (119/155) tilt toward recent winners. The tilt comes almost entirely from **buying winners** (mostly large caps), not from selling losers. Momentum funds earn significantly higher benchmark-free performance than contrarian funds. **Herding** (many funds trading the same stock in the same direction) is statistically present but economically small. Its link to performance disappears once momentum is controlled for. Implication: part of the fund "skill" found in Grinblatt–Titman (1989, 1993) may just be a mechanical Jegadeesh–Titman momentum rule.

## Measures
**Momentum measure (holdings-based)**, lag $k$, with 41 quarterly holdings × 3 monthly returns:
$$M_k=\frac1{120}\sum_{t=1}^{40}\sum_{i=1}^{3}\sum_{j=1}^{N}\big(w_{j,3t}-w_{j,3t-3}\big)\,R_{j,3t-3k+i}.$$
This is the benchmark-period return of the current minus the previous portfolio.
- **L0M** ($k=1$): returns in the same quarter as the revision. **L1M** ($k=2$): the prior quarter. L2M–L4M are also computed.
- **Passive-drift fix:** weights are computed using the *average of beginning- and end-of-quarter prices*, so buy-and-hold does not register as momentum. The authors argue that intra-quarter trade timing introduces no systematic bias.
- **Buy/Sell L0M:** partial sums over $w_{j,3t}>w_{j,3t-3}$ (buys) and $<$ (sells), with returns demeaned by the stock's return 12 months ahead as a proxy for its expected return.
- **TAL0M** (turnover-adjusted): revisions normalised so that \$1 is bought and \$1 is sold each quarter.
- **Inference:** time-series t on the 120 monthly differences. Cross-sectional regressions use Grinblatt–Titman (1994) time-series-based t/F, because residuals are correlated across funds.

**Performance (Grinblatt–Titman 1993, benchmark-free):** a zero-investment portfolio of the 4-quarter change in weights times next-quarter returns,
$$\alpha=\frac1{111}\sum_{t=1}^{37}\sum_{i=1}^{3}\sum_{j=1}^{N}(w_{j,3t+9}-w_{j,3t-3})R_{j,3t+9+i},$$
which assumes the current and lagged portfolios have equal betas.

**Herding (Lakonishok–Shleifer–Vishny):**
$$UHM_{it}=|p_{it}-\bar p_t|-E|p_{it}-\bar p_t|,$$
where $p_{it}$ is the share of trading funds that buy stock $i$ in quarter $t$ and the adjustment term comes from a binomial null.
- **Signed stock measure** $SHM_{it}=I_{it}\,UHM_{it}-E[I\cdot UHM]$: $I=+1$ if the fund trades with the herd and $-1$ if against. It is set to 0 when fewer than 10 funds trade or when herding is negative.
- **Fund herding measure:** $FHM=\frac1{120}\sum(w_{j,3t}-w_{j,3t-3})SHM_{j,t}$.

## Results
**Momentum by objective (Table 1, % per quarter; t in parentheses)**
| | All (155) | Aggr. growth (45) | Growth (44) | Growth-income (37) | Balanced (10) | Income (13) |
|---|---|---|---|---|---|---|
| L0M | **0.74 (10.96)** | 1.25 (9.80) | 0.89 (10.71) | 0.32 (6.33) | 0.29 (3.83) | 0.17 (1.63) |
| % funds positive | 76.8 | 88.9 | 81.8 | 67.6 | 60.0 | 61.5 |
| Buy L0M | 1.03 (2.63) | 1.53 (2.90) | 1.07 (2.65) | 0.64 (2.14) | 0.50 (1.76) | 0.69 (2.08) |
| Sell L0M | −0.29 (−0.86) | −0.40 | −0.13 | −0.31 | −0.12 | −0.51 |
| L1M | 0.30 (5.46) | 0.53 (4.18) | 0.43 (6.16) | −0.04 | −0.02 | 0.03 |
| TAL0M | 2.07 (9.50) | 3.39 (9.75) | 2.98 (9.27) | 0.54 (1.71) | 0.60 (1.16) | 0.14 (0.36) |

- F-tests reject both L0M = 0 in all categories (F = 51.57) and equality of L0M across categories (F = 18.24).
- Sell L0M is insignificant everywhere (joint F = 0.62). **Momentum = buying winners.**
- Buy TAL0M is 2.31% per quarter. The top 10 funds by TAL0M buy stocks whose returns exceed those of the stocks they sell by more than 8% per quarter; the top 25, by about 6%.
- The tilt is **persistent**: winner-buyers in 1975–79 are more likely to be winner-buyers in 1980–84.
- L0M and L1M are correlated (≈0.65).
- **Almost all of the Buy L0M contribution comes from large-cap past winners**, and there is no significant loser-selling in any size decile.

**Momentum vs performance (Tables 2–3)**
- **Split on L0M:** 119 momentum funds earn **2.61% per year** (t 3.25) versus 0.15% (t 0.51) for 36 contrarians. The long-momentum/short-contrarian differenced portfolio earns 2.46% per year (t 3.32). Aggressive growth: 3.75% vs 0.63%.
- **Split on L1M:** 91 momentum funds earn 2.79% vs 0.97% for 64 contrarians. The differenced portfolio earns 1.81% (t 2.44).
- **Cross-sectional regressions** with objective dummies: performance on L0M has slope 1.27 (t 2.67), i.e. +1%/qtr of L0M adds about 1.27%/yr of performance; on L1M, 1.20 (t 2.02). L0M carries the explanatory power, and L1M–L4M add nothing.
  - Controlling for Buy L0M, neither L0M nor Sell L0M matters.
  - Buy L0M dominates Buy L1M: 1.33 (t 2.48) vs 0.44 (t 0.71).
- **Gross returns** (not risk-adjusted): momentum funds 17.9% per year, contrarians 17.2%, CRSP VW 14.7%. The top L0M quintile earns 19.0% versus 17.5% for the bottom quintile.
  - The risk-adjusted gap (≈2.5%) exceeds the gross gap (0.7%) because contrarians hold smaller, riskier stocks.
- Performance survives with a 4-quarter lag in the benchmark but is small with a 1-quarter lag. Picks therefore pay off over the following year, not just the first quarter.

**Herding (Tables 4–6)**
- **All 274 funds, all stock-quarters:** UHM = **2.5%**, similar to LSV's 2.7% for pension funds. That is, of 100 funds trading a stock, 2.5 more than chance trade on the same side.
  - Buy-side herding is stronger for past winners (2.51%) than for past losers. Sell-side herding (3.14% overall) is less related to past returns.
- **Conditioning on activity:**
  - With at least 5 funds trading: UHM = 4.32%.
  - With at least 10: UHM = **5.50%**.
  - Aggressive-growth funds with at least 10 trading: 8.23%.
  - Herding is *weaker* within objective subgroups when all stock-quarters are used.
- **FHM:** 0.84% overall, t = 6.73, significant in all categories. For a fund turning over 10% of its portfolio per quarter, this means buying stocks with ≈8.4% excess buying by the other funds. Aggressive growth: 1.05%.
- **Performance on FHM alone:** slope 1.61 (t 2.82), adj. $R^2$ 0.25.
- **Adding L0M:** L0M 1.24 (t 2.23) and **FHM 0.12 (t 0.20)**. Herding does not add to momentum: performing funds buy past winners, and herding into winners is a by-product.

## Critical assessment
- **Strength.** Direct holdings evidence, sharper than regressing fund returns on a momentum factor. The buy/sell asymmetry and the large-cap concentration are clean facts.
  - The performance link is almost *mechanical*: the Grinblatt–Titman measure rewards holding recent winners in the Jegadeesh–Titman period, and the authors say so. The paper shows fund alpha overlaps with momentum; it does not show managers had information.
- **Caveats.**
  - Survivorship: only surviving funds are used for momentum/performance. The authors cite evidence that the effect on inference is small.
  - The sample is short (1975–84, 10 years), with no costs or fees.
  - OTC holdings are dropped.
  - The Buy/Sell split uses a noisy expected-return proxy (the return 12 months ahead).
  - Quarterly snapshots miss intra-quarter round trips.
  - The objective categories for special-purpose and venture funds contain only 3 funds each.
- Table 3's reported $R^2$ for the single-regressor L0M model (0.03) looks odd next to the others (≈0.3–0.4), even though all regressions include category dummies. It may be an OCR or print artefact.

## Practical relevance for a quant PM
- Institutional momentum demand is **one-sided** (buying large-cap winners). This is a mechanism for crowding on the long leg of momentum; losers are not systematically dumped by long-only funds.
- The holdings-based L0M/TAL0M and LSV/FHM statistics are reusable on 13F or N-PORT data to measure fund style, crowding, and whether a manager's alpha is just a momentum tilt. **Control for momentum before crediting selection skill.**
- Herding is modest on average but material in heavily traded names (≈5.5% with at least 10 funds active), which is where crowding risk concentrates.
