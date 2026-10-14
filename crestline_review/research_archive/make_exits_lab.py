"""Builds crestline_exits_lab.py from crestline_v2_4.py: next-round exit/re-entry mechanisms. All switches default OFF == v2.4 exactly."""
import os
here = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(here, "crestline_v2_4.py")).read()
def sub(old, new, count=1):
    global s
    assert s.count(old) == count, (s.count(old), old[:80]); s = s.replace(old, new)

sub('''BEAR_NO_ENTRY        = False            # True: no NEW entries while bench < SMA200 (instead of scaling by BEAR_SCALE)
''', '''BEAR_NO_ENTRY        = False            # True: no NEW entries while bench < SMA200 (instead of scaling by BEAR_SCALE)
# ── NEXT-ROUND exit / re-entry switches (all OFF = v2.4) ──────────────────────────────────────────────────────
MON_FREQ_DAYS        = 0                # >0: rank-monitor rows every N bars (ranks for exit/re-entry decisions only; no rank exits, no new names)
SA_RANK              = 0                # >0: SIGNAL-AWARE STOP - peak/vol trailing stops are suppressed while the latest rank <= SA_RANK
SA_CATA_PCT          = 0.25             # ... a catastrophic trailing stop (peak close * (1-SA_CATA_PCT)) stays active meanwhile; hard stop stays too
RE_RANK              = 0                # >0: RE-ENTRY of a name exited by a STOP when its latest rank <= RE_RANK (on monitor rows), into a free slot
RE_COOLDOWN          = 5                # ... not before this many bars after the exit
RE_WINDOW            = 60               # ... and not later than this many bars after the exit
PW_GAIN              = 0.0              # >0: PROFIT-WIDENED STOP - once peak close / entry - 1 >= PW_GAIN the peak and vol stop widths are multiplied by PW_MULT
PW_MULT              = 1.0
''')
sub('''me_pos = np.union1d(rebal_pos, refill_pos).astype(int)
me_pos = me_pos[(me_pos >= 1) & (me_pos + 1 < n_bars)]
is_rebal = np.isin(me_pos, rebal_pos)            # True: full rebalance row; False: refill-only row
''', '''mon_pos = np.arange(sched_start_pos, n_bars, MON_FREQ_DAYS) if MON_FREQ_DAYS > 0 else np.array([], dtype=int)
me_pos = np.union1d(np.union1d(rebal_pos, refill_pos), mon_pos).astype(int)
me_pos = me_pos[(me_pos >= 1) & (me_pos + 1 < n_bars)]
is_rebal = np.isin(me_pos, rebal_pos)            # True: full rebalance row; False: refill-only row
is_mon_only = ~np.isin(me_pos, np.union1d(rebal_pos, refill_pos))   # monitor rows: rank information only
''')
sub('''for j in range(n_m):
    a_ = me_pos[j] + 1
    b_ = me_pos[j + 1] if j + 1 < n_m else n_bars - 1
''', '''_base_rows = np.where(~is_mon_only)[0]           # benchmark/regime membership is refreshed on the ORIGINAL rows only (monitor rows must not change it)
for _ii, j in enumerate(_base_rows):
    a_ = me_pos[j] + 1
    b_ = me_pos[_base_rows[_ii + 1]] if _ii + 1 < len(_base_rows) else n_bars - 1
''')
sub('''    last_exit_bar = np.full(n_stk, -10**9, dtype=np.int64)
''', '''    last_exit_bar = np.full(n_stk, -10**9, dtype=np.int64)
    last_exit_was_stop = np.zeros(n_stk, dtype=bool)
    cur_rank = np.full(n_stk, np.nan)
''')
sub('''        last_exit_bar[idxs] = t
''', '''        last_exit_bar[idxs] = t
        last_exit_was_stop[idxs] = np.array([reasons[i] != "REBAL_EXIT" for i in idxs])
''')
sub('''            k = rebal_map[t]
            rk = ranks[k]
            ok_rk = ~np.isnan(rk)
            if ok_rk.any():
                if is_rebal[k]:''', '''            k = rebal_map[t]
            rk = ranks[k]
            cur_rank = rk
            ok_rk = ~np.isnan(rk)
            if ok_rk.any() and not (is_mon_only[k] and RE_RANK <= 0):
                if is_rebal[k]:''')
sub('''                cand = (~held) & ok_rk & (rk <= N) & ~np.isnan(o) & (o > 0) & ((t - last_exit_bar) >= REFILL_COOLDOWN_DAYS)
''', '''                if is_mon_only[k]:
                    cand = ((~held) & ok_rk & (rk <= RE_RANK) & last_exit_was_stop & ~np.isnan(o) & (o > 0)
                            & ((t - last_exit_bar) >= RE_COOLDOWN) & ((t - last_exit_bar) <= RE_WINDOW))
                else:
                    cand = (~held) & ok_rk & (rk <= N) & ~np.isnan(o) & (o > 0) & ((t - last_exit_bar) >= REFILL_COOLDOWN_DAYS)
''')
sub('''            if USE_PEAK_STOP:
                lvl = peak * (1 - PEAK_STOP_PCT)
                flag(held & (c < lvl), "PEAK_STOP", lvl, PEAK_STOP_PCT * 100)

            if USE_VOL_SCALED_STOP:
                lvl = peak * (1 - vs_width)
                flag(held & (c < lvl), "VOLSTOP", lvl, vs_width * 100)
''', '''            sa_on = (held & (cur_rank <= SA_RANK)) if SA_RANK > 0 else np.zeros(n_stk, dtype=bool)
            pw = np.where(held & (entry_px > 0) & (peak / np.where(entry_px > 0, entry_px, 1.0) - 1.0 >= PW_GAIN), PW_MULT, 1.0) if PW_GAIN > 0 else 1.0

            if USE_PEAK_STOP:
                lvl = peak * (1 - PEAK_STOP_PCT * pw)
                flag(held & ~sa_on & (c < lvl), "PEAK_STOP", lvl, PEAK_STOP_PCT * 100)

            if USE_VOL_SCALED_STOP:
                lvl = peak * (1 - vs_width * pw)
                flag(held & ~sa_on & (c < lvl), "VOLSTOP", lvl, vs_width * 100)

            if SA_RANK > 0:
                lvl = peak * (1 - SA_CATA_PCT)
                flag(sa_on & (c < lvl), "SA_CATA", lvl, SA_CATA_PCT * 100)
''')
s = s.replace('STRATEGY_NAME        = "CRESTLINE_V2_4"', 'STRATEGY_NAME        = "CRESTLINE_EXITS_LAB"').replace('"crestline_v2_4_output"', '"crestline_exits_lab_output"')
open(os.path.join(here, "crestline_exits_lab.py"), "w").write(s); print("ok")
