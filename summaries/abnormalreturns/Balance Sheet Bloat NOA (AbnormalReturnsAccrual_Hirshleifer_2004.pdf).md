# Do Investors Overvalue Firms with Bloated Balance Sheets? — Hirshleifer, Hou, Teoh & Zhang (2004) — Detailed Quantitative Research Notes

## Bibliographic Header

| Field | Detail |
|------|--------|
| **Title** | Do investors overvalue firms with bloated balance sheets? |
| **Authors** | David Hirshleifer; Kewei Hou; Siew Hong Teoh; Yinglei Zhang — Fisher College of Business, Ohio State |
| **Journal** | *Journal of Accounting and Economics* 38 (2004) 297–331 |
| **DOI** | 10.1016/j.jacceco.2004.10.002 |
| **Sample** | NYSE/AMEX/Nasdaq firms in CRSP ∩ Compustat; July 1964 – December 2002 (462 months); 1,625,570 firm-months; 141,254 firm-years (FY1963–2000) |
| **Source file** | `Finance/AbnormalReturnsAccrual_Hirshleifer_2004.pdf` |

---

## Question and hypothesis

With limited attention, investors anchor on salient accounting earnings and underuse the incremental information in cash profitability. Net operating assets are, by identity, the cumulative gap between accounting value added and cash value added:

$$
\mathrm{NOA}_T=\sum_{t\le T}\mathrm{OI}_t-\sum_{t\le T}\mathrm{FCF}_t
=\sum_{t\le T}(\mathrm{OIBD}_t-\mathrm{CFO}_t)+\sum_{t\le T}(\mathrm{Inv}_t-\mathrm{Dep}_t)
=\sum_{t\le T}\mathrm{OpAccruals}_t+\sum_{t\le T}\mathrm{Inv}_t .
$$

High scaled NOA ("balance-sheet bloat") means strong past earnings weakly corroborated by free cash flow: lingering receivables, low deferred revenue, over- or replacement investment, or expenditures capitalized that pay off only briefly. If investors do not discount this, high-NOA firms are overpriced and earn low subsequent abnormal returns — the **sustainability effect**. Earnings management (Barton–Simko 2002) is compatible with the story but not required.

Why NOA should beat accruals: it is the accounting–cash deviation itself rather than a correlate of it; it includes investment in excess of depreciation (which Sloan accruals miss); and it cumulates the full history rather than one year's flow. Because high NOA implies high past growth, the paper stresses controlling for growth-related risk (B/M, past returns).

## Measurement

$$
\mathrm{NOA}_t=\frac{\mathrm{OA}_t-\mathrm{OL}_t}{\mathrm{TA}_{t-1}},\quad
\mathrm{OA}=\mathrm{TA}-\mathrm{Cash\&STI},\quad
\mathrm{OL}=\mathrm{TA}-\mathrm{STD}-\mathrm{LTD}-\mathrm{MI}-\mathrm{PS}-\mathrm{CE}.
$$

Compustat items: TA #6, Cash&STI #1, STD #34, LTD #9, MI #38, PS #130, CE #60; missing STD/TP/LTD/MI/PS set to zero. Operating accruals use the balance-sheet method, $[\Delta\mathrm{CA}-\Delta\mathrm{Cash}-(\Delta\mathrm{CL}-\Delta\mathrm{STD}-\Delta\mathrm{TP})-\mathrm{Dep}]/\mathrm{TA}_{t-1}$; Earnings = income from continuing operations (#178)/lagged TA; Cash Flows = Earnings − Accruals. Portfolios use NOA from the prior fiscal year with at least a 4-month lag. Abnormal returns: DGTW-style characteristic benchmarks (125 size × B/M × prior 12-2 month return portfolios; EW benchmarks for EW portfolios, VW for VW). Hedge = lowest minus highest NOA decile. Results survive scaling by ending TA or sales, excluding bottom-size firms or price < $5, industry-demeaned NOA, excluding financials, and an item-by-item NOA definition (NOA_alt, Fairfield et al. 2003; Pearson correlation 0.92 with NOA).

## Descriptives (Tables 1–3)

- Median NOA runs from 0.26 (D1) to 1.45 (D10) of lagged assets (means 0.247 → 1.596).
- Median earnings rise from 0% (D1) to 13.6% (D10), almost entirely through accruals (median −9.1% → +13.4%). Cash flows are flat across D2–D9 and sharply negative in D10 (mean −4.8%, median −3.4%).
- Both extreme deciles hold smaller, lower-B/M, higher-beta firms. D1 overweights pharma and financials; D10 extractive, transportation and utilities; both extremes overweight computers and services.
- NOA is persistent (Spearman 0.62 with lagged NOA) and positively related to accruals (Spearman 0.32). Pearson and Spearman correlations with earnings and cash flows have opposite signs because of outliers.

## Main results

### Earnings and return profile (Fig. 1)
High-NOA firms show rising earnings into the ranking year and a sharp decline afterward; low-NOA firms are the mirror image. Because high-NOA firms are high-earnings firms cross-sectionally, high NOA does not predict *lower levels* of future earnings than low NOA, only *declining* earnings — the key to the Mishkin result below. Annual raw returns cross over: high-NOA firms earn about 45% in year −1 and under 5% in year +1; the gap persists out to year +5.

### Decile returns (Table 4, monthly)

| | EW raw t+1 | EW adj t+1 | EW adj t+2 | EW adj t+3 | VW raw t+1 | VW adj t+1 | VW adj t+2 | VW adj t+3 |
|---|---|---|---|---|---|---|---|---|
| Lowest NOA | 1.79% | 0.51% | 0.29% | 0.27% | 1.06% | 0.22% | 0.12% | 0.15% |
| Highest NOA | 0.31% | −0.73% | −0.54% | −0.30% | 0.30% | −0.47% | −0.47% | −0.35% |
| Hedge L−H | 1.48% (8.45) | 1.24% (10.31) | 0.83% (7.66) | 0.57% (5.44) | 0.76% (4.18) | 0.69% (5.24) | 0.60% (4.34) | 0.49% (3.73) |
| Carhart α of hedge | 1.40% (8.32) | 1.26% (10.08) | 0.88% (7.66) | 0.67% (6.22) | 0.74% (3.93) | 0.61% (4.70) | 0.54% (4.06) | 0.58% (4.10) |

(t-statistics in parentheses.) CAPM and FF3 intercepts are similar or larger (e.g. EW adjusted t+1: CAPM 1.27%, FF3 1.34%). The value-weighted decay is slower than the equal-weighted: 0.69 → 0.60 → 0.49.

- **Sharpe ratios (annualized):** EW raw hedge t+1 1.36; EW adjusted 1.66 / 1.23 / 0.88 for t+1..t+3; VW adjusted 0.84 / 0.70 / 0.60. Same-period factors: MKT 0.36, SMB 0.22, HML 0.48, MOM 0.77.
- **Short vs long leg:** the short side is larger in absolute value, but the five lowest deciles all earn significantly positive abnormal returns in t+1 and t+2 (four lowest in t+3), so long-only harvesting works; a long-only accruals strategy does not in this sample.
- **Versus accruals:** the EW NOA hedge profit is more than 88% larger than the operating-accruals hedge in t+1 and over 138% larger in t+3. NOA beats accruals in 28 of 38 years (EW; more evenly split VW), and accruals lose significantly in 2000–2002 while NOA does not.
- **Time series (Fig. 2):** EW hedge profitable in 35 of 38 years, the losing years all before 1973; the strongest year is 1999, but results survive dropping it; profits are larger in recent years. The VW series is less uniform.

### Fama–MacBeth (Tables 5, 7; 438 months, July 1966–Dec 2002)
Controls: ln size, ln B/M, Ret(−1), Ret(−12:−2), Ret(−36:−13).

| Specification | Accruals coef (t) | NOA coef (t) |
|---|---|---|
| NOA lag 1, no accruals | — | −0.0069 (−8.98) |
| NOA lag 1 + accruals | −0.0079 (−3.73) | −0.0058 (−6.67) |
| NOA lag 2 + accruals | −0.0062 (−3.13) | −0.0023 (−2.68) |
| NOA lag 3 + accruals | −0.0019 (−1.01) | −0.0024 (−2.72) |

NOA remains significant at a three-year lag where accruals do not. NOA_alt gives almost identical coefficients (−0.0066, t = −8.92).

**Stock vs flow.** The latest ΔNOA alone is strongly significant (−0.0078, t = −8.85), consistent with Fairfield et al. (2003), but once NOA is included ΔNOA becomes insignificant (t = −0.88 without accruals, t = 0.17 with), while NOA stays significant (t ≈ −4). Controlling for the sum of the past three years' accruals leaves the NOA coefficient essentially unchanged (−0.0058, t = −7.20); what remains of NOA after cumulative accruals is mostly cumulative investment, which therefore matters too.

**Financing side.** Because NOA = Equity + Debt − Cash (scaled), the components enter separately: Equity −0.0050 (t = −4.24), Debt −0.0066 (t = −6.03), and −Cash with a coefficient of the same sign and similar size (t ≈ 4). External financing predicts low returns mainly when it is put into operating assets, not when it is held as cash. The results survive removing firms with equity issuance > 10% of TA (so this is not just the new-issues puzzle) and M&A > 10% of TA. A multiplicative NOA × accruals term is insignificant; two-way sorts hint at a nonlinear interaction left for future work.

### Mishkin test (Table 8; FY1965–2000; 130,468 firm-years after 0.5% trimming)

$$
\mathrm{E}_{t+1}=\gamma_0+\gamma_1\mathrm{Acc}_t+\gamma_2\mathrm{NOA}_t+\gamma_3\mathrm{CF}_t+\nu_{t+1},\qquad
\mathrm{AR}_{t+1}=\beta(\mathrm{E}_{t+1}-\gamma_0-\gamma_1^*\mathrm{Acc}_t-\gamma_2^*\mathrm{NOA}_t-\gamma_3^*\mathrm{CF}_t)+\varepsilon_{t+1}
$$

The system is estimated by nonlinear GLS each year, and the differences are averaged Fama–MacBeth style (to avoid pooled cross-correlation bias).

| | Rational $\gamma$ | Market $\gamma^*$ | Test $\gamma=\gamma^*$ | Years $\gamma<\gamma^*$ (of 36) |
|---|---|---|---|---|
| Accruals | 0.557 | 0.628 | t = 1.82 | 22 |
| NOA | −0.004 (t = −0.57) | 0.043 (t = 3.10) | t = 4.18 | 28 |
| Cash flows | 0.663 | 0.552 | t = −4.18 | 11 |

$\beta = 1.506$ (t = 13.96). The rational weight on NOA is about zero: higher cross-sectional earnings levels offset the subsequent decline. The market's weight is positive and significant, so investors treat NOA as good news for next year's earnings. Once NOA is in the system, accrual overweighting is only marginal, and cash flows are underweighted. The overweighting of NOA survives replacing Accruals with SumAccruals or ΔNOA. The results are similar with 0.25% trimming. The portfolio and Fama–MacBeth tests use no trimming.

## Limitations

- The risk-vs-mispricing question is addressed only through controls (DGTW characteristics, FF3/Carhart, B/M and past returns as growth proxies). There is no explicit investment-based risk model; later q-theory work (asset growth, investment factors) reads the same pattern as a discount-rate effect.
- The Mishkin test covers only one-year-ahead earnings, needs trimming in three of 36 years, and is subject to Kothari et al. (2005) concerns about trimming-induced bias.
- The results are strongest equal-weighted and on the short side, where small, hard-to-borrow high-NOA names concentrate. Transaction costs and borrow are not modeled.
- The operating/financial classification is residual-based (e.g. operating cash lumped with short-term investments; goodwill kept in NOA). NOA_alt mitigates this.
- The sample ends in 2002; the paper itself notes that arbitrage had not yet removed the effect.

## Assessment

**Convincing:** the identity-based motivation, the long horizon (three years, with monotone decile patterns), survival of ΔNOA, summed accruals and a three-year lag in the regressions, and the Mishkin evidence that the market weight on NOA has the wrong sign. The financing decomposition is a useful reframing: it places NOA alongside asset growth and net issuance as one balance-sheet phenomenon, with the cash component separating "raised and invested" from "raised and hoarded".

**Fragile or dated:** the equal-weighted magnitudes (Sharpe 1.66) are largely small-cap and short-leg driven; value-weighted numbers (0.69%/month, Sharpe 0.84) are the relevant benchmark for capacity. Much of the NOA signal overlaps with later asset-growth and investment factors (Cooper–Gulen–Schill; the CMA/investment factor), so its standalone alpha against modern factor sets is smaller than these 1964–2002 tables suggest. The attention mechanism is asserted rather than directly tested (no attention proxies or interactions).

**Practical use:** scaled NOA (lagged-TA deflator, at least a 4-month reporting lag) is a slow-decaying, low-turnover accounting signal that complements accruals and cash-based profitability. Its multi-year decay supports annual rebalancing. Industry-neutralize it, given the strong industry composition of the extreme deciles. In a factor-model context, test it for incremental alpha over investment/asset-growth and profitability before assigning weight.

## Relation to literature

Extends Sloan (1996) accruals and the one-year accrual/ΔNOA results of Richardson et al. (2003) and Fairfield, Whisenant and Yohn (2003) to a cumulative stock measure; builds on Hirshleifer–Teoh (2003) limited-attention theory; relates to Barton–Simko (2002; NOA constrains beating forecasts), Loughran–Ritter (1995) new issues, and Titman–Wei–Xie (investment); Zhang (2004) studies industry versus within-industry NOA.

## Scholar Tags

`NOA`, `balance-sheet-bloat`, `sustainability-effect`, `limited-attention`, `accruals`, `Mishkin`, `1964-2002`, `JAE`.
