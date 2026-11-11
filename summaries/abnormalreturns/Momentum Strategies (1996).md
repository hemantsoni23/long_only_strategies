# Momentum Strategies
**Authors:** Louis K. C. Chan, Narasimhan Jegadeesh, Josef Lakonishok
**Year:** 1996
**Journal/Venue:** Journal of Finance 51(5), pp. 1681–1713
**Source file:** `Finance/AbnormalReturnsTrading_ChanJegadeeshLakonishok_1996.pdf`

## Question
Is Jegadeesh–Titman (1993) price momentum the same phenomenon as post-earnings-announcement drift? Three candidate stories: (i) price momentum is just underreaction to earnings news, so it should vanish after conditioning on earnings surprises; (ii) it is overreaction from positive-feedback trading (DeLong et al. 1990), so it should later reverse; (iii) price and earnings momentum reflect underreaction to *different* information (near-term earnings vs. broader, longer-term prospects), so both survive jointly and neither reverses. The evidence favours (iii).

## Data and design
- NYSE/AMEX/Nasdaq domestic primary stocks on CRSP and COMPUSTAT (excluding closed-end funds, REITs, trusts, ADRs, foreign stocks), plus I/B/E/S where available. Portfolios formed at the start of each month, January 1977 – January 1993.
- Decile breakpoints from NYSE stocks only (for earnings sorts, NYSE firms that reported in the prior three months); equal-weighted portfolios; buy-and-hold returns after skipping the first five days post-formation (bid–ask bounce); delisted stocks replaced by the value-weighted market until period end.
- Signals:
  - Price momentum $R6$: compound return over the prior six months.
  - $SUE_{it} = (e_{iq}-e_{iq-4})/\sigma_{it}$, seasonal random walk expectation (per Foster–Olsen–Shevlin 1984), $\sigma_{it}$ = std. of unexpected earnings over the prior eight quarters.
  - $ABR_{it}=\sum_{j=-2}^{+1}(r_{ij}-r_{mj})$ around the latest announcement, $r_m$ the equal-weighted market; model-free but covers only a few days of news.
  - $REV6_{it}=\sum_{j=0}^{5}(f_{it-j}-f_{it-j-1})/P_{it-j-1}$, $f$ the mean I/B/E/S FY1 consensus; results robust to scaling by book value, median-estimate % changes, and up/down revision counts.
- Pooled correlations (Table I) are modest: $R6$–SUE 0.293, $R6$–ABR 0.160, $R6$–REV6 0.294, SUE–REV6 0.440 (highest), ABR–REV6 0.115. The signals carry partly distinct information.

## Results

### One-way decile sorts (Tables II–V), top minus bottom decile

| Sort | Next 6 months | First year | Years 2–3 |
|---|---:|---:|---|
| $R6$ | 8.8% | 15.4% (deciles 9−2: 6.3%) | flat, no reversal |
| SUE | 6.8% | 7.5% | top decile below average |
| ABR | 5.9% | 8.3% | no reversal |
| REV6 | 7.7% | 9.7% | no reversal |

Price momentum is the largest and most persistent; earnings-sorted spreads are concentrated in the first six months. The $R6$ spread is driven by the extreme deciles. Formation-period moves are large: winners +69.6%, losers −30.8% over the prior six months. Winners are glamour (B/M 0.696) and losers value (B/M 1.080); both extremes are smaller stocks (average NYSE size decile 2.9 vs. 3.7–4.4 for the rest).

### Returns around subsequent earnings announcements
- $R6$ winners minus losers: +2.6% at the first and +1.0% at the second post-formation announcement; the 3.6% combined is **41%** of the 8.8% six-month spread. Nothing after two quarters.
- SUE deciles: 2.4% and 0.8% at the next two announcements, about half (3.2%) of the six-month spread.
- ABR deciles: 8.8% spread at the next announcement.
- Winner–loser SUE spreads *widen* in the following quarter, consistent with persistence in earnings surprises (or a misspecified expectation model, which is why the authors lean on announcement returns).
This also reconciles Foster–Olsen–Shevlin's finding that ABR does not predict: their window stopped short of the next announcement (as in Bernard–Thomas–Wahlen 1995).

### Analysts
Revisions are negative on average across portfolios (initial optimism). For $R6$ losers, average monthly downward revisions are 2.1% of price over months 1–6 and still 1.8% over months 7–12. The authors ascribe this asymmetry to incentives (brokerage business, access to management). Announcement-return reactions show no comparable asymmetry, so the market is not simply following analysts.

### Two-way independent tercile sorts (Table VI)
Joint top-minus-bottom six-month spreads: 7.9% ($R6$×ABR), 8.1% ($R6$×SUE), 8.8% ($R6$×REV6). Average conditional spreads:

| Panel | Earnings signal, holding $R6$ fixed (6m / 12m) | $R6$, holding earnings signal fixed (6m / 12m) |
|---|---|---|
| ABR | 2.8% / 3.8% | 4.6% / 8.6% |
| SUE | 4.3% / 3.8% | 3.1% / 7.0% |
| REV6 | 3.8% / 3.5% | 4.5% / 9.2% |

Both contribute. The earnings component stops growing after six months, while the $R6$ component roughly doubles by twelve months. Horse-races among earnings measures (Panels D–E) show each adds information: REV6 given SUE 3.23% vs. SUE given REV6 3.37%; REV6 given ABR 4.90% vs. ABR given REV6 2.70%.

### Fama–MacBeth regressions (Table VII)
Regressors are cross-sectional percentile ranks scaled to [0,1], plus size; t-stats adjusted for MA(5)/MA(11) overlap.
- Six-month returns: $R6$ alone 0.057 (t = 4.07); SUE alone 0.060, REV6 0.060, ABR 0.037. All four together: $R6$ 0.029 (2.07), ABR 0.017 (4.25), SUE 0.032 (4.00), REV6 0.031 (3.10). Earnings surprises absorb about half of the $R6$ coefficient.
- One-year returns: $R6$ alone 0.103 (3.96), falling to 0.076 (3.17) jointly and remaining the largest coefficient; REV6 is marginal (t = 1.94).

### Reversals (Section IV)
- No reversal in one-way sorts. Losers stay low for years even though their small-cap/high-B/M tilt should raise returns.
- The doubly-bad portfolio (low $R6$, bad earnings news) underperforms for three years (Panel C: 16.9% and 16.4% in years 2–3, lowest of the nine cells).
- Where winners are *not* confirmed by earnings (high $R6$, low ABR), the first-year return is 21.3% vs. 27.0% for confirmed winners and a 20% overall mean; in year 2 it falls to 18.3% vs. the 19.6% average, a reversal. Unconfirmed price momentum is the part that looks like overreaction.

### Robustness (Section V)
- **Large stocks** (above NYSE median cap): one-year spreads are $R6$ 14.0%, REV6 7.6%, ABR 4.3%, SUE 2.9%. In the joint regression only $R6$ is significant (0.064, t = 2.21); SUE, ABR and REV6 are not. Earnings momentum is largely a small-cap effect; price momentum is not.
- **FF3 time-series regressions** on the $R6$×REV6 extreme portfolios (six-month holding, Table X): winners α = 0.478%/month (t = 4.11), losers α = −0.953% (t = −6.08), long-short α = **1.431% (t = 5.91)**. Market and size loadings are identical for the two legs; the HML loading of the spread is −0.434, so FF3 makes the anomaly *larger*. Most of the alpha is on the short side.
- **Downside risk:** the winner-minus-loser spread is +0.60%/month in down-market months and +1.79% in up months. There is no evidence that winners carry more downside risk.

### Implementation caveat (authors')
Buying the top two $R6$ deciles earns about 27%/yr vs. about 22% for the universe, an excess of about 5%. Small-stock round-trip costs of about 3% (Chan–Lakonishok 1995) plus shorting constraints on losers remove much of it.

### Reconciling with long-horizon reversal
Momentum losers look "normal" over the longer past (return from month −36 to −6 about 61% vs. 62% for all stocks), so investors anchor on that and discount new bad news. Contrarian losers have long histories of disappointment and excessive pessimism. Both are cast as over-weighting the past. The authors call this suggestive only.

## Assessment
- **Convincing:** the design (common universe, three earnings proxies, independent double sorts, announcement-window decomposition, overlap-corrected FM t-stats) is the right one for "does X subsume Y", and the 41% announcement-window share is direct evidence that part of momentum is delayed reaction to fundamentals. The confirmed/unconfirmed-winner split is an early and underused result: price moves not backed by earnings news partly reverse.
- **Fragile or dated:** the results are equal-weighted, and the one-way $R6$ spread lives in the extreme deciles, which are small-cap. The five-day skip is not the now-standard one-month skip. The sample (1977–1993) predates momentum crashes (e.g., 2009) and the post-2000 decay of earnings drift in large caps. Two-way sorts use only terciles. "No reversal" rests on raw returns while the extreme portfolios have size and B/M tilts that bias the comparison in opposite directions for winners, which the authors call "muddy".
- **Practical relevance:** (1) For large caps, $R6$ dominates in a joint model, and analyst-revision signals add little once price momentum is included; for small caps the earnings signals carry independent alpha. (2) Earnings-surprise alpha decays within about two quarters, while price momentum's accrues over about a year, which matters for rebalancing frequency and turnover budgeting. (3) Much of the alpha comes from the short leg (losers with bad news and slow analyst downgrades), where borrow costs and constraints bind. (4) Conditioning price momentum on earnings confirmation (e.g., $R6$ × ABR/SUE interaction) is a cheap refinement that the paper already suggests.
