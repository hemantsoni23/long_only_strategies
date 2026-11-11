# The Shorting Premium and Asset Pricing Anomalies (Drechsler–Drechsler 2014) — Detailed Quantitative Research Notes

| Field | Detail |
|------|--------|
| Authors | Itamar Drechsler (NYU Stern, NBER); Qingyi (Freda) Drechsler (WRDS) |
| Date / venue | January 2014 working paper, SSRN 2387099 |
| Source file | Finance/AbnormalReturns_Drechsler_2014.pdf |
| Fee data | Markit Security Finance (formerly DataExplorers): actual (not quoted) loan rates self-reported by >100 lenders; >95% of CRSP stocks, >85% of US borrowing. 30-day volume-weighted average fee, observed at month-end |
| Samples | Fee sample Jan 2004 – Oct 2012 (106 months; the 2002-03 data are monthly and mostly large-cap, so dropped). Long sample Jan 1980 – Oct 2012 using the proxy SIRIO = short interest / institutional shares |
| Filters | Drop the bottom 10% by size and by price each month (about 15% of observations). A percentile price cut is used rather than $5, because many large financials traded below $5 in 2008-09. Results are said to be insensitive to the cutoffs |
| Anomalies | B/M, momentum, idiosyncratic volatility (Ang et al.), composite equity issuance (Daniel-Titman), distress (Campbell-Hilscher-Szilagyi), MAX (Bali-Cakici-Whitelaw), net share issuance (Loughran-Ritter) |

## Claim in one paragraph

Sort stocks each month on the short-loan fee. The portfolio long the cheapest-to-short decile and short the most expensive (CME) earns **1.45%/month gross (t = 4.96), 0.92% net of fees, and a 1.55% FF4 alpha (t = 7.03)**. All seven anomalies are essentially absent among the 80% of stocks with low fees and very large among the highest-fee stocks. Adding CME as a fifth factor to FF4 removes most anomaly alpha in every fee bucket; high-fee value is the one exception. The authors interpret CME as a premium for concentrated short-side risk, which *raises* prices of hard-to-short stocks.

## Fee distribution and the shorting premium (Tables 1-3)

- Fees are extremely skewed: deciles 1-8 average below about 31-32 bps/yr. Decile 9 averages 78 bps, decile 10 582 bps, and the top half of decile 10 ("10b") 908 bps. D10's average fee is about the size of the equity or value premium, and it is income forgone by every owner who does not lend.
- The equal-weighted average fee peaks at 126 bps in 2008. The dollar value on loan peaks around $587B/day in 2007 and falls to $315B by 2012. Institutional ownership is stable at about 60%.
- Returns are flat across deciles 1-8, then collapse: D10 earns -0.71%/month gross (-0.17% net), with FF4 alpha -1.44%. 10b earns -1.39% gross (-0.52% net). The 1-minus-10b spread is 2.13% gross, 1.27% net, with FF4 alpha 2.27% (t = 7.81).
- Size: D9 and D10 have aggregate market caps of about $1.1T and $415B. The average D10 stock is about $1.27B (10b just under $1B), i.e. a smallish mid-cap.
- High-fee stocks have extreme anomaly characteristics: high ivol, MAX, distress, issuance, and low B/M. For momentum and B/M the relation is **bimodal**: both extreme winners and losers carry high fees. SIRIO is about 6% in deciles 1-7 and rises to 26.8% in D10 and 34.5% in 10b.
- CME moments (Table 3):

| | Value |
|---|---|
| Mean | 1.45%/month |
| Std. dev. | 3.00%/month |
| Sharpe (annualized) | 1.67 gross, 1.06 net |
| Skewness | -0.52 |
| Kurtosis | 2.05 (the text calls excess kurtosis negative; the table reports 2.05) |
| AC(1) | 0.27 (MKT, HML and UMD are also 0.21-0.35 in this period) |
| Correlation with MKT / SMB / HML / UMD | -0.38 / -0.49 / -0.31 / +0.50 |

- Excess comovement: FF4 residual variance is 3.02% for the expensive portfolio vs 1.71% for the cheap one. The implied average pairwise residual correlation is **61% vs 38%**, pointing to a common factor among hard-to-short names beyond FF4.

## Mechanism (verbal, no formal model)

With finite fees, a Miller-type "infinite fee" story cannot explain *net* underperformance. The proposed story:

- The marginal sellers of high-fee stocks are a narrow group (hedge funds). A Goldman estimate cited via Ben-David, Franzoni and Moussawi: about 85% of equity shorts at Goldman's prime brokerage in March 2010 were hedge funds.
- These sellers hold concentrated short positions, so covariance with the expensive-to-short portfolio is priced *for them*.
- They stop short of pushing prices down to the representative investor's valuation. Prices stay high, and the low subsequent returns are their compensation. With incomplete risk sharing, the premium raises prices, the opposite of the usual long-side premium.
- The necessary other side is owners who hold high-fee stocks and do not lend them, forgoing the fee. The authors call this inefficient and argue it is logically implied by the existence of high fees. Institutional lending restrictions do not rationalize it, since restricted institutions should not own these stocks.

Test implication: stocks that load on the short-risk portfolio earn low returns. CME is used as the empirical proxy for that risk.

## Anomalies unconditionally, 2004-2012 (Table 4)

Monthly returns in %; L-S = decile 1 minus decile 10.

| | B/M | Mom | Ivol | CEI | Distress | MAX | NSI |
|---|--:|--:|--:|--:|--:|--:|--:|
| L-S gross (t) | 0.54 (1.40) | 0.02 (0.04) | 0.88 (1.69) | 0.63 (2.17) | 0.66 (1.08) | 0.71 (1.45) | 0.59 (2.23) |
| L-S net | 0.46 | -0.06 | 0.67 | 0.54 | 0.49 | 0.55 | 0.46 |
| FF4 alpha (t) | 0.44 (2.20) | 0.18 (0.58) | 1.23 (4.47) | 0.79 (3.50) | 0.96 (3.71) | 1.05 (4.15) | 0.74 (3.58) |
| FF4+CME alpha (t) | **0.62 (2.53)** | 0.07 (0.19) | 0.10 (0.36) | 0.17 (0.68) | 0.47 (1.56) | 0.20 (0.73) | 0.08 (0.34) |
| D10 (short-leg) fee, bps | 149 | 173 | 225 | 142 | 209 | 185 | 164 |

Raw spreads are noisy in 106 months. Fees cut the L-S returns by 8-21 bps/month (largest for ivol). Every short leg has an average fee above 140 bps, and fees rise monotonically from decile 5 to decile 10.

## Main result: anomalies conditional on fee (Table 5)

Construction: F0 = fee deciles 1-8, with anomaly deciles formed inside it. F1-F3 = terciles of the remaining 20% by fee, with anomaly terciles formed inside each.

| Bucket | B/M | Mom | Ivol | CEI | Distress | MAX | NSI |
|---|--:|--:|--:|--:|--:|--:|--:|
| **Raw, F0** | 0.12 | -0.25 | **-0.04** | 0.25 | 0.01 | 0.03 | 0.16 |
| **Raw, F3** | 0.96 | 0.84 | **1.85** (t 3.77) | 1.18 | 1.18 | 1.45 | 0.87 |
| F3-F0 (t) | 0.84 (2.15) | 1.09 (1.48) | 1.89 (3.68) | 0.93 (1.91) | 1.16 (1.93) | 1.42 (3.15) | 0.71 (2.10) |
| **FF4 alpha, F0** | 0.02 | -0.08 | 0.29 | 0.38 (t 2.07) | 0.31 | 0.35 | 0.31 |
| **FF4 alpha, F3** | 0.95 | 0.81 | **1.99** (t 4.31) | 1.29 | 1.31 | 1.62 | 0.97 |
| **FF4+CME alpha, F0** | 0.18 | -0.01 | -0.27 | 0.04 | 0.13 | 0.08 | -0.00 |
| **FF4+CME alpha, F3** | **1.44** (t 3.12) | 0.82 | **0.38** (t 0.78) | 0.79 | -0.05 | 0.24 | 0.31 |
| FF4+CME alpha, F3-F0 (t) | 1.26 (2.77) | 0.83 | 0.65 | 0.75 | -0.18 | 0.17 | 0.31 |

- In F0 (80% of stocks, and more of market cap), no raw spread is significant or exceeds 25 bps. Only CEI has a significant FF4 alpha, and it drops to 4 bps under FF4+CME.
- Anomaly returns rise monotonically F0 -> F1 -> F2 -> F3. Momentum, dead unconditionally, earns 84 bps in F3.
- Under FF4+CME, all 28 bucket alphas are insignificant **except high-fee value**, whose alpha *rises* from 0.95 to 1.44. The F1 and F2 alphas are all insignificant; the largest t-stat is 1.60, for value.

## Long sample with SIRIO, 1980-2012 (Tables 6-9)

- **SIRIO-sorted CME:** 1.48%/month, FF4 alpha 1.54%. The 1-minus-10b spread is 1.88% with FF4 alpha 1.96% (t = 9.83); the 10b portfolio's average SIRIO is 81.8%. CME has standard deviation 4.99%, Sharpe about 1.03, AC(1) 0.06. Correlations: MKT -0.55, SMB -0.55, **HML +0.47** (the sign flips from the fee sample), UMD +0.19.
- **Unconditional anomalies (Table 8):** all seven raw spreads are significant; the FF4 alpha is insignificant only for momentum. FF4+CME alphas: B/M 0.05, mom -0.25, ivol 0.19, CEI 0.47 (t 3.69), distress 0.26, MAX 0.36 (t 2.03), NSI 0.49 (t 3.99). Distress, ivol and MAX each lose at least 1.16%/month of alpha.
- **Conditional (Table 9):** F0 anomalies are *significant* here, unlike in the fee sample. The authors attribute this to proxy noise, which blurs the sort. F3 is still much larger: ivol 2.24% (t 7.38), MAX 2.21%. Under FF4+CME:
  - The F1/F2 alphas are all below 32 bps.
  - F3 alphas for ivol (0.91, t 3.76), MAX (1.10, t 4.34) and NSI (0.50) stay significant.
  - The F3-F0 alpha gaps stay significant for ivol and MAX. Absorption is less complete than in the fee sample.

## Assessment

**Convincing**
- The fee data are much better than earlier single-lender datasets.
- The F0 null is the strongest result, and it matters in practice. Across seven canonical anomalies, the 2004-12 predictability lives almost entirely in the 20% of stocks with meaningful borrow cost.
- The net-of-fee CME spread (0.92%/month) rules out the pure "fee as a dividend to lenders" explanation.

**Fragile or open**
- **Short, crisis-heavy sample.** There are 106 months, with equal-weighted portfolios only; no value-weighted results or Fama-MacBeth regressions are reported. Most raw anomaly spreads are insignificant even unconditionally.
- **Partly mechanical factor test.** CME is built from the same fee sort that defines the buckets, and anomaly short legs are high-fee stocks by construction. A high-minus-low-fee factor absorbing high-fee anomaly alpha is close to relabeling. The test does not separate "short-risk compensation" from "any friction or mispricing concentrated in high-fee stocks". CME's own alpha is not priced by anything, and the theory has no formal model or quantity predictions: no link from concentration or short-seller capital to the size of the premium.
- **Why do owners not lend?** The explanation rests on owners who do not lend high-fee stocks. The paper labels this inefficient rather than explaining it, and it is the crux.
- **Value survives, with the wrong sign.** It survives CME, and its alpha increases. HML's correlation with CME also flips sign between samples (-0.31 vs +0.47), so the factor's composition is sample-dependent.
- **Proxy weakness.** SIRIO does not reproduce the F0 null, so the long-sample evidence is weaker corroboration than the headline suggests.

**Relation to the literature:** Extends Jones-Lamont, Ofek-Richardson-Whitelaw, Cohen-Diether-Malloy, Nagel (institutional ownership), Asquith-Pathak-Ritter, and Hanson-Sunderam (short interest). It complements Stambaugh-Yu-Yuan (short legs, sentiment) and Avramov et al. (distress) by using direct fees and net returns. The authors see it as consistent with the skeptics (Geczy-Musto-Reed, Battalio-Schultz, Ljungqvist-Qian), because the premium is attributed to risk concentration rather than to fee drag.

**For a quant PM**
- Condition every cross-sectional signal on borrow cost. The paper's own numbers imply that anomaly books restricted to general-collateral names had little gross edge in 2004-12, and books that short specials pay fees of about 140-225 bps on the short leg.
- Treat CME (or a borrow-fee factor) as a risk-model and attribution factor for any short-heavy book. It correlates -0.38 with the market, so it loses in rallies and squeezes, and hard-to-borrow names show about 61% average residual correlation.
- Do not read FF4+CME alpha of about zero as "no edge". It means the returns are harvesting the fee-sorted spread, which needs locate capacity and bears short-squeeze risk.
- Check post-2012 behavior (e.g. 2021 squeezes) before sizing; the paper provides none.
