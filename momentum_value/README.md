> **Warning (2026-10-08):** absolute CAGR/Sharpe/drawdown figures in this document come from the Elendel engine's original booking (same-day weight × close-to-close return), which overstates results by ~17-26 CAGR points (see `csm_value/AUDIT.md`). Relative comparisons between variants may or may not survive; they have not been re-run.

# Value × momentum on the real live engines

Test of the lead idea in `../factor_research/MOMENTUM_LITERATURE_PLAYBOOK.md`: replace each engine's monthly score by
`z(base) + w · z(E/P)` (E/P = TTM net profit / (price × shares), point-in-time from quarterly results' `filed_date`, expires after 140 days,
missing = neutral). `Old_live_strategies` is imported unmodified; stops, regimes, vol target and 0.3% cost are the live ones.

```
python3 run_value_engines.py elendel quad zenith    # ~3 min -> .cache/value_*.pkl
python3 report_value_engines.py                     # -> value_engines_report.txt
```

Result (2019-06 → 2025-06, the only window with fundamentals): Zenith +9.5 pt CAGR / Sharpe +0.46; Quad +4 to +7 pt / +0.23 to +0.40; Elendel ≈ 0.
Fundamentals end with 2024Q4 results, so the variants equal the baseline after mid-2025. Six years, one cyclical-value regime, survivorship
in the cheap end — read the playbook's caveats before building.
