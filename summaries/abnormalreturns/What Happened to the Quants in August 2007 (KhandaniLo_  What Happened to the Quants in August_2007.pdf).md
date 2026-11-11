# What Happened to the Quants in August 2007? — Khandani & Lo (2007) — Detailed Quantitative Research Notes

## Bibliographic Header

| Field | Detail |
|------|--------|
| **Title** | What Happened To The Quants In August 2007? |
| **Authors** | Amir E. Khandani (MIT EECS / LFE); Andrew W. Lo (MIT Sloan / LFE; AlphaSimplex) |
| **Date** | First draft and latest revision September 20, 2007 (SSRN 1015987) |
| **Type** | Real-time case study; the authors stress it is "an evolving case study, not formal academic research" |
| **Data** | CRSP US common stocks (share codes 10–11, price \$5–\$2,000), daily, Jan 3, 1995 – Aug 31, 2007 (2007 from Yahoo price returns); TASS (Aug 20, 2007 snapshot); CS/Tremont indexes |
| **Source file** | `Finance/KhandaniLo_  What Happened to the Quants in August_2007.pdf` |
| **Drive file_id** | `0B-6kBz0I0dMseXF4cXdYNXpoSEU` |

---

## Question

In the week of August 6, 2007, quantitative equity market-neutral funds suffered losses of 5–30% within days (press reports: Renaissance key fund −8.7% MTD; Highbridge Statistical Opportunities −18% by Aug 8; Tykhe ~−20%; Goldman Sachs Global Equity Opportunities >−30% in a week). This happened while equity, bond, FX and commodity indexes were quiet on Aug 7–8 and no other hedge-fund style reported losses. Without access to fund or prime-broker data, what can public data reveal about the mechanism?

## Instrument: the Lehmann / Lo–MacKinlay contrarian strategy

$$
\omega_{it}=-\frac{1}{N}\left(R_{i,t-k}-R_{m,t-k}\right),\qquad R_{m,t-k}=\frac1N\sum_i R_{i,t-k},\qquad k=1\text{ day},
$$

a dollar-neutral portfolio that buys yesterday's losers and sells yesterday's winners. It is both a bet on short-horizon reversal and a form of market making (it absorbs order imbalances). Returns are computed per unit of capital:

$$
I_t=\tfrac12\sum_i|\omega_{it}|,\qquad R_{pt}=\frac{\sum_i\omega_{it}R_{it}}{I_t}\ \ (\text{Reg T, }2{:}1),\qquad L_{pt}(\theta)=\frac{\theta}{2}R_{pt}.
$$

Leverage $\theta{:}1$ is gross (long + short) over capital, so 8:1 multiplies the Reg-T return by 4. Size deciles are rebalanced semi-annually. No transaction costs.

## Findings

### 1. Alpha decay (Table 2, Fig. 1)

Average daily return, all stocks (unlevered, gross): 1995 **1.38%**, 1996 1.17%, 1997 0.88%, 1998 0.57%, 1999–2000 0.44%, 2001 0.31%, 2002 0.45%, 2003 0.21%, 2004 0.37%, 2005 0.26%, 2006 **0.15%**, 2007 YTD **0.13%**. Annualized Sharpe ($\sqrt{250}\,\mu/\sigma$) falls from 53.9 (1995) to 4.5 (2006) and 2.8 (2007 YTD). Profitability is concentrated in small caps (1995: smallest decile 3.57%/day, largest 0.04%). The authors attribute the decline to competition, technology, decimalization, lower retail order flow, lower volatility (market-making profits rise with volatility), and asset growth. They note the Sharpe ratios are inflated by ignoring costs but argue that a strategy which supplies liquidity earns the spread rather than paying it, so the levels are "probably not off by an order of magnitude".

### 2. The August 2007 fingerprint (Tables 3–4)

| Date | Unlevered (all stocks) | 8:1 levered (×4) | Market context |
|------|------:|------:|------|
| Mon 8/6 | +0.50% | +2.01% | |
| Tue 8/7 | −1.16% | −4.64% | S&P +0.62% |
| Wed 8/8 | −2.83% | −11.33% | S&P +1.44% |
| Thu 8/9 | −2.86% | −11.43% | S&P −2.95%, VIX +5.03; BNP Paribas freezes funds |
| Fri 8/10 | **+5.92%** | **+23.67%** | S&P +0.04% |

- Aug 7–9 cumulative (arithmetic): −6.85%, which the paper calls 12 daily standard deviations of 2006 volatility (0.52%); a straight division gives ~13. Aug 10 is +11.4 sd. The whole week is −0.43% unlevered, an unremarkable week for anyone who held on.
- Levered 8:1: about −25% from Aug 6 to Aug 9 ("a little over a quarter" of capital). The arithmetic weekly return is −1.72%, while the geometric weekly return is −5.52%. The difference matters: it depends on whether the book is rebalanced to fixed notional.
- The cross-section of deciles is diagnostic. Three-day losses were largest in the *intermediate* deciles (3: −8.09%, 4: −9.33%, 5: −8.95%, 8: −8.81%), which are the deciles a large stat-arb book would actually trade. The smallest decile was *positive* on each of Aug 7–9. On Aug 10 the mid deciles rebounded 7–9%.
- The choice of 8:1 is not arbitrary. Table 6 computes the leverage needed to match the 1998 expected return: $\theta^*_t=2\,E[R_{p,1998}]/E[R_{pt}]$, which rises from 2.0 (1998) to 7.76 (2006) and 8.96 (2007). The authors use the 2006 value because it was the level known to managers at the start of 2007.

### 3. The August 1998 contrast (Table 5)

Across the Russian default and LTCM (Aug–Sep 1998), the same strategy was profitable on most days. Fixed-income arbitrage deleveraging left no discernible footprint in U.S. equity reversal. The authors offer three non-exclusive explanations for why 2007 differed: more multi-strategy funds and prop desks spanning credit and equities, much more capital in equity L/S, and higher leverage. They argue all three hold to some degree.

### 4. Crowding and illiquidity (Sections 6, 8)

- In TASS Long/Short Equity Hedge and Equity Market Neutral, average AUM per fund grew from \$62MM (Jan 1994) to \$229MM (Jul 2007). Assets in the two categories exceeded \$160bn at the start of 2007, excluding ~\$75bn in 130/30 products.
- The 130/30 point: a \$100MM 130/30 fund is a long index plus a \$30MM-per-side market-neutral overlay built with the same signals and risk models, so it adds to both shorting demand and commonality.
- Illiquidity proxy: the first-order autocorrelation $\hat\rho_1$ of monthly fund returns (Getmansky–Lo–Makarov). Its 60-month rolling equal-weighted mean, asset-weighted mean and median for the two categories have risen since 2000, apart from a brief dip in late 2004. The standard error of the mean is about 0.65% under cross-sectional independence, so the rise is statistically significant. The level remains well below convertible arbitrage and emerging markets. An Amaranth natural-gas spread example shows rolling $\hat\rho_1$ breaching its 95% band months before the unwind.

### 5. Connectedness (Section 9)

Absolute pairwise correlations among 13 CS/Tremont indexes rose between Apr 1994–Dec 2000 and Jan 2001–Jun 2007. For example, Multi-Strategy vs Emerging Markets went from 7% to 52%. Earlier-period correlations are heavily dependent on August 1998. The 36-month rolling mean and median absolute correlations trend up, especially after 2004. Multi-Strategy's covariances with Long/Short Equity and Equity Market Neutral cluster and rise after 1999, consistent with multi-strategy funds adding equity books. The authors note that part of the correlation increase comes from lower volatility (a smaller denominator), and argue it still matters for systemic risk. Every CS/Tremont index lost money in August 2007 (broad index −1.53%, EMN −0.39%, managed futures −4.61%).

## The unwind hypothesis (8 claims, condensed)

1. The losses were initiated by temporary price impact from a rapid liquidation of one or more large quant market-neutral books. The likely seller was a multi-strategy fund or prop desk responding to credit margin calls, a risk cut, or a change in business line. Liquidation of *market-neutral* rather than long-biased books is inferred from the S&P and MSCI ex-US rising on Aug 7–8.
2. The impact on Aug 7–8 forced other L/S, 130/30 and quant long-only managers to deleverage, via their own risk limits or prime-broker limits, which produced the Aug 8–9 losses. This was "both prudent and, unfortunately, disastrous".
3. The selling was over by Thursday's close. The Friday reversal was partial, because some capital had been destroyed and some participants still attributed the price moves to information (a Kyle-type partial reversion). Mechanically, the losses also enlarged next-day contrarian signals.
4. This was a liquidity event, not a permanent breakdown of the strategies, but it revealed a common component in the sector.
5. Amplifiers: asset growth, alpha decay, the leverage needed to offset it, underappreciated crowding, and subprime-induced risk aversion.
6. The "quant" label is incidental. Their illustration: the forced liquidation of an odd-vs-even-CUSIP market-neutral book would hurt every portfolio with overlapping holdings, whatever its ex-ante merit. Common exposures come from shared anomalies (value, momentum, reversal, earnings surprise) and shared Barra/Northfield risk models.
7. Systemic risk in hedge funds has increased (from the 1998 contrast, AUM growth, rising correlations, and the growth of credit strategies).
8. Further credit shocks could hit liquid styles (L/S equity, macro, CTAs), although better knowledge of the sector's size might mute the next equity event.

Policy implications drawn: "hedge-fund beta" (common L/S equity factors) now demonstrably exists. Registration under the '40 Act addresses investor protection, not systemic risk. The authors call for an NTSB-like forensic body for capital markets.

## Limitations (largely acknowledged by the authors)

- The contrarian strategy is a one-day-reversal proxy with no factor-selection component. It fits high-frequency stat-arb but is a poor proxy for lower-turnover multi-factor books (value, momentum, quality), which, by the authors' own account, reduces its power to detect factor-portfolio unwinds.
- Gross returns, no costs, no borrow constraints. The 2007 returns are Yahoo price returns for a fixed Dec-2006 universe, with 169 securities dropped.
- The leverage level is inferred from a return-targeting identity (constant required return since 1998), not observed.
- The σ-normalization uses 2006 volatility. 2007 YTD daily volatility was 0.72%, which would make the event smaller in sigma terms.
- TASS is voluntary and excludes many of the funds involved. Correlation-based "network" evidence is crude and volatility-sensitive.
- The initiating seller and its motive (forced or voluntary) cannot be identified from outside.

## Assessment

- **Convincing:** the identification rests on three facts that are hard to reconcile with a fundamental shock. (i) Losses on Aug 7–8 came with rising broad indexes. (ii) The worst losses were in the mid-cap deciles a large stat-arb book would trade, and the smallest decile gained. (iii) An 11-sigma reversal the next day left the week roughly flat. The alpha-decay → leverage → fragility chain is a clean quantitative argument, and the leverage identity $\theta^* \propto 1/E[R_p]$ is simple but useful.
- **Weaker:** the 1998 "no sign of stress" claim is broadly right, but Table 5 shows the strategy at −1.62% on Aug 31, 1998 and +6.59% on Sep 1 (market crash and rebound days), so the 1998 record is not entirely clean. The systemic-risk evidence from TASS autocorrelations and index correlations is suggestive rather than decisive. The authors themselves revisited the event later with factor and transactions data; this paper should be read as the first, indirect pass.
- **For a quant PM:**
  1. Market-neutral is not liquidation-neutral. Risk models need a "peer-crowding" dimension: common signals, common risk models and common universes create a latent factor that is invisible in normal times.
  2. Monitor a simple public proxy (a short-horizon reversal book, and residual-return PCA of standard quant factors). Simultaneous multi-sigma moves with quiet markets are the signature of a liquidation.
  3. When expected return decays, hold leverage constant and accept lower returns rather than restoring the return target. Deleveraging mid-event locked in the loss and forfeited the rebound; liquidity reserves and pre-agreed financing terms determine whether you can hold on.
  4. Stop-loss and risk-limit rules that are synchronized across the industry are an amplifier. Design deleveraging rules that account for liquidity and crowding, not just realized volatility.

---

*Scholar batch_2026-09-24_4. Source Drive id `0B-6kBz0I0dMseXF4cXdYNXpoSEU`.*
