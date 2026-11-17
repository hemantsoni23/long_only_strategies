# Archived CSM PEAD material

On 17 November 2026, `csm_pead/` was renamed to
`csm_earnings_surprise_reaction/` (CSM Earnings Surprise & Reaction).

- `output/` and `output_run.log` are older, unaudited results from the
  original implementation. They use different data and trading assumptions.
- `output_audited/` is the corrected pre-rename research run,
  with the default report covering 1 September 2020–31 December 2024.
- `diag_*.py`, `_generate_report_style.py` and `run_pead_backtest.py` are
  preserved for historical reference. They rely on old paths, imports, caches
  or assumptions and are not maintained as runnable entry points.
- `README_before_rename.md` records the description immediately before the
  rename.

The maintained implementation, documentation, tests and current results are
in `../../csm_earnings_surprise_reaction/`.
