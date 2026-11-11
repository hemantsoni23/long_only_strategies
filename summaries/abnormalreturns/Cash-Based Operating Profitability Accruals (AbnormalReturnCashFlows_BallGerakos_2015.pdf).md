# Accruals, Cash Flows, and Operating Profitability — Ball, Gerakos, Linnainmaa & Nikolaev (2015) — Detailed Quantitative Research Notes

**Ray Ball, Joseph Gerakos, Juhani T. Linnainmaa, Valeri Nikolaev** (Chicago Booth) · "Accruals, Cash Flows, and Operating Profitability in the Cross Section of Stock Returns" · Chicago Booth Working Paper No. 15-12, SSRN 2587199, April 17, 2015 (working-paper draft; numbers below are from this version) · Source file: `Finance/AbnormalReturnCashFlows_BallGerakos_2015.pdf`

---

## Question and claim

Profitability predicts returns positively (Novy-Marx 2013; Ball et al. 2014), but profitability contains accruals, which predict returns negatively (Sloan 1996), and the accrual anomaly survives FF3, FF5, Novy-Marx GP and Hou–Xue–Zhang $q$ — it actually *strengthens* once a profitability factor is added. The paper's claims:

1. **Cash-based operating profitability (CbOP)** beats operating profitability (OP), and thereby GP and net income (which Ball et al. 2014 showed OP dominates).
2. CbOP **subsumes** the accrual anomaly.
3. CbOP predicts returns up to **ten years** ahead, which argues against announcement-period mispricing of earnings components.

Motivation mirrors Fama–French (1992) collapsing $\ln(A/ME)$ and $\ln(A/BE)$ into $\ln(BE/ME)$: in a joint Fama–MacBeth regression the OP and accruals slopes are of opposite sign and similar magnitude (2.55 vs −1.76, ×100), so an OP increase that is entirely accrual-driven predicts roughly no change in expected return. Only the cash part of profitability is priced.

## Definitions (Appendix)

All scaled by lagged total assets $AT_{t-1}$.

$$\mathrm{OP}=\mathrm{REVT}-\mathrm{COGS}-(\mathrm{XSGA}-\mathrm{XRD})$$
(R&D is added back to SG&A to undo Compustat's folding of R&D into XSGA — so OP is before R&D expense.)

$$\mathrm{CbOP}=\mathrm{OP}-\Delta\mathrm{RECT}-\Delta\mathrm{INVT}-\Delta\mathrm{XPP}+\Delta(\mathrm{DRC}+\mathrm{DRLT})+\Delta\mathrm{AP}+\Delta\mathrm{XACC}$$
Missing balance-sheet items set to zero. Post-1988 alternative: $\mathrm{OP}-\mathrm{RECCH}-\mathrm{INVCH}-\mathrm{APALCH}$ from the cash-flow statement.

**Accruals** (Sloan 1996, balance-sheet): $\Delta ACT-\Delta CH-(\Delta LCT-\Delta DLC-\Delta TXP)-DP$. Note this includes depreciation and working-capital items outside the OP perimeter, so CbOP is *not* OP minus Sloan accruals; the two signals are constructed from overlapping but different accounts.

CbOP is neither "earnings + depreciation" (which still contains working-capital accruals) nor GAAP CFO (which is after interest and taxes, hence levered).

The paper frames accruals as absorbing two things: payment-timing shocks and working-capital investment for growth. CbOP therefore mixes profitability, payment shocks and growth, which accrual accounting deliberately purges from earnings.

## Data

CRSP monthly returns and Compustat annual, NYSE/Amex/NASDAQ ordinary common shares, **July 1963 – December 2013**; financials (SIC first digit 6) excluded; missing performance-related delisting returns set to −30%; standard six-month reporting lag; book equity per Davis–Fama–French with DFF fill-ins. Microcaps = below NYSE 20th percentile of ME. FM regressions control for $\ln(BE/ME)$, $\ln ME$, $r_{1,1}$, $r_{12,2}$, with all regressors trimmed at 1/99 on a common sample across columns (2)–(7).

**Table 1.** Means: OP 0.129 (SD 0.158), accruals −0.028 (0.114; negative largely because of depreciation), CbOP 0.117 (0.174). Correlations (Pearson/Spearman): OP–CbOP 0.844/0.804; OP–accruals 0.165/0.132; CbOP–accruals −0.253/−0.280. The last sign is the key: firms that are profitable because of accruals tend to be cash-poor.

## Results

### Fama–MacBeth (Table 2, slopes ×100, $t$ in parentheses)

All-but-microcaps:

| Col | OP | Accruals | CbOP |
|---|---|---|---|
| (1) OP, own trim | 3.04 (8.97) | | |
| (2) OP, common sample | 2.56 (6.97) | | |
| (3) Accruals | | −1.58 (−4.40) | |
| (4) OP + Acc | 2.55 (7.01) | −1.76 (−4.99) | |
| (5) CbOP | | | 2.65 (9.84) |
| (6) CbOP + Acc | | 0.01 (0.02) | 2.57 (7.40) |
| (7) OP + CbOP | 0.62 (1.19) | | 2.12 (5.83) |

Microcaps: OP 2.09 (5.24); accruals −2.01 (−6.41); OP+Acc 2.30 (5.78) / −2.54 (−8.43); CbOP 2.47 (9.50); CbOP+Acc 2.25 (6.55) / −0.80 (−1.85); OP vs CbOP 0.21 (0.42) vs 2.19 (7.23).

Because FM slopes are returns on orthogonalized long–short portfolios (Fama 1976 ch. 9), $t\approx SR_{ann}\sqrt{T}$. Moving from OP to CbOP raises the strategy's annualized Sharpe ratio by over 40% in all-but-microcaps (bootstrap $t=4.91$, 1,000 resamples of the slope series) and by 0.65 in microcaps ($t=3.29$). In microcaps accruals retain a marginal residual ($t=-1.85$) — subsumption is cleaner in larger stocks.

**Interpretation of column (4).** OP and accruals are positively correlated but carry opposite return loadings, so each is attenuated when the other is omitted; adding both makes both stronger. This is the same mechanism that makes FF5's accrual-inclusive RMW worsen the pricing of accrual-sorted portfolios.

**Against Sloan's fixation story.** If investors failed to see that accruals are less persistent than cash flows, accruals should still predict (negative) surprises conditional on CbOP. They do not ($t=0.02$).

**Cash-flow-statement accruals** (Table 3, July 1988–2013, all-but-microcaps): same conclusions with lower $t$ from the shorter sample — CbOP standalone $t\approx 6.3$–$6.5$ vs OP 5.1–5.5; accruals insignificant with CbOP ($|t|<0.9$); OP insignificant in the horse race (t 0.77/0.19) while CbOP stays at 3.3/3.7.

**Time variation (Fig. 1, rolling 10-year $t$).** CbOP's $t$ generally exceeds OP's; the accrual $t$ is negative until 2008. From about 2004 all three, and momentum, attenuate toward zero — a general anomaly decay (Green–Hand–Soliman 2011; Keloharju–Linnainmaa–Nyberg), not specific to earnings signals.

### Portfolio sorts (Table 4, VW, NYSE breakpoints, annual June rebalance)

| Signal | Decile H−L excess | Decile H−L FF3 α | Quintile H−L FF3 α |
|---|---|---|---|
| OP | 0.29%/mo (1.84) | 0.75 (5.99) | 0.56 (5.81) |
| Accruals | −0.38 (−2.76) | −0.43 (−3.25) | −0.29 (−3.00) |
| CbOP | 0.47 (3.16) | **0.90 (8.50)** | **0.72 (8.21)** |

Detail missed by most readings: the CbOP spread is driven more by the **short leg** — decile 1 FF3 α −0.56%/mo ($t=-6.75$) vs decile 10 +0.35 ($t=5.90$). Excess-return spreads are much smaller than alphas because profitable firms load negatively on HML/SMB; the profitability premium is largely a "pure bet" only after hedging those exposures.

### Two-way sorts (Table 5): accruals within profitability deciles

- Within OP deciles, the OP-neutral high-minus-low accrual strategy earns FF3 α −0.31%/mo ($t=-3.62$), essentially the unconditional −0.29 — OP does nothing to explain accruals.
- Within CbOP deciles, the CbOP-neutral accrual strategy earns −0.04 ($t=-0.42$); only one decile shows a significant spread, and it is *positive*.
- Conversely, the accrual-neutral CbOP 10−1 spread is 1.28%/mo ($t=12.75$), with similar 1.2–1.33 spreads inside every accrual quintile.

### Factor tests (Table 6: 25 size × accruals portfolios)

Factors built FF2015-style (2×3 size × NYSE 30/70 profitability, SMB averaged across the two sort sets).

| Model | GRS | $A|\hat\alpha|$ | $A|a_i|/A|\bar r_i|$ | $A(\hat\alpha^2)/A(\hat\mu^2)$ | $A(R^2)$ |
|---|---|---|---|---|---|
| FF3 | 3.59 | 0.115 | 0.71 | 0.46 | 0.90 |
| FF3 + RMW$^{OP}$ | 4.06 | 0.156 | 0.96 | 0.91 | 0.90 |
| FF3 + RMW$^{CbOP}$ | **2.22** | 0.125 | 0.77 | 0.47 | 0.90 |

RMW$^{OP}$ makes the low-accrual alphas larger (small/low-accrual α rises from 0.85% to 3.50% p.a.). With RMW$^{CbOP}$ no high-accrual portfolio has a significant alpha. The model is still rejected, but its GRS (2.22) is below FF3's on its own home turf (25 size–B/M, GRS 3.52 over the same period). Note RMW$^{CbOP}$ beats FF3 on GRS but is only comparable on the other statistics.

### Investment opportunity set (Table 7, ex post tangency Sharpe ratios)

Market 0.39 → + SMB, HML, UMD 1.07 → +Acc 1.13; +RMW$^{OP}$ 1.40; +RMW$^{CbOP}$ **1.70**; +RMW$^{CbOP}$+Acc 1.72; +RMW$^{OP}$+Acc 1.58. Factor means (annual): accruals 2.9% ($t=3.65$), OP 3.53% ($t=3.97$), CbOP 4.82% ($t=6.3$). The striking result: OP and accruals factors together (1.58) are dominated by the single CbOP factor (1.70). The authors attribute this to information lost when each characteristic is coarsened into its own six portfolios — the combination of coarsened factors cannot reconstruct the coarsened version of the combined characteristic. Growth of \$1 (compounded FF3 α + residual of decile H−L, June 1963–Dec 2013): OP \$71.5, accruals \$9.8, CbOP \$191.9, market excess \$11.0.

### Horizon (Figs. 3–4; July 1973–Dec 2013, all-but-microcaps, lagged signal, updated controls)

- OP and CbOP slopes decay but remain reliably positive for ten years. Accruals are at best marginally significant one year out and insignificant thereafter.
- CbOP–OP Sharpe difference: positive in mean out to seven years, 95% CI above zero out to four years.
- Cumulative slopes (Jegadeesh–Titman-style overlapping-strategy logic, slopes not ×100): 0.028 at lag 0, ~0.5 at two years, crossing 1.0 at about five years. For a firm with AT = ME, a \$1M increase in CbOP is associated with more than \$1M of additional shareholder returns over five years.
- Untabulated reverse-timing test: current CbOP is *positively* related to past returns, so the forward predictability is not a reversal of past underreaction.

The authors read decade-long predictability as more consistent with stationary expected-return determinants (e.g., risk) than with mispricing, since limits to arbitrage are unlikely to persist that long. They also stress that accruals remain valuable for contracting and performance measurement (Dechow 1994); the claim is about return prediction only.

## Assessment

**Convincing.**
- Three independent lenses agree: FM subsumption ($t=0.02$), nonparametric conditional sorts (−4 bp), and factor spanning (Sharpe 1.70 vs 1.72). The results hold with cash-flow-statement accruals post-1988, which addresses the Hribar–Collins M&A contamination of balance-sheet accruals.
- The finding is clean and parsimonious: one characteristic replaces two, and it gives a simple explanation of the accrual anomaly — high-accrual firms are less profitable on a cash basis.

**Fragile or open.**
- "Subsumes accruals" is a statement about Sloan balance-sheet accruals. CbOP itself contains the working-capital accrual components with the opposite sign, so part of the result is mechanical re-packaging; the substantive content is that the accrual items *outside* the OP perimeter (depreciation, other current items) carry no incremental information.
- The risk interpretation rests on horizon persistence alone; no risk factor, covariance or macro exposure is identified. Persistent characteristics (profitability is highly autocorrelated) mechanically generate long-horizon predictability even under slow-moving mispricing, and the controls are updated while the signal is stale.
- Tangency Sharpe ratios are in-sample and gross of costs; the 1963–2013 full-sample $t$ masks a post-2004 decay shared by nearly all anomalies.
- Microcap subsumption is incomplete ($t=-1.85$ on accruals).
- The alpha is short-leg heavy (low-CbOP firms), which matters for borrow cost and capacity.

**For a quant PM/researcher.**
- Use CbOP (with R&D added back) rather than GP/OP/ROE-type profitability in a multi-factor alpha or risk model; a separate accrual sleeve adds essentially nothing once CbOP is in (1.70 → 1.72).
- Build profitability from the characteristic, not by combining coarsened factor returns — the Table 7 result is a general caution about 2×3 factor construction.
- The signal is annual and slow-decaying (CI above OP out to four years), so turnover is low; construction details matter (XSGA−XRD, sign conventions on deferred revenue/payables, zero-filling missing items, −30% delisting returns on the short side).
- Treat the post-2004 attenuation as the base case when sizing; monitor rolling FM $t$.

Related: Sloan (1996); Ball et al. (2014) "Deflating profitability"; Novy-Marx (2013); Fama–French (2015); Hou–Xue–Zhang (2015); Desai–Rajgopal–Venkatachalam (2004) and Cheng–Thomas (2006) on accruals vs. CFO/P value; Foerster–Tsagarelis–Wang (2015) on free cash flow.
