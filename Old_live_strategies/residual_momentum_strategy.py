"""
residual_momentum_strategy.py
==============================
Residual Momentum — strategy core: signal construction, universe filtering, position
generation/sizing, and Stage-1-lite data-integrity diagnostics (universe card + return
spot-check). The day-by-day backtest loop and metrics live in residual_momentum_backtest.py.

Signal   : CAPM residual momentum (r - beta*r_mkt, summed over a formation window), composite
           with a 52-week-high tilt (see calculate_factors()). illiq_weight/lowpx_weight
           default to 0 (off) — see STRATEGY_OVERVIEW.md for why.
Universe : monthly top-N by trailing-63d median dollar turnover, plus an absolute min_price/
           min_adv tradability floor (see filter_universe()).
Positions: rank-based enter/exit hysteresis + inverse-vol weighting with a position cap,
           realized-vol targeting, an SMA trend gate, and a correlation guard (see
           get_positions()).

No live-trading path yet — the drawdown-stop logic lives entirely in the backtest file's
day loop. See STRATEGY_OVERVIEW.md for the full signal/portfolio/risk writeup and the
rationale behind each default.
"""
import glob
import os

import numpy as np
import pandas as pd


# Local-CSV directory. Override with the RESIDUAL_MOM_DATA_DIR env var (e.g.
# `export RESIDUAL_MOM_DATA_DIR=/path/to/data`) instead of editing this file -- the hard-coded
# default below only works on the original dev machine.
LOCAL_DIR = os.environ.get(
    "RESIDUAL_MOM_DATA_DIR", "/Users/hemantsoni/Documents/upstox_data_folder/ohlcv_data")

# ══════════════════════════════════════════════════════════════════════════════
# DATA LOADER
# ══════════════════════════════════════════════════════════════════════════════

def _nse_files(d):
    """NSE-ticker files only: filename stem contains a letter (skips pure-numeric BSE codes)."""
    out = []
    for f in glob.glob(os.path.join(d, "*.csv")):
        stem = os.path.splitext(os.path.basename(f))[0]
        if any(c.isalpha() for c in stem):
            out.append((stem, f))
    return out


def load_data(dir=LOCAL_DIR, start=None, end=None):
    """Read per-symbol OHLCV CSVs from `dir` (NSE-ticker files only). Returns
    (prices_df, volumes_df, highs_df, lows_df, opens_df). Drops rows with volume<=0,
    close<=0, or high<low. No caching -- always reads fresh, so corrected source CSVs are
    never silently served stale."""
    frames = []
    for sym, path in _nse_files(dir):
        try:
            df = pd.read_csv(path, usecols=["datetime", "open", "high", "low", "close", "volume"])
        except Exception:
            continue
        if df.empty:
            continue
        df["datetime"] = pd.to_datetime(df["datetime"], format="%Y-%m-%d", errors="coerce")
        df = df.dropna(subset=["datetime"])
        if start:
            df = df[df["datetime"] >= pd.Timestamp(start)]
        if end:
            df = df[df["datetime"] <= pd.Timestamp(end)]
        if df.empty:
            continue
        df["symbol"] = sym
        frames.append(df)
    px = pd.concat(frames, ignore_index=True).drop_duplicates(["symbol", "datetime"])
    bad = ((px["volume"].fillna(0) <= 0) | (px["close"] <= 0)
           | (px["high"] < px["low"]) | px["close"].isna())
    px = px[~bad]
    wide = lambda c: px.pivot(index="datetime", columns="symbol", values=c).sort_index()
    F = {c: wide(c) for c in ("open", "high", "low", "close", "volume")}

    return F["close"], F["volume"], F["high"], F["low"], F["open"]


# ══════════════════════════════════════════════════════════════════════════════
# SMALL UTILITIES
# ══════════════════════════════════════════════════════════════════════════════

def _month_end_days(index):
    s = pd.Series(index, index=index)
    return pd.DatetimeIndex(s.groupby([index.year, index.month]).last().values)


def _trailing_vol(ret, window, min_periods=40):
    return ret.rolling(window, min_periods=min_periods).std()


# ══════════════════════════════════════════════════════════════════════════════
# DATA-INTEGRITY DIAGNOSTICS
# ══════════════════════════════════════════════════════════════════════════════
# build_universe_card(F, top_n) -> universe definition + breadth/listing-history stats
# spot_check_returns(F)         -> unclipped-return outlier scan (split/data-quality risk)
# Lightweight pass/caution-flag checks, not a full data-cleaning pipeline.

REFERENCE_TICKERS = ("RELIANCE", "INFY", "TCS", "HDFCBANK", "ITC")
BREADTH_FLOOR = 8
SPLIT_JUMP_FLAG = 1.50   # |return| > 150% -> needs eyeballing
CARD_RET_CLIP = 0.50     # matches the strategy's ret_clip default; duplicated here to avoid coupling


def build_universe_card(F, top_n=500, start=None):
    """`start`, if given, scopes the breadth/listing-history stats to the report window
    (`close.index >= start`) instead of the full loaded panel. Raw-CSV/NSE-file counts are
    directory-level and never date-scoped."""
    close, univ = F["close"], F["univ"]
    report_window = close.index
    if start is not None:
        report_window = close.index[close.index >= pd.Timestamp(start)]

    total_csv = len(glob.glob(os.path.join(LOCAL_DIR, "*.csv")))
    nse_files = _nse_files(LOCAL_DIR)
    n_nse = len(nse_files)
    n_excluded = total_csv - n_nse

    me = _month_end_days(report_window)
    names_per_month = univ.loc[me].sum(axis=1)
    breadth_violations = int((names_per_month < BREADTH_FLOOR).sum())

    close_w = close.loc[report_window]
    hist_days = close_w.notna().sum(axis=0)
    hist_days = hist_days[hist_days > 0]

    ref_status = {}
    last_day = report_window.max()
    for t in REFERENCE_TICKERS:
        if t in univ.columns:
            ref_status[t] = bool(univ[t].loc[:last_day].iloc[-1])
        else:
            ref_status[t] = None  # file not present at all

    card = dict(
        top_n=top_n,
        analysis_window=(str(report_window.min().date()), str(report_window.max().date())),
        total_raw_csv=total_csv,
        nse_alpha_kept=n_nse,
        nse_alpha_kept_pct=n_nse / total_csv if total_csv else float("nan"),
        excluded_numeric=n_excluded,
        excluded_numeric_pct=n_excluded / total_csv if total_csv else float("nan"),
        symbols_in_panel=close.shape[1],
        load_window=(str(close.index.min().date()), str(close.index.max().date())),
        names_per_month_mean=float(names_per_month.mean()),
        names_per_month_min=int(names_per_month.min()),
        names_per_month_max=int(names_per_month.max()),
        breadth_floor=BREADTH_FLOOR,
        breadth_violations=breadth_violations,
        breadth_violations_pct=breadth_violations / len(me) if len(me) else float("nan"),
        listing_days_min=int(hist_days.min()),
        listing_days_median=float(hist_days.median()),
        listing_days_max=int(hist_days.max()),
        symbols_under_252d=int((hist_days < 252).sum()),
        reference_ticker_status=ref_status,
    )
    return card


def print_universe_card(card):
    print("=" * 78)
    print("UNIVERSE CARD")
    print("=" * 78)
    print(f"Raw CSVs in output_stocks/            : {card['total_raw_csv']:,}")
    print(f"NSE-alpha files kept                   : {card['nse_alpha_kept']:,} "
          f"({card['nse_alpha_kept_pct']:.0%})")
    print(f"Pure-numeric (BSE) files excluded      : {card['excluded_numeric']:,} "
          f"({card['excluded_numeric_pct']:.0%})")
    print(f"Symbols surviving into panel           : {card['symbols_in_panel']:,}")
    print(f"Full load window                       : {card['load_window'][0]} .. {card['load_window'][1]}")
    print(f"Stats below scoped to (report) window  : {card['analysis_window'][0]} .. {card['analysis_window'][1]}")
    print(f"Top-{card['top_n']} universe names/month  mean/min/max : "
          f"{card['names_per_month_mean']:.0f} / {card['names_per_month_min']} / {card['names_per_month_max']}")
    print(f"Breadth-floor (<{card['breadth_floor']} names) violations : "
          f"{card['breadth_violations']} months ({card['breadth_violations_pct']:.0%})")
    print(f"Listing history (days) min/median/max  : "
          f"{card['listing_days_min']} / {card['listing_days_median']:.0f} / {card['listing_days_max']}")
    print(f"Symbols with <252d total history       : {card['symbols_under_252d']:,}")
    print("Reference-ticker in-universe at end of window:")
    for t, status in card["reference_ticker_status"].items():
        label = "MISSING (no file)" if status is None else ("True" if status else "False")
        print(f"    {t:10s}: {label}")
    print("=" * 78)


def spot_check_returns(F, n_top=25):
    close = F["close"]
    raw_ret = close.pct_change(fill_method=None)  # UNCLIPPED, deliberately not the strategy's clipped returns

    long = raw_ret.stack()
    long.index.names = ["date", "symbol"]
    abs_long = long.abs()

    total_obs = int(abs_long.notna().sum())
    thresholds = [0.20, 0.50, 1.00, 2.00]
    dist = {f">{int(t*100)}%": int((abs_long > t).sum()) for t in thresholds}

    # top-N by |return|, with price context
    top_idx = abs_long.sort_values(ascending=False).index[:n_top]
    rows = []
    for date, sym in top_idx:
        pos = close.index.get_loc(date)
        prev_close = close[sym].iloc[pos - 1] if pos > 0 else np.nan
        cur_close = close.loc[date, sym]
        rows.append(dict(symbol=sym, date=str(pd.Timestamp(date).date()),
                          raw_return=float(long.loc[(date, sym)]),
                          close_before=float(prev_close) if pd.notna(prev_close) else None,
                          close_after=float(cur_close) if pd.notna(cur_close) else None))
    outliers = pd.DataFrame(rows)

    worst_per_symbol = abs_long.groupby(level="symbol").max().sort_values(ascending=False)

    summary = dict(
        total_obs=total_obs,
        dist=dist,
        n_flagged_over_150pct=int((abs_long > SPLIT_JUMP_FLAG).sum()),
        pct_exceeding_50pct_clip=float((abs_long > CARD_RET_CLIP).sum()) / total_obs if total_obs else float("nan"),
        worst_symbol=worst_per_symbol.index[0] if len(worst_per_symbol) else None,
        worst_symbol_value=float(worst_per_symbol.iloc[0]) if len(worst_per_symbol) else None,
    )
    return summary, outliers


def print_spot_check(summary, outliers):
    print("=" * 78)
    print("SPLIT-ADJUSTMENT / DATA-QUALITY SPOT-CHECK (unclipped daily returns)")
    print("=" * 78)
    print(f"Total (date,symbol) return observations : {summary['total_obs']:,}")
    for label, n in summary["dist"].items():
        print(f"  |return| {label:>5s}  : {n:,}")
    print(f"Flagged (|return| > {SPLIT_JUMP_FLAG:.0%})       : {summary['n_flagged_over_150pct']:,}  <-- needs eyeballing if > 0")
    print(f"Fraction exceeding strategy's 50% clip   : {summary['pct_exceeding_50pct_clip']:.4%}")
    if summary["worst_symbol"] is not None:
        print(f"Single worst symbol                      : {summary['worst_symbol']} "
              f"(max |return| {summary['worst_symbol_value']:.1%})")
    print(f"\nTop {len(outliers)} largest single-day |return| observations:")
    if len(outliers):
        print(outliers.to_string(index=False))
    print("=" * 78)


# ══════════════════════════════════════════════════════════════════════════════
# SIGNAL MATH (ported from src/signals.py)
# ══════════════════════════════════════════════════════════════════════════════

def _daily_returns(close, clip):
    return close.pct_change(fill_method=None).clip(-clip, clip)


def _market_return(ret, univ):
    # NOTE: this equal-weighted proxy includes each stock's own return, so a given stock's
    # beta/residual is computed against a benchmark that's partly itself (~1/breadth per name --
    # small at universe_top_n=500, would matter more if the universe were ever shrunk a lot).
    # Left as-is: this is the currently-validated composite's math, and excluding each stock
    # from its own market proxy is a deliberate signal-methodology change, not a bugfix -- flag
    # it if you want that changed.
    return ret.where(univ).mean(axis=1)


def _rolling_beta(ret, mkt, window, min_periods):
    mean_m  = mkt.rolling(window, min_periods=min_periods).mean()
    var_m   = (mkt * mkt).rolling(window, min_periods=min_periods).mean() - mean_m ** 2
    mean_r  = ret.rolling(window, min_periods=min_periods).mean()
    mean_rm = ret.mul(mkt, axis=0).rolling(window, min_periods=min_periods).mean()
    cov     = mean_rm.sub(mean_r.mul(mean_m, axis=0))
    return cov.div(var_m.replace(0, np.nan), axis=0)


def _residual_returns(ret, beta, mkt, clip):
    return ret.sub(beta.mul(mkt, axis=0)).clip(-clip, clip)


def _residual_momentum(resid, lookback, skip, scale_by_vol=False):
    cum = resid.cumsum()
    raw = cum.shift(skip) - cum.shift(lookback)
    if not scale_by_vol:
        return raw
    n = lookback - skip
    vol = resid.shift(skip).rolling(n, min_periods=int(n * 0.6)).std()
    return raw.div(vol * np.sqrt(n))


# ══════════════════════════════════════════════════════════════════════════════
# STRATEGY CLASS
# ══════════════════════════════════════════════════════════════════════════════

class ResidualMomentumStrategy:
    """Residual momentum with monthly rebalancing and daily-simulated drawdown/ATR stops.

    Call order: calculate_factors() then get_positions(start). The day-by-day simulation
    (residual_momentum_backtest.backtest_event_driven) reads self.positions/self.close/
    self.opn/self.tv/self.atr/self.breaker/self.atr_k afterward."""

    def __init__(
        self,
        prices_df, volumes_df, highs_df=None, lows_df=None, opens_df=None,
        # Universe
        universe_top_n=500, min_price=20.0, min_adv=1e7,
        # Signal
        ret_clip=0.50,
        beta_window=252, beta_min=200,
        formation_9m=189, formation_3m=63, formation_skip=21,
        vol_window=63,
        # Position generation
        n=40, enter_rank=30, exit_rank=80,
        dual_horizon=False, recency_veto=False,
        rebalance_freq_months=1,
        z9_weight=1.0, high52_weight=1.0, illiq_weight=0.0, lowpx_weight=0.0,
        beta_shrink=0.0,
        pos_cap=0.12, target_vol=0.20, trend_window=150, corr_guard=True, drift_band=0.03,
        breaker=0.25, atr_k=None,
        trading_days=252,
    ):
        self.close  = prices_df
        self.volume = volumes_df
        self.high   = highs_df if highs_df is not None else pd.DataFrame()
        self.low    = lows_df  if lows_df  is not None else pd.DataFrame()
        self.opn    = opens_df if opens_df is not None else pd.DataFrame()

        self.universe_top_n = universe_top_n
        self.min_price      = min_price
        self.min_adv        = min_adv

        self.ret_clip    = ret_clip
        self.beta_window  = beta_window
        self.beta_min     = beta_min
        self.formation_9m   = formation_9m
        self.formation_3m   = formation_3m
        self.formation_skip = formation_skip
        self.vol_window   = vol_window

        self.n          = n
        self.enter_rank = enter_rank
        self.exit_rank  = exit_rank
        self.dual_horizon = dual_horizon
        self.recency_veto = recency_veto
        self.rebalance_freq_months = rebalance_freq_months

        self.z9_weight     = z9_weight
        self.high52_weight = high52_weight
        self.illiq_weight  = illiq_weight
        self.lowpx_weight  = lowpx_weight
        self.beta_shrink   = beta_shrink

        self.pos_cap     = pos_cap
        self.target_vol  = target_vol
        self.trend_window = trend_window
        self.corr_guard  = corr_guard
        self.drift_band  = drift_band

        self.breaker = breaker
        self.atr_k   = atr_k

        self.trading_days = trading_days

        self.univ      = None
        self.positions  = None
        self.rebalance_dates = None
        self.held_by_t  = None
        self.position_metadata = []   # populated by residual_momentum_backtest.backtest_event_driven()

        print(f"Residual Momentum initialised  |  universe_top_n={universe_top_n}  "
              f"min_price={min_price}  min_adv={min_adv:,.0f}  n={n}  "
              f"enter/exit_rank={enter_rank}/{exit_rank}  pos_cap={pos_cap}  drift_band={drift_band}  "
              f"target_vol={target_vol}  breaker={breaker}  corr_guard={corr_guard}  "
              f"dual_horizon={dual_horizon}  recency_veto={recency_veto}")
        _defaults = dict(rebalance_freq_months=1, z9_weight=1.0, high52_weight=1.0,
                         illiq_weight=0.0, lowpx_weight=0.0, beta_shrink=0.0)
        _changed = {k: v for k, v in dict(rebalance_freq_months=rebalance_freq_months,
                                          z9_weight=z9_weight, high52_weight=high52_weight,
                                          illiq_weight=illiq_weight, lowpx_weight=lowpx_weight,
                                          beta_shrink=beta_shrink).items() if v != _defaults[k]}
        if _changed:
            print(f"  [EXPERIMENTAL — off validated defaults]  "
                  + "  ".join(f"{k}={v}" for k, v in _changed.items()))

    # ──────────────────────────────────────────────────────────────────────────
    # UNIVERSE FILTER
    # ──────────────────────────────────────────────────────────────────────────

    def filter_universe(self):
        """Monthly top-`universe_top_n` by trailing-63d median dollar turnover (close*volume),
        floored by an absolute `min_price`/`min_adv` live-tradability filter and a
        data-quality exclusion, both applied BEFORE the top-N rank cut -- so a thin/cheap or
        glitched name can't qualify just by being "top-N among a thin field" in a low-breadth
        month. ffilled to daily. Look-ahead-safe: membership at month-end t uses only
        turnover/price/glitch history <= t. Sets and returns self.univ."""
        tv = self.close * self.volume
        # min_periods=45 (was 30): raises the bar for a just-listed/IPO-pop name to qualify
        # on a noisy partial window, without requiring a full 63-count window -- that stricter
        # bar was tested and rejected: it also disqualifies long-listed but thinly/gappy-traded
        # early-2000s names (breadth-floor violations jumped from 6% to 26% of months).
        # Stored on self so calculate_factors()'s illiq_z can reuse this exact series instead
        # of recomputing the identical close*volume rolling-median from scratch with a
        # different (and easy to forget to keep in sync) min_periods.
        self.dv = tv.rolling(63, min_periods=45).median()
        advm = self.dv

        # Data-quality guard: a single-day |return| > SPLIT_JUMP_FLAG only excludes a symbol
        # if it does NOT revert within 5 trading days (price stays far from its pre-jump
        # level) -- a genuine unadjusted corporate action / bad-data regime shift, not a
        # one-off bad print (which reverts the very next day and is otherwise harmless: e.g.
        # a name spiking 861% then landing back within 1% the next session). Reverting jumps
        # are left alone so one bad tick doesn't permanently blacklist an otherwise-clean
        # 20-year price series. Excluded from `.shift(10)` trading days after the jump
        # onward, cumulatively -- the 10-day buffer keeps the +5-day reversion check itself
        # point-in-time safe (never visible before its own confirmation window has closed).
        raw_ret = self.close.pct_change(fill_method=None)
        jump = raw_ret.abs() > SPLIT_JUMP_FLAG
        pre, post = self.close.shift(1), self.close.shift(-5)
        spike = (self.close - pre).abs()
        reverted = (post - pre).abs() < 0.5 * spike
        persistent = jump & ~reverted.fillna(False)
        ever_glitched = persistent.shift(10).fillna(False).cummax()
        self.data_glitch_symbols = sorted(ever_glitched.columns[ever_glitched.iloc[-1]])
        if self.data_glitch_symbols:
            sample = self.data_glitch_symbols[:10]
            print(f"[Data-quality] {len(self.data_glitch_symbols)} symbols excluded from the "
                  f"universe from ~10 trading days after a non-reverting |daily return| > "
                  f"{SPLIT_JUMP_FLAG:.0%}: {sample}{'...' if len(self.data_glitch_symbols) > 10 else ''}")

        me = _month_end_days(self.close.index)
        memb = pd.DataFrame(False, index=me, columns=self.close.columns)
        for t in me:
            s = advm.loc[t].dropna()
            s = s[~ever_glitched.loc[t, s.index]]
            if self.min_adv > 0:
                s = s[s >= self.min_adv]
            if self.min_price > 0:
                px = self.close.loc[t, s.index]
                s = s[px >= self.min_price]
            if s.empty:
                continue
            memb.loc[t, s.nlargest(min(self.universe_top_n, len(s))).index] = True
        self.univ = memb.reindex(self.close.index, method="ffill").fillna(False).astype(bool)
        return self.univ

    # ──────────────────────────────────────────────────────────────────────────
    # FACTOR CALCULATION
    # ──────────────────────────────────────────────────────────────────────────

    def calculate_factors(self):
        """CAPM residual momentum:
            r      = daily close-to-close return (clipped)
            r_mkt  = cross-sectional mean of active-universe returns (equal-weighted proxy)
            beta   = rolling CAPM beta
            e      = r - beta * r_mkt   (idiosyncratic residual)
            signal = sum(e) over the formation window, vol-scaled
        Composite R3b = z9_weight*z(9m resid-mom) + high52_weight*z(52w-high ratio) +
        illiq_weight*z(illiquidity) + lowpx_weight*z(low-price). Calls filter_universe() first."""
        self.filter_universe()

        close, opn, high, low, vol_, univ = (self.close, self.opn, self.high,
                                             self.low, self.volume, self.univ)

        self.ret   = _daily_returns(close, self.ret_clip)
        self.mkt   = _market_return(self.ret, univ)
        # .shift(1): beta_t is estimated using data through t-1 only, so today's residual
        # never uses a beta that was itself fit partly on today's own return.
        self.beta_raw = _rolling_beta(self.ret, self.mkt, self.beta_window, self.beta_min).shift(1)
        if self.beta_shrink > 0:
            # Blend the noisy rolling-beta estimate toward 1.0 (market-neutral prior).
            # beta_shrink=0 (default) leaves self.beta == self.beta_raw bit-for-bit.
            self.beta = (1 - self.beta_shrink) * self.beta_raw + self.beta_shrink * 1.0
        else:
            self.beta = self.beta_raw
        self.resid = _residual_returns(self.ret, self.beta, self.mkt, self.ret_clip)
        self.ivol  = _trailing_vol(self.ret, self.vol_window)

        def csz(x):
            x = x.where(univ)
            return x.sub(x.mean(axis=1), axis=0).div(x.std(axis=1), axis=0)

        # self.dv already set by filter_universe() above (called at the top of this method) --
        # reused here rather than recomputed, so the universe's turnover figure and the illiq
        # factor's turnover figure can never silently drift apart.
        self.z9 = csz(_residual_momentum(self.resid, self.formation_9m, self.formation_skip,
                                         scale_by_vol=True))
        self.z3 = csz(_residual_momentum(self.resid, self.formation_3m, self.formation_skip,
                                         scale_by_vol=True))
        self.high52_z = csz(close / close.rolling(252, min_periods=150).max())
        self.illiq_z  = csz(-np.log(self.dv.replace(0, np.nan)))
        self.lowpx_z  = csz(-np.log(close))
        self.R3b = (self.z9_weight * self.z9
                    + self.high52_weight * self.high52_z
                    + self.illiq_weight * self.illiq_z
                    + self.lowpx_weight * self.lowpx_z)

        self.ret21 = close / close.shift(21) - 1
        self.tr = pd.concat([(high - low),
                             (high - close.shift(1)).abs(),
                             (low  - close.shift(1)).abs()]).groupby(level=0).max()
        self.atr = self.tr.rolling(22, min_periods=12).mean()

        self.sv   = self.ret.rolling(63, min_periods=40).var().where(univ).mean(axis=1)
        self.corr = self.mkt.rolling(63, min_periods=40).var() / self.sv
        self.corr_z = ((self.corr - self.corr.rolling(252, min_periods=120).mean())
                       / self.corr.rolling(252, min_periods=120).std())

        self.tv    = close * vol_
        self.days  = close.index
        self.glvl  = (1 + self.mkt.fillna(0)).cumprod()

        print(f"Factors calculated  |  {self.days.min().date()}..{self.days.max().date()}  "
              f"{close.shape[1]} symbols  R3b non-NaN/day (avg): {self.R3b.notna().sum(axis=1).mean():.0f}")
        return self

    def _sigframe(self):
        s = self.R3b
        if self.dual_horizon:
            s = s + 0.5 * self.z3
        return s

    # ──────────────────────────────────────────────────────────────────────────
    # POSITION GENERATION (selection + sizing)
    # ──────────────────────────────────────────────────────────────────────────

    def get_positions(self, start):
        """Monthly cross-sectional ranking with hysteresis (enter_rank/exit_rank), then
        inverse-vol weighting with a position cap, vol-targeting, an SMA trend gate, and a
        correlation guard.

        `start` gates which month-end dates get a real rebalance/selection event — the held
        set restarts fresh (empty) at `start`. This is NOT equivalent to running from the
        earliest date and slicing results afterward, so `start` must reach this method, not
        just final reporting.

        Sets and returns self.positions (dates x tickers target-weight DataFrame)."""
        held_by_t, rebs = self._select_holdings(start)
        self.positions = self._size_weights(held_by_t, rebs)
        self.rebalance_dates = rebs
        self.held_by_t = held_by_t   # cached for reuse (e.g. diagnose_sizing_gaps) so a
                                      # diagnostic replay can't silently diverge from what
                                      # actually ran, and so it doesn't re-run the full
                                      # selection/sizing pass a second time
        print(f"Positions generated  |  {len(rebs)} rebalance months  n={self.n}  "
              f"enter/exit_rank={self.enter_rank}/{self.exit_rank}")
        return self.positions

    def _select_holdings(self, start):
        """rebalance_freq_months>1 keeps every Nth month-end from the FULL data history's
        month-end grid (not from `start`), so cadence stays anchored to calendar months
        regardless of which report window you slice -- e.g. freq=3 always lands on the same
        quarterly dates whether start='2002-01-01' or '2005-06-01'."""
        S = self._sigframe()
        all_rebs = _month_end_days(self.days)
        if self.rebalance_freq_months > 1:
            all_rebs = all_rebs[::self.rebalance_freq_months]
        rebs = all_rebs[all_rebs >= pd.Timestamp(start)]
        rank_r = S.reindex(rebs).rank(axis=1, ascending=False)
        held, out = [], {}
        for t in rebs:
            rk = rank_r.loc[t]
            keep = sorted([h for h in held
                           if not np.isnan(rk.get(h, np.nan)) and rk[h] <= self.exit_rank],
                          key=lambda x: rk[x])[:self.n]
            cand = [c for c in rk[rk <= self.enter_rank].sort_values().index if c not in keep]
            if self.recency_veto:
                cand = [c for c in cand if self.ret21.loc[t].get(c, 0) >= -0.03]
            held = keep + cand[:max(0, self.n - len(keep))]
            out[t] = held
        return out, rebs

    def _size_weights(self, held_by_t, rebs, target=None):
        target = self.target_vol if target is None else target
        gate = self.glvl > self.glvl.rolling(self.trend_window).mean()
        WT = pd.DataFrame(0.0, index=rebs, columns=self.close.columns)
        cap = self.pos_cap
        for t, names in held_by_t.items():
            iv = (1.0 / self.ivol.loc[t, names]).replace([np.inf, -np.inf], np.nan).dropna()
            if iv.empty:
                continue
            w = iv / iv.sum()
            if cap:
                for _ in range(6):
                    over = w > cap
                    if not over.any():
                        break
                    excess = (w[over] - cap).sum()
                    w[over] = cap
                    room = ~over & (w > 0)
                    if room.any():
                        w[room] += excess * w[room] / w[room].sum()
                    else:
                        break   # every held name is already at/over cap -- nothing to redistribute into
                still_over = w[w > cap + 1e-6]
                if len(still_over):
                    print(f"[Sizing] {pd.Timestamp(t).date()}: {len(still_over)} name(s) still "
                          f"above pos_cap={cap} after 6 redistribution passes -- n/pos_cap may be "
                          f"too tight to fully converge; shipping the slightly-over-cap weights.")
            rv = (self.ret.loc[:t, w.index].tail(self.vol_window) * w).sum(axis=1).std() * np.sqrt(self.trading_days)
            vt = float(np.clip(target / rv, 0, 1)) if rv > 0 else 1.0
            exp = vt * (1.0 if bool(gate.get(t, False)) else 0.0)
            if self.corr_guard:
                exp *= float(np.clip(1 - 0.5 * max(0.0, self.corr_z.get(t, 0.0)), 0.5, 1.0))
            WT.loc[t] = (w * exp).reindex(self.close.columns).fillna(0.0).values
        return WT