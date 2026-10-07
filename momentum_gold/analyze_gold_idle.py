import os, sys, pickle, warnings
import numpy as np, pandas as pd
warnings.filterwarnings('ignore')
from gold_overlay import *
rng = np.random.default_rng(21)
HOLD = pd.Timestamp('2015-01-01')

def stitched_metrics(r, rf=0.06):
    r = r.dropna(); eq = (1 + r).cumprod(); yrs = len(r) / 252
    cagr = eq.iloc[-1] ** (1 / yrs) - 1; vol = r.std() * np.sqrt(252)
    rfd = (1 + rf) ** (1 / 252) - 1
    sh = (r - rfd).mean() / r.std() * np.sqrt(252); dd = (eq / eq.cummax() - 1)
    m = (1 + r).groupby([r.index.year, r.index.month]).prod() - 1
    return dict(cagr=cagr, vol=vol, sharpe=sh, sharpe_rf0=np.sqrt(252) * r.mean() / r.std(), maxdd=dd.min(), calmar=cagr / abs(dd.min()), worst_month=m.min(), days=len(r))

def block_boot_delta(a, b, reps=2000, blk=6):
    """a, b monthly return arrays (same months). returns P(delta Sharpe>0), P(delta MaxDD shallower), CI of delta Sharpe"""
    n = len(a); ds, dd = [], []
    def mdd(x): e = np.cumprod(1 + x); return (e / np.maximum.accumulate(e) - 1).min()
    for _ in range(reps):
        idx = []
        while len(idx) < n:
            s = rng.integers(0, n); L = min(rng.geometric(1 / blk), n); idx.extend([(s + k) % n for k in range(L)])
        i = np.array(idx[:n]); x, y = a[i], b[i]
        ds.append((x.mean() / x.std() - y.mean() / y.std()) * np.sqrt(12)); dd.append(mdd(x) - mdd(y))
    ds, dd = np.array(ds), np.array(dd)
    return (ds > 0).mean(), (dd > 0).mean(), np.percentile(ds, 5), np.percentile(ds, 95)

if __name__ == '__main__':
    out_rows = []; yearly = {}; store = {}
    for name in ('elendel', 'zenith'):
        payload = pickle.load(open(f'.cache/engine_{name}.pkl', 'rb'))
        V, meta = idle_cash_variants(payload)
        gvalid = meta['gvalid']
        base_key = 'V0 engine default (idle cash at engine rate)'; fair_key = 'V0b idle cash in liquid fund 6.5% (fair baseline)'
        window = gvalid & (payload['net_returns'].index >= '2003-01-01')
        # also exclude the first 126 days after the gap/start where PV has no signal? keep all valid days: PV falls back to cash there (f=0)
        print(f"\n===== {name.upper()} | valid-gold days {int(window.sum())} ({window.sum()/252:.1f} yrs) | mean idle cash {meta['cash_w'][window].mean():.2f} | bear/panic days share {meta['bear'][window].mean():.2f}")
        for k, (r, gpos) in V.items():
            rr = r[window]; m = stitched_metrics(rr)
            a = rr[rr.index < '2011-06-01']; b = rr[rr.index >= HOLD]
            ma, mb = stitched_metrics(a), stitched_metrics(b)
            out_rows.append(dict(strategy=name, variant=k, **m, avg_gold_weight=gpos[window].mean(), pct_days_gold=(gpos[window] > 0.01).mean(),
                                 cagr_A=ma['cagr'], sharpe_A=ma['sharpe'], maxdd_A=ma['maxdd'], cagr_B=mb['cagr'], sharpe_B=mb['sharpe'], maxdd_B=mb['maxdd']))
            store[(name, k)] = rr
        # bootstrap each variant vs the relevant baseline (monthly returns on valid days)
        mon = lambda s: ((1 + s).groupby([s.index.year, s.index.month]).prod() - 1)
        for k in V:
            if k == base_key: continue
            ref = fair_key if (k.startswith(('N', 'W')) or k == fair_key) else base_key
            if k == fair_key: ref = base_key
            a, b = mon(store[(name, k)]), mon(store[(name, ref)])
            pS, pD, lo, hi = block_boot_delta(a.values, b.values)
            for row in out_rows:
                if row['strategy'] == name and row['variant'] == k:
                    row.update(vs=ref[:3], P_dSharpe_pos=pS, P_dMaxDD_better=pD, dSharpe_lo=lo, dSharpe_hi=hi)
    R = pd.DataFrame(out_rows); R.to_csv('results_gold_idle_variants.csv', index=False, float_format='%.4f')
    pd.set_option('display.width', 270); pd.set_option('display.max_columns', 40); pd.set_option('display.max_colwidth', 66)
    for name in ('elendel', 'zenith'):
        x = R[R.strategy == name].set_index('variant')
        print(f'\n######## {name.upper()}  (stitched valid-gold days; Sharpe vs 6% cash)')
        print(x[['cagr', 'vol', 'sharpe', 'maxdd', 'calmar', 'worst_month', 'avg_gold_weight', 'pct_days_gold']].round(3).to_string())
        print(x[['cagr_A', 'sharpe_A', 'maxdd_A', 'cagr_B', 'sharpe_B', 'maxdd_B', 'vs', 'P_dSharpe_pos', 'P_dMaxDD_better', 'dSharpe_lo', 'dSharpe_hi']].round(3).to_string())
    pickle.dump(store, open('.cache/variant_returns.pkl', 'wb'), protocol=4)
