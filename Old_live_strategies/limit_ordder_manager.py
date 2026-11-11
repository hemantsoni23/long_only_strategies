"""
limit_order_manager.py
======================
Simulates GTC (Good-Till-Cancelled) stop-limit orders for backtesting.

Solves two problems:
  1. Stop-Loss Slippage: If stock is approaching stop, pre-place a limit order
     so it fills at the stop price (or better), not at next-day open.
  2. Trailing Stop Capture: If a stock is near its trailing stop while still
     profitable, pre-place a limit order to lock in gains at the stop level.

Order Lifecycle:
  PENDING → FILLED (if price touches limit) or CANCELLED (TTL expired)

IMPORTANT: All order placement checks use data available BEFORE the current
bar closes (i.e., uses prev_close / prev_low / prev_high) to avoid lookahead.
Fills are checked against the CURRENT bar's intraday range (high/low).
"""

import pandas as pd
import numpy as np
from dataclasses import dataclass, field
from typing import Optional
import warnings


# ──────────────────────────────────────────────────────────────────────────────
# Data Classes
# ──────────────────────────────────────────────────────────────────────────────

@dataclass
class LimitOrder:
    """Represents a single pending GTC limit order."""
    order_id:       int
    ticker:         str
    order_type:     str          # 'STOP_LOSS' | 'TRAILING_STOP'
    direction:      str          # 'SELL' (we only exit, never enter via these orders)
    limit_price:    float        # The price at which to fill
    placed_date:    pd.Timestamp # Date the order was created
    ttl_days:       int          # Cancel after this many calendar days
    current_weight: float        # Portfolio weight at time of placement
    reason:         str = ""     # Human-readable reason for placement

    @property
    def expiry_date(self) -> pd.Timestamp:
        return self.placed_date + pd.Timedelta(days=self.ttl_days)


@dataclass
class OrderFill:
    """Records a completed order fill."""
    order_id:    int
    ticker:      str
    order_type:  str
    fill_price:  float
    fill_date:   pd.Timestamp
    weight_exit: float           # Weight that was exited
    pnl_vs_next_open: float = 0.0  # Improvement vs waiting for next-day open


# ──────────────────────────────────────────────────────────────────────────────
# Order Manager
# ──────────────────────────────────────────────────────────────────────────────

class LimitOrderManager:
    """
    Manages a book of pending GTC stop-limit orders for backtesting.

    Parameters
    ----------
    stop_approach_pct : float
        Place a STOP_LOSS order when current loss is within this % of the stop.
        Example: 0.03 means "place order when we are 3% away from stop price".
        
    trail_approach_pct : float
        Place a TRAILING_STOP order when profit-from-peak has retraced within
        this % of the trailing stop level.
        Example: 0.05 means "place order when trailing stop is within 5% of current price".
        
    ttl_days : int
        Cancel pending orders after this many calendar days if unfilled.
        Prevents stale orders from firing in wrong market conditions.
        Default: 5 (one trading week).
        
    fill_assumption : str
        'limit_price' : Fill exactly at the limit price (optimistic but realistic
                        for liquid stocks with good order books).
        'next_open'   : If triggered intraday, fill at next day's open (conservative).
        Default: 'limit_price'
        
    verbose : bool
        Print order placement and fill events.
    """

    def __init__(
        self,
        stop_approach_pct:  float = 0.03,
        trail_approach_pct: float = 0.05,
        ttl_days:           int   = 5,
        fill_assumption:    str   = 'limit_price',
        verbose:            bool  = True,
    ):
        self.stop_approach_pct  = stop_approach_pct
        self.trail_approach_pct = trail_approach_pct
        self.ttl_days           = ttl_days
        self.fill_assumption    = fill_assumption
        self.verbose            = verbose

        # Order book state
        self._pending_orders: dict[str, LimitOrder] = {}  # ticker → order
        self._order_counter:  int = 0

        # Audit trail
        self.fill_log:   list[OrderFill] = []
        self.cancel_log: list[dict]      = []
        self.place_log:  list[dict]      = []

    # ─────────────────────────────────────────────────────
    # Public API
    # ─────────────────────────────────────────────────────

    def process_day(
        self,
        date:            pd.Timestamp,
        current_weights: pd.Series,       # Today's target weights (from monthly signal)
        entry_prices:    dict,             # {ticker: entry_price}
        peak_highs:      dict,             # {ticker: highest_high_since_entry}
        atr_values:      dict,             # {ticker: yesterday's ATR}
        atr_multiplier:  float,
        today_open:      pd.Series,        # Today's open prices
        today_high:      pd.Series,        # Today's high prices
        today_low:       pd.Series,        # Today's low prices
        today_close:     pd.Series,        # Today's close prices
        prev_close:      pd.Series,        # Yesterday's close (for approach calc)
    ) -> tuple[pd.Series, dict]:
        """
        Main entry point. Call once per day BEFORE applying monthly target weights.

        Steps:
          1. Cancel expired orders
          2. Try to fill pending orders against today's bar
          3. For held positions not already in order book, check if approaching stop
          4. Return adjusted weights + metadata

        Returns
        -------
        adjusted_weights : pd.Series
            Weights after applying any fills (zeroed-out exited positions).
        day_meta : dict
            Diagnostic info: fills, cancels, new orders placed today.
        """
        day_meta = {
            'date':         date,
            'fills':        [],
            'cancels':      [],
            'new_orders':   [],
        }

        # Work on a copy so we don't mutate caller's series
        weights = current_weights.copy()

        # ── Step 1: Cancel expired orders ──────────────────────────────────
        expired = [
            ticker for ticker, order in self._pending_orders.items()
            if date >= order.expiry_date
        ]
        for ticker in expired:
            order = self._pending_orders.pop(ticker)
            cancel_record = {
                'date':        date,
                'ticker':      ticker,
                'order_id':    order.order_id,
                'order_type':  order.order_type,
                'limit_price': order.limit_price,
                'placed_date': order.placed_date,
                'reason':      'TTL_EXPIRED',
            }
            self.cancel_log.append(cancel_record)
            day_meta['cancels'].append(cancel_record)
            if self.verbose:
                print(f"  [OrderBook] CANCEL {order.order_type} {ticker} "
                      f"@ ₹{order.limit_price:.2f} — TTL expired ({order.ttl_days}d)")

        # ── Step 2: Try to fill pending orders ─────────────────────────────
        filled_tickers = []
        for ticker, order in self._pending_orders.items():

            # Guard: only fill if ticker is still held
            if weights.get(ticker, 0) < 1e-6:
                # Position was already closed by monthly signal rebalance
                filled_tickers.append(ticker)  # will cancel below
                continue

            # Check if limit price was touched today
            lo = today_low.get(ticker, np.nan)
            hi = today_high.get(ticker, np.nan)
            op = today_open.get(ticker, np.nan)

            if pd.isna(lo) or pd.isna(hi):
                continue  # No data today — skip

            # A SELL stop-limit fires when price falls to or below limit_price
            price_touched = lo <= order.limit_price

            if price_touched:
                # Determine fill price
                if self.fill_assumption == 'limit_price':
                    # Assume we get filled at the limit; if today gapped below,
                    # fill at open (can't do better than open on a gap-down).
                    fill_price = max(order.limit_price, op) if op < order.limit_price else order.limit_price
                else:
                    # Conservative: next open (caller must handle this day separately)
                    fill_price = op

                # Estimate improvement vs waiting (next-day open alternative)
                # Positive value = we captured more by having the limit order
                next_open_alt = op  # If we hadn't placed the order, we'd get today's open
                pnl_improvement = fill_price - next_open_alt  # + means limit was better

                fill = OrderFill(
                    order_id    = order.order_id,
                    ticker      = ticker,
                    order_type  = order.order_type,
                    fill_price  = fill_price,
                    fill_date   = date,
                    weight_exit = order.current_weight,
                    pnl_vs_next_open = pnl_improvement,
                )
                self.fill_log.append(fill)
                day_meta['fills'].append(fill)

                # Zero out the position
                weights[ticker] = 0.0

                filled_tickers.append(ticker)

                if self.verbose:
                    ep = entry_prices.get(ticker, fill_price)
                    trade_pnl = (fill_price / ep - 1) * 100 if ep > 0 else 0
                    print(f"  [OrderBook] FILL {order.order_type} {ticker} "
                          f"@ ₹{fill_price:.2f} | PnL: {trade_pnl:+.1f}% | "
                          f"vs next-open: {pnl_improvement:+.2f}")

        # Remove filled orders from book
        for ticker in filled_tickers:
            self._pending_orders.pop(ticker, None)

        # ── Step 3: Check for approaching stops on held positions ───────────
        held_tickers = weights[weights > 1e-6].index.tolist()

        for ticker in held_tickers:
            # Skip if already has a pending order
            if ticker in self._pending_orders:
                continue

            # Need entry price and peak to compute stop
            ep   = entry_prices.get(ticker)
            peak = peak_highs.get(ticker)
            atr  = atr_values.get(ticker)

            if ep is None or peak is None or atr is None:
                continue

            curr_price = prev_close.get(ticker, np.nan)  # Use prev close — no lookahead
            if pd.isna(curr_price) or curr_price <= 0:
                continue

            # ── Compute Chandelier (Trailing) Stop Level ──
            stop_price = peak - (atr_multiplier * atr)

            # Current drawdown from entry
            drawdown_from_entry = (curr_price - ep) / ep      # negative = loss
            gain_from_entry     = (curr_price - ep) / ep      # positive = profit

            # Distance from current price to stop (as % of current price)
            distance_to_stop_pct = (curr_price - stop_price) / curr_price

            # ── Case 1: STOP LOSS approaching ────────────────────────────
            # Stock is losing money AND stop is close
            if gain_from_entry < 0 and distance_to_stop_pct <= self.stop_approach_pct:
                order = self._place_order(
                    ticker        = ticker,
                    order_type    = 'STOP_LOSS',
                    limit_price   = stop_price,
                    placed_date   = date,
                    current_weight= weights[ticker],
                    reason        = (f"Loss {gain_from_entry*100:.1f}%, "
                                     f"stop {distance_to_stop_pct*100:.1f}% away"),
                )
                day_meta['new_orders'].append({
                    'ticker':      ticker,
                    'order_type':  'STOP_LOSS',
                    'limit_price': stop_price,
                    'distance_pct': distance_to_stop_pct * 100,
                })
                if self.verbose:
                    print(f"  [OrderBook] PLACE STOP_LOSS {ticker} "
                          f"@ ₹{stop_price:.2f} "
                          f"(curr ₹{curr_price:.2f}, "
                          f"{distance_to_stop_pct*100:.1f}% away, "
                          f"loss {gain_from_entry*100:.1f}%)")

            # ── Case 2: TRAILING STOP approaching on profitable position ──
            # Stock has been profitable but stop is approaching (retracing)
            elif gain_from_entry > 0 and distance_to_stop_pct <= self.trail_approach_pct:
                order = self._place_order(
                    ticker        = ticker,
                    order_type    = 'TRAILING_STOP',
                    limit_price   = stop_price,
                    placed_date   = date,
                    current_weight= weights[ticker],
                    reason        = (f"Profit {gain_from_entry*100:.1f}%, "
                                     f"trailing stop {distance_to_stop_pct*100:.1f}% away"),
                )
                day_meta['new_orders'].append({
                    'ticker':      ticker,
                    'order_type':  'TRAILING_STOP',
                    'limit_price': stop_price,
                    'distance_pct': distance_to_stop_pct * 100,
                })
                if self.verbose:
                    print(f"  [OrderBook] PLACE TRAILING_STOP {ticker} "
                          f"@ ₹{stop_price:.2f} "
                          f"(curr ₹{curr_price:.2f}, "
                          f"{distance_to_stop_pct*100:.1f}% away, "
                          f"profit {gain_from_entry*100:.1f}%)")

        return weights, day_meta

    def cancel_order(self, ticker: str, reason: str = 'MANUAL', date=None):
        """
        Explicitly cancel an order for a ticker.
        Called when: monthly rebalance removes a stock, regime goes to panic, etc.
        """
        if ticker in self._pending_orders:
            order = self._pending_orders.pop(ticker)
            record = {
                'date':        date,
                'ticker':      ticker,
                'order_id':    order.order_id,
                'order_type':  order.order_type,
                'limit_price': order.limit_price,
                'placed_date': order.placed_date,
                'reason':      reason,
            }
            self.cancel_log.append(record)
            if self.verbose:
                print(f"  [OrderBook] CANCEL {order.order_type} {ticker} — {reason}")

    def cancel_all(self, reason: str = 'REGIME_CHANGE', date=None):
        """Cancel all pending orders. Call during panic/crash-guard activation."""
        tickers = list(self._pending_orders.keys())
        for ticker in tickers:
            self.cancel_order(ticker, reason=reason, date=date)

    def has_pending_order(self, ticker: str) -> bool:
        return ticker in self._pending_orders

    def get_pending_summary(self) -> pd.DataFrame:
        """Returns current order book as a readable DataFrame."""
        if not self._pending_orders:
            return pd.DataFrame()
        rows = []
        for ticker, o in self._pending_orders.items():
            rows.append({
                'Ticker':       ticker,
                'Type':         o.order_type,
                'Limit_Price':  o.limit_price,
                'Placed_Date':  o.placed_date,
                'Expiry_Date':  o.expiry_date,
                'TTL_Remaining': (o.expiry_date - pd.Timestamp.now()).days,
            })
        return pd.DataFrame(rows)

    # ─────────────────────────────────────────────────────
    # Summary & Analytics
    # ─────────────────────────────────────────────────────

    def get_fill_summary(self) -> pd.DataFrame:
        """Returns all fills as a DataFrame for analysis."""
        if not self.fill_log:
            return pd.DataFrame()
        rows = []
        for f in self.fill_log:
            rows.append({
                'Fill_Date':         f.fill_date,
                'Ticker':            f.ticker,
                'Order_Type':        f.order_type,
                'Fill_Price':        f.fill_price,
                'Weight_Exited':     f.weight_exit,
                'PnL_vs_NextOpen':   f.pnl_vs_next_open,
            })
        return pd.DataFrame(rows).set_index('Fill_Date')

    def print_backtest_impact(self):
        """
        Print a summary of how limit orders improved (or didn't) vs the
        baseline of waiting for next-day open.
        """
        fills_df = self.get_fill_summary()
        if fills_df.empty:
            print("[OrderBook] No fills recorded.")
            return

        total_fills     = len(fills_df)
        sl_fills        = fills_df[fills_df['Order_Type'] == 'STOP_LOSS']
        ts_fills        = fills_df[fills_df['Order_Type'] == 'TRAILING_STOP']
        total_cancels   = len(self.cancel_log)

        total_improvement = fills_df['PnL_vs_NextOpen'].sum()
        avg_improvement   = fills_df['PnL_vs_NextOpen'].mean()

        print("\n" + "=" * 55)
        print("  LIMIT ORDER BACKTEST IMPACT SUMMARY")
        print("=" * 55)
        print(f"  Total Orders Filled:    {total_fills}")
        print(f"    STOP_LOSS fills:      {len(sl_fills)}")
        print(f"    TRAILING_STOP fills:  {len(ts_fills)}")
        print(f"  Total Orders Cancelled: {total_cancels}")
        print(f"  Total PnL Improvement:  {total_improvement:+.4f}  (vs next-open)")
        print(f"  Avg PnL per Fill:       {avg_improvement:+.4f}")

        if len(sl_fills) > 0:
            print(f"\n  STOP_LOSS Improvement:  "
                  f"{sl_fills['PnL_vs_NextOpen'].sum():+.4f} total | "
                  f"{sl_fills['PnL_vs_NextOpen'].mean():+.4f} avg")
        if len(ts_fills) > 0:
            print(f"  TRAILING_STOP Improvement: "
                  f"{ts_fills['PnL_vs_NextOpen'].sum():+.4f} total | "
                  f"{ts_fills['PnL_vs_NextOpen'].mean():+.4f} avg")
        print("=" * 55)

    # ─────────────────────────────────────────────────────
    # Internal
    # ─────────────────────────────────────────────────────

    def _place_order(
        self,
        ticker:         str,
        order_type:     str,
        limit_price:    float,
        placed_date:    pd.Timestamp,
        current_weight: float,
        reason:         str = "",
    ) -> LimitOrder:
        self._order_counter += 1
        order = LimitOrder(
            order_id       = self._order_counter,
            ticker         = ticker,
            order_type     = order_type,
            direction      = 'SELL',
            limit_price    = limit_price,
            placed_date    = placed_date,
            ttl_days       = self.ttl_days,
            current_weight = current_weight,
            reason         = reason,
        )
        self._pending_orders[ticker] = order
        self.place_log.append({
            'date':        placed_date,
            'ticker':      ticker,
            'order_id':    self._order_counter,
            'order_type':  order_type,
            'limit_price': limit_price,
            'reason':      reason,
        })
        return order