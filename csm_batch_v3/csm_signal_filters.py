"""
csm_signal_filters.py
=====================
Optional trend / strength gates for the CSM strategy. Each filter turns a stock-day
into True (pass) or False (fail). The strategy uses them as gates on the monthly
signal date: a stock that fails any ENABLED filter is not a candidate, so the top-N
is picked from the stocks that pass.

All functions return DAILY boolean DataFrames computed from bar t only. The strategy
shifts them by one bar before using them, so nothing here looks ahead.

To add a new filter: write a function with the same signature as the ones below,
register it in FILTERS, and add its parameters to SIGNAL_FILTERS in the backtest
config. Nothing else needs to change.

Filters
  adx         trend strength: ADX >= min_adx, and (optionally) +DI > -DI
  high52      price within min_pct of its 252-day closing high
  supertrend  Supertrend (ATR bands) is in an up-trend
  vwap        close above the rolling volume-weighted average price
"""

import numpy as np
import pandas as pd


def _wilder(df, period):
    return df.ewm(alpha=1.0 / period, adjust=False).mean()


def _true_range(h, l, c):
    pc = c.shift(1)
    return np.maximum(np.maximum(h - l, (h - pc).abs()), (l - pc).abs())


def _bars(prices, highs, lows):
    """Forward-filled close / high / low on the price grid. If high/low data is
    missing the close is used for both (indicators degrade to close-only)."""
    c = prices.ffill()
    if highs is None or highs.empty or lows is None or lows.empty:
        print("  [filters] Warning: no high/low data - using close for high and low.")
        return c, c, c
    h = highs.reindex(index=c.index, columns=c.columns).ffill()
    l = lows.reindex(index=c.index, columns=c.columns).ffill()
    return c, h, l


# ── ADX ───────────────────────────────────────────────────────────────────────

def adx_filter(prices, volumes, highs, lows, period=14, min_adx=20.0, require_di=True, **_):
    c, h, l = _bars(prices, highs, lows)
    up, dn = h.diff(), -l.diff()
    plus_dm  = up.where((up > dn) & (up > 0), 0.0)
    minus_dm = dn.where((dn > up) & (dn > 0), 0.0)
    atr = _wilder(_true_range(h, l, c), period).replace(0, np.nan)
    plus_di  = 100.0 * _wilder(plus_dm, period) / atr
    minus_di = 100.0 * _wilder(minus_dm, period) / atr
    dx  = 100.0 * (plus_di - minus_di).abs() / (plus_di + minus_di).replace(0, np.nan)
    adx = _wilder(dx, period)
    warm = c.notna().cumsum() >= 3 * period          # let the smoothing settle
    passed = (adx >= min_adx) & warm
    if require_di:
        passed &= plus_di > minus_di
    return passed.fillna(False)


# ── 52-week high proximity ────────────────────────────────────────────────────

def high52_filter(prices, volumes, highs, lows, min_pct=0.85, window=252, **_):
    c = prices.ffill()
    hi = c.rolling(window, min_periods=int(window * 0.8)).max()
    return ((c / hi) >= min_pct).fillna(False)


# ── Supertrend ────────────────────────────────────────────────────────────────

def supertrend_filter(prices, volumes, highs, lows, period=10, mult=3.0, **_):
    c_df, h_df, l_df = _bars(prices, highs, lows)
    atr = _wilder(_true_range(h_df, l_df, c_df), period)
    c, hl2 = c_df.to_numpy(float), ((h_df + l_df) / 2.0).to_numpy(float)
    a = atr.to_numpy(float)
    ub, lb = hl2 + mult * a, hl2 - mult * a

    n, m = c.shape
    fub, flb = ub.copy(), lb.copy()
    bull = np.zeros((n, m), dtype=bool)
    bull[0] = c[0] > hl2[0]
    for t in range(1, n):
        take_ub = (ub[t] < fub[t - 1]) | (c[t - 1] > fub[t - 1]) | np.isnan(fub[t - 1])
        take_lb = (lb[t] > flb[t - 1]) | (c[t - 1] < flb[t - 1]) | np.isnan(flb[t - 1])
        fub[t] = np.where(take_ub, ub[t], fub[t - 1])
        flb[t] = np.where(take_lb, lb[t], flb[t - 1])
        bull[t] = np.where(bull[t - 1], ~(c[t] < flb[t]), c[t] > fub[t])
    bull &= ~np.isnan(a)
    return pd.DataFrame(bull, index=c_df.index, columns=c_df.columns)


# ── rolling VWAP ──────────────────────────────────────────────────────────────

def vwap_filter(prices, volumes, highs, lows, window=63, **_):
    c, h, l = _bars(prices, highs, lows)
    if volumes is None or volumes.empty:
        print("  [filters] Warning: no volume data - VWAP filter passes nothing.")
        return pd.DataFrame(False, index=c.index, columns=c.columns)
    v  = volumes.reindex(index=c.index, columns=c.columns).fillna(0.0)
    tp = (h + l + c) / 3.0
    mp = max(2, window // 2)
    vwap = (tp * v).rolling(window, min_periods=mp).sum() / v.rolling(window, min_periods=mp).sum().replace(0, np.nan)
    return (c > vwap).fillna(False)


FILTERS = {
    'adx':        adx_filter,
    'high52':     high52_filter,
    'supertrend': supertrend_filter,
    'vwap':       vwap_filter,
}


def compute_filter_masks(prices, volumes, highs, lows, config):
    """config: {name: {'enabled': bool, ...params}}. Returns {name: daily bool DataFrame}
    for the enabled filters only."""
    out = {}
    for name, params in (config or {}).items():
        if not params.get('enabled', False):
            continue
        if name not in FILTERS:
            raise ValueError(f"Unknown filter '{name}'. Available: {list(FILTERS)}")
        out[name] = FILTERS[name](prices, volumes, highs, lows,
                                  **{k: v for k, v in params.items() if k != 'enabled'})
    return out
