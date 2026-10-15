"""
residual_momentum_v2_strategy.py
===================================
ResidualMomentumV2 -- subclasses the LIVE ResidualMomentumStrategy (imported from
Old_live_strategies/residual_momentum_strategy.py, never copied or edited). Signal math,
sizing, stops are all inherited/reused unchanged. Three changes, each independently
pre-registered and backtested before being combined here (full evidence/numbers in
README.md; the original round-by-round research scripts have been cleaned up, their
findings are preserved in README.md):

1. ENTRY-SPIKE FILTER (validated, factor_research round 3 / residual_momentum_entry_filter/):
   a fresh-entry candidate (rank <= enter_rank, not already held) is skipped -- not a forced
   exit of an existing holding -- if its trailing `spike_lookback`-day return sits above the
   `spike_quantile` percentile of that month's live-tradable universe. Defaults (5 days, 0.80)
   are taken directly from STRATEGY_IMPROVEMENT_IDEAS.md B2's external evidence, not tuned on
   this backtest. Measured effect (full sample, 2002-2026): Sharpe 1.15->1.19, win rate
   56.1%->58.5%, "fast damage" trades (lose >=10% within 45 days) 7.7%->6.7%, at ~flat MaxDD.

2. UNIVERSE BAND (new, this request): the live strategy uses rank 1-500 by trailing-63d
   turnover. Reading every other book's OWN live runner config in Old_live_strategies (no
   guessing -- see README.md for the exact grep):
       Zenith 1-1000, Elendel 1-1000, csm_absolute 1-1000, HR breakout 1-500 (IDENTICAL to
       residual momentum), csm_quad 500-1000, VCP 500-1000.
   Residual momentum's rank 1-500 pool is therefore a strict subset of 3 books' pools and
   bit-identical to a 4th's -- the most structurally crowded band in the repo.

   `_band_breadth_check.py` screened wider/shifted candidates under the SAME min_price=20 /
   min_adv=1e7 tradability floor (not relaxed -- that floor is a live-execution constraint,
   not an overlap dial). Finding: bands shifted past rank ~500 (300-1200, 400-1500, 500-1500)
   are too thin for much of 2002-2026 -- some months have 0-2 tradable names past that rank,
   because the actually-tradable (>=Rs20, >=Rs1cr/day) universe itself often doesn't reach
   1000-1500 names, especially pre-2010. Full non-overlap with Zenith/Elendel/absolute's
   1-1000 pool is therefore not achievable without breaking the enter/exit-rank hysteresis.
   Default here is the best-evidenced compromise: `universe_rank_min=50`,
   `universe_top_n=1000` -- trims only the ~50 most extreme-liquidity names (the tier every
   single book in the repo would include first if it screens well, so the highest-crowding-
   risk slice) while nearly doubling breadth (389 vs 324 avg eligible names/month) and no
   longer sharing an IDENTICAL band with HR breakout. Thin-month count rises modestly (43 vs
   29 of 297 months with <80 eligible names, concentrated pre-2010) -- a real, disclosed cost,
   not hidden. `universe_rank_min=1` with the inherited `universe_top_n` reproduces the live
   engine's rank 1-N selection exactly (checked in run_residual_momentum_v2.py's parity test).

3. GOLD/SILVER ETF CASH SWEEP (validated for gold, adopted; silver offered but unverified):
   WE ARE EXPLICITLY USING A GOLD OR SILVER ETF (GOLDBEES or SILVERBEES, traded on NSE) TO
   PARK IDLE CASH, instead of leaving it uninvested. This strategy sits only ~50% invested
   on average at its real intended AUM (the trend gate alone drops it to ~10% for about a
   third of all days) -- that idle capital is this strategy's single largest untapped lever.
   Declared here via `cash_sweep_etf` ('GOLDBEES', 'SILVERBEES', or None for plain cash) so
   it is a visible, explicit part of the strategy's own configuration -- the backtest engine
   (residual_momentum_v2_backtest.py) reads this attribute exactly the way it already reads
   self.breaker / self.atr_k, and sweeps 100% of idle cash into that ETF whenever this
   strategy isn't holding it in stocks.
       - GOLDBEES (default, validated): vs a true 0%-yielding cash baseline, +CAGR 24.37%->
         33.03%, Sortino 1.80->2.06, Calmar 1.15->1.56, MaxDD essentially unchanged
         (-21.10%->-21.18%); at the more conservative rf=6.5% Sharpe convention it's also
         BETTER (1.34->1.43), not just a wash. Requires GOLDBEES OHLCV data (available
         2007-03-19 onward -- the full backtest window is restricted to that history).
       - SILVERBEES (available, NOT validated): only 4.5 years of data (2022-02-07 onward)
         -- too short a sample to trust. Offered for completeness, not recommended as a
         default.
       - Tested and REJECTED (see README.md): a broad-equity sweep (NIFTYBEES) is
         catastrophic (MaxDD -18.7%->-61.6%, reintroduces full market risk exactly when the
         trend gate exists to avoid it); a CONDITIONAL gold sweep (gold only while the trend
         gate is off) is worse than the always-on version on every risk metric, because it
         concentrates gold's own volatility into the worst windows instead of diversifying
         it away.

Everything else -- signal (R3b composite), beta/residual math, inverse-vol sizing, the
25%-from-peak breaker, monthly rebalance, correlation guard, the trend gate itself -- is
INHERITED UNCHANGED. Each of those was independently tested (tighter breaker, slower
rebalance, true staggered tranching, a graded/continuous trend gate) and found not to beat
the live defaults on risk-adjusted terms, so they are deliberately left alone, not re-tuned
here. Full numbers for every tested-and-rejected idea are in README.md.
"""
import os
import sys

_LIVE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Old_live_strategies")
if _LIVE not in sys.path:
    sys.path.insert(0, _LIVE)

import numpy as np
import pandas as pd

from residual_momentum_strategy import (ResidualMomentumStrategy, _month_end_days,  # noqa: E402
                                        SPLIT_JUMP_FLAG)

CASH_SWEEP_ETF_CHOICES = (None, "GOLDBEES", "SILVERBEES")


class ResidualMomentumV2(ResidualMomentumStrategy):
    def __init__(self, *args,
                 universe_rank_min=50, universe_top_n=1000,
                 spike_filter=True, spike_lookback=5, spike_quantile=0.80,
                 cash_sweep_etf="GOLDBEES",
                 **kwargs):
        super().__init__(*args, universe_top_n=universe_top_n, **kwargs)
        self.universe_rank_min = universe_rank_min
        self.spike_filter = spike_filter
        self.spike_lookback = spike_lookback
        self.spike_quantile = spike_quantile
        if cash_sweep_etf not in CASH_SWEEP_ETF_CHOICES:
            raise ValueError(f"cash_sweep_etf must be one of {CASH_SWEEP_ETF_CHOICES}, got {cash_sweep_etf!r}")
        self.cash_sweep_etf = cash_sweep_etf   # read by residual_momentum_v2_backtest.py
        print(f"  [v2] universe band = rank {universe_rank_min}-{universe_top_n}"
              + ("  (== live engine 1-N)" if universe_rank_min <= 1 else "")
              + f"  |  spike_filter={spike_filter} ({spike_lookback}d, q={spike_quantile})"
              + ("  (== live engine)" if not spike_filter else "")
              + f"  |  cash_sweep_etf={cash_sweep_etf}"
              + ("  [UNVERIFIED -- <5y of data]" if cash_sweep_etf == "SILVERBEES" else "")
              + ("  (idle cash earns plain rf, not swept)" if cash_sweep_etf is None else ""))

    # ──────────────────────────────────────────────────────────────────────────
    # CHANGE 1: universe band instead of a single top-N cut
    # ──────────────────────────────────────────────────────────────────────────

    def filter_universe(self):
        """Identical to ResidualMomentumStrategy.filter_universe, except the final
        selection step keeps rank [universe_rank_min, universe_top_n] instead of always
        [1, universe_top_n]. Turnover computation, the min_price/min_adv tradability floor
        and the bad-data glitch exclusion are all unchanged and still applied BEFORE the
        rank cut, in the same order as the live method."""
        tv = self.close * self.volume
        self.dv = tv.rolling(63, min_periods=45).median()
        advm = self.dv

        raw_ret = self.close.pct_change(fill_method=None)
        jump = raw_ret.abs() > SPLIT_JUMP_FLAG
        pre, post = self.close.shift(1), self.close.shift(-5)
        spike = (self.close - pre).abs()
        reverted = (post - pre).abs() < 0.5 * spike
        persistent = jump & ~reverted.fillna(False)
        ever_glitched = persistent.shift(10).fillna(False).cummax()
        self.data_glitch_symbols = sorted(ever_glitched.columns[ever_glitched.iloc[-1]])
        if self.data_glitch_symbols:
            sample = self.data_glitch_symbols[:10]
            print(f"[Data-quality] {len(self.data_glitch_symbols)} symbols excluded from the "
                  f"universe from ~10 trading days after a non-reverting |daily return| > "
                  f"{SPLIT_JUMP_FLAG:.0%}: {sample}{'...' if len(self.data_glitch_symbols) > 10 else ''}")

        me = _month_end_days(self.close.index)
        memb = pd.DataFrame(False, index=me, columns=self.close.columns)
        for t in me:
            s = advm.loc[t].dropna()
            s = s[~ever_glitched.loc[t, s.index]]
            if self.min_adv > 0:
                s = s[s >= self.min_adv]
            if self.min_price > 0:
                px = self.close.loc[t, s.index]
                s = s[px >= self.min_price]
            if s.empty:
                continue
            ranked = s.rank(ascending=False, method="first")
            sel = ranked[(ranked >= self.universe_rank_min) & (ranked <= self.universe_top_n)]
            memb.loc[t, sel.index] = True
        self.univ = memb.reindex(self.close.index, method="ffill").fillna(False).astype(bool)
        return self.univ

    # ──────────────────────────────────────────────────────────────────────────
    # CHANGE 2: entry-spike filter (validated separately, see module docstring)
    # ──────────────────────────────────────────────────────────────────────────

    def calculate_factors(self):
        super().calculate_factors()
        self.ret_short = self.close.pct_change(self.spike_lookback)
        return self

    def _select_holdings(self, start):
        """Identical to ResidualMomentumStrategy._select_holdings, except fresh-entry
        candidates that just spiked (top `spike_quantile` of the universe's trailing
        `spike_lookback`-day return) are dropped from the candidate pool before filling
        empty slots. Already-held names are never force-exited by this filter."""
        S = self._sigframe()
        all_rebs = _month_end_days(self.days)
        if self.rebalance_freq_months > 1:
            all_rebs = all_rebs[::self.rebalance_freq_months]
        rebs = all_rebs[all_rebs >= pd.Timestamp(start)]
        rank_r = S.reindex(rebs).rank(axis=1, ascending=False)
        held, out = [], {}
        n_filtered = 0
        for t in rebs:
            rk = rank_r.loc[t]
            keep = sorted([h for h in held
                           if not np.isnan(rk.get(h, np.nan)) and rk[h] <= self.exit_rank],
                          key=lambda x: rk[x])[:self.n]
            cand = [c for c in rk[rk <= self.enter_rank].sort_values().index if c not in keep]
            if self.recency_veto:
                cand = [c for c in cand if self.ret21.loc[t].get(c, 0) >= -0.03]
            if self.spike_filter and len(cand):
                r5 = self.ret_short.loc[t]
                univ_names = self.univ.loc[t]
                univ_names = univ_names[univ_names].index
                thresh = r5.reindex(univ_names).quantile(self.spike_quantile)
                before = len(cand)
                cand = [c for c in cand if not (pd.notna(r5.get(c)) and r5.get(c) > thresh)]
                n_filtered += before - len(cand)
            held = keep + cand[:max(0, self.n - len(keep))]
            out[t] = held
        if self.spike_filter:
            print(f"  [v2] {n_filtered} candidate-months blocked for a recent "
                  f"{self.spike_lookback}d spike across {len(rebs)} rebalances")
        return out, rebs
