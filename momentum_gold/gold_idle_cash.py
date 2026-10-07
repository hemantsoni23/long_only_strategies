"""
gold_idle_cash.py
=================
GoldIdleCashOverlay -- park a CAPPED slice of a momentum book's idle cash in a gold ETF when the market is weak.

What it does
------------
The live-chassis momentum books (Elendel / Zenith / Quad) are rarely fully invested: with top-15 names at a 5% cap at most 75% is
ever invested, and regime leverage / vol targeting / Crash Guard cut it further (idle cash averages ~35-46% and reaches 64-100% in
weak regimes). This overlay decides what that idle cash holds:

    gold weight  = min(idle cash weight, cap)          when the engine's regime is weak (BEAR / PANIC / HIGH_VOL)
                 = 0                                    otherwise
    rest of idle cash -> liquid fund (LIQUIDBEES) at ~6.5%

The stock decisions are untouched. In the engine's return line, `cash_w * cash_rate` is simply replaced, which is why this can be applied
as an exact post-processing step on a finished backtest (see run_momentum_gold_report.py) and as a one-line rule live.

Evidence summary (3 live-chassis strategies, 15 usable years; see README.md)
---------------------------------------------------------------------------
  * ALL idle cash -> gold in weak markets (uncapped) HURTS: Sharpe -0.09..-0.17, max drawdown 5-11 pts deeper (the book becomes mostly gold in stress).
  * Capped at 10% of the portfolio: CAGR +0.6 pt, Sharpe +0.025..+0.03, max drawdown ~unchanged; if gold's excess drift were zero the effect is ~0
    (no harm). It does NOT reduce drawdowns of these books -- their drawdowns happen with the book already largely in cash.
  * The much larger, riskless lever is the liquid-fund sweep itself (Elendel/Quad backtests assume idle cash earns 0%).

Data note: GOLDBEES history has a 2011-01..2014-12 hole. The overlay never trades gold when its return cannot be trusted (missing price, or a
return spanning a gap): that day's idle cash stays in the liquid fund.
"""
import os
import numpy as np
import pandas as pd

ETF_FOLDER = '/Users/hemantsoni/Documents/upstox_data_folder/etf_ohlcv_data'
WEAK_REGIMES = ('BEAR', 'PANIC', 'HIGH_VOL')


def load_close(path):
    df = pd.read_csv(path)
    dc = [c for c in df.columns if c.lower() in ('datetime', 'date', 'timestamp')][0]
    idx = pd.to_datetime(df[dc], errors='coerce', utc=True).dt.tz_convert('Asia/Kolkata').dt.tz_localize(None).dt.normalize()
    s = pd.Series(df['close'].values, index=idx).sort_index()
    s = s[~s.index.duplicated(keep='last')]
    return s.where(s > 0)


class GoldIdleCashOverlay:
    def __init__(
        self,
        cap                 = 0.10,                 # max gold weight as a share of TOTAL portfolio value
        regimes             = WEAK_REGIMES,         # engine regime labels in which gold is allowed
        mode                = 'weak',               # 'weak' = only in `regimes` | 'always' = every day (cap still applies) | 'off'
        liquid_fund_annual  = 0.065,                # return on the non-gold part of idle cash
        gold_cost_one_way   = 0.0015,               # cost on |change in gold weight|
        gold_symbol         = 'GOLDBEES',
        etf_folder          = ETF_FOLDER,
        stale_days          = 5,
        drift_multiplier    = 1.0,                  # RESEARCH ONLY: 1 = actual gold returns; 0 = gold's excess drift over the liquid fund removed
    ):
        if mode not in ('weak', 'always', 'off'):
            raise ValueError("mode must be 'weak', 'always' or 'off'")
        self.cap, self.regimes, self.mode = cap, tuple(regimes), mode
        self.lf_daily = (1 + liquid_fund_annual) ** (1 / 252) - 1
        self.cost = gold_cost_one_way
        self.gold_symbol, self.etf_folder, self.stale_days = gold_symbol, etf_folder, stale_days
        self.drift_multiplier = drift_multiplier
        self._close = None
        print(f"GoldIdleCashOverlay | mode={mode} cap={cap:.0%} regimes={self.regimes} lf={liquid_fund_annual:.1%} cost={gold_cost_one_way:.2%}"
              + ("" if drift_multiplier == 1.0 else f" | RESEARCH drift_multiplier={drift_multiplier}"))

    # ------------------------------------------------------------------ data
    def _gold_close(self):
        if self._close is None:
            self._close = load_close(os.path.join(self.etf_folder, self.gold_symbol + '.csv'))
        return self._close

    def gold_daily_returns(self, index):
        """daily gold return on `index`; NaN when it cannot be trusted (no price, or a return that spans a data gap)."""
        c = self._gold_close()
        r = c.pct_change(fill_method=None)
        r[c.index.to_series().diff().dt.days > 5] = np.nan
        return r.reindex(index)

    # ------------------------------------------------------------------ live rule
    def target_gold_weight(self, idle_cash_weight, regime):
        """Gold weight (share of total portfolio) the overlay wants today."""
        if self.mode == 'off' or idle_cash_weight <= 0:
            return 0.0
        if self.mode == 'weak' and regime not in self.regimes:
            return 0.0
        return float(min(idle_cash_weight, self.cap))

    def live_instruction(self, idle_cash_weight, regime, today=None):
        """What to hold in the idle bucket today. Raises if the gold price feed is stale."""
        last = self._gold_close().dropna().index[-1]
        today = pd.Timestamp(today) if today is not None else pd.Timestamp.today().normalize()
        if (today - last).days > self.stale_days:
            raise RuntimeError(f"stale gold price: last close {last.date()} is {(today - last).days} days old (> {self.stale_days})")
        g = self.target_gold_weight(idle_cash_weight, regime)
        return {'regime': regime, 'idle_cash_weight': idle_cash_weight, 'gold_weight': g, 'liquid_fund_weight': max(idle_cash_weight - g, 0.0),
                'reason': ('regime weak -> capped gold' if g > 0 else 'regime not weak or no idle cash -> all idle cash in liquid fund')}

    # ------------------------------------------------------------------ backtest (post-processing of an engine run)
    def apply(self, executed_weights, net_returns, regime, daily_cash_rate):
        """executed_weights, net_returns, regime: the live engine's daily outputs. Returns a DataFrame with the overlay's daily net return."""
        idx = executed_weights.index
        net = net_returns.reindex(idx)
        cash_w = (1.0 - executed_weights.sum(axis=1)).clip(lower=0.0)
        eq_part = net - cash_w * daily_cash_rate                       # stock P&L net of the engine's own stock trading costs
        rg = self.gold_daily_returns(idx)
        valid = rg.notna()
        if self.drift_multiplier != 1.0:
            drift = (rg[valid] - self.lf_daily).mean()
            rg = rg - (1 - self.drift_multiplier) * drift
        reg = regime.reindex(idx)
        if self.mode == 'off':
            allowed = pd.Series(0.0, index=idx)
        elif self.mode == 'always':
            allowed = pd.Series(1.0, index=idx)
        else:
            allowed = reg.isin(self.regimes).astype(float)
        gold_w = np.minimum(self.cap * allowed, cash_w).where(valid, 0.0)
        liq_w = cash_w - gold_w
        cost = gold_w.diff().abs().fillna(0.0) * self.cost
        out = pd.DataFrame({
            'net_return': eq_part + liq_w * self.lf_daily + gold_w * rg.fillna(0.0) - cost,
            'gold_weight': gold_w, 'liquid_weight': liq_w, 'idle_cash_weight': cash_w, 'gold_valid': valid, 'regime': reg,
        })
        return out

    # ------------------------------------------------------------------ metrics
    @staticmethod
    def metrics(r, rf=0.06):
        r = r.dropna()
        eq = (1 + r).cumprod(); yrs = len(r) / 252
        cagr = eq.iloc[-1] ** (1 / yrs) - 1
        vol = r.std() * np.sqrt(252)
        rfd = (1 + rf) ** (1 / 252) - 1
        sharpe = (r - rfd).mean() / r.std() * np.sqrt(252)
        dd = (eq / eq.cummax() - 1)
        mth = (1 + r).groupby([r.index.year, r.index.month]).prod() - 1
        return dict(cagr=cagr, vol=vol, sharpe=sharpe, max_drawdown=dd.min(), calmar=cagr / abs(dd.min()), worst_month=mth.min(), days=len(r))
