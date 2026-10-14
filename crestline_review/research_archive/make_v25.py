"""Builds crestline_v2_5.py from crestline_gold_lab.py: native gold sleeve inside the engine. GOLD_CAP=0 + CASH_RATE 6.5% == v2.4 bit-exactly."""
import os
here = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(here, "crestline_gold_lab.py")).read()
def sub(old, new, count=1):
    global s
    assert s.count(old) == count, (s.count(old), old[:80]); s = s.replace(old, new)
sub('''ETF_MIN_OBS          = 240              # eligible only after this many genuine observations in the last 252 bars (no stale/forward-filled windows)
''', '''ETF_MIN_OBS          = 240              # eligible only after this many genuine observations in the last 252 bars (no stale/forward-filled windows)
# ── v2.5 GOLD SLEEVE: idle capital is held in a gold ETF (untimed), up to GOLD_CAP of equity ──────────────────
GOLD_CAP             = 0.25             # max share of equity in the gold ETF (always <= idle cash). 0 = off. Pre-registered rule output; 0.15-0.20 is the more cautious end of the plateau
GOLD_SYM             = "GOLDBEES"
GOLD_COST            = 0.0015           # one-way cost on gold ETF trades
GOLD_BAND            = 0.02             # trade only when the target differs from the holding by > this share of equity
GOLD_FILL            = "close"          # ETF fills at the PREVIOUS close. The vendor's ETF opening prints are noisy and snap back (GOLDBEES overnight +109%/yr, intraday -87%/yr), so "open" fills flatter results; "open" is diagnostic only
GOLD_TARGET_RET      = None             # None = real ETF prices; a number re-centres the ETF's ARITHMETIC mean daily return so its usable-sample annual return equals it (scenario testing, e.g. 0.08)
GOLD_FLAT            = False            # debug: freeze the ETF price; with GOLD_COST=0 the result must equal the no-gold book
GOLD_NOISE           = 0                # debug: replace the ETF with iid zero-mean noise (this seed, ~15% vol)
''')
sub('CASH_RATE_ANNUAL     = 0.065          # idle cash swept to a liquid fund (live must actually do this)', 'CASH_RATE_ANNUAL     = 0.0            # v2.5: idle cash earns NOTHING in the backtest (conservative accounting); the gold sleeve is how idle capital works')
sub('''is_etf = np.array([c in etf_cols for c in prices.columns], dtype=bool)
''', '''is_etf = np.array([c in etf_cols for c in prices.columns], dtype=bool)
g_o = g_c = g_has = None
if GOLD_CAP > 0:
    _g = pd.read_csv(os.path.join(ETF_FOLDER, GOLD_SYM + ".csv")); _g["t"] = pd.to_datetime(_g.timestamp.str[:10]); _g = _g.set_index("t")[["open", "close"]]
    _g = _g[~_g.index.duplicated(keep="last")].sort_index().mask(lambda d: d <= 0)
    if GOLD_FLAT:
        _g["open"] = 100.0; _g["close"] = 100.0
    if GOLD_NOISE:
        _rng = np.random.default_rng(GOLD_NOISE); _n = _rng.normal(0.0, 0.15 / np.sqrt(252), len(_g)); _c = 100.0 * np.cumprod(1 + _n)
        _g["close"] = _c; _g["open"] = np.r_[100.0, _c[:-1]]
    if GOLD_TARGET_RET is not None:     # re-centre the ARITHMETIC mean daily return over the usable 2007-03..2025-12 days (same definition as the post-processing study)
        _gs = _g.close["2007-03-01":"2025-12-31"]; _r = _gs.pct_change(fill_method=None); _r[_gs.index.to_series().diff().dt.days > 5] = np.nan
        _rr = _g.close.pct_change(fill_method=None); _rr[_g.index.to_series().diff().dt.days > 5] = np.nan
        _rn = _rr - (np.nanmean(_r) - ((1 + GOLD_TARGET_RET) ** (1 / 252) - 1))
        _f = ((1 + _rn.fillna(0.0)) / (1 + _rr.fillna(0.0))).cumprod(); _g = _g.mul(_f, axis=0)
    g_o = _g.open.reindex(index).to_numpy(dtype=float); g_has = _g.close.reindex(index).notna().to_numpy(); g_c = _g.close.reindex(index).ffill().to_numpy(dtype=float)   # g_c forward-filled ONLY for marking; units are zero across gaps
''')
sub('''    cash, traded = INITIAL_CAPITAL, 0.0
''', '''    cash, traded = INITIAL_CAPITAL, 0.0
    gold_units = 0.0; gold_w = np.zeros(n_bars); gold_traded = 0.0
''')
sub('''        eq_open = cash + float((shares * c_prev)[held].sum())
''', '''        g_prev = (g_c[t - 1] if np.isfinite(g_c[t - 1]) else 0.0) if GOLD_CAP > 0 else 0.0
        eq_open = cash + float((shares * c_prev)[held].sum()) + gold_units * g_prev
''')
sub('''                    scale = min(1.0, max(cash, 0.0) / (tot * (1 + COST_ONE_WAY))) if tot > 0 else 0.0
''', '''                    if gold_units > 0 and tot * (1 + COST_ONE_WAY) > cash:       # fund stock entries by selling gold (at the previous close; entries are known from yesterday's signals)
                        _px = (g_o[t] if (GOLD_FILL == "open" and np.isfinite(g_o[t])) else g_prev)
                        _u = min(gold_units, (tot * (1 + COST_ONE_WAY) - cash) / (_px * (1 - GOLD_COST)))
                        cash += _u * _px * (1 - GOLD_COST); gold_traded += _u * _px; gold_units -= _u
                    scale = min(1.0, max(cash, 0.0) / (tot * (1 + COST_ONE_WAY))) if tot > 0 else 0.0
''')
sub('''        # end of day: carry cash, mark to close, update excursions, ratchet stops, flag any that trip
        cash *= (1.0 + cash_daily)
''', '''        # gold sleeve: idle capital (cash + gold) is held in the ETF up to GOLD_CAP of equity
        if GOLD_CAP > 0:
            if gold_units > 0 and not np.isfinite(g_o[t]):                          # no ETF price today (data gap): close the position at the last known price
                cash += gold_units * g_prev * (1 - GOLD_COST); gold_traded += gold_units * g_prev; gold_units = 0.0
            elif np.isfinite(g_o[t]) and g_has[t - 1]:                              # trade only on consecutive genuine ETF prices (never at a stale price after the gap)
                _fp = g_o[t] if GOLD_FILL == "open" else g_prev
                _val = gold_units * _fp; _tgt = min(GOLD_CAP * eq_open, cash + _val)
                if abs(_tgt - _val) > GOLD_BAND * eq_open:
                    if _tgt > _val:
                        _amt = min(_tgt - _val, cash / (1 + GOLD_COST)); gold_units += _amt / _fp; cash -= _amt * (1 + GOLD_COST); gold_traded += _amt
                    else:
                        _u = (_val - _tgt) / _fp; cash += _u * _fp * (1 - GOLD_COST); gold_units -= _u; gold_traded += _u * _fp
        # end of day: carry cash, mark to close, update excursions, ratchet stops, flag any that trip
        cash *= (1.0 + cash_daily)
''')
sub('''        eq[t] = cash + float(pos.sum())
        expo[t] = pos.sum() / eq[t] if eq[t] > 0 else 0.0
''', '''        _gv = gold_units * g_c[t] if (GOLD_CAP > 0 and gold_units > 0) else 0.0
        eq[t] = cash + float(pos.sum()) + _gv
        expo[t] = pos.sum() / eq[t] if eq[t] > 0 else 0.0
        gold_w[t] = _gv / eq[t] if eq[t] > 0 else 0.0
''')
sub('''    return dict(eq=eq_s, expo=''', '''    return dict(gold_w=pd.Series(gold_w, index=index).iloc[t_first:], gold_traded=gold_traded, eq=eq_s, expo=''')
sub('''"nheld": res["nheld"], "bear"''', '''"nheld": res["nheld"], "gold_w": res["gold_w"], "bear"''')
s = s.replace('STRATEGY_NAME        = "CRESTLINE_GOLD_LAB"', 'STRATEGY_NAME        = "CRESTLINE_V2_5"').replace('"crestline_gold_lab_output"', '"crestline_v2_5_output"')
hdr = '''"""
crestline_v2_5.py -- CRESTLINE v2.5 = v2.4 + a native GOLD SLEEVE, with conservative cash accounting
===========================================================================================
Idle capital (the ~50% of equity the core logic leaves uninvested) is held in a gold ETF (GOLDBEES), up to GOLD_CAP (25%) of equity and never more than the idle cash.
Untimed by design: pre-registered tests (PREREG_GOLD2.md) found trend gating, bear-regime tilts and a silver split all WORSE than a plain capped holding; weight, not timing, is the lever.
ETF trades fill at the PREVIOUS close (the vendor's ETF opening prints are unreliable - see GOLD_FILL); the ETF is sold to fund stock entries; trades only when the target differs by > 2% of equity;
0.15% one-way cost; no ETF price in the 2011-14 data gap -> position closed at the last price and nothing is bought on a stale price.
Backtest accounting: idle cash earns 0% (CASH_RATE_ANNUAL = 0). Report Sharpe at rf = 0.
GOLD_CAP=0 with CASH_RATE_ANNUAL=0.065 reproduces v2.4 exactly (test_v2_5.py).
Honest-return warning: gold returned ~17%/yr (INR) in the usable 2007-10 + 2015-25 sample and ~14% point-to-point incl. the unobserved 2011-14. Quote results under GOLD_TARGET_RET=0.08 (planning) as well as real.
"""
'''
i = s.index("import os\nimport glob"); s = hdr + "\n" + s[i:]
open(os.path.join(here, "crestline_v2_5.py"), "w").write(s); print("ok")
