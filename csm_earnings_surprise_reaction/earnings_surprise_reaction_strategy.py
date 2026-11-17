"""
earnings_surprise_reaction_strategy.py
================
CSM Earnings Surprise & Reaction -- event-driven research on earnings surprises and the
subsequent price reaction. See README.md for limitations and execution rules.

Signal (all known after the close of the signal day S = 2nd trading day after the filing date; point-in-time):
    SUE    = standardised unexpected EPS (seasonal difference / std of the last 4-8 differences)
    EAR    = announcement return = stock return from close(d-1) to close(d+2) minus the equal-weight benchmark over the same days   (d = first trading day >= filing date)
    BUY    when SUE and EAR are BOTH in the top `top_pct` (30%) of liquid-universe events filed in the previous `pool_days` (120) calendar days
           (thresholds are trailing, never look at later filings; needs >= `min_pool` events).  "Good news the market confirmed."
    Optional: `require_margin_up` (EBIT margin improved yoy), `use_market_gate` (equal-weight benchmark above its SMA200).
Execution: enter at a valid open after S, up to `entry_window` trading days
later; each position initially targets 1/max_positions of equity. Hold-expiry
and close-confirmed stop decisions execute at a later valid open. The former
close-execution results and old research figures are not comparable.
Universe: matched fundamentals/OHLCV, price and flat-day checks; no liquidity
ranking cutoff. Research is restricted through 2024-12-31.

Public interface mirrors the other strategies: calculate_factors(), get_positions(), get_exit_signals(...), plus get_entry_candidates(...) for live use and simulate() (the single
event loop used by the backtest, get_positions and the tests).
"""
import datetime as _dt

import numpy as np
import pandas as pd

from earnings_surprise_reaction_fundamentals import build_events, RESEARCH_END


class EarningsSurpriseReactionStrategy:
    def __init__(
        self,
        prices_df, volumes_df, highs_df=None, lows_df=None, opens_df=None, benchmark_series=None,
        events_df=None,
        # signal
        top_pct            = 0.30,
        pool_days          = 120,
        min_pool           = 150,
        require_margin_up  = False,
        use_market_gate    = False,
        gate_sma           = 200,
        # universe
        universe_top_n     = None,
        universe_min_n     = 1,
        min_price          = 20.0,
        max_circuit_days   = 5,
        # portfolio
        max_positions      = 20,
        hold_days          = 60,
        entry_window       = 5,
        hard_stop          = 0.15,
        stop_slippage_pct  = 0.003,
        stop_cooldown_days = 20,
        # money
        transaction_cost   = 0.003,
        cash_annual_rate   = 0.065,
        initial_capital    = 100_000.0,
    ):
        if benchmark_series is None:
            raise ValueError('EarningsSurpriseReactionStrategy needs the equal-weight benchmark series (announcement return is benchmark-relative).')
        self.prices = prices_df.loc[:RESEARCH_END].sort_index()
        self.volumes = volumes_df.loc[:RESEARCH_END].sort_index()
        self.highs = highs_df.loc[:RESEARCH_END].sort_index() if highs_df is not None else pd.DataFrame()
        self.lows = lows_df.loc[:RESEARCH_END].sort_index() if lows_df is not None else pd.DataFrame()
        self.opens = opens_df.loc[:RESEARCH_END].sort_index() if opens_df is not None else pd.DataFrame()
        self.benchmark = benchmark_series.loc[:RESEARCH_END].sort_index()
        if universe_top_n is not None or universe_min_n != 1:
            raise ValueError('Earnings Surprise & Reaction does not apply a liquidity-rank universe cutoff.')
        self._events_in = events_df
        self.top_pct, self.pool_days, self.min_pool = top_pct, pool_days, min_pool
        self.require_margin_up, self.use_market_gate, self.gate_sma = require_margin_up, use_market_gate, gate_sma
        self.universe_top_n, self.universe_min_n, self.min_price, self.max_circuit_days = universe_top_n, universe_min_n, min_price, max_circuit_days
        self.max_positions, self.hold_days, self.entry_window = max_positions, hold_days, entry_window
        self.hard_stop, self.stop_slippage_pct, self.stop_cooldown_days = hard_stop, stop_slippage_pct, stop_cooldown_days
        self.transaction_cost, self.cash_annual_rate, self.initial_capital = transaction_cost, cash_annual_rate, initial_capital
        self.candidates = None
        self.positions = None
        self.results = None
        self.position_metadata = []
        print(f"CSM Earnings Surprise & Reaction initialised | signal: SUE & EAR both top {top_pct:.0%} of trailing {pool_days}d liquid events (pool>={min_pool})"
              f"{' & margin up' if require_margin_up else ''}{' | market gate SMA%d' % gate_sma if use_market_gate else ''}\n"
              f"  No liquidity-rank cutoff, price>{min_price}, circuit<={max_circuit_days}/63d | {max_positions} slots (1/{max_positions} each), hold {hold_days}d, "
              f"entry window {entry_window}d, hard stop {hard_stop:.0%} | cost {transaction_cost:.2%} one-way, cash {cash_annual_rate:.1%}")

    # ───────────────────────────── indicators / signals ─────────────────────────────
    def calculate_factors(self):
        P = self.prices
        self._dates = P.index
        self._cols = {s: i for i, s in enumerate(P.columns)}
        self._close_ff = P.ffill()
        self._C = self._close_ff.values
        op = self.opens.reindex(index=P.index, columns=P.columns) if not self.opens.empty else pd.DataFrame(np.nan, index=P.index, columns=P.columns)
        # A missing open is not replaceable with the day's unknown close.
        self._O = op.where(op > 0).values
        self._Craw = P.values
        dv = (P * self.volumes.reindex(index=P.index, columns=P.columns)).rolling(63, min_periods=21).median().shift(1)
        self._dv = dv
        if not self.highs.empty and not self.lows.empty:
            circ = ((self.highs == self.lows) & self.highs.notna()).astype('float64').rolling(63, min_periods=1).sum().shift(1)
        else:
            circ = pd.DataFrame(0.0, index=P.index, columns=P.columns)
        self._circ = circ.reindex(index=P.index, columns=P.columns).values
        self._prev_close = P.ffill().shift(1).values
        self._rank_cache = {}
        b = self.benchmark.reindex(P.index).ffill()
        self._bench = b.values
        self._gate_ok = (b.shift(1) > b.rolling(self.gate_sma, min_periods=int(self.gate_sma * 0.8)).mean().shift(1)).fillna(False).values

        ev = build_events(facts=None, symbols=list(P.columns)) if self._events_in is None else self._events_in.copy()
        ev = ev[ev.symbol.isin(self._cols)].copy().reset_index(drop=True)
        ev['filed'] = pd.to_datetime(ev['filed']).dt.normalize()
        ev = ev[ev.filed <= RESEARCH_END].reset_index(drop=True)
        pos = self._dates.searchsorted(ev.filed.values)                    # first trading day >= filing date
        ev['pos'] = pos
        ev['sig_idx'] = pos + 2                                            # signal known after this day's close
        ev = ev[(pos >= 1) & (ev.sig_idx + 1 < len(self._dates))].reset_index(drop=True)
        cj = ev.symbol.map(self._cols).astype(int).values
        a, b2 = ev.pos.values - 1, ev.sig_idx.values
        # A stale forward-filled quote is not an observed announcement return.
        p0, p1 = self._Craw[a, cj], self._Craw[b2, cj]
        with np.errstate(invalid='ignore', divide='ignore'):
            r = p1 / p0 - 1
            br = self._bench[b2] / self._bench[a] - 1
        ear = r - br
        ear[(r < -0.6) | (r > 2.0) | ~(p0 > 0) | ~(p1 > 0)] = np.nan
        ev['ear'] = ear
        ev['sig_date'] = self._dates[ev.sig_idx.values]
        ev['liquid'] = [self._universe_ok(int(i), int(j)) for i, j in zip(ev.sig_idx.values + 1, cj)]     # as it would look on the entry day (data to the prior close)
        ev = ev.sort_values('sig_idx').reset_index(drop=True)

        # trailing thresholds (point-in-time): liquid events with a signal date within pool_days before (and including) this event's signal date
        sd = ev.sig_date.values.astype('datetime64[D]')
        valid = ev.liquid.values & ev.sue_eps.notna().values & ev.ear.notna().values
        sue, ear_v = ev.sue_eps.values, ev.ear.values
        q = 1 - self.top_pct
        thr_s = np.full(len(ev), np.nan); thr_e = np.full(len(ev), np.nan); sd_s = np.full(len(ev), np.nan); sd_e = np.full(len(ev), np.nan); pool_n = np.zeros(len(ev), int)
        left = 0
        for k in range(len(ev)):
            while sd[left] < sd[k] - np.timedelta64(self.pool_days, 'D'):
                left += 1
            idx = np.arange(left, k + 1)
            idx = idx[valid[idx] & (sd[idx] <= sd[k])]
            # include later rows that share this signal date (same information set)
            j = k + 1
            while j < len(ev) and sd[j] == sd[k]:
                if valid[j]: idx = np.append(idx, j)
                j += 1
            pool_n[k] = len(idx)
            if len(idx) >= max(self.min_pool, 1):
                thr_s[k] = np.quantile(sue[idx], q); thr_e[k] = np.quantile(ear_v[idx], q)
                sd_s[k] = np.std(sue[idx]); sd_e[k] = np.std(ear_v[idx])
        ev['pool_n'], ev['thr_sue'], ev['thr_ear'], ev['sd_sue'], ev['sd_ear'] = pool_n, thr_s, thr_e, sd_s, sd_e
        ev['buy'] = valid & (ev.sue_eps.values >= thr_s) & (ev.ear.values >= thr_e)
        if self.require_margin_up:
            ev['buy'] &= (ev.dm_ebit > 0).values
        # ranking when slots are scarce: distance above both trailing thresholds, in trailing-pool standard deviations (causal)
        ev['score'] = (((ev.sue_eps - ev.thr_sue) / ev.sd_sue.replace(0, np.nan)).clip(lower=0, upper=5) + ((ev.ear - ev.thr_ear) / ev.sd_ear.replace(0, np.nan)).clip(lower=0, upper=5))
        ev['buy'] &= ev.score.notna()
        self.events = ev                                                   # every filing with its signals (for IC analysis)
        self.candidates = ev[ev.buy].sort_values('sig_idx').reset_index(drop=True)
        print(f"  events {len(ev):,} | with valid SUE & EAR & liquid {int(valid.sum()):,} | BUY signals {len(self.candidates):,} "
              f"({self.candidates.sig_date.min().date() if len(self.candidates) else '-'} .. {self.candidates.sig_date.max().date() if len(self.candidates) else '-'})")
        return self.candidates

    # ───────────────────────────── universe ─────────────────────────────
    def _rank_row(self, i):
        r = self._rank_cache.get(i)
        if r is None:
            r = self._dv.iloc[i].rank(ascending=False, method='min').values
            self._rank_cache[i] = r
        return r

    def _universe_ok(self, i, j):
        """Eligibility on trading-day index i for column j, using data up to the PRIOR close only."""
        if i >= len(self._dates):
            return False
        pc = self._prev_close[i, j]
        if not (pc > self.min_price):
            return False
        return bool(self._circ[i, j] <= self.max_circuit_days)

    # ───────────────────────────── shared exit rule (backtest AND live) ─────────────────────────────
    def exit_decision(self, entry_price, trading_days_held, close, open_=None):
        """Evaluate at the close; both exit reasons execute at a later open."""
        if trading_days_held >= self.hold_days:
            return 'exit_next_open', 'TIME_STOP'
        if close <= entry_price * (1 - self.hard_stop):
            return 'exit_next_open', 'STOP_HIT'
        return None, None

    # ───────────────────────────── the single event loop ─────────────────────────────
    def simulate(self, start=None, end=None):
        """Run a cash-and-shares book; decisions at close fill at a later open."""
        if self.candidates is None:
            raise ValueError('Call calculate_factors() first.')
        if end is not None and pd.Timestamp(end) > RESEARCH_END:
            raise ValueError(f'Earnings Surprise & Reaction research is limited to {RESEARCH_END.date()}.')
        dates = self._dates; n = len(dates); cols = list(self.prices.columns)
        C, O = self._C, self._O
        cost, slip = self.transaction_cost, self.stop_slippage_pct
        rf_d = (1 + self.cash_annual_rate) ** (1 / 252) - 1
        cand = self.candidates
        first = int(cand.sig_idx.min()) + 1 if len(cand) else n
        i0 = max(first, 0) if start is None else max(first, int(dates.searchsorted(pd.Timestamp(start))))
        i1 = n - 1 if end is None else min(n - 1, int(dates.searchsorted(pd.Timestamp(end), side='right')) - 1)
        by_idx = {}
        for r in cand.itertuples(index=False):
            by_idx.setdefault(int(r.sig_idx), []).append(r)
        pending = []                                   # (last_entry_idx, record)
        cash = self.initial_capital; hold = {}          # col -> dict(shares, entry_idx, entry_price, rec)
        stop_pending = {}                              # col -> reason; retry missing opens
        cooldown = {}
        equity = np.full(n, np.nan); W = np.zeros((n, len(cols)), dtype=np.float32); trades = []; daily = []; transactions = []
        for i in range(i0, i1 + 1):
            cash *= (1 + rf_d)
            exited_today = set()
            def open_mark(j):
                return O[i, j] if np.isfinite(O[i, j]) and O[i, j] > 0 else C[i - 1, j]
            opening_value = cash + sum(h['shares'] * open_mark(j) for j, h in hold.items())
            traded_value = 0.0
            # All previously scheduled exits execute at a genuine current open.
            for j in list(stop_pending):
                if j not in hold:
                    stop_pending.pop(j, None)
                    continue
                if not np.isfinite(O[i, j]) or O[i, j] <= 0:
                    continue
                reason = stop_pending.pop(j)
                px = O[i, j] * (1 - slip if reason == 'STOP_HIT' else 1)
                h = hold.pop(j); proceeds = h['shares'] * px * (1 - cost); cash += proceeds
                amount = h['shares'] * px
                traded_value += amount
                transactions.append({'Date': dates[i], 'Ticker': cols[j], 'Side': 'SELL', 'Price': px,
                                     'Shares': h['shares'], 'Trade_Value': amount, 'Transaction_Cost': amount * cost,
                                     'Reason': reason})
                trades.append(self._trade(h, cols[j], dates[i], px, reason, proceeds, i))
                exited_today.add(j)
                if reason == 'STOP_HIT':
                    cooldown[j] = i
            # Signals known at the previous close become executable now.
            for r in by_idx.get(i - 1, []):
                pending.append((i - 1 + self.entry_window, r))
            pending = [(e, r) for (e, r) in pending if e >= i]
            if pending and len(hold) < self.max_positions and not (self.use_market_gate and not self._gate_ok[i]):
                # At the open, current closing prices are not yet available.
                val_now = cash + sum(h['shares'] * open_mark(j) for j, h in hold.items())
                slots = self.max_positions - len(hold)
                taken = []
                for e, r in sorted(pending, key=lambda x: -x[1].score):
                    if slots <= 0:
                        break
                    j = self._cols[r.symbol]
                    if j in hold or j in exited_today or (j in cooldown and i - cooldown[j] <= self.stop_cooldown_days):
                        continue
                    if not self._universe_ok(i, j) or not np.isfinite(O[i, j]) or O[i, j] <= 0:
                        continue
                    tgt = min(val_now / self.max_positions, cash / (1 + cost))
                    if tgt <= 0:
                        break
                    shares = tgt / O[i, j]; cash -= shares * O[i, j] * (1 + cost)
                    hold[j] = dict(shares=shares, entry_idx=i, entry_price=O[i, j], rec=r)
                    traded_value += tgt
                    transactions.append({'Date': dates[i], 'Ticker': cols[j], 'Side': 'BUY', 'Price': O[i, j],
                                         'Shares': shares, 'Trade_Value': tgt, 'Transaction_Cost': tgt * cost,
                                         'Reason': 'EARNINGS_SURPRISE_REACTION'})
                    slots -= 1; taken.append(r)
                pending = [(e, r) for (e, r) in pending if not any(r is t for t in taken)]
            # Only after the close may today's exit decisions be made.
            for j, h in hold.items():
                if j in stop_pending or not np.isfinite(self._Craw[i, j]) or self._Craw[i, j] <= 0:
                    continue
                act, why = self.exit_decision(h['entry_price'], i - h['entry_idx'], self._Craw[i, j])
                if act == 'exit_next_open':
                    stop_pending[j] = why
            val = cash + sum(h['shares'] * C[i, j] for j, h in hold.items())
            equity[i] = val
            for j, h in hold.items():
                W[i, j] = h['shares'] * C[i, j] / val
            daily.append((dates[i], val, len(hold), 1 - cash / val,
                          traded_value / opening_value if opening_value > 0 else 0.0))
        self.position_metadata = list(hold.values())  # final positions are marked, not sold
        eq = pd.Series(equity, index=dates).dropna()
        dd = pd.DataFrame(daily, columns=['date', 'equity', 'n_positions', 'invested', 'turnover']).set_index('date')
        net_returns = eq.pct_change()
        if len(net_returns):
            net_returns.iloc[0] = eq.iloc[0] / self.initial_capital - 1
        res = dict(equity=eq, net_returns=net_returns, executed_weights=pd.DataFrame(W[eq.index.map(dates.get_loc)], index=eq.index, columns=cols),
                   trades=pd.DataFrame(trades), transactions=pd.DataFrame(transactions), daily=dd, open_positions=len(hold))
        self.results = res
        return res

    def _trade(self, h, sym, exit_date, px, reason, proceeds, i_exit):
        r = h['rec']; invested = h['shares'] * h['entry_price']
        return dict(Ticker=sym, Signal_Date=r.sig_date, Entry_Date=self._dates[h['entry_idx']], Entry_Price=h['entry_price'], Exit_Date=exit_date, Exit_Price=px,
                    Reason=reason, Shares=h['shares'], Days_Held=i_exit - h['entry_idx'], Return=proceeds / (invested * (1 + self.transaction_cost)) - 1, SUE=r.sue_eps, EAR=r.ear, Score=r.score,
                    Filed=r.filed)

    def get_positions(self):
        """Daily executed-weight DataFrame from the event loop (dates x stocks)."""
        res = self.simulate() if self.results is None else self.results
        self.positions = res['executed_weights']
        return self.positions

    # ───────────────────────────── live interface ─────────────────────────────
    def get_entry_candidates(self, as_of):
        """Names that may be bought at the open of `as_of`: signal day before as_of and within entry_window, passing the universe test. Sorted by score (best first). Free-slot and
        cooldown checks belong to the caller's portfolio state."""
        i = int(self._dates.searchsorted(pd.Timestamp(as_of), side='right')) - 1
        c = self.candidates
        c = c[(c.sig_idx < i) & (c.sig_idx >= i - self.entry_window)]
        keep = [self._universe_ok(i, self._cols[s]) for s in c.symbol]
        out = c[keep].sort_values('score', ascending=False)
        if self.use_market_gate and not self._gate_ok[i]:
            return out.iloc[0:0]
        return out[['symbol', 'filed', 'sig_date', 'sue_eps', 'ear', 'dm_ebit', 'score']]

    def get_exit_signals(self, portfolio: dict, live_data: dict, today=None) -> dict:
        """Evaluate the exit rules on one live bar (T-1 settled close).
        portfolio : ticker -> {'entry_price': float, 'entry_date': date-like}
        live_data : ticker -> {'close': float, optional 'open'}
        Returns {'exits': {ticker: {'reason','action','fill'}}, 'holds': {ticker: {'days_held','stop_level'}}}; exit_next_open schedules a sale on a later session."""
        today = pd.Timestamp(today if today is not None else _dt.date.today()).normalize()
        exits, holds = {}, {}
        for t, pos in portfolio.items():
            bar = live_data.get(t, {})
            close = float(bar.get('close', np.nan))
            if not np.isfinite(close) or close <= 0:
                continue
            ed = pd.Timestamp(str(pos['entry_date'])[:10])
            if len(self._dates) and self._dates[-1] >= today:
                held = int(self._dates.searchsorted(today, side='right') - self._dates.searchsorted(ed, side='left')) - 1
            else:
                held = int(np.busday_count(ed.date(), today.date()))
            act, why = self.exit_decision(float(pos['entry_price']), held, close)
            stop_level = float(pos['entry_price']) * (1 - self.hard_stop)
            if act:
                exits[t] = dict(reason=why, action=act, fill=close if act == 'exit_now' else None)
            else:
                holds[t] = dict(days_held=held, stop_level=stop_level)
        return {'exits': exits, 'holds': holds}
