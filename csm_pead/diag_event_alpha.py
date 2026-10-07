"""Diagnostic: does the PEAD edge survive CAUSAL selection (trailing thresholds, entry the day after the signal day, no slot limit)?
Per-BUY-signal 60-day return from the entry close vs the equal-weight LIQUID universe over the same days; compared with all liquid events and with the earlier month-ranked event study."""
import os, sys, pickle, numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from run_pead_backtest import load_all
from pead_strategy import PEADStrategy
prices, volumes, highs, lows, opens, bench = load_all()
st = PEADStrategy(prices_df=prices, volumes_df=volumes, highs_df=highs, lows_df=lows, opens_df=opens, benchmark_series=bench)
cand = st.calculate_factors()
FR = '/Users/hemantsoni/Documents/long_only_strategies/factor_research'
U1 = pickle.load(open(os.path.join(FR, '.cache', 'state.pkl'), 'rb'))['U']['U1_liquid1000']
idx = st._dates
U1d = U1.reindex(idx.union(U1.index)).ffill().shift(1).reindex(idx).fillna(False).astype(bool).reindex(columns=prices.columns, fill_value=False)
r = st._close_ff.pct_change(fill_method=None).where(lambda x: (x > -0.4) & (x < 3.0), 0.0).fillna(0.0)
mk = r.where(U1d).mean(axis=1, skipna=True).fillna(0.0).values
cum = np.cumsum(np.log1p(r.values), axis=0); bcum = np.cumsum(np.log1p(mk))
def stats(df, h, label):
    e = df.sig_idx.values + 1; j = df.symbol.map(st._cols).astype(int).values
    ok = e + h < len(idx); e, j, d = e[ok], j[ok], df[ok]
    ret = np.expm1(cum[e + h, j] - cum[e, j]); m = np.expm1(bcum[e + h] - bcum[e]); ex = np.clip(ret - m, -0.6, 1.5)
    g = pd.Series(ex).groupby(d.sig_date.dt.to_period('M').values).mean()
    t = g.mean() / (g.std() / np.sqrt(len(g)))
    print(f'{label:<46} n={len(d):5d}  mean excess {ex.mean()*100:+5.2f}%  median {np.median(ex)*100:+5.2f}%  win {np.mean(ret>m):.0%}  t(by month) {t:+.2f}  mean raw {ret.mean()*100:+.1f}% vs mkt {m.mean()*100:+.1f}%')
ev = st.candidates.copy()
alle = pd.read_pickle('/Users/hemantsoni/Documents/long_only_strategies/factor_research/.cache/stage15d_events.pkl') if False else None
for h in (20, 40, 60):
    stats(ev, h, f'causal BUY signals, hold {h}d')
# baseline: all valid liquid events with SUE & EAR (need the full table: rebuild quickly)
st2 = PEADStrategy(prices_df=prices, volumes_df=volumes, highs_df=highs, lows_df=lows, opens_df=opens, benchmark_series=bench, top_pct=0.9999, min_pool=0)
base_all = st2.calculate_factors()
# top_pct~1 -> threshold at the minimum -> buys every valid liquid event
for h in (60,):
    stats(base_all, h, 'ALL valid liquid events (baseline), hold 60d')
for k in range(4):
    pass
print('\nBy year (causal BUY signals, 60d):')
e = ev.sig_idx.values + 1; j = ev.symbol.map(st._cols).astype(int).values; ok = e + 60 < len(idx)
ret = np.expm1(cum[e[ok] + 60, j[ok]] - cum[e[ok], j[ok]]); m = np.expm1(bcum[e[ok] + 60] - bcum[e[ok]])
d = ev[ok].assign(ex=np.clip(ret - m, -0.6, 1.5))
print(d.groupby(d.sig_date.dt.year).ex.agg(['count', lambda x: x.mean() * 100]).round(2).rename(columns={'<lambda_0>': 'mean_excess%'}).T.to_string())
