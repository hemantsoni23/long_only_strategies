"""
csm_aegis_strategy.py
=====================
CSM Aegis -- strategy CORE (signal, universe, selection, entry filters, stops, sizing, risk overlays, live helpers).
The daily event loop, booking, reports, output files and command-line runner live in csm_aegis_backtest.py.

STRATEGY IN ONE PAGE
--------------------
Signal      v1.2/v1.3/v1.4: score = z(R1) + z(-Ulcer252) inside the pool.
              R1     residual (beta-stripped) 12m momentum, window [t-252, t-21], vol-scaled (beta: 252d, lagged 1d, vs the EW universe)
              Ulcer  RMS drawdown from the rolling 252d closing high (smooth compounders score high)
            presets: 'v1.4_low_dd' (v1.3 plus daily ADX/DMI quality gate and GOLDBEES idle-cash sleeve), 'v1.3' (frozen equity-only comparator), 'v1.2' (frozen comparator),
            'v1.2_high_return' (R1 + 52w-high proximity, band 200-1000: opt-in), 'v1.1' and 'v1.0' (open fills,
            reproduction only).
Universe    1. price >= min_price
            2. rank by 63d average rupee volume (prior day) inside [universe_min_rank, universe_max_rank]
            3. <= max_circuit_days circuit-locked sessions in the last 63
            4. close above SMA-200 (trend gate)
            5. worst 20% by M3 (largest 1-month single-day spike) removed ("lottery" exclusion)
            (optional) absolute-momentum gate, falling-knife gate
Selection   month-end close: rank the pool; buy ranks <= top_n; a held name stays until rank > hold_rank (hysteresis) or it leaves the pool.
            v1.3 additionally rejects fresh five-day price spikes and allows at most two names per Industry_clean label;
            v1.4 additionally requires ADX(14)>=25 and +DI>-DI for fresh entries.
Regime      market trend gate: month-end EW market index <= its SMA(mkt_gate_window) -> exit everything, no entries.
            vol-state gate: no NEW entries while 63d benchmark vol > its expanding 85th percentile.
            regime leverage reduces stock exposure in bear/panic states; crash guard, vol targeting and corr guard are optional.
Entry       fill='close': decided at a close, filled at the NEXT close (the data's open field is not a tradable price);
            names more than ext_x above their SMA-50 are skipped (extension filter); fill='open' adds a gap-up cancel.
            A fill requires a raw, positive-price OHLC bar with positive volume and no high==low circuit lock; forward-filled closes are indicators/marks only.
Exits       hard stop -stop from entry | trailing stop -trail from peak close | time stop | rank/pool exit | market gate | (optional) crash guard.
            All triggers use CLOSES; execution is at the next fill. One implementation (check_stop_exit) serves backtest and live.
Sizing      risk-based: weight = risk_pct_per_trade / stop, clamped to [w_lo, w_hi]; gross <= max_gross of equity.
Booking     faithful: positions drift, exit day charged, transaction cost is charged per leg, idle cash earns zero, and fills require raw tradable OHLCV bars.
Secondary   optional GOLDBEES/SILVERBEES sleeve can sweep idle cash at raw tradable ETF closes. It is an always-on
            cash sweep (so market-gate/bear/panic cash naturally moves to the ETF), not a conditional hedge. GOLDBEES is
            the candidate to validate; SILVERBEES has only a short history and is research-only.

Research switches (mostly default OFF, kept so the tests can be re-run): risk_adjusted_signal, entry_spike_filter, entry_path_filter, entry_turnover_filter, liq_mode (six OHLCV liquidity filters), atr_stops, chandelier, loss_cooldown, stop_cooldown_days,
min_hold_stops, abs_momentum_gate, falling_knife_gate, quarterly_entries, inverse_vol_sizing, vol_target, corr_guard, crash_guard, resting_stop, placebo_seed. Regime leverage is enabled by the current configuration.
Pre-registered and validated in decay_check/PREREG.md (Addenda 4-8). Nothing here was tuned beyond what those addenda report; evidence summary in README.md.
"""
import os
import glob
from collections import Counter
import numpy as np
import pandas as pd

DEFAULT_INSTRUMENTS_FILE = os.environ.get(
    "CSM_AEGIS_INSTRUMENTS_FILE",
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "instruments_clean.csv"),
)
DEFAULT_SECONDARY_ETF_DIR = os.environ.get(
    "CSM_AEGIS_ETF_DATA_FOLDER",
    "/Users/hemantsoni/Documents/upstox_data_folder/gold_silver_ohlcv_data",
)
SECONDARY_ETF_CHOICES = (None, "GOLDBEES", "SILVERBEES")

# ══════════════════════════════════════════════════════════════════════════════
# PRESETS  (keyword overrides for CSMAegis.__init__)
# ══════════════════════════════════════════════════════════════════════════════
PRESETS = {
    "v1.3": dict(selector="R1_ULCER", mkt_gate_window=120, fill="close", entry_spike_filter=True, entry_spike_window=5, entry_spike_quantile=0.80, industry_cap=2),
    # Drawdown-focused promotion from the isolated ADX experiment. The ETF is
    # real invested capital, not a risk-free/cash-return assumption.
    "v1.4_low_dd": dict(selector="R1_ULCER", mkt_gate_window=120, fill="close", entry_spike_filter=True, entry_spike_window=5, entry_spike_quantile=0.80, industry_cap=2,
                          adx_entry_filter=True, adx_window=14, adx_threshold=25.0, adx_require_positive_di=True, secondary_etf="GOLDBEES"),
    "v1.2": dict(selector="R1_ULCER", mkt_gate_window=120, fill="close"),  # frozen comparator; uninvested cash has no modeled return
    "v1.2_high_return": dict(selector="R1_A1", mkt_gate_window=120, fill="close", universe_min_rank=200),
    "v1.1": dict(selector="R1", mkt_gate_window=150, fill="open"),
    "v1.0": dict(selector="R1", mkt_gate=False, fill="open"),
}


# ══════════════════════════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════════════════════════
def load_data(folder_path, cache_dir=None, min_names=2000):
    """Per-symbol OHLCV CSVs -> (prices, volumes, highs, lows, opens) aligned DataFrames (date x symbol).
    Cleaning identical to factor_research/data.py: duplicate dates dropped, non-positive prices -> NaN, any close-to-close move outside
    [-40%, +300%] masks O/H/L/C for that day (un-adjusted splits/bonus/bad prints), calendar days with < 30 live names dropped,
    series cut at the last day with >= min_names live names. Optional parquet cache."""
    if not folder_path or not os.path.isdir(folder_path):
        raise FileNotFoundError("Daily OHLCV folder is missing. Set CSM_AEGIS_DATA_FOLDER or pass --data-folder.")
    fields = ("open", "high", "low", "close", "volume")
    if cache_dir and os.path.exists(os.path.join(cache_dir, "close.parquet")):
        missing_cache = [f for f in fields if not os.path.exists(os.path.join(cache_dir, f"{f}.parquet"))]
        if missing_cache:
            raise FileNotFoundError(f"Incomplete panel cache {cache_dir}: missing {', '.join(missing_cache)}")
        P = {f: pd.read_parquet(os.path.join(cache_dir, f"{f}.parquet")).astype("float64") for f in fields}
    else:
        frames = {}
        for path in sorted(glob.glob(os.path.join(folder_path, "*.csv"))):
            try:
                df = pd.read_csv(path, usecols=["datetime", "open", "high", "low", "close", "volume"], parse_dates=["datetime"], index_col="datetime")
            except Exception:
                continue
            df = df[~df.index.duplicated(keep="last")]
            for c in ("open", "high", "low", "close"):
                df[c] = df[c].mask(df[c] <= 0)
            if len(df):
                frames[os.path.basename(path)[:-4]] = df.astype("float64")
        if not frames:
            raise ValueError("No valid daily OHLCV CSVs found. Each file needs datetime,open,high,low,close,volume columns.")
        P = {f: pd.DataFrame({s: d[f] for s, d in frames.items()}).sort_index() for f in fields}
        keep = P["close"].notna().sum(axis=1) >= 30
        P = {f: d.loc[keep] for f, d in P.items()}
        r = P["close"].pct_change(fill_method=None)
        bad = (r < -0.40) | (r > 3.00)
        for f in ("open", "high", "low", "close"):
            P[f] = P[f].mask(bad)
        if cache_dir:
            os.makedirs(cache_dir, exist_ok=True)
            for f, d in P.items():
                d.astype("float32").to_parquet(os.path.join(cache_dir, f"{f}.parquet"))
    n_live = P["close"].notna().sum(axis=1)
    if not (n_live >= min_names).any():
        raise ValueError(f"No session has the required {min_names} live names; check the panel or lower min_names deliberately.")
    last_ok = n_live[n_live >= min_names].index.max()
    P = {f: d.loc[:last_ok] for f, d in P.items()}
    return P["close"], P["volume"], P["high"], P["low"], P["open"]


def build_benchmark(prices):
    """Equal-weight index of all listed names (daily returns clipped at +-50%, averaged, compounded). Used for the market gate and vol state."""
    r = prices.pct_change(fill_method=None).clip(-0.5, 0.5).mean(axis=1, skipna=True).fillna(0.0)
    return (1 + r).cumprod()


class Holding:
    """One open position. v = unscaled notional (fraction of equity at entry, then drifting); the live exposure is multiplier * v."""
    __slots__ = ("v", "entry_px", "entry_idx", "peak", "entry_date", "w_rel", "min_close", "max_close", "rank_at_entry", "score_at_entry", "signal_date", "regime")

    def __init__(self, v, entry_px, entry_idx, entry_date, w_rel, rank_at_entry=np.nan, score_at_entry=np.nan, signal_date=None, regime=""):
        self.v, self.entry_px, self.entry_idx, self.peak = v, entry_px, entry_idx, entry_px
        self.entry_date, self.w_rel = entry_date, w_rel
        self.min_close = self.max_close = entry_px
        self.rank_at_entry, self.score_at_entry, self.signal_date, self.regime = rank_at_entry, score_at_entry, signal_date, regime


# ══════════════════════════════════════════════════════════════════════════════
# STRATEGY
# ══════════════════════════════════════════════════════════════════════════════
class CSMAegis:
    def __init__(
        self,
        prices_df, volumes_df, highs_df, lows_df, opens_df, benchmark_series=None,
        # ── Signal ──────────────────────────────────────────────────────────────
        selector="R1_ULCER",            # 'R1' | 'R1_ULCER' | 'R1_A1'
        beta_window=252, beta_min_periods=200,      # R1 residual beta window (days), lagged 1 day
        r1_window=231, r1_skip=21,                  # R1 sums residuals over [t-252, t-21]
        risk_adjusted_signal=False, ramom_horizon=12, ramom_fast_alpha=0.50,
                                                        # research: average lagged-fast-vol-normalized residual returns (RAMOM-style) over the R1 formation window
        ulcer_window=252,
        # ── Universe ────────────────────────────────────────────────────────────
        universe_min_rank=1, universe_max_rank=1000,   # rank by 63d avg rupee volume (prior day)
        min_price=20.0, max_circuit_days=5,
        liq_mode="dv63",                # 'dv63' (default, 63d mean rupee volume rank) | research alternatives: 'floor20' | 'floor20_abs' | 'amihud' | 'continuity' | 'cvvol' | 'cs_spread' | 'tradability' | 'tradability_log'
        trend_gate=True,                # close > SMA-200
        m3_exclusion=True, m3_quantile=0.20,           # drop the worst 20% by M3 (largest 1-day spike in the last month)
        abs_momentum_gate=False,        # 12m return (skip 1m) > 0            (momentum-book gate, tested: not adopted)
        falling_knife_gate=False,       # previous month's return >= -15%      (momentum-book gate, tested: not adopted)
        # ── Selection ───────────────────────────────────────────────────────────
        top_n=20, hold_rank=40,
        quarterly_entries=False,        # entries only Jan/Apr/Jul/Oct month-ends (tested: not adopted)
        industry_cap=0, industry_labels_path=DEFAULT_INSTRUMENTS_FILE, industry_label_seed=None,
                                                        # research: maximum names per Industry_clean label; 0 disables it
        # ── Entry filters ───────────────────────────────────────────────────────
        extension_filter=True, extension_x=0.25,       # skip names more than 25% above their SMA-50
        entry_spike_filter=False, entry_spike_window=5, entry_spike_quantile=0.80,
                                                        # research: fresh entries only; reject a name whose trailing raw-close return is above this eligible-pool percentile
        entry_path_filter=False, entry_path_quantile=0.80,
                                                        # research: fresh entries only; reject the most jump-driven eligible price paths (Frog-in-the-Pan ID, same 12m-skip-1m window as R1)
        entry_turnover_filter=False, turnover_fast_window=21, turnover_slow_window=252, turnover_quantile=0.80,
                                                        # research: fresh entries only; reject the highest abnormal rupee-turnover names (fast mean / slow median)
        adx_entry_filter=False, adx_window=14, adx_threshold=25.0, adx_require_positive_di=True,
                                                        # v1.4 low-DD gate: fresh entries need daily ADX >= threshold and +DI > -DI
        vol_gate=True, vol_gate_pctile=0.85,           # no new entries when 63d benchmark vol > expanding 85th pct (needs 5y of history)
        gap_cancel=0.03,                # fill='open' only: skip if the open gaps up more than this
        # ── Market regime ───────────────────────────────────────────────────────
        mkt_gate=True, mkt_gate_window=120,
        # ── Stops ───────────────────────────────────────────────────────────────
        stop_from_entry=0.15, trail_from_peak=0.20,
        atr_stops=False, atr_stop_mult=3.0, atr_stop_lo=0.08, atr_stop_hi=0.18,   # per-name initial stop = clip(mult * ATR14 / close, lo, hi); weight = risk / stop (research, off by default)
        time_stop=True, time_stop_days=45, time_stop_loss=-0.05,
        min_hold_stops=False, chandelier=False,        # min-hold 5d / ATR chandelier (tested: not adopted)
        resting_stop=False,             # research only: intraday stop fills
        loss_cooldown=False,            # re-entry cooldown after a losing stop (tested: not adopted)
        stop_cooldown_days=0,           # research: fixed calendar-day re-entry ban after every STOP_ENTRY/STOP_TRAIL (Zenith/Batch convention)
        # ── Sizing ──────────────────────────────────────────────────────────────
        risk_sizing=True, risk_pct_per_trade=0.01, w_lo=0.03, w_hi=0.08, w_equal=0.05, max_gross=1.0,
        inverse_vol_sizing=False,
        # ── Risk overlays (regime leverage enabled; other overlays opt-in) ──────
        vol_target=None,                # e.g. 0.15: exposure multiplier = min(1, target / ex-ante 63d vol of current holdings)
        regime_leverage=True, leverage_bear=0.6, leverage_panic=0.3,
        corr_guard=False, corr_guard_threshold=0.8,
        crash_guard=False, crash_guard_cooldown=10,
        # ── Execution ───────────────────────────────────────────────────────────
        fill="close",                   # 'close' (v1.2, recommended) | 'open'
        require_tradable_fill=True,      # raw bar must have price, volume and range; disable only to reproduce legacy research
        transaction_cost=0.003,
        adv_fraction=None,              # cap each position at this share of 63d median rupee volume (capacity)
        execution_delay=0,              # extra days between decision and fill (stress test)
        secondary_etf=None,             # None | GOLDBEES | SILVERBEES; sweeps all idle cash when its raw ETF bar is tradable
        secondary_etf_data_dir=DEFAULT_SECONDARY_ETF_DIR,
        secondary_transaction_cost=None, # defaults to transaction_cost when None
        start="2005-01-01",
        placebo_seed=None,              # research: random picks through the identical wrapper
        initial_capital=1.0,
    ):
        self.prices, self.volumes, self.highs, self.lows, self.opens = prices_df, volumes_df, highs_df, lows_df, opens_df
        self.benchmark = benchmark_series if benchmark_series is not None else build_benchmark(prices_df)
        loc = dict(locals()); loc.pop("self"); [loc.pop(k) for k in ("prices_df", "volumes_df", "highs_df", "lows_df", "opens_df", "benchmark_series")]
        self.p = loc
        for k, v in loc.items():
            setattr(self, k, v)
        assert selector in ("R1", "R1_ULCER", "R1_A1"), selector
        assert fill in ("close", "open"), fill
        assert liq_mode in ("dv63", "floor20", "floor20_abs", "amihud", "continuity", "cvvol", "cs_spread", "tradability", "tradability_log"), liq_mode
        assert entry_spike_window >= 1, entry_spike_window
        assert 0 < entry_spike_quantile < 1, entry_spike_quantile
        assert 0 < entry_path_quantile < 1, entry_path_quantile
        assert turnover_fast_window >= 1 and turnover_slow_window >= turnover_fast_window, (turnover_fast_window, turnover_slow_window)
        assert 0 < turnover_quantile < 1, turnover_quantile
        assert adx_window >= 2 and adx_threshold >= 0, (adx_window, adx_threshold)
        assert ramom_horizon >= 2 and ramom_horizon < r1_window, (ramom_horizon, r1_window)
        assert 0 < ramom_fast_alpha < 1, ramom_fast_alpha
        assert stop_cooldown_days >= 0, stop_cooldown_days
        assert industry_cap >= 0, industry_cap
        assert secondary_etf in SECONDARY_ETF_CHOICES, secondary_etf
        if secondary_transaction_cost is not None:
            assert secondary_transaction_cost >= 0, secondary_transaction_cost
        self.industry_labels = self._load_industry_labels(industry_labels_path, industry_label_seed) if industry_cap else {}
        self._ready = False

    @staticmethod
    def _load_industry_labels(path, label_seed=None):
        """Ticker -> Industry_clean. A cap must never silently guess a group.

        `label_seed` is a research-only placebo: it permutes labels while
        preserving group sizes, and must remain None in a production preset.
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"industry_cap requires a label file: {path}")
        labels = pd.read_csv(path, usecols=["trading_symbol", "Industry_clean"])
        labels = labels.dropna(subset=["trading_symbol", "Industry_clean"]).drop_duplicates("trading_symbol", keep="last")
        labels["Industry_clean"] = labels["Industry_clean"].astype(str).str.strip()
        labels = labels[labels["Industry_clean"] != ""]
        mapping = labels.set_index("trading_symbol")["Industry_clean"].to_dict()
        if label_seed is not None:
            tickers = list(mapping)
            values = np.asarray([mapping[ticker] for ticker in tickers], dtype=object)
            mapping = dict(zip(tickers, np.random.default_rng(label_seed).permutation(values)))
        return mapping

    # ── construction helpers ────────────────────────────────────────────────────
    @classmethod
    def from_preset(cls, preset, prices_df, volumes_df, highs_df, lows_df, opens_df, benchmark_series=None, **overrides):
        kw = dict(PRESETS[preset]); kw.update(overrides)
        return cls(prices_df, volumes_df, highs_df, lows_df, opens_df, benchmark_series, **kw)

    @classmethod
    def from_panels(cls, panels, **kw):
        return cls(panels["close"], panels["volume"], panels["high"], panels["low"], panels["open"], None, **kw)

    @staticmethod
    def execution_bar_reason(close, volume, high, low, fill_price):
        """Return the reason an OHLCV bar cannot support a conservative fill.

        Indicators and portfolio marks may carry a prior close forward, but a
        broker order needs an observed bar.  A high==low session is treated as
        a non-fillable circuit lock for either side; this is deliberately
        conservative because daily OHLCV does not reveal queue priority.
        """
        if not (np.isfinite(close) and close > 0 and np.isfinite(fill_price) and fill_price > 0):
            return "STALE_OR_MISSING_PRICE"
        if not (np.isfinite(volume) and volume > 0):
            return "NO_VOLUME"
        if not (np.isfinite(high) and high > 0 and np.isfinite(low) and low > 0):
            return "MISSING_OHLC"
        if high == low:
            return "CIRCUIT_LOCK"
        return None

    def fillability_reason(self, i, j, fill="close"):
        """Raw-bar execution validation for a proposed close/open fill."""
        fill_price = self.C_RAW[i, j] if fill == "close" else self.O[i, j]
        return self.execution_bar_reason(self.C_RAW[i, j], self.V[i, j], self.H[i, j], self.L[i, j], fill_price)

    # ══════════════════════════════════════════════════════════════════════════
    # FACTORS
    # ══════════════════════════════════════════════════════════════════════════
    def calculate_factors(self):
        """Compute everything that is known at a month-end close (no look-ahead): signals, pool inputs, regime series, daily arrays."""
        close, high, low, vol = self.prices, self.highs, self.lows, self.volumes
        self.dates, self.cols = close.index, list(close.columns)
        cf = close.ffill(limit=10)
        ret = close.pct_change(fill_method=None)
        bench_ret = ret.clip(-0.5, 0.5).mean(axis=1, skipna=True).fillna(0.0)
        s = pd.Series(self.dates, index=self.dates)
        me = pd.DatetimeIndex(s.groupby(self.dates.to_period("M")).max().values)
        me = me[me >= pd.Timestamp("2004-06-01")]
        self.me, self.me_idx, self.per = me, [self.dates.get_loc(d) for d in me], pd.PeriodIndex(me, freq="M")

        # R1: residual momentum -------------------------------------------------
        mk = bench_ret
        w, mp = self.beta_window, self.beta_min_periods
        mean_m = mk.rolling(w, min_periods=mp).mean()
        var_m = (mk * mk).rolling(w, min_periods=mp).mean() - mean_m ** 2
        rr = ret.clip(-0.5, 0.5)
        cov = rr.mul(mk, axis=0).rolling(w, min_periods=mp).mean() - rr.rolling(w, min_periods=mp).mean().mul(mean_m, axis=0)
        beta = cov.div(var_m.replace(0, np.nan), axis=0).shift(1)
        resid = rr.sub(beta.mul(mk, axis=0)).clip(-0.5, 0.5)
        r1_standard = resid.rolling(self.r1_window, min_periods=180).sum().shift(self.r1_skip) / resid.rolling(self.r1_window, min_periods=180).std().shift(self.r1_skip)
        # RAMOM-style signal engineering: a 12-day residual return is scaled by
        # a one-day-lagged fast EWMA volatility estimate before aggregation. The
        # shorter aggregation window keeps the effective formation span equal to
        # R1's [t-252, t-21] interval. It changes the rank signal only; sizing,
        # execution, and all gates are untouched.
        fast_vol = np.sqrt((resid ** 2).ewm(alpha=self.ramom_fast_alpha, adjust=False, min_periods=self.ramom_horizon).mean()).shift(1)
        ramom_days = resid.rolling(self.ramom_horizon, min_periods=self.ramom_horizon - 2).sum().div(fast_vol)
        ramom_window = self.r1_window - self.ramom_horizon + 1
        r1_ramom = ramom_days.rolling(ramom_window, min_periods=max(160, ramom_window - 40)).mean().shift(self.r1_skip)
        r1 = r1_ramom if self.risk_adjusted_signal else r1_standard
        # Ulcer, 52w-high proximity, M3 -------------------------------------------
        dd = cf / cf.rolling(self.ulcer_window, min_periods=200).max() - 1
        ulcer_neg = -np.sqrt((dd ** 2).rolling(self.ulcer_window, min_periods=200).mean())
        a1 = cf / high.rolling(252, min_periods=200).max()
        m3 = -ret.rolling(21, min_periods=15).max()
        self.R1, self.ULC, self.A1, self.M3 = (x.loc[me].values.astype("float64") for x in (r1, ulcer_neg, a1, m3))
        self.R1_frame = r1.loc[me]
        # pool inputs ---------------------------------------------------------------
        sma200, sma50 = cf.rolling(200, min_periods=150).mean(), cf.rolling(50, min_periods=40).mean()
        circ = (high == low).rolling(63, min_periods=1).sum()
        dv = (close * vol).rolling(63, min_periods=45).mean().shift(1)
        self.sma200_me, self.sma50_me, self.circ_me = sma200.loc[me].values, sma50.loc[me].values, circ.loc[me].values
        self.dv_rank_me = dv.loc[me].rank(axis=1, ascending=False, method="min").values
        self.liq_extra_me = self._liquidity_variant(close, high, low, vol, ret, me) if self.liq_mode != "dv63" else None
        self.r121_me = (cf.shift(21) / cf.shift(252) - 1).loc[me].values
        cm = cf.loc[me].values
        self.prev_ret_me = np.full_like(cm, np.nan)
        self.prev_ret_me[2:] = cm[1:-1] / cm[:-2] - 1
        self.vol21_me = ret.rolling(21, min_periods=15).std().loc[me].values
        # Raw close return, available at the signal close.  It intentionally uses
        # no forward filling: stale/missing prices must not make a name look calm.
        self.entry_spike_ret_me = close.pct_change(self.entry_spike_window, fill_method=None).loc[me].values
        # Frog-in-the-Pan information discreteness (Da, Gurun & Warachka):
        # sign(12m-skip-1m return) * (negative-day share - positive-day share).
        # Lower values describe a more gradual same-signed path.  Missing/stale
        # prices do not count as directional days.
        direction = np.sign(ret)
        pos_days = (direction > 0).astype(float).rolling(self.r1_window, min_periods=180).sum().shift(self.r1_skip)
        neg_days = (direction < 0).astype(float).rolling(self.r1_window, min_periods=180).sum().shift(self.r1_skip)
        path_days = pos_days + neg_days
        path_return = close.shift(self.r1_skip) / close.shift(self.r1_window + self.r1_skip) - 1
        path_id = np.sign(path_return) * (neg_days - pos_days) / path_days.replace(0, np.nan)
        self.entry_path_id_me = path_id.loc[me].values
        # Abnormal rupee turnover: a stock's recent participation relative to its
        # own history. This is an attention/crowding proxy, not the universe
        # liquidity measure (which ranks absolute 63d rupee volume).
        dvol = close * vol
        turnover_fast = dvol.rolling(self.turnover_fast_window, min_periods=max(10, self.turnover_fast_window // 2)).mean()
        turnover_slow = dvol.rolling(self.turnover_slow_window, min_periods=max(126, self.turnover_slow_window // 2)).median()
        self.entry_turnover_ratio_me = (turnover_fast / turnover_slow.replace(0, np.nan)).loc[me].values
        # ADX/DMI is a fresh-entry trend-quality confirmation for the low-DD
        # preset. It uses only completed daily OHLC bars at the signal close.
        # Existing positions are deliberately not rank-exited if ADX later fades.
        prior_close = close.ffill(limit=10).shift(1)
        dmi_tr = pd.concat([(high - low), (high - prior_close).abs(), (low - prior_close).abs()]).groupby(level=0).max()
        dmi_up, dmi_down = high.diff(), -low.diff()
        plus_dm = dmi_up.where((dmi_up > dmi_down) & (dmi_up > 0), 0.0).where(high.notna() & low.notna())
        minus_dm = dmi_down.where((dmi_down > dmi_up) & (dmi_down > 0), 0.0).where(high.notna() & low.notna())
        dmi_alpha = 1.0 / self.adx_window
        dmi_atr = dmi_tr.ewm(alpha=dmi_alpha, adjust=False, min_periods=self.adx_window).mean()
        plus_di = 100 * plus_dm.ewm(alpha=dmi_alpha, adjust=False, min_periods=self.adx_window).mean().div(dmi_atr.replace(0, np.nan))
        minus_di = 100 * minus_dm.ewm(alpha=dmi_alpha, adjust=False, min_periods=self.adx_window).mean().div(dmi_atr.replace(0, np.nan))
        dx = 100 * (plus_di - minus_di).abs().div((plus_di + minus_di).replace(0, np.nan))
        adx = dx.ewm(alpha=dmi_alpha, adjust=False, min_periods=self.adx_window).mean()
        self.ADX_ME, self.PLUS_DI_ME, self.MINUS_DI_ME = (x.loc[me].values.astype("float32") for x in (adx, plus_di, minus_di))
        # regime series ---------------------------------------------------------------
        bvol = bench_ret.rolling(63).std()
        self.vol_gate_me = (bvol > bvol.expanding(min_periods=1260).quantile(self.vol_gate_pctile)).loc[me].values
        bvol21 = bench_ret.rolling(21).std().shift(1)
        self.panic = (bvol21 > bvol21.expanding(min_periods=126).quantile(0.95)).fillna(False).values
        self.bench = (1 + bench_ret).cumprod().values
        self._sma_cache = {}
        # daily arrays -----------------------------------------------------------------
        pc = cf.shift(1)
        tr = pd.concat([(high - low), (high - pc).abs(), (low - pc).abs()]).groupby(level=0).max()
        self.ATR = tr.ewm(com=13, adjust=False, min_periods=14).mean().shift(1).values
        # Raw arrays are exclusively for executable fills.  `CL` retains the
        # bounded forward fill used by legacy indicators/stops, while `MARK_CL`
        # and returns carry the last observed close for faithful position marks
        # across a temporary data gap.
        mark_close = close.ffill()
        self.C_RAW, self.V = close.values, vol.values
        self.O, self.H, self.L, self.CL, self.MARK_CL = self.opens.values, high.values, low.values, cf.values, mark_close.values
        # Explicit legacy reproduction retains the historical return series for
        # bit-for-bit parity. The production execution model carries the last
        # observed mark across a gap so the catch-up move is not discarded.
        mark_ret = mark_close.pct_change(fill_method=None).fillna(0.0)
        self.RET = (mark_ret if self.require_tradable_fill else ret.fillna(0.0)).values
        self.ADV = (close * vol).rolling(63, min_periods=21).median().shift(1).values
        self.factors = None            # filled by build_factor_frame()
        self._ready = True
        return self

    def _liquidity_variant(self, close, high, low, vol, ret, me, window=63):
        """Alternative liquidity measures from OHLCV only (research). All shifted one day like the default dv63 rank. Returns (rank_array or None, mask_array or None, spread_array or None)."""
        dvol = close * vol
        mode = self.liq_mode
        at = lambda x: x.shift(1).loc[me].values
        if mode in ("floor20", "floor20_abs", "tradability", "tradability_log"):
            floor = at(dvol.rolling(window, min_periods=45).quantile(0.20))
        if mode in ("amihud", "tradability", "tradability_log"):
            illiq = (ret.abs() / dvol.replace(0, np.nan)).rolling(window, min_periods=45).mean()
            cap = at(-np.log(illiq.replace(0, np.nan)))
        if mode in ("continuity", "tradability", "tradability_log"):
            cont = at(((vol > 0) & (high > low)).astype(float).where(close.notna()).rolling(126 if mode == "continuity" else window, min_periods=40).mean())
        rank = mask = spread = None
        rk = lambda a: pd.DataFrame(a).rank(axis=1, ascending=False, method="min").values
        if mode == "floor20":
            rank = rk(floor)
        elif mode == "floor20_abs":
            mask = floor >= 2.5e6
        elif mode == "amihud":
            rank = rk(cap)
        elif mode == "continuity":
            mask = cont >= 0.95
        elif mode == "cvvol":
            mask = at(vol.rolling(window, min_periods=45).std() / vol.rolling(window, min_periods=45).mean().replace(0, np.nan)) <= 1.8
        elif mode == "cs_spread":
            hl = np.log(high / low).where(high > low)
            h2, l2 = high.combine(high.shift(1), np.maximum), low.combine(low.shift(1), np.minimum)
            beta = hl ** 2 + hl.shift(1) ** 2
            gamma = np.log(h2 / l2) ** 2
            k0 = 3 - 2 * np.sqrt(2)
            alpha = (np.sqrt(2 * beta) - np.sqrt(beta)) / k0 - np.sqrt(gamma / k0)
            sp = (2 * (np.exp(alpha) - 1) / (1 + np.exp(alpha))).clip(lower=0)
            spread = at(sp.rolling(21, min_periods=10).mean())
        elif mode in ("tradability", "tradability_log"):
            zz = lambda a: (a - np.nanmean(a, axis=1, keepdims=True)) / np.nanstd(a, axis=1, keepdims=True)
            f = np.log(np.where(floor > 0, floor, np.nan)) if mode == "tradability_log" else floor
            rank = rk(zz(f) + 0.5 * zz(cap) + 0.5 * zz(cont))
        return rank, mask, spread

    def build_factor_frame(self):
        """Month x symbol DataFrame of the final selector score inside the pool (NaN outside). Used by IC diagnostics and universe card."""
        rows = [self.score_pool(k)[1] for k in range(len(self.me))]
        self.factors = pd.DataFrame(rows, index=self.per, columns=self.cols)
        return self.factors

    def bench_sma(self, window=None):
        w = int(window or self.mkt_gate_window)
        if w not in self._sma_cache:
            self._sma_cache[w] = pd.Series(self.bench).rolling(w).mean().values
        return self._sma_cache[w]

    # ══════════════════════════════════════════════════════════════════════════
    # UNIVERSE
    # ══════════════════════════════════════════════════════════════════════════
    def filter_universe(self, k, with_counts=False):
        """Eligibility mask at month-end k. Every filter uses information available at that close.
        with_counts=True also returns the funnel (names surviving each step) for the universe card."""
        px = self.CL[self.me_idx[k]]
        counts = {"listed": int(np.isfinite(px).sum())}
        elig = np.isfinite(px) & (px >= self.min_price) & (self.circ_me[k] <= self.max_circuit_days)
        counts["price & circuit"] = int(elig.sum())
        rk = self.dv_rank_me[k]
        if self.liq_extra_me is not None and self.liq_extra_me[0] is not None:
            rk = self.liq_extra_me[0][k]
        elig &= (rk >= self.universe_min_rank) & (rk <= self.universe_max_rank)
        if self.liq_extra_me is not None:
            if self.liq_extra_me[1] is not None:
                elig &= self.liq_extra_me[1][k]
            if self.liq_extra_me[2] is not None:                    # drop the worst 15% by spread proxy among the band
                sp = self.liq_extra_me[2][k]
                ok = elig & np.isfinite(sp)
                if ok.sum() > 50:
                    elig &= ~(np.isfinite(sp) & (sp > np.nanquantile(sp[ok], 0.85)))
        counts["liquidity band"] = int(elig.sum())
        if self.trend_gate:
            elig &= px > self.sma200_me[k]
        counts["trend gate (close>SMA200)"] = int(elig.sum())
        if self.abs_momentum_gate:
            elig &= np.nan_to_num(self.r121_me[k], nan=-1.0) > 0
        if self.falling_knife_gate:
            elig &= np.nan_to_num(self.prev_ret_me[k], nan=0.0) >= -0.15
        if self.m3_exclusion:
            m3 = self.M3[k]
            ok = elig & np.isfinite(m3)
            if ok.sum() > 50:
                thr = np.nanquantile(m3[ok], self.m3_quantile)
                elig &= ~(np.isfinite(m3) & (m3 < thr))
        counts["M3 exclusion (final pool)"] = int(elig.sum())
        return (elig, counts) if with_counts else elig

    def universe_card(self):
        """Average funnel by calendar year (names surviving each filter) -- 'is the pool what I think it is'."""
        rows = []
        for k in range(len(self.me)):
            if self.me[k] < pd.Timestamp("2005-01-01"):
                continue
            _, c = self.filter_universe(k, with_counts=True)
            c["year"] = self.me[k].year
            rows.append(c)
        return pd.DataFrame(rows).groupby("year").mean().round(0).astype(int)

    # ══════════════════════════════════════════════════════════════════════════
    # SIGNAL / SELECTION
    # ══════════════════════════════════════════════════════════════════════════
    @staticmethod
    def _z(x, m):
        v = np.where(m, x, np.nan)
        return (v - np.nanmean(v)) / (np.nanstd(v) + 1e-12)

    def score_pool(self, k, rng=None):
        """(eligibility mask, selector score array) at month-end k. Higher = better; NaN outside the pool."""
        elig = self.filter_universe(k)
        a = self.R1[k]
        if self.selector == "R1":
            sc = np.where(elig, a, np.nan)
        else:
            b = self.ULC[k] if self.selector == "R1_ULCER" else self.A1[k]
            sc = np.where(elig, self._z(a, elig & np.isfinite(a)) + self._z(b, elig & np.isfinite(b)), np.nan)
        sc = np.where(np.isfinite(sc) & elig, sc, np.nan)
        if rng is not None:                                   # placebo: same pool, random order
            sc = np.where(elig, rng.random(len(elig)), np.nan)
        return elig, sc

    def rank_pool(self, sc):
        nvalid = int(np.isfinite(sc).sum())
        order = np.argsort(-np.where(np.isfinite(sc), sc, -np.inf))
        rank = np.full(len(self.cols), 10 ** 6)
        rank[order[:nvalid]] = np.arange(1, nvalid + 1)
        return order, rank, nvalid

    def market_gate_off(self, i):
        w = self.bench_sma(self.mkt_gate_window)
        return bool(self.mkt_gate and np.isfinite(w[i]) and self.bench[i] <= w[i])

    def stop_pct(self, i, j):
        """Initial stop distance for name j on day i. Flat stop_from_entry unless atr_stops (research): clip(mult * ATR14 / close, lo, hi)."""
        if not self.atr_stops:
            return self.stop_from_entry
        a, c = self.ATR[i, j], self.CL[i, j]
        return float(np.clip(self.atr_stop_mult * a / c, self.atr_stop_lo, self.atr_stop_hi)) if np.isfinite(a) and np.isfinite(c) and c > 0 else self.stop_from_entry

    def entry_weight(self, j, k, elig):
        """Position weight (fraction of equity) at entry."""
        if self.inverse_vol_sizing:
            v21 = self.vol21_me[k]
            medv = np.nanmedian(np.where(elig, v21, np.nan))
            return float(np.clip(0.05 * medv / v21[j], self.w_lo, self.w_hi)) if np.isfinite(v21[j]) and v21[j] > 0 else 0.05
        if self.risk_sizing:
            return float(np.clip(self.risk_pct_per_trade / self.stop_pct(self.me_idx[k], j), self.w_lo, self.w_hi))
        return self.w_equal

    def select_entries(self, k, i, order, rank, nvalid, slots, held, elig, reject=None, blocked=None, next_date=None):
        """Walk the ranking top-down and return [(j, weight)] for new entries, applying the entry filters.
        reject(reason, j) is called for names that are inside top_n but filtered."""
        out = []
        if slots <= 0:
            return out
        if self.quarterly_entries and self.per[k].month not in (1, 4, 7, 10):
            return out
        sma50, px = self.sma50_me[k], self.CL[i]
        industry_counts = Counter()
        if self.industry_cap:
            for held_j in held:
                # Unlabelled symbols are intentionally their own group. It is
                # safer than applying a false common sector label.
                group = self.industry_labels.get(self.cols[held_j], f"__solo__{self.cols[held_j]}")
                industry_counts[group] += 1
        spike_cutoff = np.nan
        if self.entry_spike_filter:
            spike_pool = self.entry_spike_ret_me[k][elig]
            spike_pool = spike_pool[np.isfinite(spike_pool)]
            if len(spike_pool):
                spike_cutoff = float(np.quantile(spike_pool, self.entry_spike_quantile))
        path_cutoff = np.nan
        if self.entry_path_filter:
            path_pool = self.entry_path_id_me[k][elig]
            path_pool = path_pool[np.isfinite(path_pool)]
            if len(path_pool):
                path_cutoff = float(np.quantile(path_pool, self.entry_path_quantile))
        turnover_cutoff = np.nan
        if self.entry_turnover_filter:
            turnover_pool = self.entry_turnover_ratio_me[k][elig]
            turnover_pool = turnover_pool[np.isfinite(turnover_pool)]
            if len(turnover_pool):
                turnover_cutoff = float(np.quantile(turnover_pool, self.turnover_quantile))
        for j in order[:nvalid]:
            if rank[j] > self.top_n:
                break
            if j in held or slots <= 0:
                continue
            if self.extension_filter and np.isfinite(sma50[j]) and px[j] / sma50[j] - 1 > self.extension_x:
                if reject: reject("EXTENSION", j)
                continue
            # A five-day price spike is a fresh-entry quality filter, not an exit
            # rule.  Existing holdings keep their normal rank/stop lifecycle.
            if self.entry_spike_filter and np.isfinite(spike_cutoff) and np.isfinite(self.entry_spike_ret_me[k, j]) and self.entry_spike_ret_me[k, j] > spike_cutoff:
                if reject: reject("ENTRY_SPIKE", j)
                continue
            if self.entry_path_filter and np.isfinite(path_cutoff) and np.isfinite(self.entry_path_id_me[k, j]) and self.entry_path_id_me[k, j] > path_cutoff:
                if reject: reject("ENTRY_PATH", j)
                continue
            if self.entry_turnover_filter and np.isfinite(turnover_cutoff) and np.isfinite(self.entry_turnover_ratio_me[k, j]) and self.entry_turnover_ratio_me[k, j] > turnover_cutoff:
                if reject: reject("ENTRY_TURNOVER", j)
                continue
            group = self.industry_labels.get(self.cols[j], f"__solo__{self.cols[j]}")
            if self.industry_cap and industry_counts[group] >= self.industry_cap:
                if reject: reject("INDUSTRY_CAP", j)
                continue
            if (self.loss_cooldown or self.stop_cooldown_days > 0) and blocked is not None and blocked.get(j, pd.Timestamp(0)) > next_date:
                if reject: reject("COOLDOWN", j)
                continue
            if self.adx_entry_filter:
                adx, pdi, mdi = self.ADX_ME[k, j], self.PLUS_DI_ME[k, j], self.MINUS_DI_ME[k, j]
                if not np.isfinite(adx):
                    if reject: reject("ADX_UNAVAILABLE", j)
                    # Preserve the isolated experiment's no-backfill behaviour:
                    # a rejected top-N candidate consumes its original slot.
                    if self.industry_cap: industry_counts[group] += 1
                    slots -= 1
                    continue
                if adx < self.adx_threshold:
                    if reject: reject("ADX_BELOW_THRESHOLD", j)
                    if self.industry_cap: industry_counts[group] += 1
                    slots -= 1
                    continue
                if self.adx_require_positive_di and (not np.isfinite(pdi) or not np.isfinite(mdi) or pdi <= mdi):
                    if reject: reject("DMI_NOT_BULLISH", j)
                    if self.industry_cap: industry_counts[group] += 1
                    slots -= 1
                    continue
            out.append((int(j), self.entry_weight(j, k, elig)))
            if self.industry_cap:
                industry_counts[group] += 1
            slots -= 1
        return out

    # ══════════════════════════════════════════════════════════════════════════
    # STOPS  (single implementation: backtest AND live)
    # ══════════════════════════════════════════════════════════════════════════
    def check_stop_exit(self, entry_px, peak, entry_idx, entry_date, i, j):
        """Reason string if a CLOSE-based exit rule fires on day i's close, else None. Fills happen at the next fill."""
        c = self.CL[i, j]
        if not np.isfinite(c):
            return None
        hold_ok = (not self.min_hold_stops) or (i - entry_idx >= 5)
        if not self.resting_stop and hold_ok:
            if c <= entry_px * (1 - self.stop_pct(entry_idx, j)):
                return "STOP_ENTRY"
            if self.chandelier:
                a14 = self.ATR[i, j]
                d = np.clip(3.0 * a14 / peak, 0.12, 0.30) if np.isfinite(a14) else 0.20
                if c <= peak * (1 - d):
                    return "STOP_TRAIL"
            elif c <= peak * (1 - self.trail_from_peak):
                return "STOP_TRAIL"
        if self.time_stop and (self.dates[i] - entry_date).days >= self.time_stop_days and c / entry_px - 1 < self.time_stop_loss:
            return "TIME_STOP"
        return None

    # ══════════════════════════════════════════════════════════════════════════
    # RISK OVERLAYS (optional)
    # ══════════════════════════════════════════════════════════════════════════
    def exposure_target(self, i, holdings, equity):
        """Exposure multiplier for tomorrow from the optional overlays. 1.0 when none is enabled."""
        lev, vs, cs = 1.0, 1.0, 1.0
        if self.regime_leverage:
            panic = bool(self.panic[i])
            w = self.bench_sma(200)
            bear = np.isfinite(w[i]) and self.bench[i] < w[i]
            lev = self.leverage_panic if panic else (self.leverage_bear if bear else 1.0)
            lev = min(lev, self.leverage_panic if panic else 1.0)
        if (self.vol_target or self.corr_guard) and i >= 63:
            js = list(holdings.keys())
            wt = np.array([holdings[j].v for j in js]) / equity
            if self.vol_target:
                pr = (self.RET[i - 62:i + 1][:, js] * wt).sum(axis=1)
                rv = pr.std() * np.sqrt(252)
                if rv > 0:
                    vs = min(1.0, self.vol_target / rv)
            if self.corr_guard:
                R21 = self.RET[i - 20:i + 1][:, js]
                pv = (R21 * wt).sum(axis=1).std()
                sv = (R21.std(axis=0) * wt).sum() / wt.sum()
                if sv > 0 and pv / sv > self.corr_guard_threshold:
                    cs = 0.5
        return lev * vs * cs

    @property
    def uses_exposure_overlay(self):
        return bool(self.vol_target or self.regime_leverage or self.corr_guard)

    # ══════════════════════════════════════════════════════════════════════════
    # LIVE HELPERS
    # ══════════════════════════════════════════════════════════════════════════
    def latest_picks(self, asof=None, held_tickers=None):
        """Ranked month-end table and portfolio-aware next-entry candidates.

        `held_tickers` is optional. When supplied, the same fresh-entry filters
        and industry cap used in the backtest are applied after reserving slots
        for those holdings. Callers should remove names already scheduled for
        exit before passing the set.
        """
        if not self._ready:
            self.calculate_factors()
        asof = pd.Timestamp(asof) if asof is not None else self.me[-1]
        k = int(np.searchsorted(self.me, asof, side="right") - 1)
        elig, sc = self.score_pool(k)
        order, rank, nvalid = self.rank_pool(sc)
        i = self.me_idx[k]
        held_tickers = set(held_tickers or ())
        held = {self.cols.index(ticker) for ticker in held_tickers if ticker in self.cols}
        entry_rejections = {}

        def capture_rejection(reason, j):
            entry_rejections.setdefault(int(j), []).append(reason)

        entry_slots = max(0, self.top_n - len(held))
        selected_entries = {
            j for j, _weight in self.select_entries(
                k, i, order, rank, nvalid, entry_slots, held, elig,
                reject=capture_rejection, blocked={}, next_date=self.dates[min(i + 1, len(self.dates) - 1)]
            )
        }
        spike_cutoff = np.nan
        if self.entry_spike_filter:
            spike_pool = self.entry_spike_ret_me[k][elig]
            spike_pool = spike_pool[np.isfinite(spike_pool)]
            if len(spike_pool):
                spike_cutoff = float(np.quantile(spike_pool, self.entry_spike_quantile))
        path_cutoff = np.nan
        if self.entry_path_filter:
            path_pool = self.entry_path_id_me[k][elig]
            path_pool = path_pool[np.isfinite(path_pool)]
            if len(path_pool):
                path_cutoff = float(np.quantile(path_pool, self.entry_path_quantile))
        turnover_cutoff = np.nan
        if self.entry_turnover_filter:
            turnover_pool = self.entry_turnover_ratio_me[k][elig]
            turnover_pool = turnover_pool[np.isfinite(turnover_pool)]
            if len(turnover_pool):
                turnover_cutoff = float(np.quantile(turnover_pool, self.turnover_quantile))
        rows = []
        for rnk, j in enumerate(order[:max(self.top_n * 2, 40)], 1):
            ext = self.CL[i][j] / self.sma50_me[k][j] - 1 if np.isfinite(self.sma50_me[k][j]) else np.nan
            spike = self.entry_spike_ret_me[k, j]
            path_id = self.entry_path_id_me[k, j]
            turnover_ratio = self.entry_turnover_ratio_me[k, j]
            adx, plus_di, minus_di = self.ADX_ME[k, j], self.PLUS_DI_ME[k, j], self.MINUS_DI_ME[k, j]
            w = self.entry_weight(j, k, elig)
            reasons = entry_rejections.get(int(j), [])
            rows.append(dict(rank=rnk, ticker=self.cols[j], score=sc[j], r1=self.R1[k][j], ulcer_neg=self.ULC[k][j], a1=self.A1[k][j], close=self.CL[i][j],
                             ext_vs_sma50=ext, blocked_extension=bool(self.extension_filter and np.isfinite(ext) and ext > self.extension_x),
                             spike_return=spike, blocked_entry_spike=bool(self.entry_spike_filter and np.isfinite(spike_cutoff) and np.isfinite(spike) and spike > spike_cutoff),
                             path_id=path_id, blocked_entry_path=bool(self.entry_path_filter and np.isfinite(path_cutoff) and np.isfinite(path_id) and path_id > path_cutoff), weight=w,
                             turnover_ratio=turnover_ratio, blocked_entry_turnover=bool(self.entry_turnover_filter and np.isfinite(turnover_cutoff) and np.isfinite(turnover_ratio) and turnover_ratio > turnover_cutoff),
                             adx=adx, plus_di=plus_di, minus_di=minus_di,
                             blocked_adx=bool(self.adx_entry_filter and (not np.isfinite(adx) or adx < self.adx_threshold)),
                             blocked_dmi=bool(self.adx_entry_filter and np.isfinite(plus_di) and np.isfinite(minus_di) and plus_di <= minus_di),
                             entry_stop=self.CL[i][j] * (1 - self.stop_pct(i, j)), in_top_n=rnk <= self.top_n, in_hold_zone=rnk <= self.hold_rank,
                             is_held=j in held, selected_new_entry=j in selected_entries,
                             blocked_industry_cap="INDUSTRY_CAP" in reasons, entry_reject_reason="|".join(reasons)))
        df = pd.DataFrame(rows)
        df.attrs = dict(signal_date=str(self.me[k].date()), pool_size=nvalid, market_gate_off=self.market_gate_off(i),
                        vol_gate_blocks_new_entries=bool(self.vol_gate and self.vol_gate_me[k]), panic_today=bool(self.panic[i]),
                        entry_spike_filter=self.entry_spike_filter, entry_spike_window=self.entry_spike_window,
                        adx_entry_filter=self.adx_entry_filter, adx_window=self.adx_window, adx_threshold=self.adx_threshold,
                        entry_spike_cutoff=spike_cutoff, entry_path_filter=self.entry_path_filter,
                        entry_path_cutoff=path_cutoff, entry_turnover_filter=self.entry_turnover_filter,
                        entry_turnover_cutoff=turnover_cutoff, held_count=len(held), entry_slots=entry_slots)
        return df

    get_positions = latest_picks        # same name as the other books in Old_live_strategies

    def get_exit_signals(self, holdings, asof):
        """Exits to place at the next fill, using only data <= asof.
        holdings: {ticker: {'entry_date': ..., 'entry_price': ...}}  ->  {ticker: reason}.
        Covers stops, time stop and (when asof is a month-end) market gate and rank/pool exits. Uses check_stop_exit, the same code as the backtest."""
        if not self._ready:
            self.calculate_factors()
        i = int(self.dates.get_indexer([pd.Timestamp(asof)], method="ffill")[0])
        out = {}
        for t, h in holdings.items():
            j = self.cols.index(t)
            ed = pd.Timestamp(h["entry_date"])
            ie = self.dates.get_loc(ed) if ed in self.dates else int(self.dates.searchsorted(ed))
            seg = self.CL[ie:i + 1, j]
            epx = h["entry_price"]
            peak = max(epx, np.nanmax(seg)) if np.isfinite(seg).any() else epx   # entry-day close counts, as in the backtest
            why = self.check_stop_exit(epx, peak, ie, ed, i, j)
            if why:
                out[t] = why
        if pd.Timestamp(asof) in set(self.me):
            k = int(np.searchsorted(self.me, pd.Timestamp(asof)))
            if self.market_gate_off(self.me_idx[k]):
                return {t: out.get(t, "MKT_GATE") for t in holdings}
            elig, sc = self.score_pool(k)
            order, rank, nvalid = self.rank_pool(sc)
            for t in holdings:
                j = self.cols.index(t)
                if t not in out and (not np.isfinite(sc[j]) or rank[j] > self.hold_rank):
                    out[t] = "RANK_EXIT"
        return out
