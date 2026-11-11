"""Isolated daily technical-overlay experiment for CSM Aegis.

This file deliberately does not alter ``csm_aegis_strategy.py``.  It keeps
the production cross-sectional residual-momentum selector intact and adds
opt-in, daily-bar overlays only:

* ADX/DMI: fresh-entry trend-quality gate.
* Supertrend: fresh-entry confirmation and/or close-based exit.
* Previous-day pivots: resistance-aware fresh-entry veto and optional support
  stop.  No profit target is modelled because that would mechanically cap the
  right tail that a momentum strategy needs.

Session VWAP is intentionally absent: daily OHLCV cannot reconstruct it.  A
separate intraday execution experiment must use real intraday OHLCV and the
same raw-bar fill validation as the production engine.
"""
import numpy as np
import pandas as pd

from csm_aegis_strategy import CSMAegis


class CSMAegisTrendExperiment(CSMAegis):
    """Aegis with isolated, opt-in daily technical overlays.

    All filters are applied only to *fresh entries*.  Existing positions retain
    their production rank/stop lifecycle unless ``supertrend_exit=True``.
    This prevents a trend-quality entry filter from silently becoming a new
    monthly liquidation rule.
    """
    def __init__(
        self, *args,
        adx_entry_filter=False, adx_window=14, adx_threshold=25.0,
        adx_require_positive_di=True,
        supertrend_entry_filter=False, supertrend_exit=False,
        supertrend_window=10, supertrend_multiplier=3.0,
        pivot_resistance_filter=False, pivot_resistance_buffer=0.02,
        pivot_stop=False, pivot_stop_floor=0.06,
        **kwargs,
    ):
        self.adx_entry_filter = adx_entry_filter
        self.adx_window = int(adx_window)
        self.adx_threshold = float(adx_threshold)
        self.adx_require_positive_di = adx_require_positive_di
        self.supertrend_entry_filter = supertrend_entry_filter
        self.supertrend_exit = supertrend_exit
        self.supertrend_window = int(supertrend_window)
        self.supertrend_multiplier = float(supertrend_multiplier)
        self.pivot_resistance_filter = pivot_resistance_filter
        self.pivot_resistance_buffer = float(pivot_resistance_buffer)
        self.pivot_stop = pivot_stop
        self.pivot_stop_floor = float(pivot_stop_floor)
        if self.adx_window < 2 or self.supertrend_window < 2:
            raise ValueError("ADX and Supertrend windows must be at least 2")
        if not 0 <= self.pivot_resistance_buffer < 1 or not 0 < self.pivot_stop_floor < 1:
            raise ValueError("pivot buffers must be fractions in (0, 1)")
        super().__init__(*args, **kwargs)

    def calculate_factors(self):
        super().calculate_factors()
        self._calculate_daily_technical_overlays()
        return self

    def _calculate_daily_technical_overlays(self):
        """Build daily indicators using only that close and earlier OHLCV.

        ADX uses Wilder-style smoothing.  Supertrend's ATR is intentionally
        lagged one day (the base strategy's ATR) so no same-bar range is used to
        set a supposedly actionable state before that bar has completed.
        """
        high, low, close = self.highs, self.lows, self.prices
        raw_close = close.values
        prior_close = close.ffill(limit=10).shift(1)
        tr = pd.concat([(high - low), (high - prior_close).abs(), (low - prior_close).abs()]).groupby(level=0).max()
        up = high.diff()
        down = -low.diff()
        plus_dm = up.where((up > down) & (up > 0), 0.0).where(high.notna() & low.notna())
        minus_dm = down.where((down > up) & (down > 0), 0.0).where(high.notna() & low.notna())
        alpha = 1.0 / self.adx_window
        atr = tr.ewm(alpha=alpha, adjust=False, min_periods=self.adx_window).mean()
        plus_di = 100 * plus_dm.ewm(alpha=alpha, adjust=False, min_periods=self.adx_window).mean().div(atr.replace(0, np.nan))
        minus_di = 100 * minus_dm.ewm(alpha=alpha, adjust=False, min_periods=self.adx_window).mean().div(atr.replace(0, np.nan))
        dx = 100 * (plus_di - minus_di).abs().div((plus_di + minus_di).replace(0, np.nan))
        adx = dx.ewm(alpha=alpha, adjust=False, min_periods=self.adx_window).mean()
        self.ADX_ME = adx.loc[self.me].values.astype("float32")
        self.PLUS_DI_ME = plus_di.loc[self.me].values.astype("float32")
        self.MINUS_DI_ME = minus_di.loc[self.me].values.astype("float32")

        # Classical pivot levels based only on the PREVIOUS completed daily bar.
        prev_h, prev_l, prev_c = high.shift(1), low.shift(1), close.shift(1)
        pivot = (prev_h + prev_l + prev_c) / 3.0
        self.PIVOT_R1_ME = (2 * pivot - prev_l).loc[self.me].values.astype("float32")

        n, m = raw_close.shape
        st_me = np.full((len(self.me), m), np.nan, dtype="float32")
        st_daily = np.full((n, m), np.nan, dtype="float32") if self.supertrend_exit else None
        me_to_k = {idx: k for k, idx in enumerate(self.me_idx)}
        final_upper = np.full(m, np.nan)
        final_lower = np.full(m, np.nan)
        trend = np.zeros(m, dtype=np.int8)  # +1 bullish, -1 bearish
        highs, lows, atr_lag = high.values, low.values, self.ATR
        for i in range(n):
            h, l, c, a = highs[i], lows[i], raw_close[i], atr_lag[i]
            valid = np.isfinite(h) & np.isfinite(l) & np.isfinite(c) & np.isfinite(a) & (a > 0)
            basic_upper = (h + l) / 2.0 + self.supertrend_multiplier * a
            basic_lower = (h + l) / 2.0 - self.supertrend_multiplier * a
            new = valid & ~np.isfinite(final_upper)
            old = valid & ~new
            prev_c = raw_close[i - 1] if i else np.full(m, np.nan)
            final_upper[new], final_lower[new] = basic_upper[new], basic_lower[new]
            if old.any():
                final_upper[old] = np.where(
                    (basic_upper[old] < final_upper[old]) | (prev_c[old] > final_upper[old]),
                    basic_upper[old], final_upper[old],
                )
                final_lower[old] = np.where(
                    (basic_lower[old] > final_lower[old]) | (prev_c[old] < final_lower[old]),
                    basic_lower[old], final_lower[old],
                )
            trend[valid & (c > final_upper)] = 1
            trend[valid & (c < final_lower)] = -1
            level = np.where(trend >= 0, final_lower, final_upper)
            level[~valid] = np.nan
            if i in me_to_k:
                st_me[me_to_k[i]] = level.astype("float32")
            if st_daily is not None:
                st_daily[i] = level.astype("float32")
        self.SUPERTREND_ME = st_me
        self.SUPERTREND = st_daily

    def _technical_entry_reason(self, k, j):
        if self.adx_entry_filter:
            adx, pdi, mdi = self.ADX_ME[k, j], self.PLUS_DI_ME[k, j], self.MINUS_DI_ME[k, j]
            if not np.isfinite(adx):
                return "ADX_UNAVAILABLE"
            if adx < self.adx_threshold:
                return "ADX_BELOW_THRESHOLD"
            if self.adx_require_positive_di and (not np.isfinite(pdi) or not np.isfinite(mdi) or pdi <= mdi):
                return "DMI_NOT_BULLISH"
        if self.supertrend_entry_filter:
            level, price = self.SUPERTREND_ME[k, j], self.CL[self.me_idx[k], j]
            if not np.isfinite(level) or not np.isfinite(price) or price <= level:
                return "SUPERTREND_NOT_BULLISH"
        if self.pivot_resistance_filter:
            r1, price = self.PIVOT_R1_ME[k, j], self.CL[self.me_idx[k], j]
            # Do not buy immediately below yesterday's R1. A confirmed close
            # through R1 is allowed; the filter is a resistance-proximity veto.
            if np.isfinite(r1) and np.isfinite(price) and price < r1 and price >= r1 * (1 - self.pivot_resistance_buffer):
                return "PIVOT_NEAR_R1"
        return None

    def select_entries(self, k, i, order, rank, nvalid, slots, held, elig, reject=None, blocked=None, next_date=None):
        """Run production entry selection, then apply experimental fresh-entry gates.

        As in production, filters do not backfill from below the original top-N;
        this keeps the experiment from changing breadth as an accidental second
        intervention.
        """
        selected = super().select_entries(k, i, order, rank, nvalid, slots, held, elig, reject, blocked, next_date)
        out = []
        for j, weight in selected:
            reason = self._technical_entry_reason(k, j)
            if reason:
                if reject:
                    reject(reason, j)
                continue
            out.append((j, weight))
        return out

    def stop_pct(self, i, j):
        base = super().stop_pct(i, j)
        if not self.pivot_stop or i < 1:
            return base
        h, l, c = self.H[i - 1, j], self.L[i - 1, j], self.C_RAW[i - 1, j]
        px = self.C_RAW[i, j]
        if not all(np.isfinite(x) and x > 0 for x in (h, l, c, px)):
            return base
        support = 2 * ((h + l + c) / 3.0) - h
        distance = 1 - support / px
        if not np.isfinite(distance) or distance <= 0:
            return base
        return float(min(base, np.clip(distance, self.pivot_stop_floor, base)))

    def check_stop_exit(self, entry_px, peak, entry_idx, entry_date, i, j):
        reason = super().check_stop_exit(entry_px, peak, entry_idx, entry_date, i, j)
        if reason or not self.supertrend_exit or self.SUPERTREND is None:
            return reason
        level, raw_close = self.SUPERTREND[i, j], self.C_RAW[i, j]
        if i > entry_idx and np.isfinite(level) and np.isfinite(raw_close) and raw_close < level:
            return "SUPERTREND_EXIT"
        return None
