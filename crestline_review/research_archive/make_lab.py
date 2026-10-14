"""Builds crestline_lab.py from ../Crestine/crestline_v2_2.py by exact-string patches (each asserted).
The colleague's file is never edited. All new switches default to the baseline behaviour (parity is checked in review_parity.txt)."""
import os
SRC = os.path.join(os.path.dirname(__file__), "..", "Crestine", "crestline_v2_2.py")
s = open(SRC).read()

def sub(old, new, count=1):
    global s
    assert s.count(old) == count, (s.count(old), old[:70])
    s = s.replace(old, new)

# 1. extra switches + env overrides, right after the config block
sub('''SAVE_OUTPUTS         = True
OUTPUT_DIR           = os.path.join(os.path.dirname(os.path.abspath(__file__)), "crestline_v2_2_output")
''', '''SAVE_OUTPUTS         = True
OUTPUT_DIR           = os.path.join(os.path.dirname(os.path.abspath(__file__)), "crestline_v2_2_output")

# ── LAB-ONLY switches (defaults == v2.2 behaviour) ────────────────────────────
SCORE_W_HP           = 1.0              # weight of z(52w-high proximity)
SCORE_W_TP           = 1.0              # weight of z(trend persistence)
RESID_W              = 0.0              # weight of z(residual momentum 12-1), as csm_resid_tilt (0 = off)
M3_EXCL_Q            = 0.0              # live-Zenith "Low-MAX": drop the top q share by 21d max daily return (0 = off)
BEAR_NO_ENTRY        = False            # True: no NEW entries while bench < SMA200 (instead of scaling by BEAR_SCALE)
SIZE_BY_VOL          = False            # True: entry weight proportional to 1/ATR% (cap/ADV rules unchanged)
import json as _json
_OVR = _json.loads(os.environ.get("CL_OVR", "{}"))
for _k, _v in _OVR.items():
    if _k not in globals():
        raise SystemExit(f"unknown override {_k}")
    globals()[_k] = _v
if "MAX_WEIGHT" not in _OVR:
    MAX_WEIGHT = 1.0 / TOP_N
if "CL_OUT" in os.environ:
    OUTPUT_DIR = os.environ["CL_OUT"]
''')

# 2. score function
sub('''    z_hp = zscore(hp[i], u & ~np.isnan(hp[i]))
    z_tp = zscore(tp[i], u & ~np.isnan(tp[i]))
    score = z_hp + z_tp
    pool = u & ~np.isnan(score)
    return score, pool''', '''    if M3_EXCL_Q > 0:
        el = u & ~np.isnan(hp[i]) & ~np.isnan(tp[i]) & ~np.isnan(m3_mat[i])
        v = m3_mat[i][el]
        pr = np.full(n_stk, np.nan)
        pr[el] = (np.argsort(np.argsort(v, kind="stable"), kind="stable") + 1) / v.size
        u = u & ~(el & (pr > 1.0 - M3_EXCL_Q))
    z_hp = zscore(hp[i], u & ~np.isnan(hp[i]))
    z_tp = zscore(tp[i], u & ~np.isnan(tp[i]))
    score = SCORE_W_HP * z_hp + SCORE_W_TP * z_tp
    if RESID_W:
        base_ok = u & ~np.isnan(score)
        score = zscore(score, base_ok)
        z_r = zscore(resid_mat[i], base_ok & ~np.isnan(resid_mat[i]))
        score = score + RESID_W * np.where(np.isnan(z_r), 0.0, z_r)
    pool = u & ~np.isnan(score)
    return score, pool''')

# 3. M3 matrix (21d max daily return at signal bars), built next to hp/tp
sub('''hp = hp_matrix(HP_WINDOW, HP_MIN_PERIODS)
tp = tp_matrix(TP_LOOKBACK, TP_MIN_PERIODS)
''', '''hp = hp_matrix(HP_WINDOW, HP_MIN_PERIODS)
tp = tp_matrix(TP_LOOKBACK, TP_MIN_PERIODS)
if M3_EXCL_Q > 0:
    m3_mat = prices_sig.pct_change(fill_method=None).rolling(21, min_periods=21).max().iloc[me_pos].to_numpy(dtype=float)
''')

# 4. move the rank loop below the benchmark block (resid needs the benchmark)
i0 = s.index("ranks, scores, pools, hv_flag = {}, {}, {}, {}")
i1 = s.index("# equal-weight benchmark of the liquid universe")
rank_block = s[i0:i1]
s = s[:i0] + s[i1:]
j = s.index('_p0 = int(me_pos[sig_rows[0]])')
resid_block = '''if RESID_W:
    _ret = prices_sig.pct_change(fill_method=None)
    _mkt = bench_idx.pct_change(fill_method=None)
    _beta = _ret.rolling(252, min_periods=200).cov(_mkt).div(_mkt.rolling(252, min_periods=200).var(), axis=0)
    _res = _ret.sub(_beta.shift(1).mul(_mkt, axis=0))
    resid_mat = _res.rolling(231, min_periods=184).sum().shift(21).iloc[me_pos].to_numpy(dtype=float)
    del _ret, _mkt, _beta, _res

'''
s = s[:j] + resid_block + rank_block + s[j:]

# 5. entry sizing: optional inverse-vol weights
sub('''                    w_int = allocate(np.ones(len(cids)), caps)''', '''                    raw_w = np.ones(len(cids))
                    if SIZE_BY_VOL:
                        a_ = atr_pct_sig[k][cids]
                        raw_w = np.where(np.isfinite(a_) & (a_ > 0), 1.0 / np.where(a_ > 0, a_, 1.0), np.nan)
                        raw_w = np.where(np.isnan(raw_w), np.nanmedian(raw_w), raw_w)
                    w_int = allocate(raw_w, caps)''')

# 6. optional: no new entries in a bear regime
sub('''                    w = w_int * tier_t''', '''                    w = w_int * (0.0 if (BEAR_NO_ENTRY and bear[t]) else tier_t)''')


# 8. CA_ADJUST: back-adjust prices/volumes for every flagged jump (unadjusted splits/bonuses/consolidations in the vendor data)
#    instead of only masking the cell. Without it a position held through a split books the split as a real -50..-90% loss.
sub("""SIZE_BY_VOL          = False""", """CA_ADJUST            = False            # True: back-adjust history for flagged jumps (split-neutral positions) instead of masking
SIZE_BY_VOL          = False""")
sub("""ca_flag  = ((_ret_raw < CA_DOWN) | (_ret_raw > CA_UP)).fillna(False)
del _ret_raw
print(f"\\nCorporate-action mask: {int(ca_flag.to_numpy().sum())} cells masked")
""", """ca_flag  = ((_ret_raw < CA_DOWN) | (_ret_raw > CA_UP)).fillna(False)
_floor_src = prices
if CA_ADJUST:
    _lr = np.nan_to_num(np.log1p(_ret_raw.where(ca_flag)).to_numpy(dtype=float), nan=0.0)
    _adj = pd.DataFrame(np.exp(np.cumsum(_lr[::-1], axis=0)[::-1] - _lr), index=prices.index, columns=prices.columns)
    prices = prices * _adj; highs = highs * _adj; lows = lows * _adj; opens = opens * _adj; volumes = volumes / _adj
    print(f"\\nCorporate-action ADJUST: {int(ca_flag.to_numpy().sum())} jump cells back-adjusted (no cells masked)")
    ca_flag = ca_flag & False
    del _lr, _adj
del _ret_raw
print(f"\\nCorporate-action mask: {int(ca_flag.to_numpy().sum())} cells masked")
""")

sub("""prices_sig = prices.ffill()
""", """prices_sig = prices.ffill()
floor_sig  = _floor_src.ffill() if CA_ADJUST else prices_sig     # the MIN_PRICE floor must use as-traded (pre-adjustment) prices: back-adjustment uses future splits
""")
sub("""price_ok = prices_sig.shift(1).iloc[me_pos].to_numpy(dtype=float) > MIN_PRICE""", """price_ok = floor_sig.shift(1).iloc[me_pos].to_numpy(dtype=float) > MIN_PRICE""")
sub("""ok_pre = (prices_sig.shift(1).to_numpy() > MIN_PRICE)[1:pre_end + 1]""", """ok_pre = (floor_sig.shift(1).to_numpy() > MIN_PRICE)[1:pre_end + 1]""")

# 7. machine-readable summary
sub('''    print(f"\\n[Saved] equity_curves.csv''', '''    _json.dump(dict(m=m, exits=ec, n_trades=res["n_trades"], entries=res["n_entries"], win=res["win_rate"],
                    pf=res["profit_factor"], ic=icir_tab.reset_index().to_dict("records")),
               open(os.path.join(OUTPUT_DIR, "summary.json"), "w"), default=float)
    print(f"\\n[Saved] equity_curves.csv''')

open(os.path.join(os.path.dirname(__file__), os.environ.get("LAB_OUT", "crestline_lab.py")), "w").write(s)
print("ok", len(s))
