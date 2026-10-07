"""Event study of daily breakout signals. Entry = close of t+1 (T+1 fill proxy). Excess = fwd return minus the
same-day liquid-universe equal-weight mean. Stats are date-clustered (mean per signal date, NW t-stat)."""
import numpy as np, pandas as pd
from data import load_panels
from factors import Ctx, rmean, rmax, rmin
from evaluate import nw_tstat
H = (5, 10, 20, 40, 60)
P = load_panels(); X = Ctx(P); idx = X.C.index
Cf, Hf, Lf, V = X.Cf, X.Hf, X.Lf, X.V
# ---- universe (daily) ----
dv = X.DV.rolling(63, min_periods=21).median()
rank = dv.rank(axis=1, ascending=False, method='min')
circ = ((X.H == X.L) & X.H.notna()).astype('float64').rolling(63, min_periods=1).sum() <= 5
uni = Cf.notna() & (Cf > 20) & (rank <= 1000) & circ
# ---- forward returns from t+1 close ----
Cff = X.C.ffill(); r = Cff.pct_change(fill_method=None); r = r.where((r > -0.4) & (r < 3.0), 0.0).fillna(0.0)
L = np.log1p(r).cumsum()
FW = {}
for h in H:
    FW[h] = np.expm1(L.shift(-(1 + h)) - L.shift(-1)).astype('float32')
EX = {}
for h in H:
    f = FW[h].where(uni); EX[h] = f.sub(f.mean(axis=1), axis=0)
# ---- features ----
s50, s150, s200 = rmean(Cf, 50), rmean(Cf, 150), rmean(Cf, 200)
TT = (Cf > s50) & (s50 > s150) & (s150 > s200) & (s200 > s200.shift(21)) & (Cf >= 0.75 * rmax(Hf, 252)) & (Cf >= 1.3 * rmin(Lf, 252))
vol_avg = rmean(V, 50).shift(1)
vsurge = V > 1.5 * vol_avg
vsurge2 = V > 2.0 * vol_avg
mom6 = (Cf.shift(21) / Cf.shift(126) - 1).where(uni)
rs_top = mom6.rank(axis=1, pct=True) >= 0.75
tr = X.true_range(); atr_ratio = (rmean(tr, 14) / rmean(tr, 63)).shift(1)
rng20 = (rmax(Hf, 20) - rmin(Lf, 20)).shift(1); rng60 = (rmax(Hf, 60) - rmin(Lf, 60)).shift(1)
compress = (rng20 / rng60 < 0.5) & (atr_ratio < 0.85)
tight20 = (rng20 / Cf.shift(1)) < 0.12
gap = (X.O / Cf.shift(1) - 1) > 0.02
clv_hi = X.clv() > 0.5
bench = P['bench']; bull = (bench > rmean(bench, 200)).reindex(idx).fillna(False)
bullm = pd.DataFrame(np.broadcast_to(bull.values[:, None], Cf.shape), index=idx, columns=Cf.columns)

def fresh(flag, gap_days=10):
    prior = flag.shift(1).astype('float64').rolling(gap_days, min_periods=1).max().fillna(0) > 0
    return flag & ~prior

E = {}
E['don55'] = fresh(Cf > rmax(Hf, 55).shift(1))
E['hi252'] = fresh(Cf > rmax(Cf, 252).shift(1))
E['stage2_vol_breakout50'] = fresh(TT & (Cf > rmax(Hf, 50).shift(1)) & vsurge)
E['vcp_proxy'] = fresh(TT & compress & (Cf > rmax(Hf, 20).shift(1)) & (V > 1.2 * vol_avg))
E['tight_base_breakout20'] = fresh(TT & tight20 & (Cf > rmax(Hf, 20).shift(1)))
splits = {}
for base in ['hi252', 'don55']:
    b = E[base]
    splits[f'{base} | vol>=1.5x'] = b & vsurge
    splits[f'{base} | vol<1.5x'] = b & ~vsurge
    splits[f'{base} | vol>=2x'] = b & vsurge2
    splits[f'{base} | RS top25%'] = b & rs_top
    splits[f'{base} | RS not top25%'] = b & ~rs_top
    splits[f'{base} | trend template'] = b & TT
    splits[f'{base} | no trend template'] = b & ~TT
    splits[f'{base} | tight 20d base'] = b & tight20
    splits[f'{base} | compressed(VCP)'] = b & compress
    splits[f'{base} | gap-up open>2%'] = b & gap
    splits[f'{base} | no gap'] = b & ~gap
    splits[f'{base} | strong close'] = b & clv_hi
    splits[f'{base} | mkt bull'] = b & bullm
    splits[f'{base} | mkt bear'] = b & ~bullm
    splits[f'{base} | TT+vol1.5+RS25'] = b & TT & vsurge & rs_top

def summarize(name, ev):
    ev = ev & uni
    out = {'event': name, 'n': int(ev.to_numpy().sum()), 'dates': int(ev.any(axis=1).sum())}
    for h in H:
        ex = EX[h].where(ev); fw = FW[h].where(ev & uni)
        dm = ex.mean(axis=1).dropna()
        pooled = ex.stack()
        out[f'ex{h}'] = pooled.mean()
        out[f'med_ex{h}'] = pooled.median()
        out[f't{h}'] = nw_tstat(dm, h)
        out[f'hit_abs{h}'] = (fw.stack() > 0).mean()
        out[f'hit_vs_uni{h}'] = (pooled > 0).mean()
        d1 = dm[dm.index <= '2014-12-31']; d2 = dm[dm.index > '2014-12-31']
        out[f'ex{h}_disc'] = ex.loc[:'2014-12-31'].stack().mean(); out[f'ex{h}_hold'] = ex.loc['2015-01-01':].stack().mean()
    return out
rows = [summarize(k, v) for k, v in E.items()] + [summarize(k, v) for k, v in splits.items()]
df = pd.DataFrame(rows).set_index('event'); df.to_csv('results/stage5_breakout_events.csv', float_format='%.4f')
pd.set_option('display.width', 300); pd.set_option('display.max_columns', 60); pd.set_option('display.max_rows', 100)
c = ['n','ex5','ex20','ex60','t20','t60','hit_abs20','hit_vs_uni20','hit_vs_uni60','med_ex20','ex20_disc','ex20_hold','ex60_disc','ex60_hold']
print(df[c].round(4).to_string())
