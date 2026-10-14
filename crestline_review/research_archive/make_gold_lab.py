"""Builds crestline_gold_lab.py from crestline_struct_lab.py: (1) daily dump (equity, invested fraction, bear, panic) for sleeve post-processing, (2) optional gold/silver ETF columns in the ranking. ETF_LIST=[] == v2.4 bit-exactly."""
import os
here = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(here, "crestline_struct_lab.py")).read()
def sub(old, new, count=1):
    global s
    assert s.count(old) == count, (s.count(old), old[:80]); s = s.replace(old, new)
sub('''RS_CATA_PCT          = 0.25             # catastrophic trailing stop kept while suppressed
''', '''RS_CATA_PCT          = 0.25             # catastrophic trailing stop kept while suppressed
# ── GOLD/SILVER switches (OFF = v2.4) ─────────────────────────────────────────────────────────────────────
ETF_LIST             = []               # e.g. ["GOLDBEES", "SILVERBEES"]: added to the ranking universe as ordinary columns
ETF_FOLDER           = '/Users/hemantsoni/Documents/upstox_data_folder/gold_silver_ohlcv_data'
ETF_DRIFT_LAMBDA     = 0.0              # >0: remove this share of each ETF's excess drift over the 6.5% liquid fund (placebo for gold's bull market)
ETF_MIN_OBS          = 240              # eligible only after this many genuine observations in the last 252 bars (no stale/forward-filled windows)
''')
sub('''if prices.empty:
    raise SystemExit("No price data loaded.")
''', '''if prices.empty:
    raise SystemExit("No price data loaded.")
etf_cols = list(ETF_LIST)
for _sym in etf_cols:
    _d = pd.read_csv(os.path.join(ETF_FOLDER, _sym + ".csv")); _d["t"] = pd.to_datetime(_d.timestamp.str[:10]); _d = _d.set_index("t")[["open", "high", "low", "close", "volume"]]
    _d = _d[~_d.index.duplicated(keep="last")].sort_index()
    for _c in ["open", "high", "low", "close"]:
        _d[_c] = _d[_c].mask(_d[_c] <= 0)
    if ETF_DRIFT_LAMBDA > 0:
        _r = _d.close.pct_change(fill_method=None); _r[_d.index.to_series().diff().dt.days > 5] = np.nan
        _dl = np.nanmean(np.log1p(_r.dropna())) - np.log1p((1.065) ** (1 / 252) - 1)
        _f = np.exp(-ETF_DRIFT_LAMBDA * _dl * _r.notna().cumsum())
        for _c in ["open", "high", "low", "close"]:
            _d[_c] = _d[_c] * _f
    prices = prices.join(_d.close.astype("float32").rename(_sym), how="left"); volumes = volumes.join(_d.volume.astype("float32").rename(_sym), how="left")
    highs = highs.join(_d.high.astype("float32").rename(_sym), how="left"); lows = lows.join(_d.low.astype("float32").rename(_sym), how="left"); opens = opens.join(_d.open.astype("float32").rename(_sym), how="left")
''')
sub('''index, n_bars, n_stk = prices.index, len(prices.index), prices.shape[1]
''', '''index, n_bars, n_stk = prices.index, len(prices.index), prices.shape[1]
is_etf = np.array([c in etf_cols for c in prices.columns], dtype=bool)
''')
sub('''liq_ok = (liq_rank >= UNIVERSE_TOP_N_MIN) & (liq_rank <= UNIVERSE_TOP_N_MAX)
''', '''if etf_cols:   # equity ranks are computed WITHOUT the ETFs (so stock membership is unchanged); an ETF is liquid enough if it would sit inside the band
    med_eq = np.where(is_etf, np.nan, med)
    liq_rank = pd.DataFrame(med_eq).rank(axis=1, ascending=False, method="min").to_numpy()
    _thr = np.array([np.nanmin(np.where(liq_rank[i] <= UNIVERSE_TOP_N_MAX, med_eq[i], np.nan)) if np.isfinite(liq_rank[i]).any() else np.nan for i in range(n_m)])
    liq_ok = ((liq_rank >= UNIVERSE_TOP_N_MIN) & (liq_rank <= UNIVERSE_TOP_N_MAX)) | (is_etf[None, :] & (med >= _thr[:, None]))
else:
    liq_ok = (liq_rank >= UNIVERSE_TOP_N_MIN) & (liq_rank <= UNIVERSE_TOP_N_MAX)
''')
sub('''universe = stale_ok & price_ok & liq_ok & circ_ok
''', '''universe = stale_ok & price_ok & liq_ok & circ_ok
if etf_cols:
    _cnt = prices.notna().rolling(252, min_periods=1).sum().iloc[me_pos].to_numpy()
    universe = universe & (~is_etf[None, :] | (_cnt >= ETF_MIN_OBS))
''')
sub('''    ok_pre = (floor_sig.shift(1).to_numpy() > MIN_PRICE)[1:pre_end + 1]
''', '''    ok_pre = (floor_sig.shift(1).to_numpy() > MIN_PRICE)[1:pre_end + 1] & ~is_etf[None, :]
''')
sub('''    seg = np.clip(ret_np[a_:b_ + 1][:, universe[j]], -0.5, 0.5)
''', '''    seg = np.clip(ret_np[a_:b_ + 1][:, universe[j] & ~is_etf], -0.5, 0.5)
''')
sub('''    res["eq"].rename(STRATEGY_NAME).to_csv(os.path.join(OUTPUT_DIR, "equity_curves.csv"))
''', '''    res["eq"].rename(STRATEGY_NAME).to_csv(os.path.join(OUTPUT_DIR, "equity_curves.csv"))
    pd.DataFrame({"eq": res["eq"], "expo": res["expo"], "nheld": res["nheld"], "bear": bear[t_first:], "panic": panic[t_first:]}, index=res["eq"].index).to_csv(os.path.join(OUTPUT_DIR, "daily.csv"))
    if etf_cols:
        _tl = pd.DataFrame(res["trades"]); _tl = _tl[_tl.Ticker.isin(etf_cols)] if len(_tl) else _tl
        _tl.to_csv(os.path.join(OUTPUT_DIR, "etf_trades.csv"), index=False)
''')
s = s.replace('STRATEGY_NAME        = "CRESTLINE_STRUCT_LAB"', 'STRATEGY_NAME        = "CRESTLINE_GOLD_LAB"').replace('"crestline_struct_lab_output"', '"crestline_gold_lab_output"')
open(os.path.join(here, "crestline_gold_lab.py"), "w").write(s); print("ok")
