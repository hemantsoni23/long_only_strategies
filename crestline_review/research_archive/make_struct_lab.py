"""Builds crestline_struct_lab.py from crestline_exits_lab.py: vol-based sizing, capacity-aware candidate walk, relative-strength stop suppression. Defaults OFF == v2.4."""
import os
here = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(here, "crestline_exits_lab.py")).read()
def sub(old, new, count=1):
    global s
    assert s.count(old) == count, (s.count(old), old[:80]); s = s.replace(old, new)
sub('''PW_MULT              = 1.0
''', '''PW_MULT              = 1.0
# ── STRUCTURAL-ROUND switches (all OFF = v2.4) ─────────────────────────────────────────────────────────────
SIZE_MODE            = 0                # 1: entry weight = (1/N) x clip(ref/ATR%, lo, hi); 2: same with the stop width (equal risk per stop)
VS_LO                = 0.5
VS_HI                = 1.5
CAPWALK_DEPTH        = 0                # >0: candidates may come from rank <= depth*N; names whose ADV cap < CAPWALK_MIN/N of equity are skipped
CAPWALK_MIN          = 0.5
RS_SUP               = 0.0              # >0: price trailing stops suppressed while the stock's relative strength (vs EW index) is within RS_SUP of its peak since entry
RS_CATA_PCT          = 0.25             # catastrophic trailing stop kept while suppressed
''')
sub('''    exit_rank = int(round(N * EXIT_RANK_MULT))
''', '''    exit_rank = int(round(N * (max(EXIT_RANK_MULT, CAPWALK_DEPTH) if CAPWALK_DEPTH > 0 else EXIT_RANK_MULT)))
''')
sub('''                    cand = (~held) & ok_rk & (rk <= N) & ~np.isnan(o) & (o > 0) & ((t - last_exit_bar) >= REFILL_COOLDOWN_DAYS)
                cand_ids = np.where(cand)[0]
''', '''                    cand = ((~held) & ok_rk & (rk <= (CAPWALK_DEPTH * N if CAPWALK_DEPTH > 0 else N)) & ~np.isnan(o) & (o > 0)
                            & ((t - last_exit_bar) >= REFILL_COOLDOWN_DAYS))
                cand_ids = np.where(cand)[0]
                if CAPWALK_DEPTH > 0 and len(cand_ids):
                    _adv = med[k][cand_ids]
                    cand_ids = cand_ids[np.where(np.isnan(_adv), True, ADV_CAP * _adv / max(eq_open, 1.0) >= CAPWALK_MIN / N)]
''')
sub('''                    w_int = allocate(np.ones(len(cids)), caps)
''', '''                    if SIZE_MODE > 0:
                        _pa = atr_pct_sig[k][ok_rk & (rk <= N)]; _pa = _pa[np.isfinite(_pa)]   # reference = the current top-N ranked names (the typical entrants)
                        _x = atr_pct_sig[k][cids]
                        if SIZE_MODE == 2:
                            _x = np.clip(VOLSTOP_K * _x, VOLSTOP_MIN_PCT, VOLSTOP_MAX_PCT); _pa = np.clip(VOLSTOP_K * _pa, VOLSTOP_MIN_PCT, VOLSTOP_MAX_PCT)
                        _ref = np.median(_pa); _mp = np.clip(_ref / np.where(_pa > 0, _pa, np.nan), VS_LO, VS_HI); _ref = _ref / np.nanmean(_mp)   # average multiplier over the top-N names -> 1 (keeps mean weight 1/N)
                        _m = np.clip(_ref / np.where(_x > 0, _x, np.nan), VS_LO, VS_HI); _m = np.where(np.isfinite(_m), _m, 1.0)
                        _advcap = np.where(np.isnan(adv), np.inf, ADV_CAP * adv / max(eq_open, 1.0))
                        w_int = np.minimum(np.minimum(_m / N, MAX_ENTRY_PCT), _advcap)
                    else:
                        w_int = allocate(np.ones(len(cids)), caps)
''')
sub('''            pw = np.where(''', '''            if RS_SUP > 0:
                _rs = c / bench_np[t]
                rs_peak[held] = np.maximum(rs_peak[held], _rs[held])
                with np.errstate(invalid="ignore", divide="ignore"):
                    rs_on = held & ((1.0 - _rs / np.where(rs_peak > 0, rs_peak, np.nan)) < RS_SUP)
            else:
                rs_on = np.zeros(n_stk, dtype=bool)
            sup = sa_on | rs_on
            pw = np.where(''')
sub('flag(held & ~sa_on & (c < lvl), "PEAK_STOP"', 'flag(held & ~sup & (c < lvl), "PEAK_STOP"')
sub('flag(held & ~sa_on & (c < lvl), "VOLSTOP"', 'flag(held & ~sup & (c < lvl), "VOLSTOP"')
sub('''                flag(sa_on & (c < lvl), "SA_CATA", lvl, SA_CATA_PCT * 100)
''', '''                flag(sa_on & (c < lvl), "SA_CATA", lvl, SA_CATA_PCT * 100)

            if RS_SUP > 0:
                lvl = peak * (1 - RS_CATA_PCT)
                flag(rs_on & ~sa_on & (c < lvl), "RS_CATA", lvl, RS_CATA_PCT * 100)
''')
s = s.replace('STRATEGY_NAME        = "CRESTLINE_EXITS_LAB"', 'STRATEGY_NAME        = "CRESTLINE_STRUCT_LAB"').replace('"crestline_exits_lab_output"', '"crestline_struct_lab_output"')
open(os.path.join(here, "crestline_struct_lab.py"), "w").write(s); print("ok")
