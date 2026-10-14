import os, numpy as np, pandas as pd
GD = "/Users/hemantsoni/Documents/upstox_data_folder/gold_silver_ohlcv_data"
RF = 0.065; CASH_D = (1 + RF) ** (1 / 252) - 1
def etf(sym):
    d = pd.read_csv(os.path.join(GD, sym + ".csv")); d["t"] = pd.to_datetime(d.timestamp.str[:10]); d = d.set_index("t")[["open", "high", "low", "close", "volume"]]
    return d[~d.index.duplicated(keep="last")].sort_index()
def valid_returns(close, calendar):
    """daily return on the engine calendar; NaN on the first observation after a gap (> 5 calendar days) and wherever a price is missing."""
    c = close.reindex(calendar)
    span = close.index.to_series().diff().dt.days.reindex(calendar)
    r = close.pct_change(fill_method=None).reindex(calendar)
    r[span > 5] = np.nan
    return r
def signals(close):
    """S_sma (close > SMA200) and S_per (share of last 126 days above SMA50 >= 0.5) at each ETF close; invalid (False) when the window touches the data gap. Uses only data to that close."""
    idx = close.index
    ok200 = (idx.to_series() - idx.to_series().shift(199)).dt.days <= 330      # 200 rows must span < ~1.1 years (no data gap inside the window)
    sma200 = close.rolling(200, min_periods=200).mean(); s_sma = (close > sma200) & ok200 & sma200.notna()
    sma50 = close.rolling(50, min_periods=50).mean(); above = (close > sma50).astype(float).where(sma50.notna())
    q = above.rolling(126, min_periods=126).mean(); ok126 = ((idx.to_series() - idx.to_series().shift(175)).dt.days <= 300)
    s_per = (q >= 0.5) & ok126 & q.notna()
    return s_sma.astype(float), s_per.astype(float)
def metrics(r, label=""):
    r = r.dropna(); yrs = (r.index[-1] - r.index[0]).days / 365.25; eq = (1 + r).cumprod()
    f = lambda x: (x.mean() - CASH_D) / x.std() * np.sqrt(252) if len(x) > 50 else np.nan
    return dict(CAGR=(eq.iloc[-1] ** (1 / yrs) - 1) * 100, Sh65=f(r), MaxDD=(eq / eq.cummax() - 1).min() * 100, Sh65_A=f(r[:"2014-12-31"]), Sh65_B=f(r["2015-01-01":]))
