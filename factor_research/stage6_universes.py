"""Conditional IC: where does each factor work? (top-250 csm_absolute universe, high-vol / low-vol terciles, mid-small caps)"""
import pickle, numpy as np, pandas as pd
from data import load_panels
from factors import Ctx, rmean, rstd, FAMILY
from evaluate import evaluate_factor, composite, SPLIT
st = pickle.load(open('.cache/state.pkl','rb')); F,FWD,U,sig = st['F'],st['FWD'],st['U'],st['sig']
P = load_panels(); X = Ctx(P)
dv = X.DV.rolling(63, min_periods=21).median().reindex(sig)
rank = dv.rank(axis=1, ascending=False, method='min')
vol = rstd(X.r,126).reindex(sig)
U1 = U['U1_liquid1000']
vr = vol.where(U1).rank(axis=1, pct=True)
circ = ((X.H==X.L)&X.H.notna()).astype('float64').rolling(63,min_periods=1).sum().reindex(sig)<=5
have = X.Cf.reindex(sig).notna() & (X.Cf.reindex(sig)>20) & circ
UN = {'U4_top250': have & (rank<=250),
      'U5_highvol_tercile': U1 & (vr>=0.667),
      'U6_lowvol_tercile': U1 & (vr<=0.333),
      'U7_midsmall_301_1000': have & (rank>300) & (rank<=1000)}
pickle.dump(UN, open('.cache/extra_universes.pkl','wb'))
names = ['q5_126','q5_189','a1_52wh','a3_rs_high','hi_3y','mom_12_1','mom_6_1','mom_12_1_sharpe','mom_6_1_sharpe','csm_abs_dual_sharpe','csm_abs_sharpe6',
         'mom_resid_12_1','mom_resid_sharpe','trend_t_126','clenow_126','weekly_consist_26','mom_consist_12m','up_days_net_231','rs_win_months_12','rs_trend_t_126',
         'lowvol_126','low_ivol_252','low_ulcer_252','low_pain_126','low_downvol_252','shallow_dd_252','low_max_21','low_volvol_126','low_beta_252','hvol_126','high_beta_252',
         'intra_over_126','intra_over_252','intraday_126_clip','neg_overnight_126_clip','tight_close_15','nh_freq_63','dist_high_atr','donch_pos_126',
         'season_same_month_5y','rev_1m','mom_1m','vr_5_252','calmar_252','ker_126']
elen = {u: composite(F,['a3_rs_high','q5_126'],m) for u,m in UN.items()}
rows=[]
for u,m in UN.items():
    print(u, int(m.sum(axis=1).mean()), flush=True)
    items=[(n,F[n]) for n in names if n in F]+[('LIVE_elendel(A3+Q5_126)',elen[u]),('LIVE_zenith(A1+Q5_189)',composite(F,['a1_52wh','q5_189'],m))]
    for n,fr in items:
        r,_=evaluate_factor(n,fr,m,FWD,base_rank=elen[u],detail=True); r['universe']=u; r['family']=FAMILY.get(n,'LIVE'); rows.append(r)
df=pd.DataFrame(rows); df.to_csv('results/stage6_universe_scan.csv',index=False,float_format='%.5f')
