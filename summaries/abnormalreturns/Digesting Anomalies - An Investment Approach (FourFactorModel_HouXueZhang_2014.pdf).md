# Digesting Anomalies: An Investment Approach

**Kewei Hou, Chen Xue, Lu Zhang · 2014 (RFS advance access 26 Sep 2014; published RFS 28(3), 2015) · Source file `Finance/FourFactorModel_HouXueZhang_2014.pdf` (accepted manuscript, 87 pp.) · CRSP + Compustat annual/quarterly, NYSE/Amex/NASDAQ ex-financials and negative-BE firms, Jan 1972 – Dec 2012 (492 months)**

## Claim / contribution

- An empirical **q-factor model** — market (MKT), size ($r_{ME}$), investment ($r_{I/A}$) and profitability ($r_{ROE}$) — "largely summarizes" the cross-section of average returns, motivated by the investment first-order condition of q-theory.
- Of ~80 anomalies (74 primary + 6 momentum-reversal variants), **38 of 73 tested high-minus-low spreads are insignificant** once portfolios use **NYSE breakpoints and value weights** (incl. 12 of 13 trading-friction anomalies). Authors: many anomaly claims are "exaggerated, likely by excessively weighting on microcaps".
- For the **35 significant anomalies**, the q-model beats Carhart and, by more, FF3 (mean |α| of H−L spreads 0.20% vs 0.33% vs 0.55%/month), with two clear failures (operating accruals, R&D-to-market).
- Model is explicitly **reduced form**: silent on risk vs mispricing; comovement of stocks with similar I/A or ROE is not implied by the first-order condition itself.

## Economic motivation (Section 1)

Two-period model; household SDF $M_1=\rho U'(C_1)/U'(C_0)$. Firm $i$ has assets $A_{i0}$, profitability $\Pi_{i0}$, invests $I_{i0}$ with quadratic adjustment cost, full depreciation ($A_{i1}=I_{i0}$):
$$D_{i0}=\Pi_{i0}A_{i0}-I_{i0}-\tfrac{a}{2}\Big(\tfrac{I_{i0}}{A_{i0}}\Big)^2A_{i0},\qquad D_{i1}=\Pi_{i1}I_{i0}.$$
FOC: $1+a\,I_{i0}/A_{i0}=E_0[M_1\Pi_{i1}]$, hence (Eqs. 3–4)
$$r^S_{i1}=\frac{\Pi_{i1}}{1+a\,I_{i0}/A_{i0}},\qquad E_0[r^S_{i1}]=\frac{E_0[\Pi_{i1}]}{1+a\,I_{i0}/A_{i0}}.$$
- **Investment channel:** given expected profitability, high I/A ⇒ low expected return (low discount rate ⇒ many positive-NPV projects). Maps to issuance, B/M (denominator = marginal q = market-to-book), accruals, long-term reversal.
- **Profitability channel:** given I/A, high expected profitability ⇒ high expected return. Maps to momentum, PEAD/earnings surprise, distress. Equivalent to a Gordon-type "expected cash flow / market equity" statement.
- Both relations are **conditional**; unconditionally investment and returns could be positively related if high investment brings high ROE — hence the joint (triple) sort.
- Current quarterly ROE is only a proxy for expected profitability; $a$ is never estimated and no structural test is run.

## Factor construction (Section 2, Table 1)

- $I/A_{i,y}=(AT_{y}-AT_{y-1})/AT_{y-1}$ (annual total-asset growth, not capex).
- $ROE_{i,q}=IBQ_{q}/BE_{q-1}$. Quarterly BE (Davis–Fama–French style): SEQQ, else CEQQ+PSTKQ, else ATQ−LTQ; + TXDITCQ; − preferred (PSTKRQ, else carrying value). SEQQ/CEQQ used first for better pre-1980 coverage.
- **Timing:** size and I/A sorted end-June $t$ (I/A for fiscal year ending in $t-1$), held July–June. ROE sorted **monthly** using the latest earnings after the announcement date RDQ (earnings announced 5 or 25 March enter the April sort, scaled by the previous quarter's BE); the fiscal quarter must have ended ≤6 months before formation. Other quarterly accounting items used in test portfolios get a 4-month lag.
- **Independent 2×3×3 sort:** NYSE median size; NYSE 30/70 breakpoints for I/A and ROE ⇒ 18 value-weighted portfolios.
$$r_{ME}=\bar R_{9\,\text{small}}-\bar R_{9\,\text{big}},\quad r_{I/A}=\bar R_{6\,\text{low }I/A}-\bar R_{6\,\text{high }I/A},\quad r_{ROE}=\bar R_{6\,\text{high ROE}}-\bar R_{6\,\text{low ROE}}$$
(simple averages across cells, VW within cells). MKT = CRSP VW − 1m T-bill; SMB/HML/UMD from French's site.
- Market-cap coverage: size/I/A/ROE factors 92.76% / 50.42% / 58.07% vs SMB/HML/UMD 97.20% / 66.92% / 54.48%.

**Table 1 (monthly %, HAC $t$ in parentheses):**

| Factor | Mean | CAPM α | FF3 α | Carhart α | Key correlations |
|---|---:|---:|---:|---:|---|
| $r_{ME}$ | 0.31 (2.12) | 0.23 (1.62) | 0.04 | 0.01 | SMB 0.95 (SMB mean 0.19, $t$=1.35) |
| $r_{I/A}$ | 0.45 (4.95) | 0.52 (5.93) | 0.33 (4.85) | 0.28 (3.85) | HML 0.69; MKT −0.36 |
| $r_{ROE}$ | 0.58 (4.81) | — | 0.77 (6.94), $R^2$=20% | 0.50 (4.75) | UMD 0.50; SMB −0.38; $r_{I/A}$ 0.06 (p=0.20) |

HML (0.40%, $t$=2.60) and UMD (0.72%, $t$=3.41) have q-alphas of only 0.06% and 0.13% (within 1 s.e.): HML/UMD look like "noisy versions" of the q-factors, not vice versa. The authors note $t$ of 4.95 and 4.81 clear the Harvey–Liu–Zhu $t>3$ hurdle.

## Test design

Time-series regressions of decile (and H−L) excess returns:
$$r^i_t-r^f_t=\alpha^i_q+\beta^i_{MKT}MKT_t+\beta^i_{ME}r_{ME,t}+\beta^i_{I/A}r_{I/A,t}+\beta^i_{ROE}r_{ROE,t}+\epsilon^i_t,$$
vs CAPM, FF3, Carhart. Diagnostics: H−L α and HAC $t$; mean |α| across deciles; GRS p-value. Test portfolios: NYSE-breakpoint deciles, VW (exceptions: industry momentum 9 groups of 5 of 45 industries; NEI 9 groups; F-score). Annual sorts use FF June timing; earnings-based monthly sorts follow the ROE timing. For monthly-rebalanced variables tested at 1- and 6-month holding periods, only the **higher-spread** horizon is reported (raises the bar for the q-model but is an in-sample choice). Categories: momentum, value-vs-growth, investment, profitability, intangibles, trading frictions. Appendix A gives full Compustat definitions (SUE, Abr, RE, R6-6, R11-1, I-Mom, B/M, E/P, CF/P, NO/P, Dur, I/A, NOA, PI/A, IG, NSI, CEI, IvG, IvC, OA, POA, PTA, ROE, ROA, GP/A, NEI, FP, OC/A, Ad/M, RD/M, OL, Svol, …).

## Main results

**Insignificant in the broad cross-section (Table 3):** 38 anomalies, e.g. idiosyncratic volatility −0.54% ($t$=−1.56), short-term reversal −0.31% ($t$=−1.39), analyst dispersion, Amihud illiquidity, abnormal investment −0.27%, total accruals −0.19%, F-score 0.37%, G-index 0.03% ($t$=0.09), accrual quality −0.18% ($t$=−0.79). Systematic volatility is the only significant friction anomaly.

**35 significant anomalies (Table 4):**

| Diagnostic | FF3 | Carhart | q |
|---|---:|---:|---:|
| Mean \|α\| of H−L, %/month | 0.55 | 0.33 | **0.20** |
| # significant H−L alphas (5%) | 27 | 19 | **5** |
| Mean \|α\| across all deciles | 0.16 | 0.12 | **0.11** |
| # decile sets rejected by GRS (5%) | 28 | 24 | **20** |

By category (mean |α| H−L, q / Carhart / FF3; # significant):
- **Momentum (9):** 0.19 / 0.29 / 0.85; significant 2 / 5 / 9; GRS rejects q and Carhart in 6/9. SUE-1: raw 0.45 ($t$=3.59), $\alpha_{FF}$ 0.55, $\alpha_C$ 0.34, $\alpha_q$ 0.16 ($t$=1.12). R6-6: raw 0.85 ($t$=3.17), $\alpha_{FF}$ 1.12, $\alpha_C$ 0.06, $\alpha_q$ 0.24 ($t$=0.71). R11-1: raw 1.18, $\alpha_C$ 0.09, $\alpha_q$ 0.24. Carhart fits price momentum itself better; q fits earnings momentum (RE-1: raw 0.89, $\alpha_C$ 0.56 vs $\alpha_q$ 0.12).
- **Value vs growth (5):** comparable across models; none of B/M, E/P, CF/P, Dur has a significant α in any model; net payout yield significant in all (q 0.36, Carhart 0.49, FF3 0.52). GRS rejects q (not the others) on CF/P deciles.
- **Investment (11):** 0.22 / 0.30 / 0.38; significant 1 / 6 / 10; GRS rejects all models for most sets.
- **Profitability (5: ROE, ROA, GP/A, NEI, FP):** 0.12 / 0.61 / 0.95; significant 0 / 5 / 5; GRS rejects q in 1/5, others 5/5. E.g. ROE decile spread 0.80% raw, $\alpha_q$ 0.05; failure probability −0.67 raw, $\alpha_{FF}$ −1.44, $\alpha_q$ −0.17.
- **Significant q-alphas (5):** Abr-1 0.64 ($t$=4.07), Abr-6 0.26 (2.18), NO/P 0.36 (2.38), OA −0.56 (−3.90), RD/M 0.60 (2.40).
- **Size factor:** dropping it raises mean |α| only 0.20 → 0.23 (Table 5), but the small-minus-big size decile α goes 0.03 → 0.66 ($t$=2.16).

**Mechanism (Table 6 loadings on H−L):** momentum/earnings anomalies load on ROE (β_ROE 0.18–1.48, all significant; ROE spreads 1.49–6.58%/quarter), not I/A. Value and investment/issuance/accrual anomalies load on I/A (e.g. B/M β_I/A 1.45, $t$=12.74; I/A deciles −1.37; NSI −0.68; I/A spreads 11.12–83.89% p.a.). Profitability/distress anomalies load on ROE (−1.61 for FP to 1.50 for ROE, |t|>7). Organizational capital captured by combination (β_I/A 0.35, β_ROE 0.51; raw 0.56, $\alpha_q$ 0.09 vs $\alpha_C$ 0.40). Svol: β_ROE −0.43, $\alpha_q$ −0.37 ($t$=−1.42) vs Carhart −0.62. Ivol (footnote 11): $\alpha_{FF}$ −0.92 ($t$=−4.66), $\alpha_C$ −0.59, $\alpha_q$ −0.08 ($t$=−0.39); β_I/A and β_ROE both −0.94.

**Deciles (Table 7):** SUE-1 ROE loadings rise −0.22 → 0.26 and characteristic ROE −0.80% → 5.00%/quarter; R6-6 loadings −0.74 → 0.28, ROE −0.71% → 3.43%. Significant decile alphas: SUE-1 5 (FF3) / 3 (Carhart) / 1 (q); R6-6 4 / 3 / 0.

## Failures and robustness

- **Operating accruals (Table 9):** raw H−L −0.30%, $\alpha_q$ −0.56% (worse than Carhart −0.33). Low- and high-OA deciles have near-identical β_I/A (−0.56 vs −0.58) despite I/A of 13.87% vs 24.02% p.a.; β_ROE −0.26 vs 0.03 goes the wrong way (accruals inflate earnings). **Percent accruals (POA)**, scaled by |earnings|, works: β_ROE flat, β_I/A 0.35 → −0.55, raw −0.46, $\alpha_q$ −0.12 ($t$=−0.87).
- **R&D-to-market:** raw 0.63 ($t$=2.31), $\alpha_{FF}$ 0.22, $\alpha_C$ 0.31, $\alpha_q$ 0.60 ($t$=2.40). Expensed R&D depresses ROE (spread −2.80%/quarter, β_ROE −0.58, $t$=−4.10). Capitalizing R&D suggested but not tested.
- **Momentum reversal (Table 8):** holding periods $t..t{+}11$, $t{+}12..t{+}35$, $t{+}36..t{+}59$; only R6-12 raw spread is significant (0.57, $t$=2.67; $\alpha_{FF}$ 0.86, $\alpha_q$ 0.17). No significant q H−L alpha, but GRS rejects q for 5 of 6 decile sets at 5%.
- **25 size–B/M (Table 10):** value premium 1.02% ($t$=4.59) in small, 0.16% in big. Mean |α| q 0.11 vs FF3 0.10, Carhart 0.11; significant 4 vs 5 vs 5; all rejected by GRS. Small-growth α: FF3 −0.54 ($t$=−4.84) vs q −0.25 ($t$=−1.48), but small-value $\alpha_q$ 0.32 ($t$=2.72). Performance driven by β_I/A spreads of 1.19–1.56.
- **Microcaps (footnote 10):** under NYSE breakpoints/VW, momentum losers/winners put 10.85%/5.17% of weight in microcaps (below NYSE 20th percentile) vs 63.58%/52.50% under all-exchange breakpoints/EW. Industry portfolios (FF 10): q roughly comparable to FF3/Carhart (online appendix, not in this PDF).

## Sharpe ratios (Table 11, monthly)

Individual: $r_{I/A}$ 0.24, $r_{ROE}$ 0.22, HML 0.13, UMD 0.16. Max SR $\sqrt{\mu_f'V_f^{-1}\mu_f}$: FF3 0.21, Carhart 0.30, **q 0.43**. Pooling 28 full-sample H−L spreads: 0.48; pooling all 28 decile sets: 1.60 (in-sample, huge covariance matrix). Category poolings: momentum 0.67, value 0.49, investment 0.65, profitability 0.49, other 0.59. So the q-factors do not span the anomaly frontier. The authors argue the q-factors' Sharpe ratios are "high, but not excessively high", implying comovement, yet concede the evidence is consistent with sentiment-driven mispricing (MacKinlay's argument applies even more strongly).

## Critical assessment

- **Convincing:** transparent, replicable construction; broad and consistently applied test set; clear economic mapping (Table 6 loadings match characteristic spreads); HML/UMD are subsumed while the reverse fails.
- **Fragile / caveats:**
  - "Explains anomalies" is relative: GRS still rejects in 20/35 sets. Insignificant α partly reflects wide standard errors.
  - Anomaly set and horizon (1 vs 6 months) chosen with knowledge of the literature; no out-of-sample period, no multiple-testing correction for the alphas.
  - The ROE factor uses monthly-updated **latest** earnings, so it partly shares information with earnings-momentum test assets (SUE, RE). Explaining them with a factor built from the same signal is closer to "spanning" than to economic explanation.
  - Results depend on the NYSE/VW estimand; conclusions about microcap anomalies are a change of target, not a refutation.
  - HAC details (kernel/lag) are not specified; only gross returns, no costs or capacity.
  - Minor: the Dur definition (Eq. A3) mixes $P$ and ME notation; RE is called a moving average but written as a sum.
- Later HXZ work (q⁵, expected-growth factor) addresses some failures; this paper is the original four-factor version.

## Practical relevance for a quant PM

- A parsimonious attribution benchmark: before claiming alpha, regress on MKT, ME, I/A, ROE (data on the authors' q-factor site). Many "new" signals are repackaged investment or profitability tilts.
- Implementation details matter: announcement-date-driven ROE timing (RDQ, ≤6-month staleness), annual vs monthly rebalance clocks, NYSE breakpoints, equal averaging of VW cells.
- Profitability/earnings signals are best updated monthly with fresh quarterly data; investment-type signals are slow (annual).
- Watch denominators (OA vs POA; R&D expensing) — a signal's factor exposures can flip sign with scaling.
- The in-sample max SR of 0.43/month for the factors themselves is not an investable forecast; costs, turnover of the monthly ROE leg, and short-side frictions are not addressed.
