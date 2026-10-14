"""Builds crestline_v2_6.py from crestline_v2_5.py: EXIT_MODE switch = Zenith's exit convention available inside Crestline.
EXIT_MODE='honest' reproduces v2.5 bit-exactly. v2.5 is only read."""
import os
here = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(here, "crestline_v2_5.py")).read()
def sub(old, new, count=1):
    global s
    assert s.count(old) == count, (s.count(old), old[:90]); s = s.replace(old, new)

sub('''GOLD_NOISE           = 0                # debug: replace the ETF with iid zero-mean noise (this seed, ~15% vol)
''', '''GOLD_NOISE           = 0                # debug: replace the ETF with iid zero-mean noise (this seed, ~15% vol)
# ── v2.6 EXIT CONVENTION ──────────────────────────────────────────────────────────────────────────────────────
EXIT_MODE            = "zenith"         # "zenith": the live engines' convention (below) | "honest": close-based stop flagged at the close, filled at the NEXT OPEN, gap booked (= v2.5) | "resting": zenith trigger+fill, booked at the fill
ZEN_SLIP             = 0.003            # Zenith's stop slippage on the logged fill (stop level x (1 - ZEN_SLIP); the open when the day gaps through the stop)
''')
sub('''    gold_units = 0.0; gold_w = np.zeros(n_bars); gold_traded = 0.0
''', '''    gold_units = 0.0; gold_w = np.zeros(n_bars); gold_traded = 0.0
    hidden_pnl = 0.0                                 # P&L the exit convention does NOT book: sum(shares x (logged fill - booked price)) over exits (zenith mode: fill vs previous close)
''')
sub('''    def close_positions(mask, t, px_exit, c_prev, reasons, levels=None, pcts=None):''', '''    def close_positions(mask, t, px_exit, c_prev, reasons, levels=None, pcts=None, fills=None):''')
sub('''        nonlocal cash, traded
        idxs = np.where(mask)[0]
        if idxs.size == 0:
            return
        sh, px = shares[idxs], px_exit[idxs]
''', '''        nonlocal cash, traded, hidden_pnl
        idxs = np.where(mask)[0]
        if idxs.size == 0:
            return
        sh, px = shares[idxs], px_exit[idxs]
        if fills is not None:
            hidden_pnl += float((sh * (fills[idxs] - px)).sum())
''')
sub('''Exit_Date=dates_np[t], Exit_Price=px[j], Close_At_Exit=c_prev[i],''', '''Exit_Date=dates_np[t], Exit_Price=px[j], Fill_Logged=(fills[i] if fills is not None else px[j]), Close_At_Exit=c_prev[i],''')
sub('''            pending_level[:] = np.nan; pending_pct[:] = np.nan
            held = shares > 0

        tier_t = tier_arr[t] if USE_OVERLAY else 1.0
''', '''            pending_level[:] = np.nan; pending_pct[:] = np.nan
            held = shares > 0

        # (0z) Zenith-style stops: the stop in force (state through the PREVIOUS bar) is tested against TODAY'S LOW and the position is closed today at the stop level x (1 - ZEN_SLIP), or at the open when
        # the day gaps through it; locked (high == low) days defer the exit. 'zenith' books the sale at the PREVIOUS CLOSE (the live engines' weight-0-on-the-exit-day convention: the move from the previous
        # close to the fill is never charged); 'resting' books it at the fill. A position bought today is first tested tomorrow.
        if EXIT_MODE != "honest" and held.any():
            _lo = low_np[t].astype(float); _hi = high_np[t].astype(float)
            _L = np.full((3, n_stk), -np.inf)
            if USE_HARD_STOP: _L[0] = np.where(cost_basis > 0, cost_basis * (1 - HARD_STOP_PCT), -np.inf)
            if USE_PEAK_STOP: _L[1] = np.where(peak > 0, peak * (1 - PEAK_STOP_PCT), -np.inf)
            if USE_VOL_SCALED_STOP: _L[2] = np.where(peak > 0, peak * (1 - vs_width), -np.inf)
            _eff = _L.max(axis=0); _which = _L.argmax(axis=0)
            _ok = (held & (entry_bar < t) & np.isfinite(_lo) & (_lo > 0) & np.isfinite(_eff) & (_eff > 0) & (_lo <= _eff)
                   & ~(np.isfinite(_hi) & (_hi == _lo)))
            if _ok.any():
                _rs = np.array(["HARD_STOP", "PEAK_STOP", "VOLSTOP"], dtype=object)[_which]
                _fill = np.where(np.isfinite(o) & (o <= _eff), o, _eff * (1 - ZEN_SLIP))
                _book = c_prev if EXIT_MODE == "zenith" else _fill
                _pct = np.where(peak > 0, (peak - _eff) / np.where(peak > 0, peak, 1.0) * 100, np.nan)
                close_positions(_ok, t, np.where(_ok, _book, c_prev), c_prev, _rs, _eff, _pct, fills=_fill)
                held = shares > 0

        tier_t = tier_arr[t] if USE_OVERLAY else 1.0
''')
sub('''                        close_positions(drop, t, px_exit, c_prev, np.full(n_stk, "REBAL_EXIT", dtype=object))''', '''                        close_positions(drop, t, (c_prev if EXIT_MODE == "zenith" else px_exit), c_prev, np.full(n_stk, "REBAL_EXIT", dtype=object),
                                        fills=(px_exit if EXIT_MODE == "zenith" else None))''')
sub('''            pending_stop |= claimed
''', '''            if EXIT_MODE == "honest":
                pending_stop |= claimed
''')
sub('''    return dict(gold_w=pd.Series(gold_w, index=index).iloc[t_first:], gold_traded=gold_traded,''', '''    return dict(hidden_pnl=hidden_pnl, gold_w=pd.Series(gold_w, index=index).iloc[t_first:], gold_traded=gold_traded,''')
sub('''    ("Est. Cost Drag %/yr", f"{m['CostDrag']:.2f}"),
''', '''    ("Est. Cost Drag %/yr", f"{m['CostDrag']:.2f}"),
    ("EXIT_MODE",           f"{EXIT_MODE}"),
    ("Exit P&L NOT booked %/yr of avg equity", f"{res['hidden_pnl'] / res['eq'].mean() / ((res['eq'].index[-1] - res['eq'].index[0]).days / 365.25) * 100:.2f}"),
''')
sub('''    _json.dump(dict(m=m, exits=ec, n_trades=res["n_trades"],''', '''    _json.dump(dict(hidden_pct_yr=res["hidden_pnl"] / res["eq"].mean() / ((res["eq"].index[-1] - res["eq"].index[0]).days / 365.25) * 100, exit_mode=EXIT_MODE, m=m, exits=ec, n_trades=res["n_trades"],''')
s = s.replace('STRATEGY_NAME        = "CRESTLINE_V2_5"', 'STRATEGY_NAME        = "CRESTLINE_V2_6"').replace('"crestline_v2_5_output"', '"crestline_v2_6_output"')
hdr = '''"""
crestline_v2_6.py -- CRESTLINE v2.6 = v2.5 + Zenith's exit convention (EXIT_MODE)
=================================================================================
Everything of v2.5 (25 names, fixed baseline, gold sleeve, idle cash 0%) is unchanged. NEW: EXIT_MODE selects how exits are executed and booked.
  "zenith"  (default, as requested): the live engines' convention. Each day the stop in force (state through the previous bar) is tested against TODAY'S LOW; a hit closes the position TODAY at
            stop level x (1 - 0.3% slippage), or at the open when the day gaps through it; locked (high == low) days defer the exit. The sale is BOOKED AT THE PREVIOUS CLOSE: exit-day weight is 0,
            so the move from the previous close to the fill is never charged - same for rebalance exits. Entries are at the open (as before).
  "honest"  : close-based stop flagged at the close, filled at the NEXT OPEN, gap booked (this is exactly v2.5).
  "resting" : zenith trigger and fill, but booked at the fill (the gap is charged) - the bridge between the two.
Each run prints and stores 'Exit P&L NOT booked %/yr' (the return the zenith convention hides) - never quote a zenith-mode number without the honest one next to it.
EXIT_MODE="honest" reproduces v2.5 bit-for-bit (test_v2_6.py).
"""
'''
i = s.index("import os\nimport glob"); s = hdr + "\n" + s[i:]
open(os.path.join(here, "crestline_v2_6.py"), "w").write(s); print("ok")
