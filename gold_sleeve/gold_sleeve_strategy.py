"""
gold_sleeve_strategy.py
=======================
Persistence x Volatility Gold Sleeve  (GoldSleevePV)

A time-series (not cross-sectional) momentum sleeve on ONE instrument: a liquid gold ETF (default GOLDBEES),
with the idle part of the sleeve parked in cash / a liquid fund.

Core logic (decided at the last trading day of each month, executed at the next day's close)
--------------------------------------------------------------------------------------------
    persistence  Q_t = share of the last `persistence_window` (126) trading days on which the gold close was above
                       its `sma_window` (50) day simple moving average.      (same idea as q5_126 in the stock books,
                       applied in time series: how *consistently* has gold been trending, not how far it moved)
    volatility   s_t = realised daily-return std over `vol_window` (63) days, annualised.
    exposure     E_t = Q_t * min(1, vol_target / s_t),   vol_target = 12%
    sleeve       E_t in gold, (1 - E_t) in cash.

Why this and not buy-and-hold / classic trend
---------------------------------------------
Research (factor_research/gold_*.py, 2008-2026, 2011-14 data gap excluded) found NO statistically meaningful gold
return timing (best signal t-stat 1.1). Textbook TSMOM / SMA rules did not beat holding gold as a sleeve. What this
rule does is manage RISK: at an equal risk budget to a 10% buy-and-hold gold sleeve it cut the blended portfolio's
max drawdown in 81/81 neighbouring parameter sets (+1.4 to +3.5 pts) with unchanged Sharpe, and the real exposure
path beat 86-90% of time-shifted placebo paths on drawdown. Expect risk reduction, NOT extra return.

Data caveat
-----------
The source ETF files are missing 2011-01 .. 2014-12. Signals/returns are NEVER forward-filled across a gap: windows
that touch missing data stay NaN until enough contiguous observations exist, and months whose entry/exit price is
missing are skipped.

This module holds strategy logic only (signals, targets, backtest on monthly strict returns, live helper).
Data loading + reporting live in run_gold_sleeve_backtest.py.
"""
import numpy as np
import pandas as pd


def load_etf_close(path, ffill_limit=5):
    """Read a Upstox ETF csv (timestamp/datetime, close) -> daily close Series (tz-naive, deduped). Gaps stay NaN beyond ffill_limit."""
    df = pd.read_csv(path)
    dc = [c for c in df.columns if c.lower() in ('datetime', 'date', 'timestamp')][0]
    idx = pd.to_datetime(df[dc], errors='coerce', utc=True).dt.tz_convert('Asia/Kolkata').dt.tz_localize(None).dt.normalize()
    s = pd.Series(df['close'].values, index=idx).sort_index()
    s = s[~s.index.duplicated(keep='last')]
    s = s.where(s > 0)
    return s


class GoldSleevePV:
    def __init__(
        self,
        gold_close,                      # daily close Series of the gold ETF (gaps = NaN)
        persistence_window  = 126,
        sma_window          = 50,
        vol_window          = 63,
        vol_target          = 0.12,
        max_exposure        = 1.0,
        min_obs_frac        = 0.8,       # windows need >= 80% observed days (same ratio the stock books use)
        deadband            = 0.0,       # >0: skip rebalances smaller than this exposure change (NOT validated; 0 = research parity)
        cost_one_way        = 0.0015,    # applied to |change in exposure|
        cash_annual         = 0.06,      # backtest-only return on the cash leg; live: sweep into LIQUIDBEES / liquid fund
        stale_days          = 5,         # live guard: refuse to emit a signal if last price is older than this many calendar days
        mode                = 'pv',      # 'pv' = persistence x vol-target | 'buy_hold' = static 100% gold (A/B reference)
    ):
        if mode not in ('pv', 'buy_hold'):
            raise ValueError("mode must be 'pv' or 'buy_hold'")
        self.g = gold_close.astype('float64').sort_index()
        self.persistence_window = persistence_window
        self.sma_window = sma_window
        self.vol_window = vol_window
        self.vol_target = vol_target
        self.max_exposure = max_exposure
        self.min_obs_frac = min_obs_frac
        self.deadband = deadband
        self.cost_one_way = cost_one_way
        self.cash_m = (1 + cash_annual) ** (1 / 12) - 1
        self.stale_days = stale_days
        self.mode = mode
        self.daily = None
        self.month_end_exposure = None
        self.results = None
        print(f"GoldSleevePV initialised | mode={mode} persistence={persistence_window}d/SMA{sma_window} "
              f"vol={vol_window}d target={vol_target:.0%} cap={max_exposure:.0%} deadband={deadband:.0%} cost={cost_one_way:.2%}")

    # ------------------------------------------------------------------ signals
    def calculate_signals(self):
        g = self.g
        mp = lambda w: max(2, int(w * self.min_obs_frac))
        sma = g.rolling(self.sma_window, min_periods=mp(self.sma_window)).mean()
        valid = g.notna() & sma.notna()
        above = (g > sma).where(valid).astype('float64')
        persistence = above.rolling(self.persistence_window, min_periods=mp(self.persistence_window)).mean()
        r = g.pct_change(fill_method=None)
        vol = r.rolling(self.vol_window, min_periods=mp(self.vol_window)).std() * np.sqrt(252)
        vol_scale = (self.vol_target / vol).clip(upper=1.0)
        if self.mode == 'buy_hold':
            expo = pd.Series(1.0, index=g.index).where(g.notna())
        else:
            expo = (persistence * vol_scale).clip(upper=self.max_exposure)
        self.daily = pd.DataFrame({'close': g, 'persistence': persistence, 'vol_ann': vol, 'vol_scale': vol_scale, 'target_exposure': expo})
        # month-end decision dates = last observed trading day of each calendar month
        s = pd.Series(g.index, index=g.index)
        self.month_end_dates = pd.DatetimeIndex(s.groupby([g.index.year, g.index.month]).max().values)
        self.month_end_exposure = self.daily['target_exposure'].reindex(self.month_end_dates)
        return self.daily

    # ------------------------------------------------------------------ monthly strict returns
    def _strict_monthly_returns(self, dates):
        """next-month return from close(t+1 after dates[k]) to close(t+1 after dates[k+1]); NaN if either price is missing."""
        idx = self.g.index
        pos = idx.get_indexer(dates)
        c = self.g.values
        out = np.full(len(dates), np.nan)
        max_lag = pd.Timedelta(days=7)          # the "next trading day" must really be next (never the other side of a data gap)
        for k in range(len(dates) - 1):
            a_i, b_i = pos[k] + 1, pos[k + 1] + 1
            if pos[k] >= 0 and pos[k + 1] >= 0 and b_i < len(idx):
                if idx[a_i] - dates[k] > max_lag or idx[b_i] - dates[k + 1] > max_lag:
                    continue
                a, b = c[a_i], c[b_i]
                if np.isfinite(a) and np.isfinite(b):
                    out[k] = b / a - 1
        return pd.Series(out, index=dates)

    def backtest(self, start=None, end=None):
        """Monthly sleeve backtest on strict returns. Capital not in gold earns cash_annual. Cost = cost_one_way * |exposure change|."""
        if self.daily is None:
            self.calculate_signals()
        dates = self.month_end_dates
        fwd = self._strict_monthly_returns(dates)
        tgt = self.month_end_exposure
        d = pd.concat([tgt, fwd], axis=1, keys=['target', 'gold_ret']).dropna()
        if start is not None:
            d = d.loc[pd.Timestamp(start):]
        if end is not None:
            d = d.loc[:pd.Timestamp(end)]
        cur, expo, trades = 0.0, [], []
        for dt, row in d.iterrows():
            t = float(row.target)
            if self.deadband > 0 and abs(t - cur) < self.deadband and expo:
                t = cur
            trades.append(abs(t - cur))
            expo.append(t)
            cur = t
        d['exposure'] = expo
        d['turnover'] = trades
        d['net_return'] = d.exposure * d.gold_ret + (1 - d.exposure) * self.cash_m - self.cost_one_way * d.turnover
        d['gross_return'] = d.exposure * d.gold_ret + (1 - d.exposure) * self.cash_m
        d['equity'] = (1 + d.net_return).cumprod()
        self.results = d
        return d

    # ------------------------------------------------------------------ live helper
    def latest_signal(self, today=None):
        """Target gold exposure for the next rebalance, from the latest observed data. Raises if data are stale."""
        if self.daily is None:
            self.calculate_signals()
        last = self.g.dropna().index[-1]
        today = pd.Timestamp(today) if today is not None else pd.Timestamp.today().normalize()
        age = (today - last).days
        if age > self.stale_days:
            raise RuntimeError(f"stale gold price: last close {last.date()} is {age} days old (> {self.stale_days}); refusing to emit a signal")
        row = self.daily.loc[last]
        if pd.isna(row.target_exposure):
            raise RuntimeError("not enough contiguous history after a data gap to compute the signal")
        e = float(row.target_exposure)
        return {
            'as_of': last.date(), 'gold_close': float(row.close), 'persistence': float(row.persistence), 'vol_ann': float(row.vol_ann),
            'vol_scale': float(row.vol_scale), 'target_gold_exposure': e, 'target_cash_exposure': 1 - e,
            'is_month_end_decision_day': bool(last in self.month_end_dates),
            'note': 'Act on the LAST trading day of the month (trade next close). Intra-month values are informational only.',
        }

    # ------------------------------------------------------------------ metrics
    @staticmethod
    def metrics(ret, periods=12, rf_annual=0.06):
        ret = ret.dropna()
        eq = (1 + ret).cumprod()
        yrs = len(ret) / periods
        cagr = eq.iloc[-1] ** (1 / yrs) - 1
        vol = ret.std() * np.sqrt(periods)
        rf_m = (1 + rf_annual) ** (1 / periods) - 1
        sharpe = (ret - rf_m).mean() / ret.std() * np.sqrt(periods)
        dd = (eq / eq.cummax() - 1)
        return dict(cagr=cagr, vol=vol, sharpe=sharpe, max_drawdown=dd.min(), calmar=cagr / abs(dd.min()) if dd.min() < 0 else np.nan, months=len(ret))
