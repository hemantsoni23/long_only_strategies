"""All non-sector signals from MOMENTUM_SIGNALS_EXPLAINED.md, computed daily then sampled at month-ends (formulas as in that file)."""
import os, sys, pickle
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C

def month_rows(df, me):
    x = df.loc[me]; x.index = pd.PeriodIndex(x.index, freq='M'); return x[~x.index.duplicated(keep='last')].astype('float32')

def build():
    P = C.load_panels(); close, high, low, vol = P['close'], P['high'], P['low'], P['volume']; bench = P['bench']
    cf = close.ffill(limit=5); me = C.month_end_days(close.index); S = {}
    ret = close.pct_change(fill_method=None)
    # universe (file definition), measured on the previous day
    dv = (close * vol).rolling(63, min_periods=45).mean().shift(1)
    rank = dv.rank(axis=1, ascending=False, method='min'); circ = (high == low).rolling(63, min_periods=1).sum().shift(1)
    uni = (rank <= 1000) & (close.shift(1) >= 10) & (circ <= 5); S['_uni'] = month_rows(uni.astype(float), me)
    S['_dvol'] = month_rows(dv, me)
    hmax = high.rolling(252, min_periods=200).max()
    S['A1'] = month_rows(cf / hmax, me)
    cmax, cmin = cf.rolling(252, min_periods=200).max(), cf.rolling(252, min_periods=200).min()
    S['A2'] = month_rows((cf - cmin) / (cmax - cmin).replace(0, np.nan), me)
    rs = cf.div(bench, axis=0); S['A3'] = month_rows(rs / rs.rolling(252, min_periods=200).max(), me); del rs
    ish = (cf >= cmax - 1e-12) & cmax.notna(); c = (~ish).astype(int); cs = c.cumsum(); S['A4'] = month_rows(-(cs - cs.where(ish).ffill()), me); del ish, c, cs
    sma50 = cf.rolling(50, min_periods=40).mean(); valid = cf.notna() & sma50.notna(); above = (cf > sma50).where(valid).astype(float)
    S['Q5'] = month_rows(above.rolling(126, min_periods=100).mean(), me); del above, sma50, valid
    logp = np.log(cf)
    def trend(win, mode):
        out = {}
        for d in me:
            i = logp.index.get_loc(d)
            if i < win: continue
            seg = logp.values[i - win + 1:i + 1]; ok = np.isfinite(seg).sum(axis=0) >= int(0.8 * win)
            t = np.arange(win, dtype=float)[:, None]; m = np.isfinite(seg)
            x = np.where(m, t, np.nan); y = seg
            xm = np.nanmean(x, axis=0); ym = np.nanmean(y, axis=0); xc = x - xm; yc = y - ym
            sxy = np.nansum(xc * yc, axis=0); sxx = np.nansum(xc ** 2, axis=0); syy = np.nansum(yc ** 2, axis=0)
            with np.errstate(all='ignore'):
                slope = sxy / sxx; r2 = sxy ** 2 / (sxx * syy)
                ret_ = np.exp(seg[-1] - seg[0]) - 1
                v = np.sign(ret_) * r2 if mode == 'q4' else (np.exp(slope * 252) - 1) * r2
            v = np.where(ok, v, np.nan); out[d] = v
        df = pd.DataFrame(out, index=logp.columns).T; return month_rows(df.reindex(close.index).ffill(limit=0).loc[me].dropna(how='all') if False else df.reindex(me), me)
    S['Q4'] = trend(126, 'q4'); S['Q3'] = trend(90, 'q3')
    # frog-in-the-pan
    pos = (ret > 0).astype(float).where(ret.notna()); neg = (ret < 0).astype(float).where(ret.notna())
    posm = pos.rolling(231, min_periods=180).mean().shift(21); negm = neg.rolling(231, min_periods=180).mean().shift(21)
    r121 = cf.shift(21) / cf.shift(252) - 1; ID = np.sign(r121) * (negm - posm)
    S['Q1'] = month_rows(-ID, me); S['_r121'] = month_rows(r121, me); S['_negID'] = month_rows(-ID, me); del pos, neg, posm, negm, ID
    # residual momentum
    mk = P['bench_ret']; mean_m = mk.rolling(252, min_periods=200).mean(); var_m = (mk * mk).rolling(252, min_periods=200).mean() - mean_m ** 2
    rr = ret.clip(-0.5, 0.5); cov = rr.mul(mk, axis=0).rolling(252, min_periods=200).mean() - rr.rolling(252, min_periods=200).mean().mul(mean_m, axis=0)
    beta = cov.div(var_m.replace(0, np.nan), axis=0).shift(1); resid = rr.sub(beta.mul(mk, axis=0)).clip(-0.5, 0.5)
    S['R1'] = month_rows(resid.rolling(231, min_periods=180).sum().shift(21) / resid.rolling(231, min_periods=180).std().shift(21), me); del cov, beta, resid, rr
    up = vol.where(ret > 0, 0.0).rolling(63, min_periods=40).sum(); dn = vol.where(ret < 0, 0.0).rolling(63, min_periods=40).sum(); S['V1'] = month_rows(np.log((up + 1) / (dn + 1)), me); del up, dn
    pc = cf.shift(1); tr = pd.concat([(high - low), (high - pc).abs(), (low - pc).abs()]).groupby(level=0).max(); atr = tr.ewm(com=13, adjust=False, min_periods=14).mean()
    ap = atr / cf; S['V2'] = month_rows(-(ap / ap.rolling(126, min_periods=100).median()), me); S['_atr'] = month_rows(atr, me); S['_atrpct_ratio'] = month_rows(ap / ap.rolling(126, min_periods=100).median(), me); del tr, atr, ap
    S['M1'] = month_rows((cf / cf.shift(63) - 1) - (cf.shift(63) / cf.shift(126) - 1), me)
    S['M2'] = month_rows(-(cf / cf.shift(21) - 1), me)
    S['M3'] = month_rows(-ret.rolling(21, min_periods=15).max(), me)
    mp = cf.resample('ME').last(); mp.index = pd.PeriodIndex(mp.index, freq='M'); mp = mp[~mp.index.duplicated(keep='last')]; mret = mp.pct_change(fill_method=None)
    seas = pd.concat([mret.shift(12 * k - 1) for k in range(1, 6)]).groupby(level=0).apply(lambda g: g.mean(skipna=True)) if False else None
    stack = np.stack([mret.shift(12 * k - 1).values for k in range(1, 6)]); cnt = np.isfinite(stack).sum(axis=0)
    with np.errstate(all='ignore'): sv = np.where(cnt >= 3, np.nanmean(stack, axis=0), np.nan)
    S['T1'] = pd.DataFrame(sv, index=mret.index, columns=mret.columns).reindex(S['A1'].index).astype('float32')
    # references
    def leg(L):
        v = ret.rolling(L, min_periods=int(.8 * L)).std().shift(21) * np.sqrt(252); return ((cf.shift(21) / cf.shift(21 + L) - 1) / v.replace(0, np.nan)).clip(-5, 5)
    S['BASE'] = month_rows((leg(231) + leg(105)) / 2, me); S['CTRL'] = month_rows(r121, me)
    # Q2 composite needs cross-sectional z in universe
    U = S['_uni'] > 0
    def z(df): x = df.where(U); return x.sub(x.mean(axis=1), axis=0).div(x.std(axis=1), axis=0)
    S['Q2'] = z(S['_r121']) + z(S['_negID'])
    S['_close_me'] = month_rows(cf, me)
    pickle.dump(S, open(f'{C.CACHE}/signals_all.pkl', 'wb')); print({k: v.shape for k, v in S.items()})
if __name__ == '__main__': build()
