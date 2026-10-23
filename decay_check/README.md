# decay_check — is each live strategy's core logic still working?

Notion write-up: "Strategy Decay Check — All 8 Live Strategies (Oct 2026)". Rules fixed before results: `PREREG.md`.
Old_live_strategies/ is imported read-only (never edited).

Run order (from this folder; panels cache is `.cache/`, separate from factor_research/.cache):

```
python3 build_panels.py                 # raw Upstox CSVs -> .cache/*.parquet
for n in residual absolute batch elendel zenith quad; do python3 build_factors.py $n; done   # live classes -> monthly factor frames
python3 analyze_cs.py                   # IC/ICIR/NW-t/horizons/basket/legs/verdict tests for the 6 ranked books
python3 analyze_events.py hr; python3 analyze_events.py vcp   # entry-signal event study
python3 analyze_events_stats.py         # chunk tables + verdicts for HR / VCP
python3 analyze_returns.py              # secondary: faithful-booked returns by chunk (Elendel/Zenith/Quad)
python3 make_charts.py                  # charts/*.png
```

Outputs: `results/cs_chunks.csv, cs_verdicts.csv, cs_legs.csv, ev_chunks.csv, ev_verdicts.csv, ret_chunks.csv`.
To refresh for a later date: rebuild panels, change `ANCHOR` in `common.py` (last signal month), re-run.

Re-check (Addendum 2 in PREREG.md): `breakout_backtest.py <hr|vcp> <cash> [base|nopattern|noregime|notrend]` runs the live engines; `faithful_replay.py` re-books from the trade log;
`breakout_checks.py`, `analyze_b1.py` (P&L chunks), `analyze_c.py` (why momentum decayed), `build_r3b1000.py` + `analyze_d.py` (improvement candidates), `make_charts2.py`.

Quad re-check (Addendum 3): `quad_variants.py` (signal by band/lookback), `analyze_quad.py`, `quad_pnl.py` (live Quad engine + faithful re-booking by band).
Lessons file: `LESSONS_BREAKOUTS_FOR_MOMENTUM.md`.

New strategy (Addendum 4): `signals_lib.py` (all file signals), `signal_battery.py` (IC/ICIR/NW/horizon/accuracy/decay), `strategy_engine.py` (research engine), `aegis_validation.py`, `aegis_checks.py`; deliverable in `../csm_aegis/` (strategy, runner, parity test, report).
