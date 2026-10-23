"""Secondary layer: realised (faithful-booked) daily returns of Elendel / Zenith / Quad, by the same 36m chunks (holding months = signal months +1)."""
import os, sys
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C
R = pd.read_csv('/Users/hemantsoni/Documents/long_only_strategies/csm_value/output/faithful_engine_returns.csv', index_col=0, parse_dates=True)
IDX = pd.read_parquet('/Users/hemantsoni/Documents/long_only_strategies/factor_research/.cache/index_data_close.parquet')
mk = IDX['Nifty_500'].dropna().pct_change().fillna(0.0)          # price index (no dividends); EW-all-stocks panel is junk-inflated, not used
mom = IDX['Nifty500Momentm50'].dropna().pct_change().dropna()
rows = []
for nm in ('elendel', 'zenith', 'quad'):
    r = R[f'{nm}_faithful'].astype(float)
    live = r[r != 0]; first = live.index.min()
    fm = pd.Period(first, 'M') + 12
    for lab, s, e in C.chunk_bounds(fm) + [('ALL', fm, C.ANCHOR)]:
        a, b = (s + 1).to_timestamp(), (e + 1).to_timestamp(how='end')
        x = r.loc[a:b]; m = mk.reindex(x.index).fillna(0); mo = mom.reindex(x.index)
        if len(x) < 100: continue
        yrs = len(x) / 252
        cagr = (1 + x).prod() ** (1 / yrs) - 1; mc = (1 + m).prod() ** (1 / yrs) - 1
        eq = (1 + x).cumprod(); dd = (eq / eq.cummax() - 1).min()
        ex = (x - m)
        rows.append(dict(strategy=nm, chunk=lab, years=round(yrs, 2), cagr=cagr, nifty500_cagr=mc,  excess_cagr=cagr - mc,
                         sharpe=x.mean() / x.std() * np.sqrt(252), maxdd=dd, excess_nw_t=C.nw_t(ex, 10),
                         hit_months=(x.groupby(x.index.to_period('M')).apply(lambda z: (1 + z).prod() - 1) >
                                     m.groupby(m.index.to_period('M')).apply(lambda z: (1 + z).prod() - 1)).mean()))
D = pd.DataFrame(rows); D.to_csv(f'{C.OUT}/ret_chunks.csv', index=False)
pd.set_option('display.width', 200)
print(D.round(3).to_string())

# regime reference: NSE Nifty500 Momentum 50 index only exists from 2024-11-12 -> compare over that exact window
rows2 = []
w0 = mom.index.min()
for nm in ('elendel', 'zenith', 'quad'):
    x = R[f'{nm}_faithful'].astype(float).loc[w0:'2026-07-16']
    yrs = len(x) / 252
    rows2.append(dict(series=nm + ' (faithful)', cagr=(1 + x).prod() ** (1 / yrs) - 1))
for lab, ser in (('Nifty 500 (price)', mk), ('Nifty500 Momentum 50 (price)', mom)):
    x = ser.loc[w0:'2026-07-16']; yrs = len(x) / 252
    rows2.append(dict(series=lab, cagr=(1 + x).prod() ** (1 / yrs) - 1))
W = pd.DataFrame(rows2); W['window'] = f"{w0.date()} -> 2026-07-16"
W.to_csv(f'{C.OUT}/ret_momentum_index_window.csv', index=False); print(W.round(3).to_string())
