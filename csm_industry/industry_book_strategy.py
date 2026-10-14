"""
industry_book_strategy.py
=========================
CSMIndustryBook -- self-contained implementation of the pre-registered industry-led staggered book "D1v" (factor_research/INDUSTRY_BOOK_PREREG.md, FINDINGS sections 8.3-8.8).
Imports nothing from factor_research or Old_live_strategies; takes the same OHLCV panels the live engines take plus instruments_clean.csv.

Monthly signal (month-end close t; information <= t)
  1. Universe U1 = close>20, 63d-median dollar-volume rank<=1000, <=5 circuit days (high==low) in 63d.  Pool U2 = U1 and close > SMA200.
  2. Industry baskets = equal-weight monthly return of the Industry_clean members that were in U1 at the PRIOR month-end; basket trailing L-month return (L=3, no skip).
  3. Usable industries = >= `min_members` live U1 members at t, trailing return > 0.  Take the top `n_ind` (8) by trailing return.
  4. In each, buy the top `m` (2) pool members by the Zenith composite z(A1)+z(Q5_189) inside the pool (score='a1': A1 = close / 252d intraday high only), subject to being tradable on the fill day (finite close, not circuit-locked).  Cohort weight 1/(n_ind*m) each.
  5. Overlapping tranches (Jegadeesh-Titman): target weights = mean of the last H=6 monthly cohorts.  Market gate: x gate_low (0.5) when the equal-weight index is below its SMA200.
Fills at the close of the next trading day; a position earns from the day after its fill; cost side_cost x sum|target - drifted weight| on the fill day; no stops; idle cash earns cash_rate.
Vol-target overlay (D1v): scale the whole book by min(1, vol_target / trailing 63d realised vol, lagged one day); remainder in cash; cost side_cost x |change in scale|.

This reproduces the research simulator exactly (csm_industry/test_parity.py).  `live_orders()` returns the target for the latest signal date.
"""
import numpy as np
import pandas as pd


def _mp(w):
    return max(2, int(w * 0.8))


def _signal_dates(index):
    s = pd.Series(index, index=index)
    return pd.DatetimeIndex(s.groupby([index.year, index.month]).max().values)


def _onehot(code, n):
    m = np.zeros((len(code), n))
    ok = code >= 0
    m[np.where(ok)[0], code[ok]] = 1.0
    return m


def _trailing(ret, L, skip):
    logr = np.nan_to_num(np.log1p(np.clip(ret, -0.9, 5.0)), nan=0.0)
    cum = np.cumsum(logr, axis=0)
    end = np.vstack([np.zeros((1, cum.shape[1])), cum[:-1]]) if skip else cum
    start = np.vstack([np.zeros((L, cum.shape[1])), end[:-L]])
    out = np.expm1(end - start)
    out[:L + (1 if skip else 0), :] = np.nan
    return out


class CSMIndustryBook:
    def __init__(self, prices_df, volumes_df, highs_df, lows_df, opens_df=None, benchmark_series=None, *,
                 instruments_path, L=3, skip=0, n_ind=8, m=2, H=6, min_members=10, gate_low=0.5, use_gate=True,
                 vol_target=0.15, vol_win=63, side_cost=0.003, cash_rate=0.065, start='2005-01-01',
                 min_price=20.0, universe_top_n=1000, max_circuit_days=5, score='zen'):
        self.C, self.V, self.Hh, self.Ll = prices_df, volumes_df, highs_df, lows_df
        self.bench_in = benchmark_series
        self.instruments_path = instruments_path
        self.L, self.skip, self.n_ind, self.m, self.H = L, skip, n_ind, m, H
        self.min_members, self.gate_low, self.use_gate = min_members, gate_low, use_gate
        self.vol_target, self.vol_win, self.side_cost, self.cash_rate = vol_target, vol_win, side_cost, cash_rate
        self.start = pd.Timestamp(start)
        self.min_price, self.universe_top_n, self.max_circuit_days = min_price, universe_top_n, max_circuit_days
        self.score = score                                                  # 'zen' (A1 + Q5_189, the live Zenith ranking signal; default) or 'a1' (52-week-high proximity only)
        self.cols, self.dates = self.C.columns, self.C.index
        self.sig = _signal_dates(self.dates)
        self.cohorts = self.positions = self.net_returns = self.info = self.scale = self.raw_returns = None

    # ───────────────────────── labels ─────────────────────────
    def _labels(self):
        inst = (pd.read_csv(self.instruments_path)[['trading_symbol', 'Sector_clean', 'Industry_clean']]
                .dropna(subset=['trading_symbol']).drop_duplicates('trading_symbol', keep='first')
                .set_index('trading_symbol').reindex(self.cols))
        self.ind_names = sorted(inst['Industry_clean'].dropna().unique())
        self.ind_code = inst['Industry_clean'].map({n: i for i, n in enumerate(self.ind_names)}).fillna(-1).astype(int).values
        self.n_ind_all = len(self.ind_names)

    # ───────────────────────── signal ─────────────────────────
    def calculate_factors(self):
        sig, C, V = self.sig, self.C, self.V
        Cf = C.ffill(limit=5)
        Hf = self.Hh.ffill(limit=5)
        have = Cf.reindex(sig).notna()
        price_ok = Cf.reindex(sig) > self.min_price
        med_dv = (C * V).rolling(63, min_periods=21).median().reindex(sig)
        rank = med_dv.rank(axis=1, ascending=False, method='min')
        circ = ((self.Hh == self.Ll) & self.Hh.notna()).astype('float64').rolling(63, min_periods=1).sum().reindex(sig) <= self.max_circuit_days
        self.U1 = have & price_ok & (rank <= self.universe_top_n) & circ
        self.U2 = self.U1 & (Cf > Cf.rolling(200, min_periods=_mp(200)).mean()).reindex(sig)
        self.A1 = (Cf / Hf.rolling(252, min_periods=_mp(252)).max()).reindex(sig)
        # Q5_189: share of the last 189 days with close above SMA50 (live Zenith trend-persistence leg)
        sma50 = Cf.rolling(50, min_periods=_mp(50)).mean()
        above = (Cf > sma50).where(Cf.notna() & sma50.notna()).astype('float64')
        self.Q5 = above.rolling(189, min_periods=int(189 * 0.79)).mean().reindex(sig)
        def _z(df):
            return df.sub(df.mean(axis=1), axis=0).div(df.std(axis=1, ddof=0), axis=0)
        f32 = lambda df: df.astype('float32')
        self.ZEN = _z(f32(self.A1).where(self.U2)) + _z(f32(self.Q5).where(self.U2))          # Zenith composite, z-scored inside the SMA200 pool
        # equal-weight benchmark index and SMA200 gate
        r = C.pct_change(fill_method=None).clip(-0.5, 0.5)
        bench = (1 + r.mean(axis=1, skipna=True).fillna(0.0)).cumprod()
        sma = bench.rolling(200, min_periods=150).mean()
        pos = self.dates.get_indexer(sig)
        up = (bench > sma).values
        self.gate_up = np.array([bool(up[p]) if p >= 0 and np.isfinite(sma.values[p]) else True for p in pos])
        # basket returns from prior-month-end U1 members
        self._labels()
        mret = C.ffill().reindex(sig).pct_change(fill_method=None)
        elig_prev = self.U1.shift(1).fillna(False)
        valid = elig_prev.values & ~np.isnan(mret.values)
        w = valid.astype('float64')
        oh = _onehot(self.ind_code, self.n_ind_all)
        num, den = np.nan_to_num(mret.values) * w @ oh, w @ oh
        with np.errstate(invalid='ignore', divide='ignore'):
            ret_ind = np.where(den > 0, num / den, np.nan)
        self.G = _trailing(ret_ind, self.L, self.skip)                       # T x n_ind trailing basket return
        self.cnt_now = self.U1.values.astype('float64') @ oh                 # live U1 members at t
        return self.G

    # ───────────────────────── positions ─────────────────────────
    def get_positions(self):
        if getattr(self, 'G', None) is None:
            self.calculate_factors()
        sig, dates = self.sig, self.dates
        T, N = len(sig), len(self.cols)
        pos = dates.get_indexer(sig)
        ok_b = (pos >= 0) & (pos + 1 < len(dates))
        self.b = np.where(ok_b, pos + 1, -1)
        Cv, Hv, Lv = self.C.values, self.Hh.values, self.Ll.values
        tradable = np.zeros((T, N), dtype=bool)
        for k in range(T):
            bb = self.b[k] if self.b[k] >= 0 else pos[k]            # newest signal row (no next-day bar yet, i.e. the live case): tradability judged on the signal day
            if bb >= 0:
                tradable[k] = np.isfinite(Cv[bb]) & ~((Hv[bb] == Lv[bb]) & np.isfinite(Hv[bb]))
        pool = self.U2.values
        A1 = (self.ZEN if self.score == 'zen' else self.A1).values
        ok = self.cnt_now >= self.min_members
        members = {g: np.where(self.ind_code == g)[0] for g in range(self.n_ind_all)}
        C = np.zeros((T, N), dtype=np.float32)
        self.selected = [None] * T
        wgt = 1.0 / (self.n_ind * self.m)
        for k in range(T):
            if pos[k] < 0 or sig[k] < self.start:
                continue
            pool_k = pool[k] & tradable[k]
            Gk = self.G[k]
            usable = ok[k] & np.isfinite(Gk) & (Gk > 0)
            cand = np.where(usable)[0]
            if len(cand) == 0:
                continue
            sel = cand[np.argsort(-Gk[cand], kind='stable')[:self.n_ind]]
            self.selected[k] = sel
            for g in sel:
                mem = members[g]
                mem = mem[pool_k[mem]]
                if len(mem) == 0:
                    continue
                s = np.nan_to_num(A1[k, mem], nan=-np.inf)
                C[k, mem[np.argsort(-s, kind='stable')[:self.m]]] += wgt
        self.cohorts = C
        cum = np.cumsum(C.astype('float64'), axis=0)
        prev = np.vstack([np.zeros((self.H, N)), cum[:T - self.H]])
        target = (cum - prev) / self.H
        gate = np.where(self.gate_up, 1.0, self.gate_low) if self.use_gate else np.ones(T)
        self.positions = pd.DataFrame(target * gate[:, None], index=sig, columns=self.cols)
        return self.positions

    # ───────────────────────── backtest (faithful accounting) ─────────────────────────
    def backtest(self):
        if self.positions is None:
            self.get_positions()
        target = self.positions.values
        T, N = target.shape
        r = self.C.ffill().pct_change(fill_method=None)
        R = r.where((r > -0.40) & (r < 3.00), 0.0).fillna(0.0).values.astype(np.float32)
        nd = len(self.dates)
        rf_d = (1 + self.cash_rate) ** (1 / 252) - 1
        has = np.where((target > 0).any(axis=1) & (self.b >= 0))[0]
        k_first = int(has[0])
        daily = np.zeros(nd)
        w = np.zeros(N)
        turn_log, expo_log, names_log, dates_log = [], [], [], []
        for k in range(k_first, T):
            b0 = self.b[k]
            if b0 < 0:
                break
            tgt = target[k]
            turnover = np.abs(tgt - w).sum()
            cost = self.side_cost * turnover
            daily[b0] = (1.0 + daily[b0]) * (1.0 - cost) - 1.0 if daily[b0] != 0 else -cost
            w = tgt.copy()
            cash = 1.0 - w.sum()
            nxt = self.b[k + 1] if k + 1 < T and self.b[k + 1] >= 0 else nd - 1
            a = np.where(w > 0)[0]
            days = np.arange(b0 + 1, nxt + 1)
            if len(days) > 0:
                growth = np.cumprod(1.0 + R[b0 + 1:nxt + 1][:, a].astype('float64'), axis=0)
                vals = growth * w[a]
                cashv = cash * (1 + rf_d) ** np.arange(1, len(days) + 1)
                total = vals.sum(axis=1) + cashv
                daily[days] = total / np.concatenate([[1.0], total[:-1]]) - 1.0
                w_new = np.zeros(N)
                w_new[a] = vals[-1] / total[-1]
                w = w_new
            turn_log.append(turnover / 2.0)
            expo_log.append(w.sum())
            names_log.append(int((w > 1e-9).sum()))
            dates_log.append(self.dates[b0])
        first_day = self.b[k_first]
        raw = pd.Series(daily[first_day:], index=self.dates[first_day:])
        self.info = pd.DataFrame({'turnover_oneway': turn_log, 'exposure': expo_log, 'names': names_log}, index=pd.DatetimeIndex(dates_log))
        self.raw_returns = raw
        if self.vol_target > 0:
            vol = raw.rolling(self.vol_win, min_periods=40).std().shift(1) * np.sqrt(252)
            s = (self.vol_target / vol).clip(upper=1.0).fillna(1.0)
            rf = (1 + self.cash_rate) ** (1 / 252) - 1
            self.net_returns = s * raw + (1 - s) * rf - self.side_cost * s.diff().abs().fillna(0)
            self.scale = s
        else:
            self.net_returns, self.scale = raw, pd.Series(1.0, index=raw.index)
        return self.net_returns

    # ───────────────────────── live helper ─────────────────────────
    def live_orders(self, top_k_print=0):
        """Target for the latest signal date: weights per ticker (before the vol-target scale), the scale, the implied cash weight and the selected industries."""
        if self.net_returns is None:
            self.backtest()
        k = len(self.sig) - 1
        w = self.positions.iloc[k]
        w = w[w > 0].sort_values(ascending=False)
        s = float(self.scale.iloc[-1])
        sel = [self.ind_names[g] for g in (self.selected[k] if self.selected[k] is not None else [])]
        return dict(signal_date=self.sig[k], weights=w, vol_scale=s, effective_weights=w * s, cash_weight=1 - float(w.sum()) * s, industries=sel, gate_up=bool(self.gate_up[k]))
