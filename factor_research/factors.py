"""
factors.py -- candidate signal library.

Every factor is oriented a-priori so that HIGHER = expected BETTER forward return (the
orientation is fixed from the literature / market logic BEFORE looking at results, so the
sign of a measured IC is a real test, not a post-hoc flip).  Each builder returns a daily
panel (dates x tickers); `build_all` samples it at the month-end signal dates so only
a (n_months x n_tickers) float32 frame per factor is kept in memory.

No lookahead: a value at date t uses data up to and including the close of t.  The
evaluation engine trades it from the close of t+1.

Families
  MOM   price momentum variants      HIGH  52w-high / anchoring / MA distance
  TQ    trend quality / smoothness   RISK  volatility, beta, skew, drawdown, MAX
  VOL   volume / flow / liquidity    CNDL  overnight / intraday / close-location
  REV   short-term reversal          BRK   breakout / compression (HR, VCP, Donchian cousins)
  RS    relative strength vs market  SEAS  calendar seasonality
"""
import numpy as np
import pandas as pd

REGISTRY = {}   # name -> (family, description, fn)


def factor(name, family, desc):
    def deco(fn):
        REGISTRY[name] = (family, desc, fn)
        return fn
    return deco


def _mp(w):
    return max(2, int(w * 0.8))


def rmean(x, w): return x.rolling(w, min_periods=_mp(w)).mean()
def rstd(x, w):  return x.rolling(w, min_periods=_mp(w)).std()
def rsum(x, w):  return x.rolling(w, min_periods=_mp(w)).sum()
def rmax(x, w):  return x.rolling(w, min_periods=_mp(w)).max()
def rmin(x, w):  return x.rolling(w, min_periods=_mp(w)).min()


class Ctx:
    """Shared daily intermediates, computed once."""

    def __init__(self, P):
        self.C = P['close']; self.H = P['high']; self.L = P['low']
        self.O = P['open'];  self.V = P['volume']
        self.mkt = P['bench_ret']; self.bench = P['bench']
        self.Cf = self.C.ffill(limit=5)
        self.Hf = self.H.ffill(limit=5)
        self.Lf = self.L.ffill(limit=5)
        self.r = self.Cf.pct_change(fill_method=None)
        self.DV = self.C * self.V
        self.t = pd.Series(np.arange(len(self.C), dtype='float64'), index=self.C.index)
        self._beta = None
        self._resid = None
        self._rs = None

    @property
    def beta(self):
        if self._beta is None:
            self._beta = (self.r.rolling(252, min_periods=200).cov(self.mkt)
                          .div(self.mkt.rolling(252, min_periods=200).var(), axis=0))
        return self._beta

    @property
    def resid(self):
        if self._resid is None:
            self._resid = self.r.sub(self.beta.shift(1).mul(self.mkt, axis=0))
        return self._resid

    @property
    def logRS(self):
        if self._rs is None:
            self._rs = np.log(self.Cf).sub(np.log(self.bench), axis=0)
        return self._rs

    def clv(self):
        rng = (self.H - self.L)
        c = ((self.C - self.L) - (self.H - self.C)) / rng
        return c.where(rng > 0, 0.0)

    def true_range(self):
        pc = self.Cf.shift(1)
        return np.maximum(np.maximum((self.Hf - self.Lf), (self.Hf - pc).abs()), (self.Lf - pc).abs())

    def newhigh_flag(self, w=252):
        return (self.Cf >= rmax(self.Cf, w)).astype('float64').where(self.Cf.notna())


def _trend_stats(logx, t, w):
    """rolling OLS of a log-series on time: returns (r, slope_per_day)"""
    r = logx.rolling(w, min_periods=_mp(w)).corr(t)
    sd_x = rstd(logx, w)
    sd_t = t.rolling(w, min_periods=_mp(w)).std()
    slope = r.mul(sd_x).div(sd_t, axis=0)
    return r, slope


# ───────────────────────────── MOMENTUM ─────────────────────────────
@factor('mom_3_1', 'MOM', '3m return skipping last month')
def _(X): return X.Cf.shift(21) / X.Cf.shift(63) - 1

@factor('mom_6_1', 'MOM', '6m return skipping last month')
def _(X): return X.Cf.shift(21) / X.Cf.shift(126) - 1

@factor('mom_9_1', 'MOM', '9m return skipping last month')
def _(X): return X.Cf.shift(21) / X.Cf.shift(189) - 1

@factor('mom_12_1', 'MOM', '12m return skipping last month (classic Jegadeesh-Titman)')
def _(X): return X.Cf.shift(21) / X.Cf.shift(252) - 1

@factor('mom_12_1_sharpe', 'MOM', '12-1 return / 252d vol (risk-adjusted momentum)')
def _(X): return (X.Cf.shift(21) / X.Cf.shift(252) - 1) / rstd(X.r, 252)

@factor('mom_6_1_sharpe', 'MOM', '6-1 return / 126d vol')
def _(X): return (X.Cf.shift(21) / X.Cf.shift(126) - 1) / rstd(X.r, 126)

@factor('mom_interm_12_7', 'MOM', 'Novy-Marx intermediate momentum (t-12..t-7)')
def _(X): return X.Cf.shift(147) / X.Cf.shift(252) - 1

@factor('mom_accel', 'MOM', 'return(t-1..t-3m) minus return(t-3..t-6m)')
def _(X): return (X.Cf.shift(21) / X.Cf.shift(63)) - (X.Cf.shift(63) / X.Cf.shift(126))

@factor('mom_resid_12_1', 'MOM', 'CAPM residual momentum, 12-1 (sum of r - beta*mkt)')
def _(X): return rsum(X.resid, 231).shift(21)

@factor('mom_resid_sharpe', 'MOM', 'residual momentum / residual vol (Blitz et al.)')
def _(X): return rsum(X.resid, 231).shift(21) / rstd(X.resid, 252)

@factor('mom_consist_12m', 'MOM', 'fraction of last 12 monthly blocks with positive return')
def _(X):
    blocks = [(X.Cf.shift(21 * k) / X.Cf.shift(21 * (k + 1)) - 1) for k in range(1, 13)]
    pos = sum((b > 0).astype('float64').where(b.notna()) for b in blocks)
    n = sum(b.notna().astype('float64') for b in blocks)
    return (pos / n).where(n >= 9)

@factor('up_days_net_231', 'MOM', 'frog-in-the-pan: %up days minus %down days over t-12..t-1')
def _(X):
    up = (X.r > 0).astype('float64').where(X.r.notna())
    dn = (X.r < 0).astype('float64').where(X.r.notna())
    return (rmean(up, 231) - rmean(dn, 231)).shift(21)


# ─────────────────────── 52-WEEK HIGH / MA DISTANCE ───────────────────────
@factor('a1_52wh', 'HIGH', 'LIVE A1: close / 252d intraday high')
def _(X): return X.Cf / rmax(X.Hf, 252)

@factor('a3_rs_high', 'HIGH', 'LIVE A3: RS line / its own 252d max')
def _(X):
    rs = X.Cf.div(X.bench, axis=0)
    return rs / rmax(rs, 252)

@factor('hi_26w', 'HIGH', 'close / 126d high')
def _(X): return X.Cf / rmax(X.Hf, 126)

@factor('hi_13w', 'HIGH', 'close / 63d high')
def _(X): return X.Cf / rmax(X.Hf, 63)

@factor('hi_2y', 'HIGH', 'close / 504d high')
def _(X): return X.Cf / rmax(X.Hf, 504)

@factor('days_since_52wh', 'HIGH', 'recency of last new 252d closing high (negated days)')
def _(X):
    flag = X.newhigh_flag(252)
    pos = pd.DataFrame(np.broadcast_to(X.t.values[:, None], flag.shape), index=flag.index, columns=flag.columns)
    last = pos.where(flag == 1).ffill()
    return -(pos - last).clip(upper=252).where(X.Cf.notna())

@factor('nh_freq_63', 'HIGH', 'share of last 63d that set a new 252d closing high')
def _(X): return rmean(X.newhigh_flag(252), 63)

@factor('above_52wl', 'HIGH', 'close / 252d low (distance above the 52w low)')
def _(X): return X.Cf / rmin(X.Lf, 252)

@factor('dist_sma200', 'HIGH', 'close / SMA200 - 1')
def _(X): return X.Cf / rmean(X.Cf, 200) - 1

@factor('dist_sma50', 'HIGH', 'close / SMA50 - 1')
def _(X): return X.Cf / rmean(X.Cf, 50) - 1

@factor('sma50_over_200', 'HIGH', 'SMA50 / SMA200 - 1 (golden-cross strength)')
def _(X): return rmean(X.Cf, 50) / rmean(X.Cf, 200) - 1


# ───────────────────────────── TREND QUALITY ─────────────────────────────
def _q5(X, lb, sma=50):
    s = rmean(X.Cf, sma)
    valid = X.Cf.notna() & s.notna()
    above = (X.Cf > s).where(valid).astype('float64')
    return above.rolling(lb, min_periods=int(lb * 0.79)).mean()

@factor('q5_126', 'TQ', 'LIVE Elendel Q5: % of last 126d above SMA50')
def _(X): return _q5(X, 126)

@factor('q5_189', 'TQ', 'LIVE Zenith Q5: % of last 189d above SMA50')
def _(X): return _q5(X, 189)

@factor('q5_63', 'TQ', '% of last 63d above SMA50')
def _(X): return _q5(X, 63)

@factor('q5_252_sma100', 'TQ', '% of last 252d above SMA100')
def _(X): return _q5(X, 252, 100)

@factor('trend_t_126', 'TQ', 't-stat of log-price slope, 126d')
def _(X):
    lx = np.log(X.Cf)
    r, _s = _trend_stats(lx, X.t, 126)
    return r * np.sqrt((126 - 2) / (1 - r ** 2).clip(lower=1e-6))

@factor('trend_t_252', 'TQ', 't-stat of log-price slope, 252d')
def _(X):
    lx = np.log(X.Cf)
    r, _s = _trend_stats(lx, X.t, 252)
    return r * np.sqrt((252 - 2) / (1 - r ** 2).clip(lower=1e-6))

@factor('clenow_90', 'TQ', 'Clenow: annualised log-slope x R^2, 90d')
def _(X):
    r, s = _trend_stats(np.log(X.Cf), X.t, 90)
    return (np.exp(s * 252) - 1) * r ** 2

@factor('clenow_126', 'TQ', 'Clenow: annualised log-slope x R^2, 126d')
def _(X):
    r, s = _trend_stats(np.log(X.Cf), X.t, 126)
    return (np.exp(s * 252) - 1) * r ** 2

@factor('clenow_252', 'TQ', 'Clenow: annualised log-slope x R^2, 252d')
def _(X):
    r, s = _trend_stats(np.log(X.Cf), X.t, 252)
    return (np.exp(s * 252) - 1) * r ** 2

@factor('signed_r2_126', 'TQ', 'R^2 of log price vs time (126d) signed by slope')
def _(X):
    r, _s = _trend_stats(np.log(X.Cf), X.t, 126)
    return np.sign(r) * r ** 2

@factor('ker_126', 'TQ', 'Kaufman efficiency ratio, signed (126d net move / path length)')
def _(X): return (X.Cf - X.Cf.shift(126)) / rsum(X.Cf.diff().abs(), 126)

@factor('sma_stack_63', 'TQ', 'share of last 63d with C>SMA50>SMA150>SMA200 (Minervini stage 2)')
def _(X):
    s50, s150, s200 = rmean(X.Cf, 50), rmean(X.Cf, 150), rmean(X.Cf, 200)
    ok = ((X.Cf > s50) & (s50 > s150) & (s150 > s200)).astype('float64').where(s200.notna() & X.Cf.notna())
    return rmean(ok, 63)

@factor('calmar_252', 'TQ', '12-1 return / max drawdown (252d)')
def _(X):
    dd = (X.Cf / rmax(X.Cf, 252) - 1)
    mdd = rmin(dd, 252).abs().clip(lower=0.02)
    return (X.Cf.shift(21) / X.Cf.shift(252) - 1) / mdd


# ───────────────────────────── RISK ─────────────────────────────
@factor('lowvol_63', 'RISK', '-63d daily vol')
def _(X): return -rstd(X.r, 63)

@factor('lowvol_252', 'RISK', '-252d daily vol')
def _(X): return -rstd(X.r, 252)

@factor('low_ivol_252', 'RISK', '-residual vol vs market (252d)')
def _(X): return -rstd(X.resid, 252)

@factor('low_beta_252', 'RISK', '-beta to equal-weight market (252d)')
def _(X): return -X.beta

@factor('high_beta_252', 'RISK', '+beta to equal-weight market (252d)')
def _(X): return X.beta

@factor('low_downvol_252', 'RISK', '-downside semi-deviation (252d)')
def _(X): return -np.sqrt(rmean(X.r.clip(upper=0) ** 2, 252))

@factor('low_max_21', 'RISK', 'LIVE Zenith M3: -max daily return in last 21d (lottery avoidance)')
def _(X): return -rmax(X.r, 21)

@factor('low_max_63', 'RISK', '-max daily return in last 63d')
def _(X): return -rmax(X.r, 63)

@factor('low_skew_252', 'RISK', '-skewness of daily returns (252d)')
def _(X): return -X.r.rolling(252, min_periods=200).skew()

@factor('shallow_dd_252', 'RISK', 'worst drawdown vs trailing-252d peak (higher = shallower)')
def _(X): return rmin(X.Cf / rmax(X.Cf, 252) - 1, 252)

@factor('low_ulcer_126', 'RISK', '-ulcer index (126d)')
def _(X): return -np.sqrt(rmean((X.Cf / rmax(X.Cf, 126) - 1) ** 2, 126))

@factor('low_atrp_14', 'RISK', '-ATR14 / close')
def _(X): return -(X.true_range().ewm(com=13, adjust=False, min_periods=10).mean() / X.Cf)

@factor('vol_calm_21_252', 'RISK', '-(21d vol / 252d vol): recent calming')
def _(X): return -(rstd(X.r, 21) / rstd(X.r, 252))

@factor('low_volvol_126', 'RISK', '-(CV of |r| over 126d): stable-vol names')
def _(X):
    a = X.r.abs()
    return -(rstd(a, 126) / rmean(a, 126))

@factor('down_resilience_252', 'RISK', 'mean stock return on market days < -1% (252d)')
def _(X):
    flag = (X.mkt < -0.01).astype('float64')
    num = rsum(X.r.mul(flag, axis=0), 252)
    den = rsum(X.r.notna().astype('float64').mul(flag, axis=0), 252)
    return (num / den).where(den >= 5)

@factor('up_capture_252', 'RISK', 'mean stock return on market days > +1% (252d)')
def _(X):
    flag = (X.mkt > 0.01).astype('float64')
    num = rsum(X.r.mul(flag, axis=0), 252)
    den = rsum(X.r.notna().astype('float64').mul(flag, axis=0), 252)
    return (num / den).where(den >= 5)


# ───────────────────────────── VOLUME / FLOW ─────────────────────────────
@factor('illiq_amihud_63', 'VOL', '+Amihud illiquidity (|r|/DV, 63d): illiquidity premium')
def _(X): return rmean(X.r.abs() / (X.DV / 1e6), 63)

@factor('small_dvol_63', 'VOL', '-log median daily traded value (63d): size/liquidity-small proxy')
def _(X): return -np.log(X.DV.rolling(63, min_periods=40).median())

@factor('vol_surge_21_252', 'VOL', 'avg volume 21d / avg volume 252d (attention)')
def _(X): return rmean(X.V, 21) / rmean(X.V, 252)

@factor('dvol_growth_63_252', 'VOL', 'avg traded value 63d / 252d')
def _(X): return rmean(X.DV, 63) / rmean(X.DV, 252)

@factor('udvr_63', 'VOL', 'log(up-day volume / down-day volume), 63d')
def _(X):
    up = rsum(X.V.where(X.r > 0, 0.0), 63)
    dn = rsum(X.V.where(X.r < 0, 0.0), 63)
    return np.log((up + 1) / (dn + 1))

@factor('money_flow_63', 'VOL', 'sum(sign(r)*DV)/sum(DV), 63d')
def _(X): return rsum(np.sign(X.r) * X.DV, 63) / rsum(X.DV, 63)

@factor('money_flow_126', 'VOL', 'sum(sign(r)*DV)/sum(DV), 126d')
def _(X): return rsum(np.sign(X.r) * X.DV, 126) / rsum(X.DV, 126)

@factor('cmf_63', 'VOL', 'Chaikin money flow, 63d')
def _(X): return rsum(X.clv() * X.V, 63) / rsum(X.V, 63)

@factor('event_ret_63', 'VOL', 'sum of returns on abnormal-volume (>3x avg) days, 63d (event/PEAD proxy)')
def _(X):
    flag = (X.V > 3 * rmean(X.V, 50).shift(1)).astype('float64')
    return rsum(X.r.mul(flag, axis=0).fillna(0.0).where(X.Cf.notna()), 63)

@factor('event_gap_126', 'VOL', 'sum of overnight gaps on abnormal-volume days, 126d (earnings-reaction proxy)')
def _(X):
    flag = (X.V > 3 * rmean(X.V, 50).shift(1)).astype('float64')
    gap = X.O / X.Cf.shift(1) - 1
    return rsum((gap * flag).fillna(0.0).where(X.Cf.notna()), 126)


# ───────────────────────────── CANDLE / INTRADAY ─────────────────────────────
@factor('overnight_126', 'CNDL', 'sum log(open/prev close), 126d (overnight drift)')
def _(X): return rsum(np.log(X.O / X.Cf.shift(1)), 126)

@factor('intraday_126', 'CNDL', 'sum log(close/open), 126d')
def _(X): return rsum(np.log(X.C / X.O), 126)

@factor('overnight_minus_intraday_126', 'CNDL', 'overnight minus intraday drift, 126d')
def _(X): return rsum(np.log(X.O / X.Cf.shift(1)), 126) - rsum(np.log(X.C / X.O), 126)

@factor('clv_21', 'CNDL', 'mean close-location-value in daypr range, 21d')
def _(X): return rmean(X.clv(), 21)

@factor('clv_63', 'CNDL', 'mean close-location-value, 63d')
def _(X): return rmean(X.clv(), 63)

@factor('gapup_freq_63', 'CNDL', 'share of days gapping up >1.5% (63d)')
def _(X):
    g = (X.O / X.Cf.shift(1) - 1)
    return rmean((g > 0.015).astype('float64').where(g.notna()), 63)


# ───────────────────────────── REVERSAL ─────────────────────────────
@factor('rev_1w', 'REV', '-5d return')
def _(X): return -(X.Cf / X.Cf.shift(5) - 1)

@factor('rev_1m', 'REV', '-21d return')
def _(X): return -(X.Cf / X.Cf.shift(21) - 1)

@factor('rev_1m_volscaled', 'REV', '-21d return / 63d vol')
def _(X): return -(X.Cf / X.Cf.shift(21) - 1) / rstd(X.r, 63)

@factor('rev_vs_sma20', 'REV', '-(close/SMA20 - 1)')
def _(X): return -(X.Cf / rmean(X.Cf, 20) - 1)


# ───────────────────────────── BREAKOUT / COMPRESSION ─────────────────────────────
def _donch(X, w):
    lo, hi = rmin(X.Lf, w), rmax(X.Hf, w)
    return (X.Cf - lo) / (hi - lo)

@factor('donch_pos_20', 'BRK', 'position in 20d Donchian channel')
def _(X): return _donch(X, 20)

@factor('donch_pos_55', 'BRK', 'position in 55d Donchian channel')
def _(X): return _donch(X, 55)

@factor('donch_pos_126', 'BRK', 'position in 126d Donchian channel')
def _(X): return _donch(X, 126)

@factor('squeeze_bw', 'BRK', '-(Bollinger bandwidth now / its 126d mean): tight = high')
def _(X):
    bw = 4 * rstd(X.Cf, 20) / rmean(X.Cf, 20)
    return -(bw / rmean(bw, 126))

@factor('atr_contraction', 'BRK', '-(ATR14 / ATR63): volatility contraction (VCP-style)')
def _(X):
    tr = X.true_range()
    return -(rmean(tr, 14) / rmean(tr, 63))

@factor('range_contraction', 'BRK', '-(21d range / 63d range)')
def _(X):
    return -((rmax(X.Hf, 21) - rmin(X.Lf, 21)) / (rmax(X.Hf, 63) - rmin(X.Lf, 63)))

@factor('nr7_count_21', 'BRK', 'count of NR7 (narrowest-range-of-7) days in last 21d')
def _(X):
    rng = (X.Hf - X.Lf)
    return rsum((rng <= rmin(rng, 7)).astype('float64').where(rng.notna()), 21)

@factor('tight_close_15', 'BRK', '-(15d close std / mean): tight closes')
def _(X): return -(rstd(X.Cf, 15) / rmean(X.Cf, 15))

@factor('nh_count_21', 'BRK', 'new 252d closing highs in last 21d')
def _(X): return rsum(X.newhigh_flag(252), 21)

@factor('nh_volconfirm_63', 'BRK', 'new 252d highs on >1.5x volume, last 63d')
def _(X):
    vs = (X.V > 1.5 * rmean(X.V, 50).shift(1)).astype('float64')
    return rsum(X.newhigh_flag(252).mul(vs), 63)


# ───────────────────────────── RELATIVE STRENGTH ─────────────────────────────
@factor('rs_trend_t_126', 'RS', 't-stat of RS-line (stock/market) log slope, 126d')
def _(X):
    r, _s = _trend_stats(X.logRS, X.t, 126)
    return r * np.sqrt((126 - 2) / (1 - r ** 2).clip(lower=1e-6))

@factor('rs_clenow_126', 'RS', 'RS-line annualised slope x R^2, 126d')
def _(X):
    r, s = _trend_stats(X.logRS, X.t, 126)
    return (np.exp(s * 252) - 1) * r ** 2

@factor('rs_near_high_63', 'RS', 'share of last 63d with RS line within 3% of its 252d high')
def _(X):
    rs = X.Cf.div(X.bench, axis=0)
    ok = (rs >= 0.97 * rmax(rs, 252)).astype('float64').where(rs.notna())
    return rmean(ok, 63)

@factor('rs_win_months_12', 'RS', 'fraction of last 12 monthly blocks beating the market')
def _(X):
    wins, n = 0, 0
    for k in range(0, 12):
        a = X.Cf.shift(21 * k) / X.Cf.shift(21 * (k + 1)) - 1
        b = X.bench.shift(21 * k) / X.bench.shift(21 * (k + 1)) - 1
        w = a.gt(b, axis=0).astype('float64').where(a.notna())
        wins = wins + w.fillna(0.0)
        n = n + a.notna().astype('float64')
    return (wins / n).where(n >= 9)

@factor('rs_accel', 'RS', 'RS-line 3m change minus prior 3m change')
def _(X):
    rs = X.Cf.div(X.bench, axis=0)
    return (rs / rs.shift(63)) - (rs.shift(63) / rs.shift(126))




# ───────────────────────────── STAGE-2 ADDITIONS ─────────────────────────────
# continuation-vs-skip-month tests (live strategies skip the most recent month)
@factor('mom_1w', 'MOM', '5d return (continuation test)')
def _(X): return X.Cf / X.Cf.shift(5) - 1

@factor('mom_1m', 'MOM', '21d return (continuation test; live signals skip this month)')
def _(X): return X.Cf / X.Cf.shift(21) - 1

@factor('mom_3_0', 'MOM', '3m return, no skip')
def _(X): return X.Cf / X.Cf.shift(63) - 1

@factor('mom_6_0', 'MOM', '6m return, no skip')
def _(X): return X.Cf / X.Cf.shift(126) - 1

@factor('mom_12_0', 'MOM', '12m return, no skip')
def _(X): return X.Cf / X.Cf.shift(252) - 1

@factor('weekly_consist_26', 'MOM', 'fraction of last 26 weekly (5d) blocks with positive return')
def _(X):
    blocks = [(X.Cf.shift(5 * k) / X.Cf.shift(5 * (k + 1)) - 1) for k in range(0, 26)]
    pos = sum((b > 0).astype('float64').where(b.notna()).fillna(0.0) for b in blocks)
    n = sum(b.notna().astype('float64') for b in blocks)
    return (pos / n).where(n >= 20)

@factor('rs_weekly_win_26', 'RS', 'fraction of last 26 weekly blocks beating the market')
def _(X):
    wins, n = 0, 0
    for k in range(0, 26):
        a = X.Cf.shift(5 * k) / X.Cf.shift(5 * (k + 1)) - 1
        b = X.bench.shift(5 * k) / X.bench.shift(5 * (k + 1)) - 1
        w = a.gt(b, axis=0).astype('float64').where(a.notna())
        wins = wins + w.fillna(0.0)
        n = n + a.notna().astype('float64')
    return (wins / n).where(n >= 20)

@factor('hi_3y', 'HIGH', 'close / 756d high')
def _(X): return X.Cf / rmax(X.Hf, 756)

def _ovn(X): return np.log(X.O / X.Cf.shift(1)).clip(-0.15, 0.15)
def _intr(X): return np.log(X.C / X.O).clip(-0.15, 0.15)

@factor('intra_over_63', 'CNDL', 'intraday drift minus overnight drift, 63d (clipped +-15%/day)')
def _(X): return rsum(_intr(X), 63) - rsum(_ovn(X), 63)

@factor('intra_over_126', 'CNDL', 'intraday drift minus overnight drift, 126d (clipped)')
def _(X): return rsum(_intr(X), 126) - rsum(_ovn(X), 126)

@factor('intra_over_252', 'CNDL', 'intraday drift minus overnight drift, 252d (clipped)')
def _(X): return rsum(_intr(X), 252) - rsum(_ovn(X), 252)

@factor('intraday_126_clip', 'CNDL', 'intraday drift 126d (clipped)')
def _(X): return rsum(_intr(X), 126)

@factor('neg_overnight_126_clip', 'CNDL', '-overnight drift 126d (clipped)')
def _(X): return -rsum(_ovn(X), 126)

@factor('low_gap_share_126', 'CNDL', '-(share of absolute movement that happens overnight), 126d')
def _(X):
    a, b = rsum(_ovn(X).abs(), 126), rsum(_intr(X).abs(), 126)
    return -(a / (a + b))

@factor('low_gap_vol_126', 'CNDL', '-std of overnight gaps, 126d')
def _(X): return -rstd(_ovn(X), 126)

@factor('low_ulcer_63', 'RISK', '-ulcer index (63d)')
def _(X): return -np.sqrt(rmean((X.Cf / rmax(X.Cf, 63) - 1) ** 2, 63))

@factor('low_ulcer_252', 'RISK', '-ulcer index (252d)')
def _(X): return -np.sqrt(rmean((X.Cf / rmax(X.Cf, 252) - 1) ** 2, 252))

@factor('low_pain_126', 'RISK', 'mean drawdown from trailing 126d peak (higher = less pain)')
def _(X): return rmean(X.Cf / rmax(X.Cf, 126) - 1, 126)

@factor('lowvol_126', 'RISK', '-126d daily vol')
def _(X): return -rstd(X.r, 126)




# ───────────────────────────── STAGE-3 ADDITIONS (volatility-flavoured / csm_absolute-style) ─────────────────────────────
@factor('vr_5_252', 'TQ', 'variance ratio VR(5) over 252d: >1 = trending, <1 = mean-reverting daily path')
def _(X):
    r5 = X.Cf / X.Cf.shift(5) - 1
    return rstd(r5, 252) ** 2 / (5 * rstd(X.r, 252) ** 2)

@factor('autocorr1_126', 'TQ', 'lag-1 autocorrelation of daily returns, 126d')
def _(X): return X.r.rolling(126, min_periods=100).corr(X.r.shift(1))

@factor('dist_high_atr', 'HIGH', '-(252d high - close) / ATR14: distance to the high measured in ATRs')
def _(X):
    atr = X.true_range().ewm(com=13, adjust=False, min_periods=10).mean()
    return -(rmax(X.Hf, 252) - X.Cf) / atr

@factor('low_jump_dn_freq_126', 'RISK', '-share of days with a >2.5 sigma down move (126d)')
def _(X):
    z = X.r / rstd(X.r, 126).shift(1)
    return -rmean((z < -2.5).astype('float64').where(z.notna()), 126)

@factor('jump_up_freq_126', 'RISK', 'share of days with a >2.5 sigma up move (126d)')
def _(X):
    z = X.r / rstd(X.r, 126).shift(1)
    return rmean((z > 2.5).astype('float64').where(z.notna()), 126)

@factor('hvol_126', 'RISK', '+126d daily vol (volatility-seeking; csm_absolute-style aggressive books)')
def _(X): return rstd(X.r, 126)

@factor('hvol_trend_126', 'RISK', '126d vol x sign of 126d trend (volatile uptrends high, volatile downtrends low)')
def _(X):
    return rstd(X.r, 126) * np.sign(X.Cf / X.Cf.shift(126) - 1)

@factor('atr_expansion_14_63', 'BRK', 'ATR14 / ATR63: volatility expansion')
def _(X):
    tr = X.true_range()
    return rmean(tr, 14) / rmean(tr, 63)

@factor('range_expansion_up', 'BRK', 'count of up days in last 21 with true range > 1.5x ATR63 and close in top half')
def _(X):
    tr = X.true_range(); atr63 = rmean(tr, 63).shift(1)
    flag = ((tr > 1.5 * atr63) & (X.r > 0) & (X.clv() > 0)).astype('float64').where(atr63.notna())
    return rsum(flag, 21)


# ───────────────────────────── BUILD ─────────────────────────────
def signal_dates(index):
    s = pd.Series(index, index=index)
    return pd.DatetimeIndex(s.groupby([index.year, index.month]).max().values)


def season_factor(Cf, sig, step=12, n_back=5, min_obs=3):
    """mean return of the upcoming month over the same calendar slot in the previous n_back cycles
    (step=12 -> same calendar month; step=3 -> same position in the earnings quarter)"""
    m = Cf.ffill().reindex(sig)
    R = m / m.shift(1) - 1
    parts = [R.shift(step * k - 1) for k in range(1, n_back + 1)]
    stack = np.stack([p.values for p in parts])
    cnt = np.isfinite(stack).sum(axis=0)
    with np.errstate(all='ignore'):
        mean = np.nanmean(np.where(np.isfinite(stack), stack, np.nan), axis=0)
    out = pd.DataFrame(mean, index=sig, columns=Cf.columns)
    return out.where(cnt >= min_obs)


SEASONS = {
    'season_same_month_5y': dict(step=12, n_back=5, min_obs=3),
    'season_same_month_3y': dict(step=12, n_back=3, min_obs=2),
    'season_same_month_8y': dict(step=12, n_back=8, min_obs=5),
    'season_qtr_8q':        dict(step=3,  n_back=8, min_obs=5),
}




def _csm_abs(X, sig, lookback=9, short=4, lag=1, which='dual'):
    """csm_absolute's own ranking score: monthly-vol-normalised return, 9m & 4m legs averaged (lag 1m), clipped +-5"""
    mp = X.Cf.ffill().reindex(sig)
    mret = mp.pct_change(fill_method=None)
    def leg(lb):
        ret = mp.shift(lag) / mp.shift(lag + lb) - 1
        vol = mret.rolling(lb).std().shift(lag) * np.sqrt(12)
        return ret / vol.replace(0, np.nan)
    if which == 'dual':
        return ((leg(lookback) + leg(short)) / 2.0).clip(-5, 5)
    return leg(6).clip(-5, 5)


def _beta_regime(X, sig):
    bull = (X.bench > rmean(X.bench, 200)).reindex(sig).fillna(False)
    sign = np.where(bull.values, 1.0, -1.0)
    return X.beta.reindex(sig).mul(sign, axis=0)


SPECIALS = {
    'csm_abs_dual_sharpe': lambda X, sig: _csm_abs(X, sig, which='dual'),
    'csm_abs_sharpe6': lambda X, sig: _csm_abs(X, sig, which='s6'),
    'beta_regime': _beta_regime,
}


def build_all(P, names=None, verbose=True):
    X = Ctx(P)
    sig = signal_dates(X.C.index)
    out = {}
    for name, (fam, desc, fn) in REGISTRY.items():
        if names and name not in names:
            continue
        df = fn(X)
        out[name] = df.reindex(sig).astype('float32')
        if verbose:
            print(f'  built {name:<28} ({fam})', flush=True)
        del df
    for sname, fn in SPECIALS.items():
        if names is None or sname in names:
            out[sname] = fn(X, sig).astype('float32')
            if verbose:
                print(f'  built {sname:<28} (SPECIAL)', flush=True)
    for sname, kw in SEASONS.items():
        if names is None or sname in names:
            out[sname] = season_factor(X.Cf, sig, **kw).astype('float32')
            if verbose:
                print(f'  built {sname:<28} (SEAS)', flush=True)
    return X, sig, out


FAMILY = {n: v[0] for n, v in REGISTRY.items()}
DESC = {n: v[1] for n, v in REGISTRY.items()}
for _n in SPECIALS:
    FAMILY[_n] = 'MOM' if 'csm' in _n else 'RISK'
    DESC[_n] = _n
for _n, _kw in SEASONS.items():
    FAMILY[_n] = 'SEAS'
    DESC[_n] = (f"seasonality: mean return of the upcoming month over its last {_kw['n_back']} "
                f"same-slot cycles (step={_kw['step']}m)")
