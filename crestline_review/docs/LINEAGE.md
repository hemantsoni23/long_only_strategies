# Crestline lineage: what each version added and what the consolidated `crestline_v2_6.py` removed

`crestline_v2_6.py` is the only strategy file to use. It is bit-identical to the frozen reference `research_archive/crestline_v2_6_precleanup.py` for every configuration tested (`python3 test_crestline.py --parity`),
except that the dead hard stop is gone (it only changed an exit-reason label in honest mode). The colleague's original is untouched in `../Crestine/crestline_v2_2.py`.

## Versions
| version | change | evidence |
|---|---|---|
| v2.2 (colleague) | Zenith composite, 15 names, 60-bar rebalance, stop stack, idle cash 0%, 2015 start | docs/REVIEW.md |
| v2.3 | split back-adjustment (a held position was booked unadjusted splits as -50..-90% losses), as-traded price floor, 2006 start, anchor reporting | docs/REVIEW.md s.3, s.10 |
| v2.4 | TOP_N 15 -> 25 (only change that passed the pre-registered ablation; +0.18 Sharpe, 6/6 anchors) | docs/ABLATION_REPORT.md |
| v2.5 | native gold sleeve (GOLDBEES, 25% cap, untimed, previous-close fills) and idle cash at 0% | docs/GOLD2_REPORT.md |
| v2.6 | EXIT_MODE zenith / honest / resting; unbooked exit P&L reported on every run | docs/V26_REPORT.md |
| v2.6 (cleaned) | consolidation (same file name `crestline_v2_6.py`, same results): everything tested and rejected, or dead, removed | this file |

## Removed from the strategy (all restorable from `research_archive/crestline_v2_6_precleanup.py` + the `make_*.py` generators)
| removed | verdict that justified removing it | where |
|---|---|---|
| 20% hard stop from entry | dead code: the 15% peak stop is always higher (peak >= entry open); removing it left every result identical | ABLATION_REPORT s.1 |
| ATR trailing stop (dynamic multiplier), volatility classes | off in v2.2; no evidence for it | v2.2 default off |
| relative-strength stop, trend-break exit | off in v2.2; trend-break instead of trailing stops: Sharpe -0.03, MaxDD -13 pts | REVIEW s.5 (S4) |
| slot refill (+ REFILL_FREQ, refill-only rows) | risk dial, not alpha: +2.8..+3.6 CAGR for -8.5 MaxDD at flat Sharpe, twice | REVIEW s.5 (R1/R2), EXITS_REPORT |
| rank-monitor rows, signal-aware stop, re-entry, profit-widened stop | none passed; moves along the return/drawdown frontier; re-entry loses | EXITS_REPORT |
| volatility-based sizing (inverse ATR, equal risk per stop) | near-miss only (+0.05..+0.07 Sharpe, below the +0.08 bar); equal-risk sizing null | STRUCT_REPORT s.T2 |
| capacity-aware candidate walk | raises exposure but deepens MaxDD 9-16 pts; Sharpe falls at every book size | STRUCT_REPORT s.T4 |
| RS-based stop suppression | worse (-0.05 / -0.03 Sharpe) | STRUCT_REPORT s.T3 |
| gold/silver in the stock ranking (ETF_LIST, drift placebo, eligibility rules) | 14-18 ETF trades in 20 years, Sharpe +-0.007 | GOLD_REPORT s.Part B |
| residual-momentum tilt, Low-MAX filter, single-leg score weights | failed the gates (+0.05 / +0.03 / -0.10..-0.14) | REVIEW s.5 (G1-G4) |
| BEAR_NO_ENTRY, USE_OVERLAY, USE_PEAK_STOP, USE_VOL_SCALED_STOP toggles | no entries in bear: -0.01; overlay off costs ~11 MaxDD pts. Disable a tier with BEAR_SCALE / PANIC_SCALE = 1.0 and a stop with PEAK_STOP_PCT = 1.0 or VOLSTOP_MIN/MAX_PCT = 1.0 | ABLATION_REPORT |
| gold timing (SMA200 trend, persistence, bear/panic tilt) and the silver split | all worse than an untimed capped holding | GOLD2_REPORT s.3-4 |
| GOLD_FILL = "open" | the vendor's ETF opening prints are noise (GOLDBEES overnight +109%/yr, intraday -87%/yr); open fills showed a fake +0.4..+0.6 CAGR | GOLD2_REPORT s.5 |
| CA_ADJUST = False (masking) | books splits as real losses | REVIEW s.3 |
| debug switches GOLD_FLAT / GOLD_NOISE | invariance tests (frozen / random gold == no-gold book) passed once on v2.5; archived | GOLD2_REPORT s.5 |
| REQUIRE_TRADED_ON_SIGNAL_BAR, FFILL_LIMIT_DAYS, has_hl / has_open fallbacks | constant True / unused / data always has OHLCV | - |

## Kept on purpose
`REENTRY_COOLDOWN_BARS = 30` (was REFILL_COOLDOWN_DAYS: it also blocks buying back a just-sold name at a rebalance, even with refill off), `GOLD_TARGET_RET` (return-scenario testing), `CASH_RATE_ANNUAL`, `INITIAL_CAPITAL` (capacity), all three EXIT_MODEs.
