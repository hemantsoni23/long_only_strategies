# Audit of updated `fundamentals` folder — 12 November 2026

The updated folder is useful but is not a complete or verified replacement for `fundamentals_data`. This audit reads both folders without changing either. The current CSM Value loader defaults to `fundamentals` unless `CSM_FUNDAMENTALS_DIR` overrides it.

## Main findings

### Banking data improved

Previously missing 2025–2026 filings have been added for HDFCBANK, SBIN and ICICIBANK. For example, the HDFCBANK March 2025 standalone block points to [the NSE banking XBRL](https://nsearchives.nseindia.com/corporate/xbrl/INTEGRATED_FILING_BANKING_1421434_21042025050837_WEB.xml), and its `other_facts` contains `ProfitLossForThePeriod = 176161400000`. Although its canonical `net_profit` is null, the current loader falls back to that banking tag and constructs TTM results. This check does not establish that every bank filing is correct or complete.

### 2026 recent main-board results regressed

The old folder contains 1,135 standalone/consolidated financial blocks with period end 30 September 2026; the updated folder has eight. Matching by symbol, actual period end and basis, 1,127 blocks for 630 symbols present in the old folder are absent from the updated folder. All 1,127 stored filing timestamps are on or before 4 November 2026. These are basis-level blocks, not 1,127 unique companies. The existence of a block in the old dataset does not independently validate its numerical values.

For example, ANGELONE's September quarter was published on 15 October 2026. It is present in the old folder and missing in the updated folder; [NSE's original consolidated filing](https://nsearchives.nseindia.com/corporate/ixbrl/INTEGRATED_FILING_NBFC_INDAS_201500_15102026175725_iXBRL_WEB.html) confirms the quarter and publication context. On 30 October, the loader consequently sees ANGELONE's June period in the updated dataset versus its September period in the old dataset.

The difference can change a signal. At the same as-of date, 360ONE's loader growth factor is approximately +14.91% using the June result in the updated folder, but -4.99% using the September result in the old folder. The default strategy requires this factor to be positive. Passing that one criterion does not mean a position was actually entered; prices and the other filters also matter.

### SME 2025–2026 financial statements are missing

The updated `fundamentals/sme` has 294 files, but no 2025–2026 quarterly/half-year or annual financial blocks. The older `fundamentals_data/sme` has 1,705 standalone/consolidated quarterly or half-year blocks with period ends in 2025–2026. For example, ACCORD's 2025–2026 half-year data exists only in the old folder; ADDICTIVE's March 2026 data also exists only in the old folder. The old ACCORD filing was independently found to contain a 100-fold source error, so copying it without verification would not repair its quality.

The strategy's loader accepts single-quarter statements, requires four consecutive quarters, and does not yet support six-month reporting. Looking across all dates, it constructs results for three SME-folder symbols with the updated folder versus 14 with the old folder. None of the three updated-folder symbols has a usable 2025 or 2026 reporting period. The strategy uses a 140-day freshness setting, so accepting half-year statements without a frequency-aware freshness policy could also create artificial gaps.

### Known numerical and revision problems remain

NAVNETEDUL March 2026 consolidated revenue in the updated JSON remains ₹4.30 crore and net profit ₹0.39 crore. The contemporaneous [company investor presentation](https://nsearchives.nseindia.com/corporate/Navneet26_21052026171333_InvestorPresentationQ4FY26Final.pdf), pages 8 and 11, reports ₹430 crore revenue and ₹39 crore net profit. Both the original XBRL and the local JSON contain the 100-times-smaller values. The updated data has not corrected this previously verified source-level problem.

The PFC March 2026 consolidated JSON still retains the [21 August revision](https://nsearchives.nseindia.com/corporate/xbrl/INTEGRATED_FILING_NBFC_INDAS_1716806_21082026041106_WEB.xml) rather than also preserving the [13 May original](https://nsearchives.nseindia.com/corporate/xbrl/INTEGRATED_FILING_NBFC_INDAS_1666633_13052026071813_WEB.xml). The loader rejects the revision because it was filed 143 days after quarter-end, exceeding the 120-day limit. It can fall back to PFC's standalone results; the example demonstrates a missing consolidated history, not necessarily loss of the whole company. Across the updated main-board 2025–2026 period-end blocks, 434 retained revisions have filing lags greater than 120 days. This is a count of blocks, not necessarily affected positions.

Some JSON quarter labels also do not match their actual period-end metadata. ASTRON is one example: FY2025-26 Q1 standalone is labelled Q1 but has an end date of 30 September 2025 and a six-month start/end range; its Q3 block ends 31 March 2026. The current CSM Value loader uses the actual period metadata and excludes six-month periods; other code using labels directly may interpret them incorrectly. Some fiscal-year metadata can be nonstandard, so flagged labels require case-by-case validation.

## Method and scope

The audit compared both corpora by file, period end, basis, dates, source identifiers, and selected financial fields. Files: 2,022 main-board and 294 SME JSONs per folder. Results from `audit_updated_folder.py` and `audit_period_identity.py` are saved in `updated_folder_audit.json` and `updated_period_identity.json`. The recent-period gap was checked by actual period end and basis, rather than only by JSON labels. Annual/quarter internal reconciliations and source spot checks are diagnostics, not verification of every field. Different filings and revisions can also explain some reconciliation discrepancies.

The population of stocks with a fresh TTM result can remain high even when a newer filing is missing: the loader may still use a 140-day-old result. Thus overall counts alone cannot establish point-in-time completeness. No backtest was rerun and the contribution of these issues to 2025–2026 performance remains unmeasured. Do not overwrite either source folder or alter the user's buy/sell and exit-day rules while fixing these issues.
