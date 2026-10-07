# Global Momentum Strategies: A Portfolio Perspective

**John M. Griffin, Xiuqing Ji, J. Spencer Martin · 2005 · Journal of Portfolio Management (Winter 2005, pp. 23–39) · Source file `Finance/AbnormalReturnsMomentum_Griffin_2005.pdf` · CRSP NYSE/AMEX (US) + Datastream, 40 markets for price momentum, 34 for earnings momentum, 1975–Dec 2000**

## Claim / contribution
A practitioner-oriented companion to Griffin, Ji & Martin (2003, JF "Pole to Pole"). Using one consistent design across 40 countries it asks: (i) is momentum profitable long-only (i.e., not just a short-side phenomenon)? (ii) are price and earnings momentum distinct? (iii) how correlated are country momentum strategies vs. country market indices, including in down markets? (iv) when does momentum pay off (market/GDP states, January), and what are its tail/drawdown risks?

## Data & methodology
- **Universe:** US = CRSP NYSE/AMEX common shares. Non-US = 39 Datastream countries with ≥ 50 non-financial stocks (live + dead lists). 11 markets from 1975; by Feb 1995 all except Egypt covered. Earnings momentum from Feb 1976 (US), Feb 1987 for many other countries.
- **Screens (Datastream hygiene):** drop preferreds (unless main class, e.g. Brazil), convertibles, warrants, units, funds, foreign listings; pick most representative share class; if the return index repeats ≥ 4 consecutive times keep the first value, set the rest missing; monthly returns > 1000% set missing.
- **Price momentum:** 6-month ranking, **skip 1 month**, 6-month holding; top/bottom **20%** (quintiles — too few stocks in many countries for deciles); JT overlapping portfolios (six vintages live). Local-currency returns; profits annualized as monthly × 12.
- **Earnings momentum:** 6-month change in consensus one-year EPS forecast scaled by end-of-period price (à la Chan, Jegadeesh & Lakonishok 1996); quintile sort, 6-month hold.
- **Constrained earnings momentum:** earnings momentum using only stocks in the *middle* 60% of past returns (excludes price winners/losers) — used for correlation and state tests to avoid overlapping positions.
- **Regional series:** equal-weighted average of country strategies.

## Main results

**Long-only viability (Exhibit 1, USD, $1 from Aug 1975 to 2000, no costs):**

| Region | Winners | Market | Losers |
|---|---|---|---|
| US | $142.29 | $33.87 (VW index) | $7.27 |
| Europe | $192.66 | $66.01 | $15.06 |

Losers *beat* the market in Americas ex-US and Asia (likely small-cap premium of momentum-extreme stocks); in Europe/US losers underperform. Much of the spread comes from the long side → usable by short-constrained institutions (before costs).

**Univariate WML (Exhibit 2, % p.a.):** price momentum positive in all African/American countries, 10/14 Asian, 14/17 European markets. Regional price momentum: Africa 19.62, Americas ex-US 9.41, **Asia 3.83** (weakest), Europe 9.21; all-country average **7.98** (price) vs **5.10** (earnings). Earnings momentum positive in 27/34 markets, significantly negative in none; Americas ex-US 10.87, Asia 4.45, Europe 4.16.

**Price vs. earnings momentum (Exhibit 3, independent 3×3-type sorts, % p.a.):**

| | Price mom. within EM groups (lo/md/hi) | Earnings mom. within PM groups (lo/md/hi) | Combined (long top-20% both, short bottom-20% both) |
|---|---|---|---|
| US | 7.44* / 9.38* / 11.06* | 2.38 / 2.13* / 6.01* | **13.45*** |
| Europe | 6.26* / 7.76* / 7.67* | 5.67* / 3.53* / 7.08* | **13.34*** |
| Asia | −3.06 / −4.65 / −1.02 | 6.81* / 2.97* / 8.85* | 6.79 |
| Developed | 5.69* / 7.65* / 9.11* | 4.59* / 3.55* / 8.01* | **13.70*** |
| Emerging | −1.84 / −4.15 / −4.91 | 7.66* / 2.37 / 4.59 | 2.75 |
| World ex-US | 3.01 / 2.36 / 3.66 | 6.76* / 3.55* / 7.40* | **10.41*** |
| World | 4.89* / 6.13* / 7.90* | 4.59* / 3.10* / 7.50* | **12.39*** |

(* = 5% significance.) Each signal survives within groups of the other → related but not redundant; the combined strategy is positive in 29 of 32 markets. In **Asia earnings momentum works where price momentum does not**; outside Asia price momentum is slightly stronger. Time-series correlation of price and constrained-earnings momentum is mostly positive but < 0.40 (US 0.338, world ex-US 0.398; negative in China, Denmark, France, Greece, Portugal; highest in Indonesia).

**Cross-country diversification (Exhibits 5–6, correlations with US):**

| | Momentum corr. with US | Market-index corr. with US |
|---|---|---|
| Europe price mom., all months | 0.328 | 0.590 |
| Asia price mom., all months | 0.198 | 0.559 |
| Europe price mom., US down months | 0.200 | 0.648 |
| Asia price mom., US down months | 0.259 | 0.543 |
| Europe price mom., US up months | 0.373 | 0.292 |
| Asia price mom., US up months | 0.167 | 0.311 |
| Europe constrained earnings mom. | 0.229 | — |

Developed-market average price-momentum correlation with US: 0.177 (Naranjo & Porter 2004 find 0.31 using larger caps — i.e., large-cap momentum likely co-moves more). Only 2 emerging markets have momentum correlation above market correlation. Key point: **index correlations spike in US down markets, momentum correlations do not**; earnings momentum correlations are lower still (Asia ≈ 0).

**State dependence (Exhibits 7–8):**
- Price momentum positive in **35/40 markets in down-market months** vs 26 in up months; all-market average 8.45% p.a. (down) vs 5.72% (up). Asia: slightly negative in up months, 6.60% in down months. Constrained earnings momentum positive in 24/32 (up) and 21/32 (down).
- GDP states (22 OECD markets): developed-market price momentum 9.15% p.a. in negative-GDP-growth quarters vs 3.69% in positive → contradicts a simple distress-risk story. Constrained earnings momentum ≈ 0 in negative-GDP periods.

**Tail risk / time series (Exhibits 9–11, monthly raw returns):**
- Regional momentum is less volatile than regional EW markets: monthly σ 3.40 (Asia) and 1.65 (Europe) vs 4.95 and 4.21.
- But losses cluster: Asia −18.31% (Nov 1998) after −12.71% (Oct) and −5.34% (Sep); US worst −20.44% (Feb 1991, after −14.92% in Jan 1991) and −20.24% (Jan 1992); Europe's worst −8.05% also Feb 1991 (Asia −5.52% that month) → simultaneous cross-region crashes do happen.
- EW global strategy (markets with ≥ 100 stocks): monthly σ **1.65** vs 4.05 for a similarly built world index; worst months only −6.10% (Feb 1991) and −5.57% (Nov 1998).
- Long dry spells: US lost money Dec 1990–Nov 1993; Asia performed poorly Jul 1989–Nov 1995. Big common gains Nov 1979–Feb 1980.
- January: price momentum negative in January in 16/40 markets (large negatives in Egypt, Taiwan, US); earnings momentum also often negative in January.

## Critical assessment
- **Convincing:** consistent cross-country design; clean evidence that price and earnings revisions carry separate information; the correlation/down-market diversification result is the paper's most useful contribution.
- **Fragile / caveats:** no transaction costs, short-sale costs or price impact (authors acknowledge large cross-market variation); equal-weighted, quintile portfolios in thin markets are small-cap-heavy (the loser-beats-market result hints at this); non-US bivariate samples start ≥ 1987 so many country numbers are noisy/insignificant; local-currency returns for most tests (no FX hedging analysis); no risk-adjusted alphas (relies on GJM 2003); "down market" defined only by sign of US return. Sample ends 2000 — before the 2009 momentum crash.
- **Inconsistency:** text says the joint strategy earns 5.79% p.a. in Asia, whereas Exhibit 3 reports 6.79 for Asia (and 7.26 ex-Japan). Several figures are bar charts only (country-level numbers not tabulated).

## Practical relevance for a quant PM
- Run momentum as a **multi-country, equal-risk sleeve**: cross-country diversification cuts volatility by more than half relative to single regions and markedly reduces worst-month losses.
- Combine price momentum with analyst **earnings-revision momentum** (especially in Asia, where price momentum is weak) — the double sort roughly doubles univariate spreads.
- Budget for multi-year drawdowns and correlated crash months (Feb 1991, Nov 1998); consider January seasonality/tax-loss effects in rebalancing.
- Clean Datastream data (stale-price and outlier filters) before trusting international momentum backtests.
