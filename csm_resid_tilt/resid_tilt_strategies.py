"""
resid_tilt_strategies.py
========================
CSMZenithResid / CSMElendelResid -- the live Zenith / Elendel engines with ONE change: a CAPM residual-momentum term is added to the monthly ranking score.

    score = z(base score) + resid_weight * z(residual momentum 12-1)          (default resid_weight = 0.5)

Everything else (universe filter, absolute-momentum gate, hysteresis/swap gap, inverse-vol sizing, stops, Crash Guard, regime leverage, costs) is inherited unchanged from the live
classes in Old_live_strategies, which are imported, never edited or copied.  resid_weight=0 reproduces the live engine bit for bit.

Why this change (see factor_research/MASTER_RANKING.md, ranks 1-2; real-engine backtests, unmodified engines, 0.3% cost):
    Zenith  +0.5*resid : Sharpe 1.87 -> 2.21 (2005+), 1.48 -> 1.98 (2015+); CAGR +6.1 / +8.8 pt; bootstrap P(better) 1.00 / 1.00
    Elendel +0.5*resid : Sharpe 1.81 -> 2.03 (2005+), 1.66 -> 1.91 (2015+); CAGR +4.5 / +5.1 pt; P 0.97 / 0.93
    (planning expectation: about half of the 2015+ gain.)  Weight 0.5 was fixed before testing, not tuned.

Residual momentum 12-1 (identical to factor_research `mom_resid_12_1`):
    r_i,t  = daily return (close forward-filled at most 5 days)
    beta_i = rolling 252d cov(r_i, r_mkt) / var(r_mkt)  (min 200 obs), lagged one day
    e_i,t  = r_i,t - beta_i,t-1 * r_mkt,t                 (r_mkt = the engine's own equal-weight benchmark)
    signal = sum of e over the last 231 trading days (min 184 obs), skipping the most recent 21 days; value at month-end.
Look-ahead: every ingredient is lagged or trailing; `test_resid_tilt.py` checks that truncating the data at a month-end does not change that month's row.

Missing residual momentum (young stocks, < 184 obs) is treated as neutral (z = 0), and months where fewer than 60 names have it leave the base score unchanged.
"""
import os
import sys

import numpy as np
import pandas as pd

LIVE = '/Users/hemantsoni/Documents/long_only_strategies/Old_live_strategies'
if LIVE not in sys.path:
    sys.path.insert(0, LIVE)

from csm_zenith_strategy import CSMZenith          # noqa: E402
from csm_elendel_strategy import CSMElendel        # noqa: E402

RESID_WINDOW = 231
RESID_SKIP = 21
BETA_WINDOW = 252
BETA_MIN = 200
MIN_NAMES = 60


def _mp(w):
    return max(2, int(w * 0.8))


def residual_momentum_daily(prices, benchmark):
    """Daily frame of residual momentum 12-1 (see module docstring). `benchmark` is the engine's equal-weight benchmark level series."""
    ret = prices.ffill(limit=5).pct_change(fill_method=None)
    mkt = benchmark.reindex(prices.index).ffill().pct_change(fill_method=None)
    beta = (ret.rolling(BETA_WINDOW, min_periods=BETA_MIN).cov(mkt)
            .div(mkt.rolling(BETA_WINDOW, min_periods=BETA_MIN).var(), axis=0))
    resid = ret.sub(beta.shift(1).mul(mkt, axis=0))
    return resid.rolling(RESID_WINDOW, min_periods=_mp(RESID_WINDOW)).sum().shift(RESID_SKIP)


def _zscore(df):
    return df.sub(df.mean(axis=1), axis=0).div(df.std(axis=1), axis=0)


def blend_resid(base, resid_monthly, weight, min_names=MIN_NAMES):
    """z(base) + weight*z(resid) on the base score's own universe; base returned unchanged where weight==0 or too few residual values."""
    if weight == 0:
        return base
    e = resid_monthly.reindex(index=base.index, columns=base.columns).where(base.notna())
    ok = e.notna().sum(axis=1) >= min_names
    z = _zscore(base) + weight * _zscore(e).fillna(0.0)
    return base.where(~ok.reindex(base.index).fillna(False), z)


class _ResidTiltMixin:
    resid_weight = 0.5

    def _init_tilt(self, resid_weight):
        self.resid_weight = resid_weight
        print(f"  [resid tilt] residual-momentum weight = {resid_weight}"
              + ("  (== live engine)" if resid_weight == 0 else ""))

    def calculate_factors(self):
        super().calculate_factors()
        self.base_factors = self.factors.copy()                      # untouched live score, kept for diagnostics / parity tests
        monthly_prices = self.prices.resample('ME').last()
        rm = (residual_momentum_daily(self.prices, self.benchmark)
              .resample('ME').last().reindex(monthly_prices.index))
        self.resid_mom = rm
        self.factors = blend_resid(self.factors, rm, self.resid_weight)
        self.factors.dropna(how='all', inplace=True)
        print(f"  [resid tilt] blended score shape {self.factors.shape}; "
              f"residual-momentum coverage (avg names/month inside universe): "
              f"{rm.reindex(self.factors.index).where(self.base_factors.reindex(self.factors.index).notna()).notna().sum(axis=1).mean():.0f}")
        return self.factors


class CSMZenithResid(_ResidTiltMixin, CSMZenith):
    def __init__(self, *args, resid_weight=0.5, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_tilt(resid_weight)


class CSMElendelResid(_ResidTiltMixin, CSMElendel):
    def __init__(self, *args, resid_weight=0.5, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_tilt(resid_weight)
