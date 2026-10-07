"""
value_strategy.py
=================
CSM Earnings-Yield -- a monthly, long-only value-with-earnings-growth strategy.  Built as a different return stream from the momentum books: it ranks on what a company earns
relative to its price, not on how the price has moved, and uses no price-trend condition at all.

Signal (month-end, point-in-time; trade at the next close):
    eligible : liquidity rank 301-1000 (63d median traded value; the 300 largest are excluded), price > 20, <= 5 circuit-locked days in 63,
               latest quarterly result filed <= 140 days ago, TTM net profit > 0, latest quarter's yoy net-profit growth > 0 (earnings still rising), E/P <= 50% (data-error guard)
    rank     : E/P = TTM net profit / (price x shares outstanding), highest first
    hold     : top `top_n` (20); a held name stays until it falls below rank `exit_rank` (30) or stops being eligible; equal weight 1/top_n of equity at entry (no rebalancing of survivors)
    risk     : hard stop -20% from entry (close-based, sell at next open less 0.3% slippage), 20-day cooldown; new entries sized at `exposure_bear` (0.7) when the equal-weight benchmark is
               below its SMA200 on the signal day; idle cash earns the liquid-fund rate; costs charged on every trade.
Why: Asness (1997) and Novy-Marx (2012) -- value and momentum are negatively correlated across stocks; in the user's data E/P books were ~0.45 correlated with the live engines (vs ~0.8 for
price-momentum variants).  Evidence is short: fundamentals exist only for results filed 2018-05..2025-04, so the backtest covers ~2019-03..2025-06 and a single cheap-cyclical regime.
Interface mirrors the other strategies: calculate_factors(), get_positions(), get_exit_signals(...), plus get_target_portfolio(...) for live use and simulate() (the single loop).
"""
import datetime as _dt

import numpy as np
import pandas as pd

from value_fundamentals import build_results, monthly_frame


class EarningsYieldStrategy:
    def __init__(
        self, prices_df, volumes_df, highs_df=None, lows_df=None, opens_df=None, benchmark_series=None, results_df=None,
        top_n=20, exit_rank=30, universe_min_n=301, universe_top_n=1000, min_price=20.0, max_circuit_days=5,
        max_age=140, require_profit_growth=True, max_ep=0.50, min_eligible=60,
        hard_stop=0.20, stop_slippage_pct=0.003, stop_cooldown_days=20,
        exposure_bear=0.70, gate_sma=200,
        transaction_cost=0.003, cash_annual_rate=0.065, initial_capital=100_000.0,
    ):
        if benchmark_series is None:
            raise ValueError('benchmark_series required (regime gate).')
        self.prices, self.volumes = prices_df, volumes_df
        self.highs = highs_df if highs_df is not None else pd.DataFrame()
        self.lows = lows_df if lows_df is not None else pd.DataFrame()
        self.opens = opens_df if opens_df is not None else pd.DataFrame()
        self.benchmark = benchmark_series
        self._results_in = results_df
        self.top_n, self.exit_rank = top_n, exit_rank
        self.universe_min_n, self.universe_top_n, self.min_price, self.max_circuit_days = universe_min_n, universe_top_n, min_price, max_circuit_days
        self.max_age, self.require_profit_growth, self.max_ep, self.min_eligible = max_age, require_profit_growth, max_ep, min_eligible
        self.hard_stop, self.stop_slippage_pct, self.stop_cooldown_days = hard_stop, stop_slippage_pct, stop_cooldown_days
        self.exposure_bear, self.gate_sma = exposure_bear, gate_sma
        self.transaction_cost, self.cash_annual_rate, self.initial_capital = transaction_cost, cash_annual_rate, initial_capital
        self.ep = None; self.positions = None; self.results = None; self.position_metadata = []
        print(f"CSM Earnings-Yield initialised | top {top_n} by E/P (exit rank {exit_rank}), liquidity rank {universe_min_n}-{universe_top_n}, price>{min_price}, "
              f"profit growth>0: {require_profit_growth}, E/P<={max_ep:.0%}\n  stop {hard_stop:.0%}, bear exposure {exposure_bear:.0%} (SMA{gate_sma}), "
              f"cost {transaction_cost:.2%}/side, cash {cash_annual_rate:.1%}")

    # ───────────────────────────── signals ─────────────────────────────
    def calculate_factors(self):
        P = self.prices
        self._dates = P.index; self._cols = {s: i for i, s in enumerate(P.columns)}
        cf = P.ffill(); self._C = cf.values
        op = self.opens.reindex(index=P.index, columns=P.columns) if not self.opens.empty else pd.DataFrame(np.nan, index=P.index, columns=P.columns)
        self._O = op.where(op.notna(), cf).values; self._Craw = P.values
        self._dv = (P * self.volumes.reindex(index=P.index, columns=P.columns)).rolling(63, min_periods=21).median().shift(1)
        if not self.highs.empty and not self.lows.empty:
            circ = ((self.highs == self.lows) & self.highs.notna()).astype('float64').rolling(63, min_periods=1).sum().shift(1)
        else:
            circ = pd.DataFrame(0.0, index=P.index, columns=P.columns)
        self._circ = circ.reindex(index=P.index, columns=P.columns).values
        self._prev_close = cf.shift(1).values
        self._rank_cache = {}
        b = self.benchmark.reindex(P.index).ffill()
        self._bear = (b < b.rolling(self.gate_sma, min_periods=int(self.gate_sma * 0.8)).mean()).values       # evaluated on the signal day's own close
        # month-end signal days (last trading day of each month)
        s = pd.Series(np.arange(len(P)), index=P.index)
        self._sig_idx = s.groupby([P.index.year, P.index.month]).last().values
        self._sig_idx = self._sig_idx[self._sig_idx + 1 < len(P)]
        res = build_results(symbols=list(P.columns)) if self._results_in is None else self._results_in
        sd = P.index[self._sig_idx]
        npttm = monthly_frame(res, 'np_ttm', sd, P.columns, self.max_age)
        shares = monthly_frame(res, 'shares', sd, P.columns, self.max_age)
        growth = monthly_frame(res, 'sg_np', sd, P.columns, self.max_age)
        px = pd.DataFrame(self._C[self._sig_idx], index=sd, columns=P.columns)
        ep = (npttm / (px * shares)).replace([np.inf, -np.inf], np.nan)
        ok = (npttm > 0) & (ep <= self.max_ep) & ep.notna()
        if self.require_profit_growth:
            ok &= (growth > 0)
        self.ep = ep.where(ok)
        self._ep_by_idx = {int(i): self.ep.iloc[k] for k, i in enumerate(self._sig_idx)}
        print(f"  signal months {len(self._sig_idx)} | fundamentals-eligible names per month (median over months with data) {int(ok.sum(axis=1)[ok.sum(axis=1) > 0].median())}")
        return self.ep

    def _rank_row(self, i):
        r = self._rank_cache.get(i)
        if r is None:
            r = self._dv.iloc[i].rank(ascending=False, method='min').values; self._rank_cache[i] = r
        return r

    def _universe_ok(self, i, j):
        """Eligibility on trading-day index i using data up to the PRIOR close."""
        if i >= len(self._dates) or not (self._prev_close[i, j] > self.min_price):
            return False
        rk = self._rank_row(i)[j]
        return bool(self.universe_min_n <= rk <= self.universe_top_n and self._circ[i, j] <= self.max_circuit_days)

    def _select(self, sig_idx, held_cols):
        """Target set for the rebalance decided at signal day `sig_idx` (execution on sig_idx+1). Returns (keep, buy) lists of column indices, best first."""
        exec_i = sig_idx + 1
        e = self._ep_by_idx.get(int(sig_idx))
        if e is None:
            return [], []
        e = e.dropna()
        elig = [(self._cols[s], v) for s, v in e.items() if self._universe_ok(exec_i, self._cols[s]) and not np.isnan(self._Craw[sig_idx, self._cols[s]])]
        if len(elig) < self.min_eligible:
            return [], []                                   # too thin: hold nothing new, sell what is held (cash)
        elig.sort(key=lambda x: -x[1])
        rank = {j: k + 1 for k, (j, _) in enumerate(elig)}
        keep = [j for j in held_cols if j in rank and rank[j] <= self.exit_rank]
        buy = [j for j, _ in elig if j not in keep][: max(0, self.top_n - len(keep))]
        return keep, buy

    # ───────────────────────────── shared exit rule ─────────────────────────────
    def stop_decision(self, entry_price, close):
        return ('exit_next_open', 'STOP_HIT') if close <= entry_price * (1 - self.hard_stop) else (None, None)

    # ───────────────────────────── the single event loop ─────────────────────────────
    def simulate(self, start=None, end=None):
        if self.ep is None:
            raise ValueError('Call calculate_factors() first.')
        dates = self._dates; n = len(dates); cols = list(self.prices.columns); C, O = self._C, self._O
        cost, slip = self.transaction_cost, self.stop_slippage_pct
        rf_d = (1 + self.cash_annual_rate) ** (1 / 252) - 1
        first_sig = next((int(i) for i in self._sig_idx if len(self._ep_by_idx[int(i)].dropna()) >= self.min_eligible), None)
        if first_sig is None:
            raise RuntimeError('no signal month has enough eligible names')
        i0 = first_sig + 1 if start is None else max(first_sig + 1, int(dates.searchsorted(pd.Timestamp(start))))
        i1 = n - 1 if end is None else min(n - 1, int(dates.searchsorted(pd.Timestamp(end), side='right')) - 1)
        exec_map = {int(i) + 1: int(i) for i in self._sig_idx}
        cash = self.initial_capital; hold = {}; stop_pending = {}; cooldown = {}
        equity = np.full(n, np.nan); W = np.zeros((n, len(cols)), dtype=np.float32); trades = []; daily = []
        for i in range(i0, i1 + 1):
            cash *= (1 + rf_d)
            for j in list(stop_pending):
                if j in hold:
                    px = O[i, j] * (1 - slip); h = hold.pop(j); cash += h['shares'] * px * (1 - cost)
                    trades.append(self._trade(h, cols[j], dates[i], px, 'STOP_HIT', h['shares'] * px * (1 - cost), i)); cooldown[j] = i
                stop_pending.pop(j, None)
            for j, h in hold.items():
                if j not in stop_pending and i + 1 <= i1:
                    act, _ = self.stop_decision(h['entry_price'], C[i, j])
                    if act:
                        stop_pending[j] = 1
            if i in exec_map:                                                       # monthly rebalance at today's close
                s_idx = exec_map[i]
                keep, buy = self._select(s_idx, [j for j in hold if j not in stop_pending])
                for j in list(hold):
                    if j not in keep and j not in stop_pending:
                        h = hold.pop(j); px = C[i, j]; cash += h['shares'] * px * (1 - cost)
                        trades.append(self._trade(h, cols[j], dates[i], px, 'REBAL_EXIT', h['shares'] * px * (1 - cost), i))
                val_now = cash + sum(h['shares'] * C[i, j] for j, h in hold.items())
                expo = self.exposure_bear if self._bear[s_idx] else 1.0
                for j in buy:
                    if len(hold) >= self.top_n:
                        break
                    if j in cooldown and i - cooldown[j] <= self.stop_cooldown_days:
                        continue
                    if np.isnan(self._Craw[i, j]) or not (C[i, j] > 0):
                        continue
                    tgt = min(val_now * expo / self.top_n, cash / (1 + cost))
                    if tgt <= 0:
                        break
                    shares = tgt / C[i, j]; cash -= shares * C[i, j] * (1 + cost)
                    hold[j] = dict(shares=shares, entry_idx=i, entry_price=C[i, j], sig=dates[s_idx], ep=self._ep_by_idx[s_idx].get(cols[j], np.nan))
            val = cash + sum(h['shares'] * C[i, j] for j, h in hold.items())
            equity[i] = val
            for j, h in hold.items():
                W[i, j] = h['shares'] * C[i, j] / val
            daily.append((dates[i], val, len(hold), 1 - cash / val))
        self.position_metadata = list(hold.values())
        eq = pd.Series(equity, index=dates).dropna()
        dd = pd.DataFrame(daily, columns=['date', 'equity', 'n_positions', 'invested']).set_index('date')
        res = dict(equity=eq, net_returns=eq.pct_change().fillna(0.0), executed_weights=pd.DataFrame(W[eq.index.map(dates.get_loc)], index=eq.index, columns=cols),
                   trades=pd.DataFrame(trades), daily=dd, open_positions=len(hold))
        self.results = res
        return res

    def _trade(self, h, sym, exit_date, px, reason, proceeds, i_exit):
        inv = h['shares'] * h['entry_price']
        return dict(Ticker=sym, Signal_Date=h['sig'], Entry_Date=self._dates[h['entry_idx']], Entry_Price=h['entry_price'], Exit_Date=exit_date, Exit_Price=px, Reason=reason,
                    Days_Held=i_exit - h['entry_idx'], Return=proceeds / inv - 1 - self.transaction_cost, EP=h['ep'])

    def get_positions(self):
        res = self.simulate() if self.results is None else self.results
        self.positions = res['executed_weights']
        return self.positions

    # ───────────────────────────── live interface ─────────────────────────────
    def get_target_portfolio(self, as_of, current_holdings):
        """Month-end rebalance advice computed after the close of `as_of` (a signal day), to be executed at the next close.
        current_holdings: iterable of tickers. Returns dict(keep=[...], sell=[...], buy=[(ticker, E/P), ...], new_position_weight=1/top_n * exposure)."""
        i = int(self._dates.searchsorted(pd.Timestamp(as_of), side='right')) - 1
        if i not in self._ep_by_idx:
            raise ValueError(f'{as_of} is not a month-end signal day in the data')
        held = [self._cols[s] for s in current_holdings if s in self._cols]
        keep, buy = self._select(i, held)
        cols = list(self.prices.columns)
        e = self._ep_by_idx[i]
        return dict(keep=[cols[j] for j in keep], sell=[cols[j] for j in held if j not in keep], buy=[(cols[j], float(e.iloc[j])) for j in buy],
                    new_position_weight=(self.exposure_bear if self._bear[i] else 1.0) / self.top_n, regime='BEAR' if self._bear[i] else 'BULL')

    def get_exit_signals(self, portfolio: dict, live_data: dict, today=None) -> dict:
        """Daily stop check. portfolio: ticker -> {'entry_price'}; live_data: ticker -> {'close'}. Returns {'exits': {ticker: {'reason','action'}}, 'holds': {ticker: {'stop_level'}}}.
        Rank-based exits happen at the month-end rebalance (get_target_portfolio)."""
        exits, holds = {}, {}
        for t, pos in portfolio.items():
            close = float(live_data.get(t, {}).get('close', np.nan))
            if not np.isfinite(close) or close <= 0:
                continue
            act, why = self.stop_decision(float(pos['entry_price']), close)
            if act:
                exits[t] = dict(reason=why, action=act)
            else:
                holds[t] = dict(stop_level=float(pos['entry_price']) * (1 - self.hard_stop))
        return {'exits': exits, 'holds': holds}
