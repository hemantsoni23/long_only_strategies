# SME fundamentals audit, 11 November 2026

This is a read-only audit of `fundamentals_data/sme` and the 15-position CSM Value output saved under `csm_value/output`. The stock list means files in this folder at the time of the audit, not a historical point-in-time record of exchange board membership.

## Coverage and strategy use

- There are 294 SME JSON files, of which 292 have matching daily OHLCV CSV names. PERFECT and VISDEM are the two without matching CSVs and without quarterly/half-year financial blocks in the inventory.
- The inventory contains 1,705 2025–26 financial blocks: 1,465 covering approximately six months and 240 covering approximately three months. These are **basis-level blocks**, not unique companies. All 292 symbols with financial blocks have at least one six-month block.
- The CSM Value loader discards six-month results and requires four consecutive single-quarter results for trailing earnings. Running that exact loader against the 294 folder names produces at least one result for only 14 symbols over the entire data history (including nine with a result period ending in 2026). This is not a claim that all 14 were eligible to trade: the rest of the strategy's price, growth, valuation and other rules still apply.
- The saved trade log contains zero closed trades in symbols currently in the SME folder. Thus none of its recorded closed-trade losses is an SME trade. Including SMEs could still alter competition for portfolio positions and overall performance; that counterfactual has not been measured.
- Once half-year support exists, the present 140-day freshness rule for quarterly reports needs a separately specified half-year policy: a half-year filing can expire before the next half-year result is published. Any new result must become available only after its actual publication date.

## Incorrect scale: ACCORD

Accord Synergy's September 2025 standalone six-month result in the local JSON records revenue of ₹1,914.28 crore, profit of ₹114.99 crore, and share capital of ₹347.20 crore. The [original company disclosure](https://nsearchives.nseindia.com/corporate/ACCORD_13112025113415_Financial_results300925.pdf), page 3, reports ₹19.1427912 crore, ₹1.1498892 crore, and ₹3.472 crore respectively. The erroneous larger rounded values are present in the [original XBRL](https://nsearchives.nseindia.com/corporate/xbrl/INTEGRATED_FILING_NONINDAS_1573184_13112025113447_WEB.xml), with unit INR. This is approximately a 100-fold source inconsistency, not simply the local parser changing a correct XBRL number.

The later [March 2026 filing](https://nsearchives.nseindia.com/corporate/xbrl/INTEGRATED_FILING_NONINDAS_1663341_04052026060030_WEB.xml) also supports this: it reports second-half revenue ₹17.6782 crore and full-year revenue ₹36.8209 crore, implying first-half revenue of approximately ₹19.1427 crore. It reports share capital of ₹3.472 crore. These later disclosures must not be treated as information available in 2025; the contemporaneous PDF is the appropriate source for a point-in-time correction.

## Revisions and completeness

- Among 2025–26 SME blocks, 312 retained entries identify themselves as revisions. Of those, 63 across 55 symbols have filing dates more than 120 days after period-end. This is a count of financial blocks, not necessarily lost companies or trades. The loader would reject the late block if it otherwise supported its period; currently it already rejects six-month blocks.
- For ADDICTIVE's March 2026 standalone result, the [original](https://nsearchives.nseindia.com/corporate/xbrl/INTEGRATED_FILING_NONINDAS_1677110_29052026114848_WEB.xml) was published 29 May 2026 and the [stored revision](https://nsearchives.nseindia.com/corporate/xbrl/INTEGRATED_FILING_NONINDAS_1722926_09092026040111_WEB.xml) is dated 9 September 2026. The JSON retains the revision rather than preserving the original as a separate version. Restore both with their own availability dates; do not use the later revision in earlier backtest periods.
- On 422 FY2025–26 issuer-and-basis cases where two adjacent six-month blocks and an annual result were all available, first-half plus second-half revenue reconciled within 1% of annual revenue for 97.6%, and net profit for 93.1%. This is an internal consistency check, not independent source validation. Filings may be revised on different dates, and discrepancies require investigation rather than automatic correction.
- The previous main-board backup comparison did not cover the SME folder. No matching original SME backups were found in the integrated-backup directory, so this audit cannot establish whether every pre-existing SME field was preserved during that merge.

## Reproduction

Run `python3 research/fundamentals_source_audit/audit_sme.py` after producing `filings_inventory.csv` with `audit_filing_data.py`. The SME script produces `sme_halfyear_reconciliation.csv`. No strategy, source JSON, position limit, execution rule, or exit-day weighting was changed.
