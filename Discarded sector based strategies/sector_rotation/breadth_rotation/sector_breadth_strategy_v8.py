"""
sector_breadth_strategy_v8.py
================================
FINAL validated configuration -- the strategy is Sector_clean breadth-
divergence rotation (v1's hypothesis, unchanged); everything below is the
risk-management + selection-quality chassis built on top of it across
v1->v8, each change kept only because it earned its place on a real
backtest, not by default.

v8 = a comprehensive leave-one-out ablation of EVERY toggleable component
against the v7 baseline (ablation_v7_full.py), run because the v7 stock-
factor change could have shifted which components still earn their place
(interaction effects a piecemeal, build-order ablation can't see). Result:
almost everything held up unchanged -- StopCooldown, StockRankDecline,
Chandelier, VolAwareStockFactor all still clearly net-positive; MinHold
still correctly OFF; CorrGuard/SwapGap/StopLoss/FallingKnife are all now
confirmed no-ops (FallingKnife newly so -- the vol-aware factor's low-vol
tilt already catches most of what it used to) but kept anyway at zero cost
as OOS/live safety nets. ONE thing needed re-tuning:

  VOL_TARGET retuned 0.20 -> 0.30 (retune_sizing_voltarget.py): the v7
  factor already smoothed the return stream, so 0.20 (tuned pre-v7) started
  binding uselessly. Calmar rose MONOTONICALLY as this loosened (0.15->off:
  0.706->0.827), a smooth plateau from 0.25+, not a spike. Jointly
  re-verified InverseVolSizing is still net-positive once compared at each
  scheme's own best VolTarget (0.827 vs 0.814 best-case) -- the earlier
  single-point ablation cell had made it look neutral only because it was
  tested at the now-stale VolTarget=0.20.

  v7 -> v8 (IS 2003-2012): CAGR 16.14%->16.97%, Sharpe 1.291->1.321,
  Calmar 0.786->0.824, MaxDD -20.52%->-20.59% (essentially unchanged).

TWO remaining ablation findings are genuine judgment calls, not resolved
here -- both trade CAGR for Calmar in the direction v8 already keeps:
  - CrashGuard OFF: CAGR 17.94% (better) but Calmar 0.763 (worse) and
    MaxDD -23.51% (worse) vs v8's 0.824/-20.59%. Kept ON -- this IS window
    only contains one real tail event (2008); a systemic-panic exit exists
    precisely for tail scenarios a single historical sample under-
    represents, not to be judged on THIS window's CAGR trade-off alone.
  - SectorRankDecline OFF: CAGR 17.10% (better) but Calmar lower and MaxDD
    worse. Kept ON for a second reason beyond the numbers: exiting when a
    sector rotates out of favor is the direct mechanical expression of the
    strategy's own core thesis (sector breadth-divergence). Turning it off
    to chase backtest CAGR would mean the strategy stops acting on the
    thing it exists to trade.

Structural parameter sweep (N_SECTORS, STOCKS_PER_SECTOR, REBALANCE_EVERY,
STOP_LOSS_PCT, ATR_MULTIPLIER, MAX_WEIGHT_PER_STOCK, TREND_PERSIST_WIN) is
the next step, not yet run as of v8.

Original v7 docstring (stock-factor redesign, still applies as history):
-----------------------------------------------------------------------
v7 is the FIRST change all session to genuinely move Calmar rather than
trade one metric for another -- every prior version (v3-v6) improved
MaxDD at a roughly proportional cost to CAGR/Sharpe, netting out flat on
Calmar (0.517->0.630->0.631->0.688->0.687 across v1/v3/v4/v5/v6). That
plateau was diagnosed as a structural ceiling on the RISK-OVERLAY layer:
overlays can only trim tails on a GIVEN return stream, they can't make the
underlying trade-selection process itself smoother. v7 goes upstream:

  §9 Vol-aware stock-quality composite -- the stock-level factor
     (trend persistence: % of trailing 126d above SMA200) measured pure
     DIRECTIONAL consistency with zero regard for how choppy the ride was.
     Sector-selection layer (breadth-divergence, the actual differentiated
     hypothesis) is COMPLETELY UNTOUCHED -- this only changes which 2
     stocks get picked within an already sector-selected, already
     trend_ok-gated pool. New composite = same equal-weight percentile-
     blend pattern as the sector-level breadth composite:
       stock_quality = W*rank(persistence) + (1-W)*rank(-realized_63d_vol)
     NOT price-return momentum (unlike CSM's own Sharpe-style stock
     factor) -- still rewards consistency of trend, just also penalizes
     chop along the way, closing the "no vol-awareness in stock selection"
     gap diagnosed after the risk-overlay layer plateaued.

     STOCK_QUALITY_WEIGHT tuned via tune_stock_quality_weight.py:
       - Naive 50/50 blend: Calmar WORSE (0.687->0.594) -- too heavy a
         tilt overrides genuinely good persistence scores for low vol
         alone, pulling in stocks that are low-vol because they're weak
         compounders, not smooth ones.
       - 0.95 is the Calmar-maximizing point (0.687->0.786, +14%), and
         MaxDD-best (-23.30%->-20.52%) -- verified this sits in a genuine
         PLATEAU (weight 0.91-0.99 all >= baseline Calmar), not a fragile
         spike: 0.94 and 0.95 land on the IDENTICAL MaxDD (-20.52%), the
         same drawdown episode avoided at both, a structural signature not
         sampling noise. Only <=0.90 falls back toward/below baseline.

  v6 -> v7 (IS 2003-2012): CAGR 16.01%->16.14%, Sharpe 1.185->1.291,
  Sortino 1.003->1.057, Calmar 0.687->0.786, MaxDD -23.30%->-20.52%.

Everything below this point (v1-v6 history) is the prior lineage, still
accurate for the risk-management chassis -- only the stock-selection
factor changed in v7.

v6's own docstring (risk-management chassis, still applies as-is):
-----------------------------------------------------------------------
v6 closes the last two items found on a granular re-read of CSM Quad's
actual code (the earlier v4 audit was a high-level table, not exhaustive):
  §6 Chandelier floor -- v5's ATR stop was recomputed fresh from
     peak/ATR every day, never persisted/ratcheted. A same-day ATR spike
     could make the effective stop RETREAT even though peak never fell --
     the opposite of what a trailing stop should do. Fixed: h["atr_stop"]
     now persists and only ratchets up, clamped to [3%,30%] of peak (CSM
     Quad's np.clip(chand_raw, peak*0.70, peak*0.97)). Ablation: small
     genuine improvement (Sharpe 1.168->1.185, Calmar essentially
     unchanged 0.688->0.687) -- kept.
  §7 Swap-gap displacement (CSM Quad's use_swap_gap) -- a new candidate
     ranking >=SWAP_GAP_RANKS(10) places better than the worst-ranked HELD
     name in the SAME sector can evict it, even when that sector's slots
     are full. Ablation: a COMPLETE NO-OP here (identical to not having it
     on every metric) -- the existing STOCK_RANK_DECLINE hysteresis band
     (STOCKS_PER_SECTOR_EXIT=4, wider than the entry band) already evicts
     weak holdings before a candidate could ever clear the stricter 10-rank
     bar. Kept anyway at zero measured cost, same reasoning as Corr Guard:
     a safety net for OOS/live periods where it might actually bind.

Both toggleable (use_chandelier_floor, use_swap_gap), same convention as
every other flag in this file.

HYPOTHESIS (unchanged since v1, validated in sector_breadth_ic_test.py):
sector-level PARTICIPATION/BREADTH (% of constituents confirming the
trend) carries real predictive information beyond price-return momentum.
Sectors are ranked by a breadth composite ORTHOGONALIZED against the
colleague's momentum+dispersion factor via a frozen pooled-OLS residual
(BETA_MOM_DISP=0.531, never re-fit here). Stocks are ranked within top
sectors by TREND PERSISTENCE (% of trailing 126d spent above SMA200), not
price-return momentum either -- deliberately orthogonal to both the
colleague's and CSM's stock-level factors, since the whole point of this
strategy existing is to NOT take correlated trades with either.

LINEAGE, each version's IS 2003-2012 numbers (CAGR / Sharpe / Calmar / MaxDD):
  v1  25.43% / 1.419 / 0.517 / -49.16%   flat equal-weight, weekly rebal,
                                          entry-only regime gate (no crash
                                          exit) -- the raw, unmanaged signal
  v2  (Industry_clean stock-filter tried on top of v1 -- wash, dropped)
  v3  17.05% / 1.270 / 0.630 / -27.05%   +monthly rebal, +regime leverage
                                          (bull 1.0/bear 0.8/panic 0.5),
                                          +Crash Guard (exit-all on bench-vol
                                          spike, ported from CSM Quad)
  v4  14.37% / 1.118 / 0.631 / -22.78%   +min-hold, +stop cooldown,
                                          +inverse-vol sizing, +Corr Guard,
                                          +Vol Target=0.15 (all 4 CSM-audit
                                          gaps closed at once)
  v5  15.94% / 1.168 / 0.688 / -23.17%   ABLATED v4 (see below) -- dropped
                                          min-hold (net-negative on both
                                          Calmar AND MaxDD), retuned
                                          Vol Target 0.15->0.20 (Calmar-
                                          maximizing point, flat plateau
                                          0.665-0.675 across 0.18-0.30, not
                                          a fragile spike), added the
                                          falling-knife gate (last item from
                                          the CSM audit table, small genuine
                                          Calmar/MaxDD gain in its own A/B)
  v6  16.01% / 1.185 / 0.687 / -23.30%   +chandelier floor (ATR stop now
                                          ratchets + clamped [3%,30%] of
                                          peak -- fixes a real bug: v5's
                                          stop could retreat on an ATR
                                          spike), +swap-gap displacement
                                          (proven no-op here, kept at zero
                                          cost -- see below)
  v7  16.14% / 1.291 / 0.786 / -20.52%   +vol-aware stock-quality composite
                                          (see §9 above) -- FIRST version to
                                          genuinely move Calmar rather than
                                          trade one metric for another; the
                                          upstream fix after the risk-overlay
                                          layer (v3-v6) plateaued at ~0.69

ABLATION FINDINGS that shaped v5 (ablation_v4_components.py,
tune_vol_target.py, test_falling_knife.py -- all reproducible, all IS-only):
  - MinHold DROPPED: alone, worsened Calmar (0.630->0.618) AND MaxDD
    (-27.05%->-27.96%) for a marginal +0.21pp CAGR. Not worth it against
    "MaxDD as low as possible."
  - StopCooldown KEPT: alone, clear net-positive (Calmar 0.630->0.660,
    MaxDD -27.05%->-25.35%, small CAGR cost).
  - InverseVolSizing KEPT: alone, net-positive on Calmar/MaxDD, at the cost
    of higher turnover and slightly worse Sharpe/Sortino (churn from
    reweighting the whole book every rebalance) -- accepted as a fair trade.
  - CorrGuard KEPT but is a COMPLETE NO-OP at threshold=0.8 in this sample
    (identical metrics to not having it at all -- an 8-position/4-sector
    book apparently never crosses portfolio-vol/avg-stock-vol > 0.8 here).
    Left in at zero cost for robustness against OOS/live periods where
    correlation genuinely spikes; not tuned further since it has nothing
    to tune against in-sample.
  - VolTarget KEPT, RETUNED 0.15->0.20: at 0.15 this was the single
    biggest drag in the whole v4 bundle (-3.1pp CAGR, Calmar WORSE than
    not having it at all, -27.05%: it was chronically clipping upside
    during genuinely productive high-vol periods like 2007, not just
    reacting to real tail risk). 0.20 is the Calmar-maximizing point on a
    flat plateau, not a fragile pick.
  - Falling-knife gate ADDED (prices.pct_change(21).shift(1) >= -15%,
    daily-resolution equivalent of CSM's monthly filter_universe gate):
    small but real Calmar/MaxDD improvement in isolation (0.675->0.688,
    -23.82%->-23.17%) for a small CAGR cost. Applied at STOCK-SELECTION
    time only (rank_sector_stocks, entries only -- not folded into
    universe_mask, which already feeds the IC-validated sector-level
    breadth factor and shouldn't be silently redefined).

All use_* flags below default to v6's validated configuration but remain
toggleable -- same convention CSM's own files use (documented flags with
sensible defaults, not stripped out once validated), so this file still
supports future ablation without a fork.

Scope discipline (still applies): this is IS-only (2003-2012), tuned by
looking at IS performance repeatedly -- exactly what makes it IS tuning,
not a live-readiness claim. STRATEGY_VALIDATION_PLAYBOOK.md's 8 stages
(OOS validation, exit-quality diagnostics, paper trading, etc.) are the
gate that comes AFTER this, not yet run.
"""

import os
import glob
import warnings

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

DATA_FOLDER     = "/Users/hemantsoni/Documents/upstox_data_folder/ohlcv_data"
INSTRUMENTS_CSV = os.path.join(REPO_ROOT, "instruments_clean.csv")
SYMBOL_COL      = "trading_symbol"
SECTOR_COL      = "Sector_clean"
OUT_DIR         = os.path.dirname(__file__)
STARTING_CAPITAL = 1_000_000.0   # Rs 10,00,000 -- only used to report a rupee equity curve
                                   # / rupee P&L per trade; every ratio metric is capital-independent

BACKTEST_START = pd.Timestamp("2003-01-01")
BACKTEST_END   = pd.Timestamp("2012-12-31")


# ══════════════════════════════════════════════════════════════════════════
# DATA LOADER  (self-contained -- no cross-file dependency on HR_breakout)
# ══════════════════════════════════════════════════════════════════════════

def load_data(folder_path):
    """Load all CSV files from folder_path.
    Returns: prices_df, volumes_df, highs_df, lows_df, opens_df (all DataFrames).
    Entries/exits fill at next-day open; falls back to prev-close if open missing.
    """
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

            if 'close' in df.columns:
                price_list.append(_clean(df['close'].rename(symbol)))
            else:
                print(f"Warning: 'close' missing in {filename}")

            if 'volume' in df.columns:
                volume_list.append(_clean(df['volume'].rename(symbol)))
            if 'high' in df.columns:
                high_list.append(_clean(df['high'].rename(symbol)))
            if 'low' in df.columns:
                low_list.append(_clean(df['low'].rename(symbol)))
            if 'open' in df.columns:
                open_list.append(_clean(df['open'].rename(symbol)))

        except Exception as e:
            print(f"Error loading {filename}: {e}")

    if not price_list:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    def _build(lst):
        if not lst:
            return pd.DataFrame()
        df = pd.concat(lst, axis=1)
        df.sort_index(inplace=True)
        return df

    prices_df  = _build(price_list)
    volumes_df = _build(volume_list)
    highs_df   = _build(high_list)
    lows_df    = _build(low_list)
    opens_df   = _build(open_list)

    print(f"Loaded  Prices:{prices_df.shape}  Volumes:{volumes_df.shape}  "
          f"Highs:{highs_df.shape}  Lows:{lows_df.shape}  Opens:{opens_df.shape}")
    if opens_df.empty:
        print("  Warning: No 'open' column found in CSV files. "
              "Entry/exit fills will fall back to close prices.")
    return prices_df, volumes_df, highs_df, lows_df, opens_df

# ══════════════════════════════════════════════════════════════════════════
# CONFIG
# ══════════════════════════════════════════════════════════════════════════

MIN_STOCKS_SECTOR = 8
UNIVERSE_TOP_N     = 1000
MIN_PRICE          = 10.0
MAX_CIRCUIT_DAYS   = 5
CA_DROP_THRESH     = 0.40
CA_GAIN_THRESH     = 3.00

# Sector ranking (breadth-divergence)
SMA_SLOW_WIN       = 200
HI_LO_WIN          = 252
HI_LO_MIN_PERIODS  = 200
NET_HI_LO_SMOOTH   = 21
SECTOR_MOM_PERIOD  = 126
DISPERSION_WINDOW  = 21
BETA_MOM_DISP      = 0.531     # FROZEN -- see module docstring, do not re-fit

N_SECTORS          = 4
N_SECTORS_EXIT     = 5

# Stock selection (trend persistence)
SMA_FAST           = 50
TREND_PERSIST_WIN  = 126
STOCKS_PER_SECTOR      = 2
STOCKS_PER_SECTOR_EXIT = 4
MAX_POSITIONS      = N_SECTORS * STOCKS_PER_SECTOR

# §9: vol-aware stock quality composite -- persistence alone measures
# DIRECTIONAL consistency (% of days above SMA200) with no regard for how
# choppy the ride was. Blends in an explicit low-volatility tilt, same
# equal-weight percentile-blend pattern already used for the sector-level
# breadth composite (0.5*rank(B1) + 0.5*rank(B2)). Sector-selection layer
# (breadth-divergence) is untouched -- this only changes which 2 stocks
# get picked WITHIN an already sector-selected, already trend_ok-gated pool.
STOCK_VOL_WIN        = 63    # trailing realized-vol window, ~3 months
STOCK_QUALITY_WEIGHT = 0.95  # weight on persistence; (1-this)=0.05 on low-vol tilt.
                               # TUNED via tune_stock_quality_weight.py: 0.5 (naive
                               # 50/50) made Calmar WORSE (0.687->0.594) -- too heavy
                               # a tilt overrides genuinely good persistence scores for
                               # low vol alone. 0.95 sits in the middle of a genuine
                               # plateau (0.91-0.99 all >= baseline Calmar), not a
                               # fragile spike -- 0.94/0.95 land on the IDENTICAL MaxDD
                               # (-20.52%), the same drawdown episode avoided at both.

# Swap-gap displacement (CSM Quad's use_swap_gap): a much-better-ranked new
# candidate can evict the worst-ranked HELD name in the SAME sector even
# when that sector's STOCKS_PER_SECTOR slots are already full -- CSM Quad's
# value, ported as-is (not rescaled), since it operates on the same kind of
# discrete rank-position gap within a candidate pool as CSM's flat ranking.
SWAP_GAP_RANKS = 10

# Regime
BENCH_SMA_PERIOD   = 50
BENCH_STREAK_MAX   = 5
BENCH_SMA200_PERIOD  = 200      # bull/bear regime for leverage (CSM Quad convention)
BENCH_VOL_WIN        = 21       # daily benchmark-return vol window
PANIC_MIN_PERIODS    = 126      # warmup before the expanding panic-threshold quantile is trusted
CRASH_GUARD_COOLDOWN = 10       # trading days blocking new entries after a crash-guard exit
LEVERAGE_BULL        = 1.0      # benchmark > its own SMA200
LEVERAGE_BEAR        = 0.8      # benchmark < its own SMA200
LEVERAGE_PANIC       = 0.5      # benchmark vol > its own expanding 95th-pct threshold;
                                  # overrides bull/bear via min(), never loosens a panic cut

# Sizing / rebalance
REBALANCE_EVERY    = 20        # trading days (~monthly, was 5/weekly in v1). This IS the exit-
                                # signal cadence, not just a sizing/entry knob -- SECTOR_RANK_DECLINE
                                # and STOCK_RANK_DECLINE are only re-checked on rebalance days, the
                                # same way CSM Quad's monthly rank recompute doubles as its REBALANCE
                                # exit signal (a name silently dropping out of the ranked list IS the
                                # exit trigger there). Difference from CSM: this counts fixed trading
                                # days from backtest start rather than true calendar month-end
                                # (.resample('ME')), so it drifts slightly from calendar boundaries
                                # over 10 years -- a simpler, same-family convention as HR/colleague's
                                # v6 (both use a trading-day counter too), not a bug, but flagged since
                                # it's a real difference from CSM's exact mechanism.

# Stops
ATR_PERIOD         = 14
ATR_MULTIPLIER     = 2.5
STOP_LOSS_PCT      = 0.15

# Min-hold grace period (CSM Quad default: 5 TRADING days -- counted via loop
# index, not calendar days, matching CSM's V1 trading-days fix)
MIN_HOLD_DAYS      = 5

# Per-ticker stop cooldown -- loss-scaled, same formula/defaults as CSM Quad's
# cooldown_mode='loss_scaled': a profitable stop (trend simply ended) gets NO
# cooldown; a bigger loss gets a longer re-entry ban, clipped to [floor, cap].
STOP_COOLDOWN_BASE_DAYS = 20
COOLDOWN_FLOOR_DAYS     = 10
COOLDOWN_CAP_DAYS       = 60

# Portfolio management: inverse-vol sizing (CSM Batch/Quad convention) instead
# of flat equal-weight. Recomputed for the WHOLE active book at every
# rebalance (not just new entries), 2-pass clip+renormalize at the cap.
SIZING_VOL_WIN         = 21
MAX_WEIGHT_PER_STOCK   = 0.20   # vs CSM's 0.05 -- that's calibrated for a 15-30
                                  # name book; ours holds ~8, so equal-weight alone
                                  # is already 12.5%, a 5% cap would be meaningless

# Risk overlays: Corr Guard + Vol Targeting (CSM Batch's apply_risk_overlays),
# applied DAILY on top of the base (vol-sized) weights, using UNSCALED gross
# portfolio-return history (not the already-scaled realized returns).
CORR_GUARD_WIN       = 21
CORR_GUARD_THRESHOLD = 0.8      # a no-op in this IS sample -- kept for OOS/live robustness, see docstring
VOL_TARGET_WIN        = 63
VOL_TARGET            = 0.30    # RE-RETUNED for v8: the v7 vol-aware stock factor already made
                                  # the return stream smoother, so 0.20 (tuned pre-v7) started
                                  # binding uselessly -- ablation showed Calmar rising MONOTONICALLY
                                  # as this loosens (0.15->off), plateauing smoothly from 0.25+, not
                                  # a spike. 0.30 is ~equal to fully-off (Calmar 0.824 vs 0.827) --
                                  # kept as a practical no-op / tail-safety-net, not literally
                                  # disabled, same reasoning as Corr Guard/StopLoss. See
                                  # retune_sizing_voltarget.py.

# Falling-knife gate (last item from the CSM audit table) -- daily-resolution
# equivalent of CSM's monthly filter_universe gate (prior return >= -15%).
# Applied at stock-SELECTION time (rank_sector_stocks), not folded into
# universe_mask -- see docstring for why.
FALLING_KNIFE_WINDOW = 21
FALLING_KNIFE_FLOOR  = -0.15

WARMUP_DAYS        = 280       # covers 252d hi/lo + 21d thrust smoothing


# ══════════════════════════════════════════════════════════════════════════
# UNIVERSE / SECTOR CONSTRUCTION  (proven plumbing, reused as-is)
# ══════════════════════════════════════════════════════════════════════════

def build_sector_membership(prices, instruments_csv, min_stocks=MIN_STOCKS_SECTOR):
    inst = pd.read_csv(instruments_csv).dropna(subset=[SYMBOL_COL, SECTOR_COL])
    ticker_sector = dict(zip(inst[SYMBOL_COL], inst[SECTOR_COL]))
    members = {}
    for ticker, sector in ticker_sector.items():
        if ticker in prices.columns:
            members.setdefault(sector, []).append(ticker)
    members = {s: m for s, m in members.items() if len(m) >= min_stocks}
    print(f"[sector_breadth_v8] {len(members)} sectors qualify: {sorted(members.keys())}")
    return members


def build_universe_mask(prices, volumes, highs, lows):
    prev_close = prices.shift(1)
    price_ok = prev_close >= MIN_PRICE
    dvol = (prices * volumes).rolling(63, min_periods=21).mean().shift(1)
    dvol_rank = dvol.rank(axis=1, ascending=False, method="min")
    dvol_ok = dvol_rank <= UNIVERSE_TOP_N
    if not highs.empty and not lows.empty:
        circuit_count = (highs == lows).rolling(63, min_periods=1).sum().shift(1)
        circuit_ok = circuit_count <= MAX_CIRCUIT_DAYS
    else:
        circuit_ok = pd.DataFrame(True, index=prices.index, columns=prices.columns)
    return (price_ok & dvol_ok & circuit_ok).fillna(False)


def build_sector_index(prices, members):
    daily_ret = prices.pct_change(fill_method=None)
    bad_tick = (daily_ret < -CA_DROP_THRESH) | (daily_ret > CA_GAIN_THRESH)
    daily_ret = daily_ret.where(~bad_tick)
    sector_ret = pd.DataFrame({s: daily_ret[m].mean(axis=1, skipna=True) for s, m in members.items()})
    sector_price = (1 + sector_ret.fillna(0)).cumprod()
    return sector_price, daily_ret


# ══════════════════════════════════════════════════════════════════════════
# SECTOR FACTOR: BREADTH-DIVERGENCE  (the hypothesis)
# ══════════════════════════════════════════════════════════════════════════

def build_breadth_composite(prices, members, universe_mask):
    sma200 = prices.rolling(SMA_SLOW_WIN, min_periods=150).mean()
    above_200 = (prices > sma200)
    roll_hi = prices.rolling(HI_LO_WIN, min_periods=HI_LO_MIN_PERIODS).max()
    roll_lo = prices.rolling(HI_LO_WIN, min_periods=HI_LO_MIN_PERIODS).min()
    new_hi = (prices >= roll_hi)
    new_lo = (prices <= roll_lo)

    b1_dict, b2_dict, n_dict = {}, {}, {}
    for sector, tickers in members.items():
        tickers = [t for t in tickers if t in prices.columns]
        elig = universe_mask[tickers]
        n_elig = elig.sum(axis=1).replace(0, np.nan)
        n_dict[sector] = n_elig

        above_200_elig = above_200[tickers].where(elig)
        b1_dict[sector] = above_200_elig.sum(axis=1) / n_elig

        net_hi_lo = (new_hi[tickers].astype(float) - new_lo[tickers].astype(float)).where(elig)
        net_hi_lo_frac = net_hi_lo.sum(axis=1) / n_elig
        b2_dict[sector] = (net_hi_lo_frac.rolling(NET_HI_LO_SMOOTH, min_periods=NET_HI_LO_SMOOTH).sum()
                            / NET_HI_LO_SMOOTH)

    B1 = pd.DataFrame(b1_dict)
    B2 = pd.DataFrame(b2_dict)
    n_elig_df = pd.DataFrame(n_dict)
    valid = n_elig_df >= MIN_STOCKS_SECTOR
    B1, B2 = B1.where(valid), B2.where(valid)

    breadth = (B1.rank(axis=1, pct=True) + B2.rank(axis=1, pct=True)) / 2.0
    return breadth


def build_mom_disp_composite(sector_price, daily_ret, members):
    mom = sector_price.pct_change(SECTOR_MOM_PERIOD, fill_method=None)
    daily_dispersion = pd.DataFrame(
        {s: daily_ret[m].std(axis=1, skipna=True) for s, m in members.items()}
    )
    dispersion = daily_dispersion.rolling(DISPERSION_WINDOW).mean()
    return (mom.rank(axis=1, pct=True) + dispersion.rank(axis=1, pct=True)) / 2.0


def build_sector_rank(prices, members, universe_mask, sector_price, daily_ret):
    """div_resid = breadth - BETA_MOM_DISP * mom_disp (frozen beta)."""
    breadth = build_breadth_composite(prices, members, universe_mask)
    mom_disp = build_mom_disp_composite(sector_price, daily_ret, members)
    sector_rank = breadth - BETA_MOM_DISP * mom_disp
    return sector_rank, breadth, mom_disp


# ══════════════════════════════════════════════════════════════════════════
# STOCK FACTOR: TREND PERSISTENCE (+ optional vol-aware quality blend, §9)
# ══════════════════════════════════════════════════════════════════════════

def build_stock_factors(prices, quality_weight=STOCK_QUALITY_WEIGHT):
    sma_fast = prices.rolling(SMA_FAST, min_periods=SMA_FAST).mean()
    sma_slow = prices.rolling(SMA_SLOW_WIN, min_periods=150).mean()
    trend_ok = (prices > sma_fast) & (prices > sma_slow)

    above_slow = (prices > sma_slow).astype(float)
    persistence = above_slow.rolling(TREND_PERSIST_WIN, min_periods=TREND_PERSIST_WIN).mean()

    # §9: vol-aware quality composite -- global cross-sectional percentile
    # blend of persistence (consistency) and low realized vol (smoothness),
    # same construction pattern as the sector-level breadth composite.
    # NOT price-return momentum (unlike CSM's Sharpe factor) -- still
    # rewards CONSISTENCY of trend, just also penalizes chop along the way.
    # quality_weight exposed as a param (not just the module constant) so a
    # tuning sweep can pass candidate values without mutating global state.
    daily_ret = prices.pct_change(fill_method=None)
    realized_vol = daily_ret.rolling(STOCK_VOL_WIN, min_periods=STOCK_VOL_WIN).std().shift(1)
    persistence_rank = persistence.rank(axis=1, pct=True)
    low_vol_rank = (-realized_vol).rank(axis=1, pct=True)
    stock_quality = (quality_weight * persistence_rank
                      + (1.0 - quality_weight) * low_vol_rank)

    return sma_slow, trend_ok, persistence, stock_quality


def build_atr(prices, highs, lows):
    highs_ff = highs.ffill() if not highs.empty else prices
    lows_ff = lows.ffill() if not lows.empty else prices
    prev_close = prices.shift(1)
    tr = (highs_ff - lows_ff).abs()
    tr = tr.combine((highs_ff - prev_close).abs(), np.maximum)
    tr = tr.combine((lows_ff - prev_close).abs(), np.maximum)
    return tr.rolling(ATR_PERIOD, min_periods=ATR_PERIOD).mean()


def build_falling_knife_gate(prices, window=FALLING_KNIFE_WINDOW, floor=FALLING_KNIFE_FLOOR):
    """
    Last item from the CSM audit table that was never ported: CSM's
    filter_universe requires prior-month raw return >= -15% ("falling
    knife" gate). Daily-resolution equivalent: trailing `window` (~1
    month) trading-day return, T-1 (causal). Applied at STOCK-SELECTION
    time (rank_sector_stocks), not folded into universe_mask -- universe_
    mask already feeds the sector-level breadth/mom_disp factor, which was
    IC-validated on its current definition; changing it now would silently
    re-derive that validation. trend_ok (price>SMA50>SMA200) already
    catches most genuine crashes, so this is likely to show a small or
    near-zero marginal effect -- exactly why it's ablation-tested before
    being kept, same as Corr Guard turned out to be a no-op here.
    """
    return prices.pct_change(window, fill_method=None).shift(1) >= floor


# ══════════════════════════════════════════════════════════════════════════
# REGIME (benchmark = equal-weight across all qualifying sector indices)
# ══════════════════════════════════════════════════════════════════════════

def compute_regime(sector_price):
    """
    bench_ok    : existing v1 gate -- blocks NEW entries only, after the
                  equal-weight sector benchmark has stayed below its own
                  SMA50 for BENCH_STREAK_MAX consecutive days. Kept as-is.
    is_panic    : NEW (ported from CSM Quad) -- benchmark 21d-return-vol
                  above its own CAUSAL expanding 95th-pct threshold
                  (min_periods=126, no lookahead). Drives Crash Guard
                  (exit ALL positions) in the backtest loop, checked DAILY.
    leverage    : NEW -- bull(1.0)/bear(0.8) from benchmark vs its own
                  SMA200, tightened further by panic(0.5) via min() when
                  is_panic is True. Same values and precedence as CSM Quad.
    """
    bench = sector_price.mean(axis=1, skipna=True)

    bench_sma = bench.rolling(BENCH_SMA_PERIOD, min_periods=30).mean()
    below = (bench < bench_sma).shift(1).fillna(False).astype(int)
    streak = below.rolling(BENCH_STREAK_MAX, min_periods=BENCH_STREAK_MAX).sum()
    bench_ok = (streak < BENCH_STREAK_MAX).fillna(True)
    bench_ok = bench_ok.reindex(sector_price.index).fillna(True)

    bench_sma200 = bench.rolling(BENCH_SMA200_PERIOD, min_periods=150).mean()
    is_bull = (bench.shift(1) > bench_sma200.shift(1)).fillna(True)

    bench_ret = bench.pct_change(fill_method=None)
    bvol_daily = bench_ret.rolling(BENCH_VOL_WIN).std().shift(1)
    panic_threshold = bvol_daily.expanding(min_periods=PANIC_MIN_PERIODS).quantile(0.95)
    is_panic = (bvol_daily > panic_threshold).fillna(False)

    leverage = pd.Series(np.where(is_bull, LEVERAGE_BULL, LEVERAGE_BEAR), index=sector_price.index)
    leverage = np.minimum(leverage, np.where(is_panic, LEVERAGE_PANIC, leverage))
    leverage = pd.Series(leverage, index=sector_price.index)

    n_panic_days = int(is_panic.sum())
    print(f"[sector_breadth_v8] Panic regime active on {n_panic_days}/{len(is_panic)} days "
          f"({n_panic_days/len(is_panic)*100:.1f}%)  |  "
          f"leverage: bull={LEVERAGE_BULL} bear={LEVERAGE_BEAR} panic={LEVERAGE_PANIC}")

    return bench_ok, is_panic, leverage


# ══════════════════════════════════════════════════════════════════════════
# SIZING / COOLDOWN / RISK-OVERLAY HELPERS  (CSM Batch/Quad conventions)
# ══════════════════════════════════════════════════════════════════════════

def build_stock_vol(prices):
    """Trailing SIZING_VOL_WIN-day daily-return std per stock, T-1 (causal).
    Reused for both inverse-vol sizing (at rebalance) and Corr Guard's
    per-stock vol read (daily)."""
    daily_ret = prices.pct_change(fill_method=None)
    return daily_ret, daily_ret.rolling(SIZING_VOL_WIN, min_periods=SIZING_VOL_WIN).std().shift(1)


def size_active_book(active, stock_vol_row, cap=MAX_WEIGHT_PER_STOCK):
    """Inverse-vol weights across the WHOLE active book (held + newly
    entered), 2-pass clip+renormalize at `cap` -- CSM Batch's
    get_positions() sizing block, adapted to an event-driven book instead
    of a monthly cross-sectional matrix. Returns {ticker: base_weight}."""
    tickers = list(active.keys())
    if not tickers:
        return {}
    vols = pd.Series({t: stock_vol_row.get(t, np.nan) for t in tickers}).fillna(0.02).replace(0, 0.02)
    inv_vol = 1.0 / vols
    raw_w = inv_vol / inv_vol.sum()
    for _ in range(2):
        raw_w = raw_w.clip(upper=cap)
        total = raw_w.sum()
        if total > 0:
            raw_w = raw_w / total
    raw_w = raw_w.clip(upper=cap)
    return raw_w.to_dict()


def cooldown_days_for(pnl_pct):
    """Loss-scaled re-entry cooldown after a STOP_HIT (CSM Quad's
    cooldown_mode='loss_scaled'): a profitable stop (trend simply ended)
    gets NO cooldown; a bigger loss gets a longer ban, clipped to
    [COOLDOWN_FLOOR_DAYS, COOLDOWN_CAP_DAYS]."""
    if pd.isna(pnl_pct) or pnl_pct >= 0:
        return 0
    return int(np.clip(STOP_COOLDOWN_BASE_DAYS * abs(pnl_pct) / 10.0,
                        COOLDOWN_FLOOR_DAYS, COOLDOWN_CAP_DAYS))


def compute_overlay_scales(base_port_ret_history, stock_daily_ret, active, idx,
                            use_corr_guard=True, use_vol_target=True,
                            corr_guard_threshold=CORR_GUARD_THRESHOLD, vol_target=VOL_TARGET):
    """
    Corr Guard + Vol Targeting -- CSM Batch's apply_risk_overlays(), ported
    near-verbatim. Uses UNSCALED gross portfolio-return history (raw
    base-weights dotted with realized returns), NOT the already-scaled
    realized series -- same distinction CSM's own docstring makes, so
    today's scaling decision doesn't get contaminated by yesterday's own
    scaling. `active` here holds YESTERDAY's base weights (this is called
    before today's exits/entries/reweighting touch it).

    use_corr_guard/use_vol_target let the two mechanisms inside this one
    overlay be ablated independently; corr_guard_threshold/vol_target are
    exposed as params (not just module constants) so a tuning sweep can
    pass candidate values without mutating global state.
    """
    corr_scale, vol_scale = 1.0, 1.0
    n_hist = len(base_port_ret_history)

    if use_corr_guard and n_hist >= CORR_GUARD_WIN and active:
        pbuf = np.array(base_port_ret_history[-CORR_GUARD_WIN:])
        p_vol = float(pbuf.std())
        w_sum = sum(active[t]["weight"] for t in active)
        if w_sum > 0 and p_vol > 0:
            tickers = list(active.keys())
            start = max(0, idx - CORR_GUARD_WIN + 1)
            window = stock_daily_ret[tickers].iloc[start:idx + 1]
            s_std = window.std()
            avg_s_vol = float(sum(s_std.get(t, 0.0) * active[t]["weight"] for t in tickers) / w_sum)
            if avg_s_vol > 0 and (p_vol / avg_s_vol) > corr_guard_threshold:
                corr_scale = 0.5

    if use_vol_target and n_hist >= SIZING_VOL_WIN:
        win = (base_port_ret_history[-VOL_TARGET_WIN:] if n_hist >= VOL_TARGET_WIN
               else base_port_ret_history[-SIZING_VOL_WIN:])
        rv = float(np.std(win)) * np.sqrt(252)
        if rv > 0:
            vol_scale = min(1.0, vol_target / rv)

    return corr_scale, vol_scale


# ══════════════════════════════════════════════════════════════════════════
# EVENT-DRIVEN POSITION GENERATION + TRADE LOG
# ══════════════════════════════════════════════════════════════════════════

def rank_sector_stocks(idx, sector, members, rank_factor, universe_mask, trend_ok,
                        stop_cooldown_tickers=None, current_date=None, falling_knife=None):
    """rank_factor is whichever DataFrame the caller wants used for ranking --
    run_backtest passes either `persistence` or the §9 vol-aware `stock_quality`
    composite depending on use_vol_aware_stock_factor, decided once per call
    rather than branching inside this function."""
    tickers = members[sector]
    elig_row = universe_mask.iloc[idx]
    trend_row = trend_ok.iloc[idx]
    rank_row = rank_factor.iloc[idx]
    fk_row = falling_knife.iloc[idx] if falling_knife is not None else None

    def _not_cooling_down(t):
        if not stop_cooldown_tickers or t not in stop_cooldown_tickers:
            return True
        exit_date, days = stop_cooldown_tickers[t]
        return (current_date - exit_date).days >= days

    def _not_falling_knife(t):
        return True if fk_row is None else bool(fk_row.get(t, True))

    pool = [t for t in tickers
            if elig_row.get(t, False) and trend_row.get(t, False) and pd.notna(rank_row.get(t, np.nan))
            and _not_cooling_down(t) and _not_falling_knife(t)]
    pool.sort(key=lambda t: rank_row[t], reverse=True)
    return pool


def run_backtest(prices, opens, sector_rank, members, universe_mask,
                  sma_slow, trend_ok, persistence, bench_ok, atr,
                  is_panic, leverage, stock_daily_ret, stock_vol,
                  use_min_hold=False, use_stop_cooldown=True,
                  use_inverse_vol_sizing=True,
                  use_corr_guard=True, use_vol_target=True,
                  corr_guard_threshold=CORR_GUARD_THRESHOLD, vol_target=VOL_TARGET,
                  falling_knife=None, use_chandelier_floor=True,
                  use_swap_gap=True, swap_gap_ranks=SWAP_GAP_RANKS,
                  use_chandelier=True, use_stop_loss=True, use_crash_guard=True,
                  use_stock_rank_decline=True, use_sector_rank_decline=True,
                  use_vol_aware_stock_factor=True, stock_quality=None):
    """
    Defaults = v6's VALIDATED configuration (see module docstring for the
    ablation evidence behind each): min-hold OFF (net-negative), everything
    else ON, vol_target=0.20 (retuned from 0.15). Flags remain toggleable
    for future ablation, same convention CSM's own files use.

    EVERY exit mechanism has its own independent on/off switch -- each can
    be disabled completely, not just tuned, so any one of them can be
    ablation-tested in isolation the same way ATR_STOP already was:
      use_chandelier          -- ATR_STOP: trailing stop at all (else ONLY the
                                  fixed -15% floor remains -- CSM Quad's own
                                  default). Tested after ATR_STOP flagged as the
                                  worst exit bucket by total Rs P&L; removing it
                                  made Calmar/MaxDD/Sharpe all WORSE for ~zero
                                  CAGR gain (see test_chandelier_off.py) -- KEPT ON.
      use_stop_loss            -- STOP_LOSS: the fixed -15%-from-entry floor
                                  (else that hard backstop never fires -- with
                                  use_chandelier also off, NO price-based stop
                                  exists at all, pure signal-driven exits only)
      use_crash_guard          -- CRASH_GUARD: exit-all-positions on a benchmark
                                  vol spike (else the book is never force-cleared
                                  on panic). NOTE: independent of regime LEVERAGE
                                  scaling (bull/bear/panic multiplier) -- that
                                  keeps applying even with this off; this flag
                                  only controls the hard exit-everything trigger.
      use_stock_rank_decline   -- STOCK_RANK_DECLINE: a held stock exits once it
                                  falls outside its sector's top
                                  STOCKS_PER_SECTOR_EXIT (else only sector-level
                                  decline, stops, or Crash Guard can remove it)
      use_sector_rank_decline  -- SECTOR_RANK_DECLINE: a held stock exits once
                                  its sector falls outside top N_SECTORS_EXIT
                                  (else a stock is never force-exited just
                                  because its sector fell out of favor -- only
                                  affects EXISTING holdings; which sectors are
                                  eligible for NEW entries is unaffected)
      (SWAP_GAP already toggleable via use_swap_gap above; END_OF_DATA is
      backtest bookkeeping -- positions must close at the data boundary to
      compute final metrics, not a real exit rule, so it has no flag.)
      use_min_hold            -- §1 min-hold grace period (OFF by default -- dropped)
      use_stop_cooldown       -- §2 loss-scaled per-ticker re-entry ban
      use_inverse_vol_sizing  -- §3 inverse-vol book sizing (else flat 1/N)
      use_chandelier_floor    -- §6 ATR stop ratchets + clamped to [3%,30%] of
                                  peak (else the pre-fix recompute-fresh behaviour)
      use_swap_gap            -- §7 a much-better-ranked new candidate can evict
                                  a worse-ranked HELD name in the SAME sector when
                                  full, if it ranks >= swap_gap_ranks places better
      use_corr_guard          -- §4a Corr Guard (else no correlation-spike scale)
      falling_knife           -- §5, optional DataFrame from
                                  build_falling_knife_gate(); None = gate not
                                  applied. main() always builds and passes it.
      use_vol_target          -- §4b Vol Targeting (else no vol-target scale)
      corr_guard_threshold/vol_target -- override the module-constant defaults
                                          for a tuning sweep, without mutating
                                          global state
    """
    min_hold_days = MIN_HOLD_DAYS if use_min_hold else 0
    # §9: whichever factor rank_sector_stocks uses for ranking, decided once
    # here rather than branching inside that function on every call.
    active_rank_factor = (stock_quality if (use_vol_aware_stock_factor and stock_quality is not None)
                           else persistence)

    dates = prices.index
    n = len(dates)
    all_stocks = list(prices.columns)
    opens_ff = opens.ffill() if not opens.empty else prices.shift(1)
    open_proxy = prices.shift(1)

    start_i = dates.searchsorted(BACKTEST_START)
    end_i = dates.searchsorted(BACKTEST_END, side="right")

    position_list = []
    active = {}     # ticker -> {entry_date, entry_i, entry_price, peak_price, sector, weight, stop_pct}
    trade_log = []
    cg_cooldown_remaining = 0     # trading days left blocking new entries after a Crash Guard exit
    n_crash_guard_fires = 0
    stop_cooldown_tickers = {}    # ticker -> (exit_date, cooldown_days), loss-scaled per CSM Quad
    base_port_ret_history = []    # UNSCALED gross daily returns, for Corr Guard / Vol Target (§4)

    for i in range(start_i, end_i):
        date = dates[i]
        idx = i - 1

        # ── §4 Corr Guard / Vol Target: decide TODAY's scale from history
        # through YESTERDAY (not including today), then realize today's
        # UNSCALED return from YESTERDAY's book -- both BEFORE anything
        # below mutates `active`, so this stays causally clean. ──
        corr_scale, vol_scale = compute_overlay_scales(
            base_port_ret_history, stock_daily_ret, active, idx,
            use_corr_guard=use_corr_guard, use_vol_target=use_vol_target,
            corr_guard_threshold=corr_guard_threshold, vol_target=vol_target,
        )
        if active:
            today_rets = stock_daily_ret.iloc[i]
            raw_ret_today = sum(
                active[t]["weight"] * (float(today_rets[t]) if t in today_rets.index and pd.notna(today_rets[t]) else 0.0)
                for t in active
            )
        else:
            raw_ret_today = 0.0
        base_port_ret_history.append(raw_ret_today)

        to_exit = {}

        # ── Crash Guard (checked DAILY, not just rebalance days): exit ──
        # ALL positions the moment benchmark vol crosses its own causal
        # expanding 95th-pct threshold. Overrides any other exit reason
        # that would otherwise fire on the same names today. NOT subject
        # to the min-hold grace period -- fires regardless of days held,
        # same as CSM's Crash Guard (STEP C).
        crash_today = use_crash_guard and (bool(is_panic.iloc[idx]) if idx >= 0 else False)
        if crash_today and active:
            for ticker in active:
                to_exit[ticker] = "CRASH_GUARD"
            n_crash_guard_fires += 1
            cg_cooldown_remaining = CRASH_GUARD_COOLDOWN

        # ── Daily: fixed stop + ATR trailing stop (§1 min-hold grace applies) ──
        for ticker, h in active.items():
            if ticker in to_exit:
                continue   # already exiting via Crash Guard today
            prev_close = prices.iloc[idx].get(ticker, np.nan)
            if pd.isna(prev_close):
                continue
            h["min_price"] = min(h.get("min_price", h["entry_price"]), prev_close)
            h["peak_price"] = max(h.get("peak_price", h["entry_price"]), prev_close)
            h["max_price"] = h["peak_price"]

            if (i - h["entry_i"]) < min_hold_days:
                continue   # §1: stop suppressed during the grace period

            fixed_stop = h["entry_price"] * (1.0 - STOP_LOSS_PCT) if use_stop_loss else -np.inf
            atr_val = atr.iloc[idx].get(ticker, np.nan)

            if not use_chandelier:
                # §8: chandelier OFF entirely (CSM Quad's own default) --
                # tested in test_chandelier_off.py after the exit breakdown
                # flagged ATR_STOP as the worst bucket by total Rs P&L.
                # Result: CAGR flat (16.01%->16.08%) but Sharpe/Calmar/MaxDD
                # all WORSE (Calmar 0.687->0.611, MaxDD -23.3%->-26.3%) --
                # those trades don't stop losing money, they just ride
                # further until the much harder -15% floor catches them
                # instead (STOP_LOSS: 4 trades/-Rs3.3L -> 29 trades/-Rs18.7L).
                # KEPT ON. Flag exists so this can be re-verified, not
                # re-argued from the exit-breakdown table alone.
                atr_stop = -np.inf
            elif use_chandelier_floor:
                # §6: chandelier RATCHETS (persisted in h["atr_stop"], only
                # ever grows) and is clamped to [3%, 30%] of peak (CSM
                # Quad's np.clip(chand_raw, peak*0.70, peak*0.97)) before
                # ratcheting the persisted value up. Bundled together since
                # clamping a value that isn't persisted wouldn't achieve
                # anything -- the flag controls both at once.
                if pd.notna(atr_val) and atr_val > 0:
                    chand_raw = h["peak_price"] - ATR_MULTIPLIER * atr_val
                    chand_raw = float(np.clip(chand_raw, h["peak_price"] * 0.70, h["peak_price"] * 0.97))
                    h["atr_stop"] = max(h.get("atr_stop", -np.inf), chand_raw)
                atr_stop = h.get("atr_stop", -np.inf)
            else:
                # Original v1-v5 behaviour: recomputed fresh each day from
                # today's peak/ATR, NOT persisted/ratcheted -- a same-day
                # ATR spike can make the effective stop retreat even though
                # peak never fell. Kept only so the ablation cell can
                # measure the fix's actual effect, not assert it.
                atr_stop = (h["peak_price"] - ATR_MULTIPLIER * atr_val
                            if pd.notna(atr_val) and atr_val > 0 else -np.inf)

            effective_stop = max(fixed_stop, atr_stop)

            if prev_close <= effective_stop:
                to_exit[ticker] = "ATR_STOP" if atr_stop >= fixed_stop else "STOP_LOSS"

        is_rebalance_day = ((i - start_i) % REBALANCE_EVERY == 0)
        if is_rebalance_day:
            sector_row = sector_rank.iloc[idx].dropna().sort_values(ascending=False)
            top_sectors_exit = list(sector_row.index[:N_SECTORS_EXIT])

            # Sector rank decline (top_sectors_exit is still computed above
            # unconditionally -- swap-gap displacement below needs it
            # regardless of whether this exit rule itself is enabled)
            if use_sector_rank_decline:
                for ticker, h in active.items():
                    if ticker in to_exit:
                        continue
                    if h["sector"] not in top_sectors_exit:
                        to_exit[ticker] = "SECTOR_RANK_DECLINE"

            # Stock rank decline within still-qualifying sector (no cooldown
            # filter here -- this evaluates whether to KEEP an existing
            # holding, not a fresh entry)
            if use_stock_rank_decline:
                for ticker, h in active.items():
                    if ticker in to_exit:
                        continue
                    sector = h["sector"]
                    pool = rank_sector_stocks(idx, sector, members, active_rank_factor, universe_mask, trend_ok)
                    if ticker not in pool[:STOCKS_PER_SECTOR_EXIT]:
                        to_exit[ticker] = "STOCK_RANK_DECLINE"

            # §7: swap-gap displacement -- a much-better-ranked NEW candidate
            # can evict the worst-ranked HELD name in the SAME sector even
            # though it hasn't yet fallen past the (wider) STOCK_RANK_DECLINE
            # band, if that candidate ranks >= swap_gap_ranks positions
            # better in the sector's full candidate pool. The freed slot is
            # filled by the ordinary "New entries" block below -- no need to
            # force-insert the specific candidate here.
            if use_swap_gap:
                for sector in top_sectors_exit:
                    if sector not in members:
                        continue
                    held_in_sector = [t for t, h in active.items()
                                       if h["sector"] == sector and t not in to_exit]
                    if len(held_in_sector) < STOCKS_PER_SECTOR:
                        continue   # sector not full -- ordinary entry logic fills it
                    pool = rank_sector_stocks(idx, sector, members, active_rank_factor, universe_mask, trend_ok,
                                               stop_cooldown_tickers, date, falling_knife)
                    pool_rank = {t: p for p, t in enumerate(pool)}   # 0 = best
                    best_new = next((t for t in pool if t not in active), None)
                    if best_new is None:
                        continue
                    worst_ticker = max(held_in_sector, key=lambda t: pool_rank.get(t, len(pool)))
                    worst_rank = pool_rank.get(worst_ticker, len(pool))
                    if (worst_rank - pool_rank[best_new]) >= swap_gap_ranks:
                        to_exit[worst_ticker] = "SWAP_GAP"

        # ── Execute exits at T+1 open ──
        for ticker, reason in to_exit.items():
            h = active.pop(ticker)
            exit_open = float(opens_ff.at[date, ticker]) if ticker in opens_ff.columns else np.nan
            if pd.isna(exit_open) or exit_open <= 0:
                exit_open = float(open_proxy.at[date, ticker]) if ticker in open_proxy.columns else np.nan
            exit_close = float(prices.at[date, ticker]) if ticker in prices.columns else np.nan
            trade_log.append({
                "Ticker": ticker, "Sector": h["sector"],
                "Entry_Date": h["entry_date"], "Entry_Price": round(h["entry_price"], 4),
                "Exit_Date": date, "Exit_Price": round(exit_open, 4) if pd.notna(exit_open) else np.nan,
                "Close_At_Exit": round(exit_close, 4) if pd.notna(exit_close) else np.nan,
                "Exit_Reason": reason,
                "Weight": round(h.get("weight", np.nan), 6),
                "Stop_Pct": round(h.get("stop_pct", np.nan), 2),
                "MAE_Pct": round((h["min_price"] / h["entry_price"] - 1) * 100, 2),
                "MFE_Pct": round((h["max_price"] / h["entry_price"] - 1) * 100, 2),
            })

            # §2: per-ticker loss-scaled stop cooldown -- only for genuine
            # stop-outs, not rank-decay/crash-guard exits (those aren't
            # "this name failed", they're rotation/regime-driven).
            if (use_stop_cooldown and reason in ("ATR_STOP", "STOP_LOSS")
                    and pd.notna(exit_open) and exit_open > 0):
                pnl_pct = (exit_open / h["entry_price"] - 1.0) * 100.0
                cd = cooldown_days_for(pnl_pct)
                if cd > 0:
                    stop_cooldown_tickers[ticker] = (date, cd)

        # Expire old cooldown entries opportunistically (keeps the dict small)
        stop_cooldown_tickers = {t: v for t, v in stop_cooldown_tickers.items()
                                  if (date - v[0]).days < v[1]}

        # ── Crash Guard cooldown: block ALL new entries for CRASH_GUARD_COOLDOWN
        # trading days after a fire (book is empty right after Crash Guard, so
        # "new" and "any" entry are equivalent here -- no held names to protect). ──
        if cg_cooldown_remaining > 0:
            cg_cooldown_remaining -= 1

        # Regime leverage (T-1 value, same causal convention as everything else) --
        # combines with corr_scale/vol_scale multiplicatively on the base weight.
        lev = float(leverage.iloc[idx]) if idx >= 0 else 1.0

        # ── New entries: only on rebalance days, only if regime OK ──
        if (is_rebalance_day and i >= WARMUP_DAYS and bool(bench_ok.iloc[idx])
                and cg_cooldown_remaining <= 0):
            sector_row = sector_rank.iloc[idx].dropna().sort_values(ascending=False)
            top_sectors_entry = list(sector_row.index[:N_SECTORS])

            for sector in top_sectors_entry:
                if sector not in members:
                    continue
                slots = MAX_POSITIONS - len(active)
                if slots <= 0:
                    break
                pool = rank_sector_stocks(idx, sector, members, active_rank_factor, universe_mask, trend_ok,
                                           stop_cooldown_tickers, date, falling_knife)
                sector_held = [t for t, h in active.items() if h["sector"] == sector]
                free_in_sector = STOCKS_PER_SECTOR - len(sector_held)
                candidates = [t for t in pool[:STOCKS_PER_SECTOR] if t not in active][:max(0, free_in_sector)]
                for ticker in candidates:
                    if len(active) >= MAX_POSITIONS:
                        break
                    entry_px = float(opens_ff.at[date, ticker]) if ticker in opens_ff.columns else np.nan
                    if pd.isna(entry_px) or entry_px <= 0:
                        entry_px = float(open_proxy.at[date, ticker]) if ticker in open_proxy.columns else np.nan
                    if pd.isna(entry_px) or entry_px <= 0:
                        continue

                    # Initial stop distance at entry (for the report's Avg Stop Pct) --
                    # same max(fixed, ATR-chandelier) logic as the daily stop check,
                    # evaluated once at entry with peak_price == entry_price.
                    atr_at_entry = float(atr.iloc[idx].get(ticker, np.nan))
                    fixed_stop_e = entry_px * (1.0 - STOP_LOSS_PCT)
                    atr_stop_e = (entry_px - ATR_MULTIPLIER * atr_at_entry
                                  if pd.notna(atr_at_entry) and atr_at_entry > 0 else -np.inf)
                    initial_stop = max(fixed_stop_e, atr_stop_e)
                    stop_pct = (entry_px - initial_stop) / entry_px * 100.0

                    active[ticker] = {
                        "entry_date": date, "entry_i": i, "entry_price": entry_px,
                        "peak_price": entry_px, "min_price": entry_px, "max_price": entry_px,
                        "sector": sector, "weight": 0.0, "stop_pct": stop_pct,
                        "atr_stop": atr_stop_e,
                    }

        # ── §3: inverse-vol sizing, recomputed for the WHOLE active book at
        # every rebalance (held names get reweighted too, not just new
        # entries -- matches CSM's monthly full-book recompute). Weight
        # persists unchanged between rebalances. Flag off -> flat 1/N,
        # matching v3's baseline sizing exactly. ──
        if is_rebalance_day and active:
            if use_inverse_vol_sizing:
                base_weights = size_active_book(active, stock_vol.iloc[idx])
            else:
                flat_w = 1.0 / MAX_POSITIONS
                base_weights = {t: flat_w for t in active}
            for t, w in base_weights.items():
                active[t]["weight"] = w

        # Final weight = base (vol-sized) x regime leverage x corr_scale x vol_scale
        curr_weights = pd.Series(
            {t: active[t]["weight"] * lev * corr_scale * vol_scale for t in active},
            dtype=float).reindex(all_stocks, fill_value=0.0)
        curr_weights.name = date
        position_list.append(curr_weights)

    # ── Close remaining positions at end of data ──
    last_date = dates[end_i - 1]
    for ticker, h in list(active.items()):
        exit_close = float(prices.at[last_date, ticker]) if ticker in prices.columns else np.nan
        trade_log.append({
            "Ticker": ticker, "Sector": h["sector"],
            "Entry_Date": h["entry_date"], "Entry_Price": round(h["entry_price"], 4),
            "Exit_Date": last_date, "Exit_Price": round(exit_close, 4) if pd.notna(exit_close) else np.nan,
            "Close_At_Exit": round(exit_close, 4) if pd.notna(exit_close) else np.nan,
            "Exit_Reason": "END_OF_DATA",
            "Weight": round(h.get("weight", np.nan), 6),
            "Stop_Pct": round(h.get("stop_pct", np.nan), 2),
            "MAE_Pct": round((h["min_price"] / h["entry_price"] - 1) * 100, 2),
            "MFE_Pct": round((h["max_price"] / h["entry_price"] - 1) * 100, 2),
        })

    print(f"[sector_breadth_v8] Crash Guard fired {n_crash_guard_fires} times "
          f"(each clears the book + blocks new entries for {CRASH_GUARD_COOLDOWN}d)")

    positions_df = pd.DataFrame(position_list, index=dates[start_i:end_i]).fillna(0.0)
    trade_log_df = pd.DataFrame(trade_log)
    return positions_df, trade_log_df


# ══════════════════════════════════════════════════════════════════════════
# METRICS
# ══════════════════════════════════════════════════════════════════════════

def compute_portfolio_returns(positions_df, prices):
    stock_ret = prices.pct_change(fill_method=None).reindex(positions_df.index)
    port_ret = (positions_df.shift(1) * stock_ret).sum(axis=1)
    return port_ret.fillna(0.0)


def compute_metrics(port_ret, rfr_annual=0.0):
    equity = (1 + port_ret).cumprod()
    n_years = len(port_ret) / 252.0
    cagr = equity.iloc[-1] ** (1 / n_years) - 1 if n_years > 0 else np.nan
    total_return = equity.iloc[-1] - 1.0

    ann_ret = port_ret.mean() * 252
    ann_vol = port_ret.std() * np.sqrt(252)
    sharpe = (ann_ret - rfr_annual) / ann_vol if ann_vol > 0 else np.nan

    downside = port_ret[port_ret < 0]
    downside_vol = downside.std() * np.sqrt(252) if len(downside) > 1 else np.nan
    sortino = (ann_ret - rfr_annual) / downside_vol if downside_vol and downside_vol > 0 else np.nan

    running_max = equity.cummax()
    drawdown = equity / running_max - 1.0
    max_dd = drawdown.min()
    calmar = cagr / abs(max_dd) if max_dd < 0 else np.nan

    win_days = (port_ret > 0).sum()
    total_days = (port_ret != 0).sum()
    win_rate_daily = win_days / total_days if total_days > 0 else np.nan

    monthly_ret = port_ret.groupby(port_ret.index.to_period("M")).apply(lambda r: (1 + r).prod() - 1)
    win_rate_monthly = (monthly_ret > 0).mean() if len(monthly_ret) else np.nan

    final_portfolio = STARTING_CAPITAL * equity.iloc[-1]

    metrics = dict(
        CAGR=cagr, TotalReturn=total_return, AnnVol=ann_vol, MaxDD=max_dd,
        Sharpe=sharpe, Sortino=sortino, Calmar=calmar, FinalPortfolio=final_portfolio,
        WinRateDaily=win_rate_daily, WinRateMonthly=win_rate_monthly,
    )
    return metrics, equity, drawdown, monthly_ret


def yearly_table(port_ret, equity):
    """Year | calendar-year return | max drawdown WITHIN that year (running max
    reset at the year's first observation, not chained from prior years)."""
    rows = []
    for year, r in port_ret.groupby(port_ret.index.year):
        yr_ret = (1 + r).prod() - 1
        yr_equity = equity.loc[r.index]
        yr_dd = (yr_equity / yr_equity.cummax() - 1.0).min()
        rows.append((year, yr_ret, yr_dd))
    return pd.DataFrame(rows, columns=["Year", "Return", "MaxDD"]).set_index("Year")


def enrich_trade_log(trade_log_df, equity):
    """Adds Return_Pct, Holding_Days, and rupee PnL (via portfolio value AT
    ENTRY x Weight x Return_Pct -- an approximation that ignores intra-trade
    compounding of the rest of the book, standard practitioner convention)."""
    df = trade_log_df.copy()
    df["Entry_Date"] = pd.to_datetime(df["Entry_Date"])
    df["Exit_Date"] = pd.to_datetime(df["Exit_Date"])
    df["Return_Pct"] = (df["Exit_Price"] / df["Entry_Price"] - 1.0) * 100.0
    df["Holding_Days"] = (df["Exit_Date"] - df["Entry_Date"]).dt.days
    df["Win"] = df["Return_Pct"] > 0

    equity_at_entry = equity.reindex(df["Entry_Date"], method="ffill").values
    portfolio_value_at_entry = STARTING_CAPITAL * equity_at_entry
    df["Rupee_PnL"] = portfolio_value_at_entry * df["Weight"].fillna(0.0) * (df["Return_Pct"] / 100.0)
    return df


def compute_trade_stats(trades):
    n = len(trades)
    wins = trades[trades["Win"]]
    losses = trades[~trades["Win"]]
    win_rate_trade = len(wins) / n if n else np.nan

    avg_win = wins["Return_Pct"].mean() if len(wins) else np.nan
    avg_loss = losses["Return_Pct"].mean() if len(losses) else np.nan
    payoff_ratio = abs(avg_win / avg_loss) if avg_loss and avg_loss != 0 else np.nan

    gross_win_pct = wins["Return_Pct"].sum()
    gross_loss_pct = losses["Return_Pct"].sum()
    profit_factor_pct = abs(gross_win_pct / gross_loss_pct) if gross_loss_pct != 0 else np.nan

    gross_win_rs = wins["Rupee_PnL"].sum()
    gross_loss_rs = losses["Rupee_PnL"].sum()
    profit_factor_rs = abs(gross_win_rs / gross_loss_rs) if gross_loss_rs != 0 else np.nan

    return dict(
        TotalTrades=n, TradeWinRate=win_rate_trade,
        AvgTradeReturn=trades["Return_Pct"].mean(), MedianTradeReturn=trades["Return_Pct"].median(),
        BestTrade=trades["Return_Pct"].max(), WorstTrade=trades["Return_Pct"].min(),
        AvgWin=avg_win, AvgLoss=avg_loss, PayoffRatio=payoff_ratio,
        ProfitFactorPct=profit_factor_pct, ProfitFactorRs=profit_factor_rs,
        AvgHoldingDays=trades["Holding_Days"].mean(), AvgStopPct=trades["Stop_Pct"].mean(),
        AvgMAE=trades["MAE_Pct"].mean(), AvgMFE=trades["MFE_Pct"].mean(),
    )


def compute_exit_breakdown(trades):
    def _agg(g):
        wins = g[g["Win"]]
        losses = g[~g["Win"]]
        return pd.Series({
            "N": len(g), "Winners": len(wins), "Losers": len(losses),
            "WinRate": len(wins) / len(g) * 100 if len(g) else np.nan,
            "AvgPnL_Pct": g["Return_Pct"].mean(), "TotalPnL_Pct": g["Return_Pct"].sum(),
            "AvgPnL_Rs": g["Rupee_PnL"].mean(), "TotalPnL_Rs": g["Rupee_PnL"].sum(),
        })
    return trades.groupby("Exit_Reason").apply(_agg).sort_values("TotalPnL_Pct")


def compute_turnover(positions_df, n_years):
    """Annualised turnover: sum of one-way |weight change| across the whole
    backtest, divided by 2 (round-trip convention) and by n_years."""
    daily_turnover = positions_df.diff().abs().sum(axis=1)
    total_turnover = daily_turnover.sum() / 2.0
    return total_turnover / n_years if n_years > 0 else np.nan


def print_performance_report(metrics, trade_stats, exit_bd, ann_turnover, yr_table):
    W = 20   # label column width
    def p(label, val, unit=""):
        print(f"  {label:<{W}}: {val}{unit}")

    print("=" * 42)
    print("PERFORMANCE REPORT")
    print("=" * 42)

    print("\n-- Portfolio Metrics ------------------")
    p("CAGR", f"{metrics['CAGR']*100:+.2f}", "%")
    p("Total Return", f"{metrics['TotalReturn']*100:+.2f}", "%")
    p("Ann Volatility", f"{metrics['AnnVol']*100:.2f}", "%")
    p("Max Drawdown", f"{metrics['MaxDD']*100:.2f}", "%")
    p("Sharpe Ratio", f"{metrics['Sharpe']:.3f}")
    p("Sortino Ratio", f"{metrics['Sortino']:.3f}" if pd.notna(metrics['Sortino']) else "n/a")
    p("Calmar Ratio", f"{metrics['Calmar']:.3f}")
    p("Final Portfolio", f"Rs {metrics['FinalPortfolio']:,.0f}")

    print("\n-- Win Rate (3 views) ------------------")
    p("Daily Win Rate", f"{metrics['WinRateDaily']*100:.2f}", "%")
    p("Monthly Win Rate", f"{metrics['WinRateMonthly']*100:.2f}", "%")
    p("Trade Win Rate", f"{trade_stats['TradeWinRate']*100:.2f}% "
      f"(n={trade_stats['TotalTrades']})")

    print("\n-- Trade Statistics --------------------")
    p("Total Trades", trade_stats['TotalTrades'])
    p("Avg Trade Return", f"{trade_stats['AvgTradeReturn']:+.2f}", "%")
    p("Median Trade Ret", f"{trade_stats['MedianTradeReturn']:+.2f}", "%")
    p("Best Trade", f"{trade_stats['BestTrade']:+.2f}", "%")
    p("Worst Trade", f"{trade_stats['WorstTrade']:+.2f}", "%")
    p("Avg Win (trade)", f"{trade_stats['AvgWin']:+.2f}", "%")
    p("Avg Loss (trade)", f"{trade_stats['AvgLoss']:+.2f}", "%")
    p("Payoff Ratio", f"{trade_stats['PayoffRatio']:.2f}  (avg win / avg loss)")
    p("Profit Factor (%)", f"{trade_stats['ProfitFactorPct']:.2f}  (equal-weighted)")
    p("Profit Factor (Rs)", f"{trade_stats['ProfitFactorRs']:.2f}  (rupee-weighted)")
    p("Avg Holding Days", f"{trade_stats['AvgHoldingDays']:.1f}")
    p("Avg Stop Pct", f"{trade_stats['AvgStopPct']:.2f}", "%")
    p("Avg MAE", f"{trade_stats['AvgMAE']:.2f}", "%")
    p("Avg MFE", f"{trade_stats['AvgMFE']:+.2f}", "%")

    print("\n-- Exit Breakdown -----------------------")
    fmt = exit_bd.copy()
    fmt["WinRate"] = fmt["WinRate"].round(1)
    fmt["AvgPnL_Pct"] = fmt["AvgPnL_Pct"].round(2)
    fmt["TotalPnL_Pct"] = fmt["TotalPnL_Pct"].round(1)
    fmt["AvgPnL_Rs"] = fmt["AvgPnL_Rs"].round(0)
    fmt["TotalPnL_Rs"] = fmt["TotalPnL_Rs"].round(0)
    print(fmt.to_string())

    print("\n-- Turnover ------------------------------")
    p("Ann Turnover", f"{ann_turnover*100:.2f}", "%")

    print("\n" + "=" * 34)
    print("  Yearly Returns & Drawdown")
    print("=" * 34)
    print("Year   |   Return |   Max DD")
    print("-" * 32)
    for year, row in yr_table.iterrows():
        print(f"{year}   |   {row['Return']*100:+.2f}% |  {row['MaxDD']*100:.2f}%")


# ══════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════

def main():
    print("Loading OHLCV data...")
    prices, volumes, highs, lows, opens = load_data(DATA_FOLDER)

    members = build_sector_membership(prices, INSTRUMENTS_CSV)
    universe_mask = build_universe_mask(prices, volumes, highs, lows)
    sector_price, daily_ret = build_sector_index(prices, members)
    sector_rank, breadth, mom_disp = build_sector_rank(prices, members, universe_mask,
                                                        sector_price, daily_ret)
    sma_slow, trend_ok, persistence, stock_quality = build_stock_factors(prices)
    atr = build_atr(prices, highs, lows)
    bench_ok, is_panic, leverage = compute_regime(sector_price)
    stock_daily_ret, stock_vol = build_stock_vol(prices)
    falling_knife = build_falling_knife_gate(prices)

    print(f"\nRunning backtest {BACKTEST_START.date()} -> {BACKTEST_END.date()} "
          f"(IN-SAMPLE ONLY)...")
    positions_df, trade_log_df = run_backtest(
        prices, opens, sector_rank, members, universe_mask,
        sma_slow, trend_ok, persistence, bench_ok, atr,
        is_panic, leverage, stock_daily_ret, stock_vol,
        falling_knife=falling_knife, stock_quality=stock_quality)

    port_ret = compute_portfolio_returns(positions_df, prices)
    metrics, equity, drawdown, monthly_ret = compute_metrics(port_ret)
    yr_table = yearly_table(port_ret, equity)
    n_years = len(port_ret) / 252.0

    trades = enrich_trade_log(trade_log_df, equity)
    trade_stats = compute_trade_stats(trades)
    exit_bd = compute_exit_breakdown(trades)
    ann_turnover = compute_turnover(positions_df, n_years)

    print()
    print_performance_report(metrics, trade_stats, exit_bd, ann_turnover, yr_table)

    # ── Save outputs (v8 filenames) ──
    trades.to_csv(os.path.join(OUT_DIR, "sector_breadth_trades_v8.csv"), index=False)
    pd.DataFrame([metrics]).to_csv(os.path.join(OUT_DIR, "sector_breadth_results_v8.csv"), index=False)
    yr_table.to_csv(os.path.join(OUT_DIR, "sector_breadth_yearly_v8.csv"))

    fig, ax = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    ax[0].plot(equity.index, equity.values)
    ax[0].set_title("Sector Breadth-Divergence v8 (Final) -- Equity Curve (IS 2003-2012)")
    ax[0].set_yscale("log")
    ax[1].fill_between(drawdown.index, drawdown.values * 100, 0, color="red", alpha=0.4)
    ax[1].set_title("Drawdown (%)")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "sector_breadth_equity_v8.png"), dpi=100)
    print(f"\nSaved trade log, results, yearly breakdown, and equity plot to {OUT_DIR}")


if __name__ == "__main__":
    main()
