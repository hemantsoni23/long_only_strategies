# Accrual Anomaly / Abnormal Returns — Sloan (1996) — Detailed Quantitative Research Notes

| Field | Detail |
|------|--------|
| **Title** | Do Stock Prices Fully Reflect Information in Accruals and Cash Flows about Future Earnings? |
| **Author** | Richard G. Sloan (University of Pennsylvania) |
| **Journal** | *The Accounting Review*, Vol. 71, No. 3 (July 1996), pp. 289–315 |
| **Sample** | 40,679 NYSE/AMEX firm-years, Compustat ∩ CRSP, fiscal years 1962–1991 |
| **Source file** | `Finance/AbnormalReturnAccrual_Sloan_1996.pdf` (Drive id `0B-6kBz0I0dMsS1NRZU9EYkhGaXM`) |

The founding paper of the accrual anomaly. Sloan formalizes the financial-statement-analysis folklore (Graham–Dodd–Cottle "earnings power" adjustments; Bernstein: a high CFO/NI ratio signals earnings quality) into three testable claims: accrual-driven earnings are less persistent than cash-driven earnings; prices behave as if investors fixate on total earnings; hence low-accrual firms outperform high-accrual firms, with the correction arriving partly at subsequent earnings announcements.

---

## Hypotheses

- **H1 (persistence):** persistence of earnings is decreasing in the accrual component and increasing in the cash-flow component.
- **H2(i) (pricing):** earnings expectations embedded in prices do not fully reflect this persistence difference.
- **H2(ii) (trading):** long low-accrual / short high-accrual earns positive abnormal returns.
- **H2(iii) (timing):** those returns cluster around subsequent earnings announcements.

The naive alternative is weaker than the random walk used by Ou–Penman (1989) and Bernard–Thomas (1990): prices may know the *average* persistence of earnings but not the component-specific persistences (functional fixation, Hand 1990). Relative to those papers Sloan (a) uses an accounting-process-based rather than statistical forecasting model and (b) checks whether the *magnitude* of return predictability matches the naive model, not only its sign. It also reconciles Bernard–Stober (1989), who found no systematic contemporaneous price reaction to the cash/accrual split: the components *do* differ in information content, but prices only absorb it when future earnings arrive.

---

## Data and Measurement

- Sample path: 71,732 Compustat NYSE/AMEX firm-years (1962–1991) → 53,322 with accrual data → 42,120 on CRSP → **40,679** with next-year earnings. Pre-1962 dropped (survivorship, missing data); banks and insurers drop out for lack of current-asset/liability data.
- **Earnings** = operating income after depreciation (Compustat #178), i.e. income from continuing operations *before* interest, taxes, special and extraordinary items — chosen because non-recurring items cannot be split into cash and accrual parts.
- **Balance-sheet accruals** (SFAS 95 cash-flow statements existed only for the last 4 sample years):

$$
\text{Accruals} = (\Delta CA - \Delta \text{Cash}) - (\Delta CL - \Delta STD - \Delta TP) - \text{Dep}
$$

(items #4, #1, #5, #34, #71, #14). Short-term debt is excluded as financing; taxes payable is excluded for consistency with a pre-tax earnings definition; interest accruals are mostly excluded via the debt accounts.
- **Cash flow component** = Earnings − Accruals. All three variables are scaled by **average total assets** (#6). Market equity is rejected as deflator because it itself predicts returns; net operating assets can be negative. Results are said to be insensitive to the deflator.
- **Returns:** buy-and-hold starting 4 months after fiscal year-end (Alford et al. 1994), years $t+1,t+2,t+3$. Delisting returns included, proceeds reinvested in the size-matched portfolio; missing performance-related delisting returns set to −100% (robust to dropping them or using 0).
- **Abnormal returns:** (1) size-adjusted — minus the value-weighted CRSP NYSE/AMEX size-decile portfolio; (2) Ibbotson (1975) event-time Jensen alphas, $(R_{pt}-R_{ft}) = \alpha_p + \beta_p(R_{mt}-R_{ft}) + \varepsilon_{pt}$, estimated on 30 annual observations per portfolio and horizon with an equal-weighted NYSE/AMEX market; December year-ends only ($N=24{,}209$).

---

## Descriptive Facts (Table 1, accrual deciles)

| | Lowest | 4 | Highest |
|---|---|---|---|
| Cash flow (mean) | 0.22 | 0.15 | 0.00 |
| Earnings (mean) | 0.07 | 0.11 | 0.15 |
| Portfolio beta | 1.25 | 0.86 | 1.23 |
| log ME | 3.80 | 4.97 | 3.99 |
| ΔCA component | −0.08 | 0.02 | 0.21 |
| ΔCL component | −0.03 | −0.02 | −0.03 |
| Depreciation | −0.06 | −0.05 | −0.03 |

- Accruals and cash flows are strongly negatively related (rank corr −0.53); accruals and earnings positively. Rank corr of accruals with accruals/earnings is 0.94, so sorting on the level of accruals is effectively sorting on the *share* of earnings that is accrual.
- Beta and size are U-shaped: extremes are smaller and riskier, but the 1–10 hedge has beta 0.02 and negligible net size exposure.
- Nearly all variation comes from the current-asset component (mainly receivables and inventory, with industry-dependent mix). But the sort is **not** a sort on ΔCA: ΔCA and ΔCL are strongly negatively correlated in growing firms, so aggregate accruals isolate *disproportionate* working-capital changes.

---

## H1: Persistence (Tables 2–3, Figure 1)

$$
E_{t+1} = \alpha_0 + \alpha_1 E_t + v_{t+1}, \qquad
E_{t+1} = \gamma_0 + \gamma_1 A_t + \gamma_2 C_t + v_{t+1}, \quad \text{H1: } \gamma_1<\gamma_2 .
$$

| | Pooled, levels | Pooled, decile ranks |
|---|---|---|
| $\alpha_1$ | 0.841 ($t$=303.98 vs 0; $t$=−57.47 vs 1, Dickey–Fuller critical values) | 0.783 |
| $\gamma_1$ (accruals) | 0.765 | 0.565 |
| $\gamma_2$ (cash) | 0.855 | 0.838 |
| $F$-test $\gamma_1=\gamma_2$ | 614.01 | 4,894.24 |
| Industries with $\gamma_1<\gamma_2$ | 86% | 99% |

Two-digit SIC regressions: mean $\alpha_1 = 0.773$ (IQR 0.708–0.863); rank-based industry $\gamma_1$ centered 0.5–0.6, $\gamma_2$ around 0.8. Fixed-effects estimates leave conclusions unchanged. Outliers inflate the raw-value accrual coefficient; ranks widen the gap considerably.

**Figure 1:** extreme-earnings and extreme-cash-flow portfolios mean-revert slowly (far from complete by year +5); extreme-accrual portfolios revert mostly in year +1 and essentially completely by year +3. This horizon matches the return-predictability horizon below.

---

## H2(i): Mishkin (1983) Rational-Expectations Tests (Tables 4–5)

Efficiency implies abnormal returns load only on unexpected earnings:

$$
\begin{aligned}
E_{t+1} &= \gamma_0 + \gamma_1 A_t + \gamma_2 C_t + v_{t+1},\\
AR_{t+1} &= \beta\,\big(E_{t+1} - \gamma_0 - \gamma_1^* A_t - \gamma_2^* C_t\big) + \varepsilon_{t+1},
\end{aligned}
$$

with efficiency $\Leftrightarrow \gamma_j^* = \gamma_j$ and naive fixation $\Leftrightarrow \gamma_1^* = \gamma_2^*$. $AR$ is the size-adjusted return. Estimated jointly by iterative weighted nonlinear least squares (asymptotically equivalent to FIML; avoids generated-regressor standard errors and holdout samples of the Ou–Penman two-step approach). Test statistic $2n\log(SSR^c/SSR^u) \sim \chi^2(q)$. Mishkin's result that the cross-equation constraint test remains valid with omitted forecasting variables is invoked to address the obvious objection that $E_{t+1}$'s forecasting model is incomplete.

- **Total earnings (Table 4):** $\alpha_1 = 0.841$, $\alpha_1^* = 0.840$, LR = 0.007 ($p$=0.933). Ranks: 0.783 vs 0.775. Prices correctly embed average annual persistence — no annual-earnings analogue of Bernard–Thomas quarterly drift.
- **Components (Table 5), levels:** forecasting $\gamma_1=0.765,\ \gamma_2=0.855$; pricing $\gamma_1^*=0.911,\ \gamma_2^*=0.826$; LR = 180.91 ($p$=0.000). Prices treat accruals as *more* persistent than cash flows — worse than pure fixation (which would put both at 0.841).
- **Ranks:** $\gamma_1=0.565$ vs $\gamma_1^*=0.675$; $\gamma_2=0.838$ vs $\gamma_2^*=0.747$ — efficiency still rejected, but prices partially anticipate the lower accrual persistence. Sloan concludes the direction is robust while "precise inferences" about magnitude relative to fixation are specification-sensitive.

The joint reading of Tables 4 and 5 is the paper's methodological point: efficiency can hold relative to a coarse information set (total earnings) and fail relative to a finer one (its components).

*Own back-of-envelope (not in the paper), using Table 1 extreme-decile means ($A \approx -0.15, C=0.22$ low; $A \approx 0.15, C=0.00$ high; intercepts cancel):* the rational forecast difference high-minus-low is $0.765(0.30) + 0.855(-0.22) \approx +0.041$ of assets, whereas the price-implied difference is $0.911(0.30)+0.826(-0.22) \approx +0.092$ — prices over-expect the high-accrual firms' relative next-year ROA by roughly 5 points of assets.

---

## H2(ii): Trading Strategy (Table 6, Figure 2, Table 7)

Equal-weighted annual accrual deciles; means and $t$-stats from the 30 annual observations.

| | Size-adj. $t+1$ | $t+2$ | $t+3$ | Jensen $\alpha$ $t+1$ | $t+2$ | $t+3$ |
|---|---|---|---|---|---|---|
| Lowest decile | 4.9% (2.65) | 1.6% (1.17) | 0.7% (0.55) | 3.9% (2.01) | 0.7% (0.40) | 0.1% (0.08) |
| Highest decile | −5.5% (−3.98) | −3.2% (−2.25) | −2.2% (−1.61) | −6.4% (−4.68) | −4.0% (−2.87) | −3.6% (−2.47) |
| Hedge | **10.4% (4.71)** | 4.8% (3.15) | 2.9% (1.64) | **10.4% (4.42)** | 4.8% (2.41) | 3.8% (1.62) |

- Years 4–10: insignificant, consistent with Figure 1.
- The short leg carries more than half the effect and is the only leg still significant in years 2–3 under Jensen alphas.
- **Figure 2:** year-1 size-adjusted hedge positive in 28 of 30 years; exceptions 1966 (−19.5%) and 1981 (−2.2%).
- Sorting instead on cash flows, accruals/cash flows or accruals/earnings gives highly correlated portfolios and similar returns (ratio sorts break with negative denominators). Using ex-post sample-wide decile cutoffs gives almost identical results.
- **Fama–MacBeth (Table 7):** accruals negatively predict returns, strongest in $t+1$. Splitting components (year $t+1$): ΔCA −0.35 ($t$=−4.81), ΔCL −0.25 ($t$=−3.44), depreciation −0.14 ($t$=−0.57). ΔCL matters jointly even though it barely varies across deciles, and neither CA nor CL alone reaches this significance univariately. With controls for log size, log B/M, 60-month beta and E/P (Fama–French 1992 set), the accrual coefficient is essentially unchanged; B/M (0.03, $t$=2.31) and E/P (0.16, $t$=2.04) are also significant.

---

## H2(iii): Announcement Clustering (Table 8, Figure 3)

Sample: 16,795 firm-years, 1973–1991, with all four Compustat quarterly announcement dates. Announcement windows: four 3-day windows $[-2,0]$ around each quarterly date in year $t+1$ (12 trading days) vs ~242 non-announcement days.

- Hedge: **4.5% in announcement windows vs 6.0% outside** — over 40% of the year-1 return in under 5% of trading days (Bernard–Thomas found ~40% for PEAD). Announcement-window hedge return positive in all 19 years.
- Strong asymmetry: low-accrual (good-news) decile earns 4.5% in windows vs 0.9% outside (>80% clustered); high-accrual (bad-news) decile earns 0.0% in windows vs −5.1% outside.
- Sloan attributes the asymmetry to preemption of bad news (Chambers–Penman 1984; Skinner 1994): 34.5% of high-accrual firm-years report at least one quarter more than two days late vs 28.5% for the low-accrual decile.

---

## Conclusions as Stated by the Author

Prices do not fully reflect accrual/cash-flow information, but Sloan explicitly does not claim irrationality or free money: real-time information and processing costs are non-trivial, price pressure limits capacity (a CRSP print is not an executable quantity), and the returns might be "a normal return to an active investment strategy based on financial statement analysis." He flags earnings management (Dechow, Sloan and Sweeney 1995: SEC-enforcement manipulations are accruals that reverse the next year; Rangan 1995 on equity offerings) as a candidate source of the low accrual persistence.

---

## Critical Assessment

**Convincing**
- Persistence result is overwhelming and industry-robust (86–99% of industries), and Figure 1 ties the 1–3 year return horizon to the 1–3 year earnings-reversal horizon — a mechanism, not just a sort.
- Mishkin framework disciplines the magnitude and yields the clean contrast "efficient w.r.t. total earnings, inefficient w.r.t. components."
- Hedge is near beta- and size-neutral by construction of the U-shapes; 28/30 positive years and announcement clustering argue against a simple risk premium.

**Fragile or limited**
- Balance-sheet accruals are contaminated by M&A, divestitures and discontinued operations (Hribar–Collins 2002 later showed material measurement error vs cash-flow-statement accruals).
- Equal-weighted deciles in which the extremes are the smallest firms; NYSE/AMEX only. Value-weighted, cost-adjusted magnitudes are not reported, and Sloan himself flags capacity.
- Risk controls are CAPM and size adjustments plus FM characteristics; no investment/profitability factors (later q-theory and investment-based explanations — accruals as a component of asset growth — reopen the risk-vs-mispricing debate).
- The pricing-weight estimates are specification-sensitive (levels vs ranks flip whether prices over- or merely under-discount accruals).
- The bad-news leg is not concentrated at announcements, so its correction mechanism is less cleanly identified than the good-news leg's.
- Sample ends 1991; post-publication decay is out of scope.

**Practical relevance for a quant PM**
- Replication spec: BS accruals / average TA, 4-month lag, annual deciles, 12-month hold; year-1 hedge of ~10% (EW, gross, 1962–91) is the benchmark, with the short leg doing most of the work.
- The signal's half-life (~1 year, gone by 3) sets turnover; the effect is incremental to size, B/M, beta and E/P as of 1992 controls but should be re-tested against investment/asset growth and profitability factors.
- Announcement-window concentration on the long side suggests timing and event-driven overlays; the short side's non-announcement drift and higher late-filing rate suggest pairing with reporting-delay signals.
- The Mishkin setup is a reusable template for any "component persistence ≠ pricing weight" signal: estimate forecasting weights, embed in a return equation, test cross-equation constraints, and trade the component if rejected in the fixation direction.
