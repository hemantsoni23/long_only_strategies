"""
crestline_v2_4.py -- CRESTLINE v2.4 = v2.3 fixed baseline + the ONE parameter change that survived the ablation study (TOP_N 15 -> 25)
============================================================================================
Derived from Crestine/crestline_v2_2.py (colleague's file, untouched) via crestline_review/make_lab.py + make_v2_3.py.
Signal, universe, ranking, sizing, stops, schedule and overlay are exactly v2.2. What changed (see crestline_review/REVIEW.md s.3):

  FIX 1  CA_ADJUST (default True)  Vendor OHLCV holds ~680 unadjusted down-jumps (splits/bonuses) and ~230 up-jumps. v2.2 only masked
         those cells, so a position HELD through one booked the split as a real -50..-90% loss (INNOVTEC -89%, AIRAN -81% ...), and the
         hard stop fired on it. v2.3 back-adjusts price history and divides volume at every flagged jump; positions are split-neutral.
  FIX 2  CASH_RATE_ANNUAL = 6.5%   v2.2 booked 0% on ~48% idle capital. Live has to sweep idle cash to a liquid fund / LIQUIDBEES.
  FIX 3  START_DATE = 2006         2015 hid 2008-09 (-28%). v2.2's first-year buffer is unchanged.
  FIX 4  anchor_report.py          v2.2's headline is a single 60-bar schedule anchor (the best of six). Always quote the distribution
         over CRESTLINE_OFFSET in {0,10,..,50} and the staggered 6-anchor blend.
  CLEAN  removed SIZE_BY_VOL (could never bind: weights are capped at 1/TOP_N).

v2.4 vs v2.3: ONLY TOP_N (15 -> 25). CL_OVR='{"TOP_N": 15}' reproduces v2.3 exactly (test_v2_4.py).
Reproduce v2.2 exactly:  CL_OVR='{"CA_ADJUST": false, "CASH_RATE_ANNUAL": 0.0, "START_DATE": "2015-01-01"}' python3 crestline_v2_3.py
Lab switches kept for later experiments (all default OFF = v2.2 logic): SCORE_W_HP/TP, RESID_W, M3_EXCL_Q, BEAR_NO_ENTRY.
Env: CL_OVR (JSON config overrides), CL_OUT (output dir), CRESTLINE_OFFSET (schedule anchor).

KNOWN LIMITATIONS NOT FIXED (unchanged v2.2 behaviour): INITIAL_CAPITAL=1 lakh so the 5%-ADV cap never binds (set it to the real book size); a capped slot is left
idle instead of walking down the rank list; fills ignore locked circuits and impact (flat 0.3%/side); overlay scales new entries only; pre-2020 volume is thin.
"""

import os
import glob
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore", message="All-NaN slice encountered")
warnings.filterwarnings("ignore", message="Mean of empty slice")


# ══════════════════════════════════════════════════════════════════════════════
# CONFIG  (edit only this block)
# ══════════════════════════════════════════════════════════════════════════════

STRATEGY_NAME        = "CRESTLINE_V2_4"
DATA_FOLDER          = '/Users/hemantsoni/Documents/upstox_data_folder/ohlcv_data'
START_DATE           = "2006-01-01"   # v2.2 used 2015, which hides 2008-09; use anchors via CRESTLINE_OFFSET / anchor_report.py
END_DATE             = "2025-12-31"
BUFFER_DAYS          = 400

# ── corporate-action mask ────────────────────────────────────────────────────
CA_DOWN, CA_UP       = -0.40, 3.00
FFILL_LIMIT_DAYS     = 5

# ── universe: liquid, tradable stocks only ───────────────────────────────────
MIN_PRICE            = 20.0
UNIVERSE_TOP_N_MIN, UNIVERSE_TOP_N_MAX = 1, 1000
DVOL_WINDOW, DVOL_MIN_PERIODS = 63, 21
CIRCUIT_WINDOW, MAX_CIRCUIT_DAYS = 63, 5
REQUIRE_TRADED_ON_SIGNAL_BAR = True

# ── score legs ────────────────────────────────────────────────────────────────
HP_WINDOW, HP_MIN_PERIODS = 252, 200
TP_LOOKBACK, TP_MIN_PERIODS = 189, 150
TP_SMA_WINDOW, TP_SMA_MIN_PERIODS = 50, 40
MIN_POOL_SIZE        = 20

# ── signal diagnostics ───────────────────────────────────────────────────────
IC_HORIZONS          = [5, 10, 15, 20, 40, 60, 120]

# ── schedule ─────────────────────────────────────────────────────────────────
REBALANCE_FREQ_DAYS  = 60               # FULL rebalance (rank exits + entries) every N trading bars
SCHEDULE_OFFSET_DAYS = int(os.environ.get("CRESTLINE_OFFSET", 0))   # shift the schedule anchor (for offset sweeps)

# ── slot refill (A) ──────────────────────────────────────────────────────────
USE_SLOT_REFILL      = False            # True: fill empty slots on the finer grid below (no rank exits there)
REFILL_FREQ_DAYS     = 20               # refill-only signal every N bars
REFILL_COOLDOWN_DAYS = 30                # bars before a just-sold name may be bought again (1 = no same-bar re-buy)

# ── portfolio construction ───────────────────────────────────────────────────
TOP_N                = 25               # v2.4: was 15 (ablation: +0.18 Sharpe, 6/6 anchors, both periods; saturates 25-40)
EXIT_RANK_MULT       = 2.0
MAX_WEIGHT           = 1.0 / TOP_N
MAX_ENTRY_PCT        = 0.10
ADV_CAP              = 0.05
INITIAL_CAPITAL      = 100_000.0

# ── (1) ATR trailing stop, optional volatility-dependent multiplier ──────────
USE_ATR_STOP         = False
ATR_WINDOW           = 14
ATR_MULT             = 4.0              # used when ATR_DYNAMIC_MULT is False
ATR_DYNAMIC_MULT     = True            # True: multiplier depends on the name's volatility class at entry
ATR_MULT_HIGH_VOL    = 1.5              # multiplier for HIGH-volatility names
ATR_MULT_LOW_VOL     = 2.5              # multiplier for LOW-volatility names
VOL_SPLIT_PCTL       = 0.5              # high-vol = ATR% at/above this percentile of the ranked pool on the signal bar

# ── (2) hard stop from entry (fixed) ─────────────────────────────────────────
USE_HARD_STOP        = True
HARD_STOP_PCT        = 0.20

# ── (3) peak % trailing stop ─────────────────────────────────────────────────
USE_PEAK_STOP        = True
PEAK_STOP_PCT        = 0.15

# ── (4) volatility-scaled % trailing stop ────────────────────────────────────
USE_VOL_SCALED_STOP  = True
VOLSTOP_K            = 2.5              # width = K * (ATR/close at entry)
VOLSTOP_MIN_PCT      = 0.10
VOLSTOP_MAX_PCT      = 0.25

# ── (5) relative-strength stop (stock vs equal-weight universe index) ────────
USE_RS_STOP          = False
RS_STOP_PCT          = 0.15

# ── (6) trend-break exit ─────────────────────────────────────────────────────
USE_TREND_BREAK_STOP = False
TREND_SMA_WINDOW     = 100
TREND_BREAK_DAYS     = 3                # consecutive closes below the SMA
TREND_BREAK_BUFFER   = 0.0              # close must be this fraction below the SMA to count

# ── regime overlay (scales NEW-entry sizing only) ────────────────────────────
USE_OVERLAY          = True
BENCH_SMA            = 200
BENCH_SMA_MIN_PERIODS = 150
BEAR_SCALE           = 0.6
PANIC_VOL_WINDOW     = 21
PANIC_PCTL           = 0.95
PANIC_MIN_PERIODS    = 126
PANIC_SCALE          = 0.3

# ── frictions ────────────────────────────────────────────────────────────────
COST_ONE_WAY         = 0.003
CASH_RATE_ANNUAL     = 0.065          # idle cash swept to a liquid fund (live must actually do this)

SAVE_OUTPUTS         = True
OUTPUT_DIR           = os.path.join(os.path.dirname(os.path.abspath(__file__)), "crestline_v2_4_output")

# ── LAB-ONLY switches (defaults == v2.2 behaviour) ────────────────────────────
SCORE_W_HP           = 1.0              # weight of z(52w-high proximity)
SCORE_W_TP           = 1.0              # weight of z(trend persistence)
RESID_W              = 0.0              # weight of z(residual momentum 12-1), as csm_resid_tilt (0 = off)
M3_EXCL_Q            = 0.0              # live-Zenith "Low-MAX": drop the top q share by 21d max daily return (0 = off)
BEAR_NO_ENTRY        = False            # True: no NEW entries while bench < SMA200 (instead of scaling by BEAR_SCALE)
CA_ADJUST            = True             # back-adjust history at flagged jumps (split-neutral positions); False = v2.2 masking (books splits as real losses)
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


# ══════════════════════════════════════════════════════════════════════════════
# DATA LOADER
# ══════════════════════════════════════════════════════════════════════════════

def load_data(folder_path):
    """Load every CSV in folder_path. Returns prices, volumes, highs, lows, opens (DataFrames).
    Non-positive prices are masked to NaN; duplicate timestamps keep the last row."""
    all_files = glob.glob(os.path.join(folder_path, "*.csv"))
    if not all_files:
        raise ValueError(f"No CSV files found in {folder_path}")

    price_list, volume_list, high_list, low_list, open_list = [], [], [], [], []
    print(f"Loading {len(all_files)} files from {folder_path}...")

    for filename in all_files:
        try:
            symbol = os.path.basename(filename).replace('.csv', '')
            df = pd.read_csv(filename, parse_dates=['datetime'], index_col='datetime')

            def _clean(s):
                return s[~s.index.duplicated(keep='last')]

            def _clean_price(s):
                s = _clean(s)
                return s.mask(s <= 0)

            if 'close' in df.columns:
                price_list.append(_clean_price(df['close'].rename(symbol)).astype("float32"))
            else:
                print(f"Warning: 'close' missing in {filename}")
            if 'volume' in df.columns:
                volume_list.append(_clean(df['volume'].rename(symbol)).astype("float32"))
            if 'high' in df.columns:
                high_list.append(_clean_price(df['high'].rename(symbol)).astype("float32"))
            if 'low' in df.columns:
                low_list.append(_clean_price(df['low'].rename(symbol)).astype("float32"))
            if 'open' in df.columns:
                open_list.append(_clean_price(df['open'].rename(symbol)).astype("float32"))
        except Exception as e:
            print(f"Error loading {filename}: {e}")

    if not price_list:
        return (pd.DataFrame(),) * 5

    def _build(lst):
        if not lst:
            return pd.DataFrame()
        df = pd.concat(lst, axis=1)
        df.sort_index(inplace=True)
        return df

    prices_df, volumes_df = _build(price_list), _build(volume_list)
    highs_df, lows_df, opens_df = _build(high_list), _build(low_list), _build(open_list)

    print(f"Loaded  Prices:{prices_df.shape}  Volumes:{volumes_df.shape}  "
          f"Highs:{highs_df.shape}  Lows:{lows_df.shape}  Opens:{opens_df.shape}")
    return prices_df, volumes_df, highs_df, lows_df, opens_df


# ══════════════════════════════════════════════════════════════════════════════
# 1. LOAD + CORPORATE-ACTION MASK + SLICE
# ══════════════════════════════════════════════════════════════════════════════

prices, volumes, highs, lows, opens = load_data(DATA_FOLDER)
if prices.empty:
    raise SystemExit("No price data loaded.")

prices = prices.sort_index()
start_ts = pd.Timestamp(START_DATE)
end_ts   = pd.Timestamp(END_DATE)

full_index = prices.index
start_pos  = int(full_index.searchsorted(start_ts))
if start_pos >= len(full_index):
    raise SystemExit(f"START_DATE {START_DATE} is after the last bar in the data.")
buf_pos = max(start_pos - BUFFER_DAYS, 0)
if buf_pos == 0 and start_pos < BUFFER_DAYS:
    print(f"WARNING: only {start_pos} bars exist before START_DATE (wanted {BUFFER_DAYS}).")
load_start = full_index[buf_pos]

prices  = prices.loc[load_start:end_ts]
volumes = volumes.reindex(index=prices.index, columns=prices.columns)
highs   = highs.reindex(index=prices.index, columns=prices.columns)
lows    = lows.reindex(index=prices.index, columns=prices.columns)
opens   = opens.reindex(index=prices.index, columns=prices.columns)

has_hl   = highs.notna().to_numpy().any() and lows.notna().to_numpy().any()
has_open = opens.notna().to_numpy().any()
if not volumes.notna().to_numpy().any():
    raise SystemExit("No volume data -- the liquidity filter cannot be built.")
if (USE_ATR_STOP or USE_VOL_SCALED_STOP) and not has_hl:
    raise SystemExit("ATR-based stops require high/low data -- none was loaded.")

index, n_bars, n_stk = prices.index, len(prices.index), prices.shape[1]

_ret_raw = prices.ffill().pct_change(fill_method=None)
ca_flag  = ((_ret_raw < CA_DOWN) | (_ret_raw > CA_UP)).fillna(False)
_floor_src = prices
if CA_ADJUST:
    _lr = np.nan_to_num(np.log1p(_ret_raw.where(ca_flag)).to_numpy(dtype=float), nan=0.0)
    _adj = pd.DataFrame(np.exp(np.cumsum(_lr[::-1], axis=0)[::-1] - _lr), index=prices.index, columns=prices.columns)
    prices = prices * _adj; highs = highs * _adj; lows = lows * _adj; opens = opens * _adj; volumes = volumes / _adj
    print(f"\nCorporate-action ADJUST: {int(ca_flag.to_numpy().sum())} jump cells back-adjusted (no cells masked)")
    ca_flag = ca_flag & False
    del _lr, _adj
del _ret_raw
print(f"\nCorporate-action mask: {int(ca_flag.to_numpy().sum())} cells masked")
prices = prices.mask(ca_flag)
highs  = highs.mask(ca_flag)
lows   = lows.mask(ca_flag)
opens  = opens.mask(ca_flag)

if REBALANCE_FREQ_DAYS < 1 or REFILL_FREQ_DAYS < 1:
    raise SystemExit("REBALANCE_FREQ_DAYS and REFILL_FREQ_DAYS must be positive integers.")

# ── signal schedule ──────────────────────────────────────────────────────────
# full-rebalance bars every REBALANCE_FREQ_DAYS; optional refill-only bars every REFILL_FREQ_DAYS.
sched_start_pos = int(index.searchsorted(start_ts)) + SCHEDULE_OFFSET_DAYS
rebal_pos  = np.arange(sched_start_pos, n_bars, REBALANCE_FREQ_DAYS)
refill_pos = np.arange(sched_start_pos, n_bars, REFILL_FREQ_DAYS) if USE_SLOT_REFILL else np.array([], dtype=int)
me_pos = np.union1d(rebal_pos, refill_pos).astype(int)
me_pos = me_pos[(me_pos >= 1) & (me_pos + 1 < n_bars)]
is_rebal = np.isin(me_pos, rebal_pos)            # True: full rebalance row; False: refill-only row
me_dates = index[me_pos]
n_m = len(me_pos)
eval_mask = (me_dates >= start_ts) & (me_dates <= end_ts)
sig_rows = np.where(eval_mask)[0]                # every signal row (rebalance + refill)
full_rebal_rows = sig_rows[is_rebal[sig_rows]]   # full rebalances only (used for the IC diagnostic)

print(f"Buffer starts : {load_start.date()}")
print(f"Schedule      : full rebalance every {REBALANCE_FREQ_DAYS} bars -> {len(full_rebal_rows)} rebalances"
      + (f"  +  refill every {REFILL_FREQ_DAYS} bars -> {len(sig_rows) - len(full_rebal_rows)} refill-only rows"
         if USE_SLOT_REFILL else "  (slot refill OFF)")
      + f"   ({me_dates[sig_rows[0]].date()} -> {me_dates[sig_rows[-1]].date()})")
print(f"Stocks loaded : {n_stk}   |  highs/lows: {has_hl}  opens: {has_open}")


# ══════════════════════════════════════════════════════════════════════════════
# 2. FEATURE MATRICES  (rows = signal bars, cols = stocks)
# ══════════════════════════════════════════════════════════════════════════════

prices_sig = prices.ffill()
floor_sig  = _floor_src.ffill() if CA_ADJUST else prices_sig     # the MIN_PRICE floor must use as-traded (pre-adjustment) prices: back-adjustment uses future splits
highs_sig  = highs.ffill() if has_hl else prices_sig
lows_sig   = lows.ffill() if has_hl else prices_sig

mclose = prices_sig.iloc[me_pos].to_numpy(dtype=float)
traded_on_signal_bar = prices.iloc[me_pos].notna().to_numpy()

# price floor: previous BAR's close (known at the signal bar)
price_ok = floor_sig.shift(1).iloc[me_pos].to_numpy(dtype=float) > MIN_PRICE

dvol = (prices_sig * volumes).to_numpy(dtype=float)
med = np.full((n_m, n_stk), np.nan)
for i, p in enumerate(me_pos):
    w = dvol[max(0, p - DVOL_WINDOW):p]
    if w.shape[0] == 0:
        continue
    cnt = np.sum(~np.isnan(w), axis=0)
    m = np.nanmedian(w, axis=0)
    med[i] = np.where(cnt >= DVOL_MIN_PERIODS, m, np.nan)
del dvol
liq_rank = pd.DataFrame(med).rank(axis=1, ascending=False, method="min").to_numpy()
liq_ok = (liq_rank >= UNIVERSE_TOP_N_MIN) & (liq_rank <= UNIVERSE_TOP_N_MAX)

if has_hl:
    locked = ((highs == lows) & highs.notna()).to_numpy(dtype=np.int32)
    cs = np.vstack([np.zeros((1, n_stk), dtype=np.int64), np.cumsum(locked, axis=0, dtype=np.int64)])
    circ_cnt = np.empty((n_m, n_stk))
    for i, p in enumerate(me_pos):
        circ_cnt[i] = cs[p] - cs[max(0, p - CIRCUIT_WINDOW)]
    circ_ok = circ_cnt <= MAX_CIRCUIT_DAYS
    del locked, cs
else:
    circ_ok = np.ones((n_m, n_stk), dtype=bool)

stale_ok = traded_on_signal_bar if REQUIRE_TRADED_ON_SIGNAL_BAR else np.ones_like(traded_on_signal_bar)

universe = stale_ok & price_ok & liq_ok & circ_ok


def hp_matrix(window, min_periods):
    hi = highs_sig.rolling(window, min_periods=min_periods).max()
    return (prices_sig / hi).iloc[me_pos].to_numpy(dtype=float)


_above_cache = {}
def above_frame(sma_window):
    if sma_window not in _above_cache:
        sma = prices_sig.rolling(sma_window, min_periods=int(round(sma_window * 0.8))).mean()
        _above_cache[sma_window] = (prices_sig > sma).astype("float32").where(prices_sig.notna() & sma.notna())
    return _above_cache[sma_window]


def tp_matrix(lookback, min_periods, sma_window=TP_SMA_WINDOW):
    return above_frame(sma_window).rolling(lookback, min_periods=min_periods).mean().iloc[me_pos].to_numpy(dtype=float)


hp = hp_matrix(HP_WINDOW, HP_MIN_PERIODS)
tp = tp_matrix(TP_LOOKBACK, TP_MIN_PERIODS)
if M3_EXCL_Q > 0:
    m3_mat = prices_sig.pct_change(fill_method=None).rolling(21, min_periods=21).max().iloc[me_pos].to_numpy(dtype=float)


def zscore(x, mask):
    out = np.full(x.shape, np.nan)
    v = x[mask]
    if v.size < 3:
        return out
    sd = v.std(ddof=1)
    if sd == 0 or np.isnan(sd):
        return out
    out[mask] = (v - v.mean()) / sd
    return out


def score_for_row(i):
    """Composite score z(HP) + z(TP) and the ranking pool for signal row i."""
    u = universe[i]
    if M3_EXCL_Q > 0:
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
    return score, pool


# ── daily ATR: TR = max(H-L, |H-prevC|, |L-prevC|), simple rolling mean ──
prev_close_d = prices_sig.shift(1)
_tr = np.maximum(
    np.maximum((highs_sig - lows_sig).to_numpy(dtype=float),
               np.abs((highs_sig - prev_close_d).to_numpy(dtype=float))),
    np.abs((lows_sig - prev_close_d).to_numpy(dtype=float)))
atr_np = pd.DataFrame(_tr, index=prices_sig.index, columns=prices_sig.columns) \
    .rolling(ATR_WINDOW, min_periods=ATR_WINDOW).mean().to_numpy(dtype=np.float32)
del _tr, prev_close_d

atr_pct_sig = atr_np[me_pos].astype(float) / np.where(mclose > 0, mclose, np.nan)   # ATR/close at each signal bar

# trend-break SMA (daily)
trend_sma_np = prices_sig.rolling(TREND_SMA_WINDOW, min_periods=int(round(TREND_SMA_WINDOW * 0.8))) \
    .mean().to_numpy(dtype=np.float32)


# ══════════════════════════════════════════════════════════════════════════════
# 3. RANKS, VOLATILITY CLASS, BENCHMARK AND REGIME TIERS
# ══════════════════════════════════════════════════════════════════════════════

# equal-weight benchmark of the liquid universe, daily returns clipped to +-50%
ret_np = prices_sig.pct_change(fill_method=None).to_numpy(dtype=np.float32)
bench_ret = np.zeros(n_bars)
# warm-up over the buffer (before the first signal bar): all names with prior close above the price floor
pre_end = int(me_pos[0])
if pre_end >= 1:
    ok_pre = (floor_sig.shift(1).to_numpy() > MIN_PRICE)[1:pre_end + 1]
    seg = np.where(ok_pre, np.clip(ret_np[1:pre_end + 1], -0.5, 0.5), np.nan)
    bench_ret[1:pre_end + 1] = np.nan_to_num(np.nanmean(seg, axis=1))
for j in range(n_m):
    a_ = me_pos[j] + 1
    b_ = me_pos[j + 1] if j + 1 < n_m else n_bars - 1
    if a_ > b_ or a_ >= n_bars:
        continue
    seg = np.clip(ret_np[a_:b_ + 1][:, universe[j]], -0.5, 0.5)
    if seg.shape[1]:
        bench_ret[a_:b_ + 1] = np.nan_to_num(np.nanmean(seg, axis=1))
del ret_np
bench_idx = pd.Series((1.0 + bench_ret).cumprod(), index=index)
bench_np = bench_idx.to_numpy(dtype=float)
bench_sma = bench_idx.rolling(BENCH_SMA, min_periods=BENCH_SMA_MIN_PERIODS).mean()
bear = (bench_idx.shift(1) < bench_sma.shift(1)).to_numpy()
bvol = pd.Series(bench_ret, index=index).rolling(PANIC_VOL_WINDOW).std().shift(1)
panic = (bvol > bvol.expanding(min_periods=PANIC_MIN_PERIODS).quantile(PANIC_PCTL)).to_numpy()
tier_arr = np.ones(n_bars)
tier_arr[bear] = BEAR_SCALE
tier_arr[panic] = np.minimum(tier_arr[panic], PANIC_SCALE)

if RESID_W:
    _ret = prices_sig.pct_change(fill_method=None)
    _mkt = bench_idx.pct_change(fill_method=None)
    _beta = _ret.rolling(252, min_periods=200).cov(_mkt).div(_mkt.rolling(252, min_periods=200).var(), axis=0)
    _res = _ret.sub(_beta.shift(1).mul(_mkt, axis=0))
    resid_mat = _res.rolling(231, min_periods=184).sum().shift(21).iloc[me_pos].to_numpy(dtype=float)
    del _ret, _mkt, _beta, _res

ranks, scores, pools, hv_flag = {}, {}, {}, {}
for k in sig_rows:
    score, pool = score_for_row(k)
    scores[k] = score
    pools[k] = pool
    rk = np.full(n_stk, np.nan)
    thr = np.nan
    if pool.sum() >= MIN_POOL_SIZE:
        idx = np.where(pool)[0]
        order = idx[np.argsort(-score[idx], kind="stable")]
        rk[order] = np.arange(1, len(order) + 1)
        ap = atr_pct_sig[k][pool]
        ap = ap[np.isfinite(ap)]
        if ap.size:
            thr = np.percentile(ap, VOL_SPLIT_PCTL * 100)
    ranks[k] = rk
    with np.errstate(invalid="ignore"):
        hv_flag[k] = np.isfinite(atr_pct_sig[k]) & (atr_pct_sig[k] >= thr)

_p0 = int(me_pos[sig_rows[0]])
print(f"\nRegime overlay ({'ON' if USE_OVERLAY else 'OFF'}): BEAR on {bear[_p0:].mean()*100:.1f}% of backtest days, "
      f"PANIC on {panic[_p0:].mean()*100:.1f}%")
print("Exits enabled:")
print(f"  ATR stop      {'ON ' if USE_ATR_STOP else 'OFF'}  " +
      (f"dynamic mult: high-vol x{ATR_MULT_HIGH_VOL}, low-vol x{ATR_MULT_LOW_VOL} (split at p{VOL_SPLIT_PCTL*100:.0f})"
       if ATR_DYNAMIC_MULT else f"fixed mult x{ATR_MULT}") + f", ATR({ATR_WINDOW})")
print(f"  Hard stop     {'ON ' if USE_HARD_STOP else 'OFF'}  {HARD_STOP_PCT*100:.0f}% below entry cost")
print(f"  Peak stop     {'ON ' if USE_PEAK_STOP else 'OFF'}  {PEAK_STOP_PCT*100:.0f}% below peak close")
print(f"  Vol-scaled    {'ON ' if USE_VOL_SCALED_STOP else 'OFF'}  width = clip({VOLSTOP_K} x ATR%, "
      f"{VOLSTOP_MIN_PCT*100:.0f}%, {VOLSTOP_MAX_PCT*100:.0f}%) below peak close")
print(f"  Rel-strength  {'ON ' if USE_RS_STOP else 'OFF'}  RS (stock/benchmark) {RS_STOP_PCT*100:.0f}% below its peak")
print(f"  Trend break   {'ON ' if USE_TREND_BREAK_STOP else 'OFF'}  {TREND_BREAK_DAYS} closes below SMA{TREND_SMA_WINDOW}")

open_np  = opens.to_numpy(dtype=np.float32) if has_open else prices.to_numpy(dtype=np.float32)
close_np = prices_sig.to_numpy(dtype=np.float32)
high_np  = highs.to_numpy(dtype=np.float32) if has_hl else close_np
low_np   = lows.to_numpy(dtype=np.float32) if has_hl else close_np
dates_np = index
rebal_map = {int(me_pos[k]) + 1: k for k in sig_rows if int(me_pos[k]) + 1 < n_bars}
t_first = min(rebal_map)
cash_daily = (1.0 + CASH_RATE_ANNUAL) ** (1.0 / 252.0) - 1.0


def allocate(raw, caps):
    """Equal-weight raw shares summing to <= 1 with per-name caps (excess left as idle cash, never levered)."""
    n = len(raw)
    w = np.zeros(n)
    free = np.ones(n, dtype=bool)
    remaining = 1.0
    while free.any() and remaining > 1e-12:
        alloc = np.where(free, raw, 0.0)
        alloc = remaining * alloc / alloc.sum()
        over = free & (alloc > caps + 1e-12)
        if not over.any():
            w[free] = alloc[free]
            break
        w[over] = caps[over]
        remaining -= caps[over].sum()
        free &= ~over
    return w


# ══════════════════════════════════════════════════════════════════════════════
# 4. DAILY EVENT LOOP
# ══════════════════════════════════════════════════════════════════════════════

def run_backtest(log_trades=False):
    N = TOP_N
    exit_rank = int(round(N * EXIT_RANK_MULT))
    entry_cap = min(MAX_WEIGHT, MAX_ENTRY_PCT)

    # ── per-position state (index = stock) ───────────────────────────────────
    shares = np.zeros(n_stk)
    cost_basis = np.zeros(n_stk)                     # entry open * (1 + cost)
    entry_px = np.zeros(n_stk)
    entry_bar = np.zeros(n_stk, dtype=np.int64)
    entry_w_int = np.zeros(n_stk); entry_pv = np.zeros(n_stk); entry_tier = np.ones(n_stk)
    entry_atr = np.full(n_stk, np.nan)
    is_hv = np.zeros(n_stk, dtype=bool)
    vs_width = np.full(n_stk, VOLSTOP_MIN_PCT)
    min_low = np.zeros(n_stk); max_high = np.zeros(n_stk)
    peak = np.zeros(n_stk); trail_stop = np.full(n_stk, -np.inf)
    rs_peak = np.zeros(n_stk); trend_cnt = np.zeros(n_stk, dtype=np.int64)
    last_exit_bar = np.full(n_stk, -10**9, dtype=np.int64)
    pending_stop = np.zeros(n_stk, dtype=bool)
    pending_reason = np.full(n_stk, "", dtype=object)
    pending_level = np.full(n_stk, np.nan); pending_pct = np.full(n_stk, np.nan)

    cash, traded = INITIAL_CAPITAL, 0.0
    eq = np.full(n_bars, np.nan); expo = np.zeros(n_bars); nheld = np.zeros(n_bars)
    trade_pnls = []                                  # NET P&L per closed trade
    trades = []
    exit_counts = {}
    n_entries = 0
    cols = prices.columns

    def close_positions(mask, t, px_exit, c_prev, reasons, levels=None, pcts=None):
        """Sell the masked positions IN FULL at px_exit (today's open)."""
        nonlocal cash, traded
        idxs = np.where(mask)[0]
        if idxs.size == 0:
            return
        sh, px = shares[idxs], px_exit[idxs]
        notion = float((sh * px).sum())
        cash += notion * (1 - COST_ONE_WAY); traded += notion
        net = sh * (px * (1 - COST_ONE_WAY) - cost_basis[idxs])
        trade_pnls.extend(net.tolist())
        for j, i in enumerate(idxs):
            rsn = reasons[i]
            exit_counts[rsn] = exit_counts.get(rsn, 0) + 1
            if log_trades:
                ep = entry_px[i]
                pos_size = sh[j] * ep
                trades.append(dict(
                    Ticker=cols[i], Entry_Date=dates_np[entry_bar[i]], Entry_Price=ep,
                    Exit_Date=dates_np[t], Exit_Price=px[j], Close_At_Exit=c_prev[i], Peak_Price=peak[i],
                    Stop_Price_At_Exit=(levels[i] if levels is not None else np.nan),
                    Stop_Pct=(pcts[i] if pcts is not None else np.nan),
                    ATR_At_Entry=entry_atr[i], Exit_Reason=rsn,
                    Intended_Weight=entry_w_int[i], Weight=pos_size / entry_pv[i],
                    Quantity=sh[j], Position_Size=pos_size, Portfolio_Value=entry_pv[i],
                    PnL_Pct=(px[j] / ep - 1) * 100, PnL_Abs=sh[j] * (px[j] - ep),
                    Net_PnL_Pct=(px[j] * (1 - COST_ONE_WAY) / cost_basis[i] - 1) * 100, Net_PnL_Abs=net[j],
                    Holding_Days=(dates_np[t] - dates_np[entry_bar[i]]).days,
                    MAE_Pct=(min_low[i] / ep - 1) * 100, MFE_Pct=(max_high[i] / ep - 1) * 100,
                    High_Vol=bool(is_hv[i]), Regime_Tier=entry_tier[i]))
        shares[idxs] = 0.0
        peak[idxs] = 0.0; trail_stop[idxs] = -np.inf; rs_peak[idxs] = 0.0; trend_cnt[idxs] = 0
        last_exit_bar[idxs] = t

    for t in range(t_first, n_bars):
        o = open_np[t].astype(float)
        c_prev = np.nan_to_num(close_np[t - 1].astype(float))
        held = shares > 0
        eq_open = cash + float((shares * c_prev)[held].sum())
        px_exit = np.where(np.isnan(o), c_prev, o)

        # (0) a stop flagged at yesterday's close -> exit in full at today's open
        if pending_stop.any():
            close_positions(pending_stop & held, t, px_exit, c_prev, pending_reason, pending_level, pending_pct)
            pending_stop[:] = False; pending_reason[:] = ""
            pending_level[:] = np.nan; pending_pct[:] = np.nan
            held = shares > 0

        tier_t = tier_arr[t] if USE_OVERLAY else 1.0

        # signal row today: full rebalance (rank exits + entries) or refill-only (entries only)
        if t in rebal_map:
            k = rebal_map[t]
            rk = ranks[k]
            ok_rk = ~np.isnan(rk)
            if ok_rk.any():
                if is_rebal[k]:
                    kept = held & ok_rk & (rk <= exit_rank)
                    if kept.sum() > N:
                        ids = np.where(kept)[0]
                        kept = np.zeros(n_stk, dtype=bool)
                        kept[ids[np.argsort(rk[ids])[:N]]] = True
                    drop = held & ~kept
                    if drop.any():
                        close_positions(drop, t, px_exit, c_prev, np.full(n_stk, "REBAL_EXIT", dtype=object))
                else:
                    kept = held.copy()                # refill-only row: never sell on rank
                slots = N - int(kept.sum())
                cand = (~held) & ok_rk & (rk <= N) & ~np.isnan(o) & (o > 0) & ((t - last_exit_bar) >= REFILL_COOLDOWN_DAYS)
                cand_ids = np.where(cand)[0]
                cids = cand_ids[np.argsort(rk[cand_ids])][:max(slots, 0)]

                if len(cids):
                    adv = med[k][cids]
                    caps = np.where(np.isnan(adv), entry_cap, np.minimum(entry_cap, ADV_CAP * adv / max(eq_open, 1.0)))
                    w_int = allocate(np.ones(len(cids)), caps)
                    w = w_int * (0.0 if (BEAR_NO_ENTRY and bear[t]) else tier_t)
                    need = np.zeros(n_stk); need[cids] = w * eq_open
                    w_int_full = np.zeros(n_stk); w_int_full[cids] = w_int
                    tot = float(need.sum())
                    scale = min(1.0, max(cash, 0.0) / (tot * (1 + COST_ONE_WAY))) if tot > 0 else 0.0
                    spend = need * scale
                    sh_buy = np.where(spend > 0, spend / np.where(o > 0, o, 1.0), 0.0)
                    bought = sh_buy > 0
                    cash -= float(spend.sum()) * (1 + COST_ONE_WAY); traded += float(spend.sum())
                    if bought.any():
                        b = np.where(bought)[0]
                        n_entries += int(b.size)
                        shares[b] += sh_buy[b]
                        cost_basis[b] = o[b] * (1 + COST_ONE_WAY)
                        entry_px[b] = o[b]; entry_bar[b] = t; entry_w_int[b] = w_int_full[b]
                        entry_pv[b] = eq_open; entry_tier[b] = tier_t
                        atr_e = atr_np[t - 1].astype(float)       # ATR at the signal bar
                        entry_atr[b] = atr_e[b]
                        is_hv[b] = hv_flag[k][b]
                        cp = c_prev[b]
                        ap = np.where(cp > 0, atr_e[b] / np.where(cp > 0, cp, 1.0), np.nan)
                        vs_width[b] = np.clip(np.nan_to_num(VOLSTOP_K * ap, nan=VOLSTOP_MIN_PCT),
                                              VOLSTOP_MIN_PCT, VOLSTOP_MAX_PCT)
                        peak[b] = o[b]; trail_stop[b] = -np.inf
                        rs_peak[b] = o[b] / bench_np[t - 1]; trend_cnt[b] = 0
                        min_low[b] = o[b]; max_high[b] = o[b]

        # end of day: carry cash, mark to close, update excursions, ratchet stops, flag any that trip
        cash *= (1.0 + cash_daily)
        c = close_np[t].astype(float)
        held = shares > 0
        pos = np.where(held, shares * np.nan_to_num(c), 0.0)
        eq[t] = cash + float(pos.sum())
        expo[t] = pos.sum() / eq[t] if eq[t] > 0 else 0.0
        nheld[t] = held.sum()

        if held.any():
            peak[held] = np.maximum(peak[held], c[held])
            min_low[held] = np.fmin(min_low[held], low_np[t].astype(float)[held])
            max_high[held] = np.fmax(max_high[held], high_np[t].astype(float)[held])

            claimed = np.zeros(n_stk, dtype=bool)   # first stop checked wins the logged reason

            def flag(hit, reason, level, pct):
                hit = hit & ~claimed
                if hit.any():
                    pending_reason[hit] = reason
                    pending_level[hit] = level[hit]
                    pending_pct[hit] = pct[hit] if isinstance(pct, np.ndarray) else pct
                    claimed[hit] = True

            if USE_ATR_STOP:
                atr_t = atr_np[t].astype(float)
                valid = held & np.isfinite(atr_t)
                mult = np.where(is_hv, ATR_MULT_HIGH_VOL, ATR_MULT_LOW_VOL) if ATR_DYNAMIC_MULT else ATR_MULT
                cand_stop = peak - mult * atr_t
                trail_stop[valid] = np.maximum(trail_stop[valid], cand_stop[valid])
                with np.errstate(invalid="ignore", divide="ignore"):
                    atr_pct_below = np.where(peak > 0, (peak - trail_stop) / peak * 100, np.nan)
                flag(valid & (c < trail_stop), "ATR_STOP", trail_stop, atr_pct_below)

            if USE_HARD_STOP:
                lvl = cost_basis * (1 - HARD_STOP_PCT)
                flag(held & (cost_basis > 0) & (c < lvl), "HARD_STOP", lvl, HARD_STOP_PCT * 100)

            if USE_PEAK_STOP:
                lvl = peak * (1 - PEAK_STOP_PCT)
                flag(held & (c < lvl), "PEAK_STOP", lvl, PEAK_STOP_PCT * 100)

            if USE_VOL_SCALED_STOP:
                lvl = peak * (1 - vs_width)
                flag(held & (c < lvl), "VOLSTOP", lvl, vs_width * 100)

            if USE_RS_STOP:
                rs_now = c / bench_np[t]
                rs_peak[held] = np.maximum(rs_peak[held], rs_now[held])
                rs_floor = rs_peak * (1 - RS_STOP_PCT)
                flag(held & (rs_now < rs_floor), "RS_STOP", rs_floor * bench_np[t], RS_STOP_PCT * 100)

            if USE_TREND_BREAK_STOP:
                sma_t = trend_sma_np[t].astype(float)
                below = held & np.isfinite(sma_t) & (c < sma_t * (1 - TREND_BREAK_BUFFER))
                trend_cnt[:] = np.where(below, trend_cnt + 1, 0)
                flag(held & (trend_cnt >= TREND_BREAK_DAYS), "TREND_BREAK", sma_t, np.nan)

            pending_stop |= claimed

    eq_s = pd.Series(eq, index=index).iloc[t_first:]

    held = shares > 0
    open_unreal = float((shares[held] * (close_np[-1].astype(float)[held] - cost_basis[held])).sum())

    pnl = np.array(trade_pnls)
    wins, losses = pnl[pnl > 0], pnl[pnl < 0]
    n_trades = len(pnl)
    win_rate = len(wins) / n_trades * 100 if n_trades else np.nan
    profit_factor = wins.sum() / abs(losses.sum()) if len(losses) and losses.sum() < 0 else np.nan
    avg_win = wins.mean() if len(wins) else np.nan
    avg_loss = abs(losses.mean()) if len(losses) else np.nan
    payoff_ratio = avg_win / avg_loss if avg_loss else np.nan

    return dict(eq=eq_s, expo=pd.Series(expo, index=index).iloc[t_first:], nheld=pd.Series(nheld, index=index).iloc[t_first:],
                traded=traded, exit_counts=exit_counts, n_entries=n_entries, trades=trades,
                open_n=int(held.sum()), open_unreal=open_unreal,
                n_trades=n_trades, win_rate=win_rate, profit_factor=profit_factor,
                avg_win=avg_win, avg_loss=avg_loss, payoff_ratio=payoff_ratio)


# ══════════════════════════════════════════════════════════════════════════════
# 5. METRICS + REPORT
# ══════════════════════════════════════════════════════════════════════════════

def metrics(eq_s, expo_s, nheld_s, traded):
    eq0 = pd.concat([pd.Series([INITIAL_CAPITAL], index=[eq_s.index[0] - pd.Timedelta(days=1)]), eq_s])
    r = eq0.pct_change().dropna()
    yrs = (eq_s.index[-1] - eq_s.index[0]).days / 365.25
    cagr = (eq_s.iloc[-1] / INITIAL_CAPITAL) ** (1 / yrs) - 1
    vol = r.std() * np.sqrt(252)
    dd = eq0 / eq0.cummax() - 1
    rf_d = (1 + CASH_RATE_ANNUAL) ** (1 / 252) - 1
    down = np.sqrt((np.minimum(r - rf_d, 0.0) ** 2).mean()) * np.sqrt(252)      # true downside deviation
    mret = eq_s.resample("ME").last().pct_change().dropna()
    avg_eq = eq_s.mean()
    return dict(CAGR=cagr * 100, Vol=vol * 100, Sharpe0=r.mean() / r.std() * np.sqrt(252),
                SharpeEx=(r.mean() - rf_d) / r.std() * np.sqrt(252),
                Sortino=((r.mean() - rf_d) * 252) / down if down > 0 else np.nan,
                MaxDD=dd.min() * 100, Calmar=cagr / abs(dd.min()) if dd.min() < 0 else np.nan,
                WinMo=(mret > 0).mean() * 100, AvgHold=nheld_s.mean(), AvgExpo=expo_s.mean() * 100,
                Turnover=traded / 2 / avg_eq / yrs * 100,                       # one-way
                CostDrag=traded * COST_ONE_WAY / avg_eq / yrs * 100)            # % of avg equity per year


def year_returns(eq_s):
    ye = eq_s.resample("YE").last()
    prev = pd.concat([pd.Series([INITIAL_CAPITAL]), ye.iloc[:-1]]).to_numpy()
    return pd.Series(ye.to_numpy() / prev - 1, index=ye.index.year) * 100


def year_drawdowns(eq_s):
    eq0 = pd.concat([pd.Series([INITIAL_CAPITAL], index=[eq_s.index[0] - pd.Timedelta(days=1)]), eq_s])
    dd = (eq0 / eq0.cummax() - 1).iloc[1:]
    return dd.groupby(dd.index.year).min() * 100


def trade_diagnostics(tr):
    """Exit-reason and holding-period breakdown on NET trade P&L."""
    if tr.empty:
        return None, None
    tr = tr.copy()
    tr["win"] = tr.Net_PnL_Abs > 0
    by_reason = tr.groupby("Exit_Reason").agg(
        N=("win", "size"), Win_Pct=("win", lambda x: x.mean() * 100), AvgRet_Pct=("Net_PnL_Pct", "mean"),
        MedRet_Pct=("Net_PnL_Pct", "median"), MedDays=("Holding_Days", "median"),
        MAE_Pct=("MAE_Pct", "median"), MFE_Pct=("MFE_Pct", "median"), NetPnL=("Net_PnL_Abs", "sum"))
    bins = pd.cut(tr.Holding_Days, [-1, 30, 60, 120, 100000], labels=["<=30d", "31-60d", "61-120d", ">120d"])
    by_hold = tr.groupby(bins, observed=True).agg(
        N=("win", "size"), Win_Pct=("win", lambda x: x.mean() * 100), AvgRet_Pct=("Net_PnL_Pct", "mean"),
        NetPnL=("Net_PnL_Abs", "sum"))
    return by_reason, by_hold


# ══════════════════════════════════════════════════════════════════════════════
# 6. SIGNAL DIAGNOSTICS: RANK-IC / ICIR vs FORWARD RETURNS, PER HORIZON
# ══════════════════════════════════════════════════════════════════════════════

def _nw_tstat(x, lags):
    """t-stat of the mean with a Newey-West (Bartlett) long-run variance."""
    x = np.asarray(x, dtype=float); n = len(x)
    if n < 3:
        return np.nan
    xc = x - x.mean()
    s = xc @ xc / n
    for l in range(1, min(lags, n - 1) + 1):
        s += 2 * (1 - l / (lags + 1)) * (xc[l:] @ xc[:-l] / n)
    return x.mean() / np.sqrt(s / n) if s > 0 else np.nan


def compute_icir(horizons):
    """Spearman rank-IC of the composite score vs forward h-day return at every FULL rebalance row
    (universe-filtered pool, gross of cost). Forward return runs signal-bar close -> close; observations
    spaced REBALANCE_FREQ_DAYS apart overlap when h > REBALANCE_FREQ_DAYS, hence the HAC t-stat."""
    close_sig = prices_sig.to_numpy(dtype=float)
    rows = []
    for h in horizons:
        ics = []
        for k in full_rebal_rows:
            p = me_pos[k]
            if p + h >= n_bars:
                continue
            pool = pools[k]
            if pool.sum() < MIN_POOL_SIZE:
                continue
            idx = np.where(pool)[0]
            s = scores[k][idx]
            c0 = close_sig[p, idx]
            c1 = close_sig[p + h, idx]
            valid = np.isfinite(s) & np.isfinite(c0) & np.isfinite(c1) & (c0 > 0)
            if valid.sum() < MIN_POOL_SIZE:
                continue
            fwd = c1[valid] / c0[valid] - 1.0
            ic = pd.Series(s[valid]).corr(pd.Series(fwd), method="spearman")
            if pd.notna(ic):
                ics.append(ic)
        ics = np.array(ics)
        n_obs = len(ics)
        if n_obs >= 2 and ics.std(ddof=1) > 0:
            ic_mean, ic_std = ics.mean(), ics.std(ddof=1)
            icir = ic_mean / ic_std
            lags = max(int(np.ceil(h / REBALANCE_FREQ_DAYS)) - 1, 0)
            rows.append(dict(Horizon=h, N=n_obs, MeanIC=ic_mean, StdIC=ic_std, ICIR=icir,
                             tStat_naive=icir * np.sqrt(n_obs), tStat_HAC=_nw_tstat(ics, lags),
                             PctPos=(ics > 0).mean() * 100))
        else:
            rows.append(dict(Horizon=h, N=n_obs, MeanIC=np.nan, StdIC=np.nan, ICIR=np.nan,
                             tStat_naive=np.nan, tStat_HAC=np.nan, PctPos=np.nan))
    return pd.DataFrame(rows).set_index("Horizon")


if SAVE_OUTPUTS:
    os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"\nRunning {STRATEGY_NAME}  (TOP_N={TOP_N}, rebalance every {REBALANCE_FREQ_DAYS}d, "
      f"refill={'every ' + str(REFILL_FREQ_DAYS) + 'd' if USE_SLOT_REFILL else 'OFF'}, "
      f"overlay={'ON' if USE_OVERLAY else 'OFF'}, offset={SCHEDULE_OFFSET_DAYS}) ...")
res = run_backtest(log_trades=True)
res["m"] = metrics(res["eq"], res["expo"], res["nheld"], res["traded"])
res["yr"] = year_returns(res["eq"])
res["yr_dd"] = year_drawdowns(res["eq"])
trades_df = pd.DataFrame(res["trades"])

W = 60
m = res["m"]
print("\n" + "=" * W)
print(f" {STRATEGY_NAME} BACKTEST")
print(f" {dates_np[t_first].date()} -> {dates_np[-1].date()}")
print(f" cost {COST_ONE_WAY*100:.1f}% one-way   cash {CASH_RATE_ANNUAL*100:.1f}%   capital {INITIAL_CAPITAL:,.0f}")
print("=" * W)
ec = res["exit_counts"]
rows = [
    ("CAGR %",              f"{m['CAGR']:.1f}"),
    ("Volatility %",        f"{m['Vol']:.1f}"),
    ("Sharpe (rf=0)",       f"{m['Sharpe0']:.2f}"),
    ("Sharpe (rf=cash)",    f"{m['SharpeEx']:.2f}"),
    ("Sortino",             f"{m['Sortino']:.2f}"),
    ("Max Drawdown %",      f"{m['MaxDD']:.1f}"),
    ("Calmar",              f"{m['Calmar']:.2f}"),
    ("Winning Months %",    f"{m['WinMo']:.1f}"),
    ("Avg Holdings",        f"{m['AvgHold']:.1f}"),
    ("Avg Exposure %",      f"{m['AvgExpo']:.0f}"),
    ("Turnover %/yr (1-way)", f"{m['Turnover']:.0f}"),
    ("Est. Cost Drag %/yr", f"{m['CostDrag']:.2f}"),
    ("Entries",             f"{res['n_entries']}"),
]
for rsn in ["REBAL_EXIT", "ATR_STOP", "HARD_STOP", "PEAK_STOP", "VOLSTOP", "RS_STOP", "TREND_BREAK"]:
    rows.append((f"Exits: {rsn}", f"{ec.get(rsn, 0)}"))
rows += [
    ("Open at end (n / unreal.)", f"{res['open_n']} / {res['open_unreal']:,.0f}"),
    ("Closed Trades",       f"{res['n_trades']}"),
    ("Trade Win Rate % (net)", f"{res['win_rate']:.1f}" if pd.notna(res['win_rate']) else "n/a"),
    ("Profit Factor (net)", f"{res['profit_factor']:.2f}" if pd.notna(res['profit_factor']) else "n/a"),
    ("Avg Win (net)",       f"{res['avg_win']:,.0f}" if pd.notna(res['avg_win']) else "n/a"),
    ("Avg Loss (net)",      f"{res['avg_loss']:,.0f}" if pd.notna(res['avg_loss']) else "n/a"),
    ("Payoff Ratio",        f"{res['payoff_ratio']:.2f}" if pd.notna(res['payoff_ratio']) else "n/a"),
]
label_w = max(len(r[0]) for r in rows) + 2
for label, val in rows:
    print(f" {label:<{label_w}}{val:>15}")

print("\n" + "=" * W)
print(" CALENDAR-YEAR RETURN % / MAX DRAWDOWN %")
print("=" * W)
yr_tab = pd.DataFrame({"Return%": res["yr"], "MaxDD%": res["yr_dd"]})
print(yr_tab.round(1).to_string())

by_reason, by_hold = trade_diagnostics(trades_df)
if by_reason is not None:
    print("\n" + "=" * W)
    print(" TRADE DIAGNOSTICS (net of cost)  --  by exit reason")
    print("=" * W)
    print(by_reason.round(1).to_string())
    print("\n by holding period")
    print(by_hold.round(1).to_string())

print("\n" + "=" * W)
print(" ENTRY-SIGNAL RANK-IC / ICIR vs FORWARD RETURNS (gross, universe-filtered pool)")
print("=" * W)
icir_tab = compute_icir(IC_HORIZONS)
print(icir_tab.round(3).to_string())

if SAVE_OUTPUTS:
    res["eq"].rename(STRATEGY_NAME).to_csv(os.path.join(OUTPUT_DIR, "equity_curves.csv"))
    trades_df.to_csv(os.path.join(OUTPUT_DIR, "trade_log_full.csv"), index=False)
    yr_tab.to_csv(os.path.join(OUTPUT_DIR, "yearly_returns.csv"))
    icir_tab.to_csv(os.path.join(OUTPUT_DIR, "icir_report.csv"))
    if by_reason is not None:
        by_reason.to_csv(os.path.join(OUTPUT_DIR, "exit_reason_summary.csv"))
    _json.dump(dict(m=m, exits=ec, n_trades=res["n_trades"], entries=res["n_entries"], win=res["win_rate"],
                    pf=res["profit_factor"], ic=icir_tab.reset_index().to_dict("records")),
               open(os.path.join(OUTPUT_DIR, "summary.json"), "w"), default=float)
    print(f"\n[Saved] equity_curves.csv, trade_log_full.csv, yearly_returns.csv, icir_report.csv, "
          f"exit_reason_summary.csv -> {os.path.abspath(OUTPUT_DIR)}")