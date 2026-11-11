# Commodity Futures Prices: Forecast Power, Premiums, and the Theory of Storage (Fama–French 1987) — Detailed Quantitative Research Notes

**Eugene F. Fama, Kenneth R. French (University of Chicago)** · *Journal of Business* 60(1), January 1987, pp. 55–73 (JSTOR 2352947) · Support: NSF (Fama), Chicago Board of Trade (French) · Source file: `Finance/Futures_FamaFrench_1987.pdf`

---

## Question

There are two standard views of the basis $F(t,T)-S(t)$:

1. **Theory of storage** (Kaldor, Working, Brennan, Telser): the basis equals interest forgone plus marginal warehousing cost minus marginal convenience yield. This view is uncontroversial.
2. **Premium + forecast** (Keynes/Hicks normal backwardation, Cootner, Dusak, Breeden, Hazuka): the basis is an expected premium plus an expected spot change. Whether either component is non-zero is long disputed.

FF test both on 21 commodities. The paper's point is that the two views describe the same economics but pose very different statistical problems. With the basis on the left-hand side, storage effects are easy to detect. With realised spot changes or premiums on the left-hand side, the signal is buried in spot-price noise. Abstract headline: forecast power for 10 of 21 commodities, time-varying premiums for 5.

## Setup

**Storage relation:**
$$\frac{F(t,T)-S(t)}{S(t)} = R(t,T) + \frac{W(t,T)-C(t,T)}{S(t)} \tag{2}$$
Here $R$ is the interest rate, $W$ the marginal storage cost, and $C$ the marginal convenience yield, which falls as inventories rise. Inventory data are mostly unavailable, so seasonal dummies stand in for seasonal convenience yield.

**Storage regression:**
$$\frac{F(t,T)-S(t)}{S(t)} = \sum_{m=1}^{12} a_m d_m + \beta R(t,T) + e \tag{3}$$
Prediction: $\beta=1$ for any continuously stored commodity. The paper calls these "apparently the first" systematic tests of this implication.

**Premium/forecast split (Fama 1984 method):**
$$F-S(t) = \mathbb{E}_t[P(t,T)] + \mathbb{E}_t[S(T)-S(t)],\qquad \mathbb{E}_t[P]=F(t,T)-\mathbb{E}_t[S(T)]$$
$$S(T)-S(t) = a_1 + b_1[F-S(t)] + u \tag{6}$$
$$F(t,T)-S(T) = a_2 + b_2[F-S(t)] + z \tag{7}$$
In logs, $b_1+b_2=1$ identically (and $a_1+a_2=0$). $b_1>0$ means the basis forecasts the spot change; $b_2>0$ means expected premiums vary over time. The adding-up means all basis variation is always allocated somewhere, so misallocation is a real risk:
- An *irrational* futures forecast shows up as $b_2>0$ (a spurious premium).
- *Measurement error* in the spot price shows up as $b_1>0$ (spurious forecast power).

**Data.**
- 21 commodities:
  - Agricultural: cocoa, coffee, corn, cotton, oats, orange juice, soybeans, soy meal, soy oil, wheat.
  - Wood: lumber, plywood.
  - Animal: broilers, cattle, eggs, hogs, pork bellies.
  - Metals: copper, gold, platinum, silver.
- Beginning-of-month T-bill yields from Salomon Brothers, January 1967–May 1984.
- Contracts are assumed to mature on the first trading day of the delivery month.
- **Spot is proxied by the maturing futures price**, so spot and futures are the same commodity sampled at the same time, at the cost of sample size. Copper, gold and silver supplemental contracts fill in extra months.
- Basis maturities 1/3/6/12 months. Split regressions are reported at 2/6/10 months.

## Results

### 1. Basis volatility follows storage costs (Table 2, 6-month basis)
| Group | Basis SD |
|---|---|
| Precious metals | gold 2.0%, silver 1.5%, platinum 4.2% |
| Agricultural | corn 4.6% to oats 9.7% |
| Animal | cattle 5.6%; broilers 10.1% to eggs 22.2% |

Why the ordering is what storage theory predicts:
- Seasonal spot swings must be large enough to pay for storage between harvests, so seasonal basis variation rises with storage cost.
- Inventories absorb supply and demand shocks, so costly storage (thin inventories) means shocks produce larger expected spot changes (French 1986).
- Metals are cheap to store relative to value and have no seasonals. Bulky or perishable goods (eggs, broilers, hogs, pork bellies, lumber) sit at the other end.

### 2. Interest-rate tracking and seasonals (regression 3)
- **Metals:**
  - Gold's 6-month $\hat\beta=1.07$; the 1-, 3- and 12-month estimates range from 0.99 to 1.06.
  - The rate alone explains **83%** of the variance of gold's 6-month basis, and 60% for silver.
  - Platinum and copper have lower $R^2$ but $\hat\beta$ close to 1.
- **Agricultural and wood:** every $\hat\beta>0$, many near 1, and only two more than 1 SE from 1. But all SEs exceed 0.5, so the evidence is not convincing.
- **Animal:** SEs are typically above 1, which is consistent with both 0 and 1. The basis is driven by $W-C$, not $R$.
- **Seasonals** (F-test that all monthly dummies are equal):
  - Metals: none, as expected.
  - Reliable for corn (at 3 months), oats, orange juice, soybeans and wheat.
  - Absent for cocoa, coffee, cotton, soy meal and soy oil. The lack of seasonals in the processed soy products, despite strong soybean seasonals, suggests processing smooths the effect.
  - Strongest in animal products: seasonal $R^2\ge0.19$ for broilers, cattle, eggs and pork bellies, and 0.47 and 0.72 for 1- and 3-month hogs.
  - Lumber and plywood show no reliable seasonals despite high storage costs and seasonal building demand. FF suggest wood production adapts more easily to demand.

### 3. The power problem (Table 3, 2-month, logs)
The SD of spot changes is large and similar across groups: 12.1–18.5% for metals, 9.0–15.0% for agricultural goods, 11.0–16.9% for animal products. FF's reading: futures markets exist precisely for commodities with highly uncertain spot prices. Basis SD is what differs:

| | Basis | Spot change | Premium |
|---|---:|---:|---:|
| Gold | 0.6 | 13.1 | 13.2 |
| Silver | 0.5 | 18.5 | 18.7 |
| Hogs | 7.1 | 12.9 | 12.1 |
| Eggs | 13.2 | 16.3 | 12.6 |

For gold and platinum, even a true slope of 1.0 would usually be less than 1 SE from zero. Since $b_1,b_2\in[0,1]$ typically, significant slopes appear "almost as a matter of arithmetic" only where basis variance is large relative to outcome variance.

### 4. Regression scoreboard (Tables 4–5)
| Type | Commodities | Evidence |
|---|---|---|
| SF: strong forecast at all maturities, no premium | broilers, eggs, hogs, oats | change-regression slopes all >2.6 SE, most >4 SE; $R^2$ 0.40–0.42 for broilers, 0.20–0.35 for oats |
| GF: forecast at most maturities | cattle, pork bellies, soybeans, soy meal | |
| SP: time-varying premium at all maturities | soy oil, lumber | largest premium $t$ = 3.71; $R^2\le0.27$, clearly weaker than SF |
| GP: premium at some maturities | cocoa, corn, wheat | |
| F&P | orange juice, plywood | forecast power at long maturities, premium at short |
| W: weak | coffee, copper, cotton (both slopes between 0 and 1, mostly insignificant); gold, platinum (basis too quiet); silver | silver slopes significant but "bizarre" (2-month change slope $-8.56$); FF say they are investigating |

No commodity shows reliable *simultaneous* variation in both premium and forecast at the same maturity.

Cross-links:
- Three of the four SF commodities rank in the top four for basis SD, and lumber (SP) ranks third.
- Of the 8 commodities with forecast power at most maturities, 5 are animal products and the other 3 (oats, soybeans, soy meal) also have high storage costs.
- Of the 10 commodities with basis seasonals, 8 show forecast power; of the 10 with forecast power, 8 have seasonals.
- So forecast power, meaning an expected spot change built into the basis, is mostly the seasonal-storage component. Hazuka (1984) found the storage-cost/forecast-power link but missed the complementary premium regression.

### 5. Unconditional premiums (Table 6)
Following Bodie–Rosansky: monthly returns on the shortest contract with at least 1 month to maturity (typically 1–3 months), equal-weighted portfolios.

| Portfolio | Obs | Simple mean %/mo | SD | $t$ | Log mean | $t$ |
|---|---:|---:|---:|---:|---:|---:|
| All 21 | 222 | 0.54 | 4.3 | 1.87 | 0.45 | 1.57 |
| Agricultural | 222 | 0.83 | 5.4 | 2.29 | 0.69 | 1.97 |
| Wood | 177 | −0.23 | 7.5 | −0.42 | −0.51 | −0.91 |
| Animal | 220 | 0.00 | 6.3 | 0.00 | −0.20 | −0.46 |
| Metals | 222 | 0.57 | 8.3 | 1.02 | 0.23 | 0.43 |

- Individual commodities:
  - 19 of 21 have positive simple means, and five exceed 1%/month (cocoa, coffee, orange juice, soy oil, hogs).
  - Only five have $|t|>2$: cocoa 1.59% ($t$ 2.33), coffee 1.84 (2.13), soy oil 1.91 (2.47), hogs 1.11 (2.06), and eggs −2.01 (−2.56).
  - With continuous compounding, only eggs is significant ($-2.60\%$, $t=-3.20$), and it is negative.
- The gap between simple and log means is the $\sigma^2/2$ term. At a 4.3% monthly SD the portfolio mean drops 0.09 pp and its $t$ falls from 1.87 to 1.57.
- CPI inflation (monthly SD about 0.25%; no major component above 0.62%, per Fama–Schwert) is negligible relative to futures volatility.
- Verdict: marginal, portfolio-level normal backwardation, sensitive to the return definition and not strong enough to settle the debate.

## Limitations

- **Spot and sample.** Using the maturing futures as the spot price means observations exist only in delivery months. Standard errors are not described in the returned text, and overlapping horizons (6/10-month maturities sampled monthly) make inference delicate.
- **Convenience yield and storage costs** are not modelled with inventories. Seasonal dummies are a crude proxy, and $W$ is not measured directly.
- **Coverage.** The sample ends in 1984 and excludes energy. Silver is unresolved.
- **Averages are not always the right estimand.** Classifications rest on counts of significant slopes across maturities (SF/GF/SP...), so they are coarse. Equal-weighted portfolio means say nothing about the cross-section of premiums.

## Assessment

- **Most durable contribution:** the asymmetry of identification. When $\sigma(\text{basis})\ll\sigma(\Delta S)$, a Fama-type split regression cannot tell premium from forecast, yet the same quiet basis gives a precise storage coefficient. This geometry applies equally to forward-FX and term-premium regressions (Fama 1984a,b), and to any "carry predicts returns" test.
- **Convincing:** gold $\beta\approx1$ with 83% $R^2$ is about as clean a no-arbitrage/carry identity as empirical finance offers. The linking of storage cost, seasonals and forecast power is neat and economically grounded.
- **Fragile:**
  - Premium evidence (SP/GP) rests on a handful of commodities with $t\le3.7$ and many implicit tests, since commodities × maturities are scanned.
  - The portfolio premium's $t$ of 1.87 would not survive a modern multiple-testing lens.
  - Egg returns dominate the negative tail.
- **For a quant PM:**
  - Roll yield (basis) in seasonal and costly-to-store commodities is largely *expected spot change*, not compensation for risk. Harvesting carry in livestock or grains without seasonal adjustment mostly captures predictable spot moves that the futures price already embeds.
  - Precious-metal calendar spreads are essentially an interest-rate trade.
  - Treat single-commodity premium estimates with heavy shrinkage. Monthly SDs of about 10% make individual means nearly uninformative over roughly 20 years.
  - Always report simple and log means together.
  - Stratify any basis/carry test by storage-cost group rather than pooling.
  - Later long-sample work (e.g. Gorton–Rouwenhorst) and inventory-based convenience-yield studies build on this dual-track framework.
