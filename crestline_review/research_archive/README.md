# research_archive
Everything produced while researching Crestline (2026-10): generators (`make_*.py`) that built each intermediate version, the intermediate versions themselves (`crestline_lab*.py`, `crestline_v2_3..6.py`, exits/struct/gold labs),
experiment and report scripts, and the result tables (`results_*.csv`, `*_out.txt`). Nothing here is needed to run `../crestline_v2_6.py`.
`crestline_v2_6_precleanup.py` is the frozen ORIGINAL v2.6 (before the logic cleanup) that `../test_crestline.py --parity` compares against - keep it until the parity test is retired.
To re-run an old experiment, run it from THIS folder (the scripts reference each other by relative path; `anchor_report.py` is a copy kept so they import). Run caches (`runs*`) and diagnostic dumps were deleted and are regenerated on demand.
The research record (reports, pre-registrations) is in `../docs/`.
