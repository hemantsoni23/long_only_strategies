# Stage 1 — Data integrity & universe

**Verdict: FAIL / UNRESOLVED**

| Universe card | Setting |
| --- | --- |
| Source | 5,205 raw OHLCV CSVs; 2000-01-03 to 2026-10-30 |
| Eligibility | ₹10 price floor; liquidity top 1,000; 252 prior observed bars; circuit, SMA-200 and prior-month return filters |
| Portfolio / costs | 30 names; 2-month rebalance; 0.3% per weight turnover; cash rate 0% |
| Windows | Early 2001–2012; late 2013–2026-10-30; full 2002–2025-12-31 |
| Accounting convention | Exit-day gains/losses omitted at user request |
| Stage 1 status | Data adjustment unresolved; survivorship coverage flagged |

| Check | Measured | Playbook bar | Result |
| --- | --- | --- | --- |
| CSV files | 5,205 | — | Observed |
| Data period | 2000-01-03 → 2026-10-30 | — | Observed |
| Early warmup | 364 calendar days | 450 calendar days requested | INCOMPLETE |
| Symbols last seen >183 days before panel end | 57 / 5205 (1.10%) | Flag proxy <2% | FLAG; delistings unverified |
| Extreme sorted adjacent valid-close changes ≤−40% or ≥+300% | 946 | No unadjusted jumps | FAIL / needs action review |
| Duplicate dates among positive-close rows | 54,930 | Loader keeps last exact timestamp | Check data |
| Nonpositive / non-finite close or missing date | 1,008 | 0 | FAIL |
| Out-of-order valid rows | 805 | Sorted panel | Sorted by loader |
| Listing age | Early 0/33,837; late 0/82,061 below 252 | ≥252 prior observed bars | PASS observed-count test |
| Liquidity rolling window | 63 days; min_periods=21 | min_periods required | PASS |
| Early breadth: months <8 | 41 / 144 (28.47%) | Exclude each month | FAIL breadth |
| Late breadth: months <8 | 0 / 166 (0.00%) | Exclude each month | PASS |
| Source CSVs added/removed/metadata-changed | 0 / 0 / 0 | 0 / 0 / 0 | PASS metadata check |

| Window | Months | Mean names | Median names | Minimum names | Months <8 |
| --- | --- | --- | --- | --- | --- |
| early | 144 | 234.98 | 214.50 | 0 | 41 |
| late | 166 | 494.34 | 498.00 | 36 | 0 |

### Synthetic behavior checks

| Check | Measured | Expected / rule | Result |
| --- | --- | --- | --- |
| Stop uses prior peak | Same-day trigger False; next-day trigger True | False / True | PASS |
| Missing current-day open | Forward-filled to 100.0 | Do not assume stale quote executable | FLAG |
| Rebalance guard | 30 ranked; 0 positive; 30 prior weights retained | Raw-pool shortage guard; thin positive selection allowed | FLAG |
| Force vs existing stop | Existing stop 85; reported fill 39.88 | Standing stop fill model 84.745 if crossed without a gap | FLAG |

| Interpretation | Limitation |
| --- | --- |
| Survivorship | Last observation is a proxy; it does not prove delisting or coverage. |
| Corporate actions | Adjacent observations may cross gaps; large changes are flags, not confirmed splits or errors. |
| Listing history | Counts non-null prices in the loaded buffer; full exchange listing history is not independently verified. |
| Source check | File sizes and modification times compared before/after; content hashes are in `_evidence/data_manifest.csv`. |
| Stop example | Actual intraday gaps may change fills; the synthetic case compares the two programmed models. |
