"""Stock-level sector factors. Sector assignment is data-driven & point-in-time: each stock -> sector index with the highest
trailing-252d correlation of market-residual daily returns (needs >=150 obs, corr>=0.25), refreshed every month-end."""
import pickle, numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore')
from data import load_panels
from assets import load_indices
from factors import Ctx
from evaluate import evaluate_factor, composite, zscore
st = pickle.load(open('.cache/state.pkl','rb')); F,FWD,U,sig = st['F'],st['FWD'],st['U'],st['sig']
UN = pickle.load(open('.cache/extra_universes.pkl','rb'))
P = load_panels(); X = Ctx(P); cal = X.C.index
I = load_indices()['close']
SECT = ['Nifty_Bank','Nifty_IT','Nifty_Pharma','Nifty_FMCG','Nifty_Auto','Nifty_Metal','Nifty_Energy','Nifty_Infra','Nifty_PSU_Bank','Nifty_Pvt_Bank',
        'Nifty_Fin_Service','Nifty_Media','Nifty_MNC','Nifty_PSE','Nifty_CPSE','Nifty_Commodities','Nifty_Consumption','Nifty_Realty','Nifty_Serv_Sector']
S = I[SECT].reindex(cal).ffill(limit=5)
sr = S.pct_change(fill_method=None)
mkt = X.mkt
rs_res = X.r.sub(mkt, axis=0)
cors = []
for j,sn in enumerate(SECT):
    sres = (sr[sn]-mkt)
    c = rs_res.rolling(252, min_periods=150).corr(sres).reindex(sig)
    cors.append(c.values); print('corr',sn,flush=True)
A = np.stack(cors)                       # sector x sig x stock
np.save('.cache/sector_corr.npy', A.astype('float32'))
with np.errstate(all='ignore'):
    best = np.nanargmax(np.where(np.isnan(A), -9, A), axis=0)
    bestc = np.nanmax(np.where(np.isnan(A), -9, A), axis=0)
for th in (0.05,0.08,0.10,0.15,0.20,0.25):
    print('threshold',th,'assigned share',round(float((bestc>=th).mean()),3), ' among valid:', round(float((bestc[bestc>-9]>=th).mean()),3))
THR = 0.10
lab = np.where(bestc>=THR, best, -1)     # -1 = unassigned
print('assigned share (avg over months):', (lab>=0).mean())
# sector-level monthly features
Ss = S.reindex(sig)
def sec_feats():
    d = {}
    d['sector_mom_6_1'] = (S.shift(21)/S.shift(126)-1).reindex(sig)
    d['sector_mom_12_1'] = (S.shift(21)/S.shift(252)-1).reindex(sig)
    d['sector_mom_3_0'] = (S/S.shift(63)-1).reindex(sig)
    d['sector_hi_252'] = (S/S.rolling(252,min_periods=200).max()).reindex(sig)
    sma50 = S.rolling(50,min_periods=40).mean(); ab = (S>sma50).where(S.notna()&sma50.notna()).astype('float64')
    d['sector_q5_126'] = ab.rolling(126,min_periods=100).mean().reindex(sig)
    return d
SF = sec_feats()
cols = pd.Index(X.C.columns)
new = {}
for n, fr in SF.items():
    v = fr.values                                    # sig x sector
    out = np.full((len(sig), len(cols)), np.nan)
    for k in range(len(sig)):
        l = lab[k]; ok = l>=0
        out[k, ok] = v[k, l[ok]]
    new[n] = pd.DataFrame(out, index=sig, columns=cols).astype('float32')
new['stock_vs_sector_6_1'] = (F['mom_6_1'] - new['sector_mom_6_1']).astype('float32')
new['stock_vs_sector_12_1'] = (F['mom_12_1'] - new['sector_mom_12_1']).astype('float32')
# unassigned stocks get NaN -> excluded from the IC universe for these factors
F2 = dict(F); F2.update(new)
pickle.dump(new, open('.cache/sector_stock_factors.pkl','wb'))
rows=[]
allU = dict(U); allU.update(UN)
for u in ['U1_liquid1000','U3_top300','U4_top250','U7_midsmall_301_1000']:
    m = allU[u]
    elen = composite(F,['a3_rs_high','q5_126'],m)
    for n in list(new)+['mom_6_1','mom_12_1']:
        r,_ = evaluate_factor(n, F2[n], m, FWD, base_rank=elen); r['universe']=u; rows.append(r)
df = pd.DataFrame(rows); df.to_csv('results/stage10_sector_stock.csv', index=False, float_format='%.5f')
pd.set_option('display.width',250); pd.set_option('display.max_columns',40)
c=['factor','universe','avg_n','ic_1','icir_1','ic_3','icir_3','hit_3','t_3','ic_6','ic_12','ic_disc_3','ic_hold_3','corr_elendel','inc_ic_3','top20_winmed_3']
print(df[c].round(3).to_string(index=False))
