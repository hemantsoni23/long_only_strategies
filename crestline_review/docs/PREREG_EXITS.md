# Next-round exit / re-entry tests - pre-registration (written 2026-10-12, BEFORE any variant was run)

Motivation (DIAG_REPORT.md): median hold 35 trading days vs signal horizon 120-180; 46% of big-winner gain captured; 49% of stop exits were still ranked top-25 and rebounded ~+3.5% vs the pool; but no-stop holds draw down 46-72% and wider stops alone buy return with drawdown at flat Sharpe.
Question: can an exit that DISCRIMINATES (uses the signal) raise risk-adjusted return, rather than just move the risk dial?

Base B = `crestline_v2_4.py` defaults (TOP_N 25, 2006-25, cash 6.5%, CA_ADJUST, INITIAL_CAPITAL 1 lakh). Tests run in `crestline_exits_lab.py` (parity with v2.4 exact; monitor grid alone also exact: `test_exits_lab.py`, 8/8 pass).
Each variant: 6 schedule anchors {0,10,..,50}; statistics are anchor means; gating metric Sharpe vs 6.5% (Sh65). P_A = 2006-14, P_B = 2015-25.
Rank information for exits comes from a monitor grid every 5 bars (ranks of the strategy's own score on its own pool); it never trades new names by itself and does not touch the benchmark/regime build.

## Variants (fixed list; no additions after seeing results)
| family | id | definition |
|---|---|---|
| SA signal-aware stop | SA1 | peak and vol trailing stops are suppressed while the name's latest rank <= 25; catastrophic trailing stop 25% from peak close and the 20% hard stop stay active |
| | SA2 | rank <= 50, catastrophic 25% |
| | SA3 | rank <= 25, catastrophic 35% |
| | SA4 | rank <= 50, catastrophic 35% |
| RE re-entry | RE1 | a name exited by a STOP is re-bought into a free slot if its latest rank <= 25, >= 5 bars and <= 60 bars after the exit |
| | RE2 | same, cooldown 10 bars |
| | RE3 | rank <= 50, cooldown 10 bars |
| PW profit-widened stop | PW1 | once peak close / entry - 1 >= 15%, peak and vol stop widths x1.5 |
| | PW2 | gain 15%, x2.0 |
| | PW3 | gain 30%, x1.5 |
| | PW4 | gain 30%, x2.0 |
| PN | PN1 | PANIC_PCTL = 0.90 (near-miss from the ablation study: Sh65 +0.04, MaxDD +3.5 pts) |

## Adoption rule for one variant vs B (all must hold)
* N1: mean dSh65 >= +0.08 (12 variants compared; expect ~1 spurious pass)
* N2: dSh65 > 0 in BOTH P_A and P_B
* N3: dSh65 > 0 in >= 5 of 6 anchors
* N4: mean MaxDD no more than 3 pts worse than B
* N5 (mechanism must show up where intended, so a win cannot come from an unrelated side effect): SA and PW: mean holding days up >= 10% vs B AND winner-capture ratio (mean realised net return / mean MFE over trades with MFE >= 30%) up >= 3 points; RE: re-entries (a trade entered <= 90 calendar days after the same ticker's stop exit in the same anchor) >= 5% of all trades.
* N6 (family consistency; SA, RE, PW only): at least 2 variants of the family pass N1-N4, otherwise the passing variant is labelled "isolated" and NOT adopted.
Several passing variants of one family: take the one closest to B (smallest move: highest rank threshold / smallest widening / largest cooldown).
RISK-DIAL label: CAGR up >= 1.5 pts but dSh65 < +0.08 (not adopted).

## Stack rule
Adopted variants (one per family, PN1 if it passes N1-N4) are ordered by dSh65 and added one at a time; an addition is kept only if the new stack passes N1-N4 against the previous stack (N5 for the added mechanism). Max 3 additions.
Then ONE fixed combination test: final stack + slot refill (USE_SLOT_REFILL, every 20 bars, cooldown 30 = the file's own setting) judged against the stack with N1-N4 (refill alone was +0.04 / MaxDD -9 earlier; the idea is that signal-aware exits plus refill might use the idle ~49% of capital).
Final stack robustness: cost x2 (0.6%/side), cash 0%, 2015-25 window alone, 6-anchor staggered blend, mechanism table (hold lengths, winner capture, SA_CATA/re-entry counts, exit reasons).
Nothing else is tuned. Any post-look change is logged below.

## Caveats stated in advance
In-sample 2006-25, no lockbox; capacity-free at 1 lakh; the signal-aware exits use the same ranks that selected the names, so they inherit the three weak-payoff regimes (2009-11, 2015-17, 2024-25) - per-block behaviour of any adopted stack is reported; pooled mechanism statistics are descriptive.

## Post-look change log
* Outcome of the single-variant round: no variant passed N1-N6, so the stack is empty. The pre-registered combination test therefore reduces to B + slot refill (RF = USE_SLOT_REFILL, every 20 bars, cooldown 30), judged against B with N1-N4. Run as written.
* Extra descriptive diagnostic (no decision attached): left-tail of post-exit returns by rank group at exit, to explain why the rank-aware exits did not help.
