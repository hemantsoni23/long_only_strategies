import pickle, numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore')
import index_lab as L
from data import load_panels
from evaluate import composite
from portfolio_lab import topn_book
st = pickle.load(open('.cache/state.pkl','rb')); F,FWD,U,sig = st['F'],st['FWD'],st['U'],st['sig']
UN = pickle.load(open('.cache/extra_universes.pkl','rb')); allU=dict(U); allU.update(UN)
I,Ec,Ev,cal = L.prep(); isig = L.month_ends(cal)
assert isig.equals(sig) or True
# --- stock books (U1 liquid-1000, top-15, net of 0.3% costs) ---
m = allU['U1_liquid1000']
def book(c, mask=m):
    sc = composite(F,c,mask) if len(c)>1 else F[c[0]].where(mask); return topn_book(sc,mask,FWD[1],n=15)['net']
B = {'Elendel_book':book(['a3_rs_high','q5_126']), 'Zenith_book':book(['a1_52wh','q5_189']), 'csm_abs_score_book':book(['csm_abs_dual_sharpe']),
     'P4_resid+persist':book(['mom_resid_12_1','q5_126']), 'P6_tight+persist':book(['tight_close_15','q5_126']),
     'P2_low_risk':book(['lowvol_126','low_ulcer_252']), 'P1_intraday+ulcer':book(['intra_over_252','low_ulcer_252'])}
m7 = allU['U7_midsmall_301_1000']
B['P6_tight+persist(midsmall)'] = book(['tight_close_15','q5_126'], m7); B['Elendel_book(midsmall)'] = book(['a3_rs_high','q5_126'], m7)
# --- index / ETF strategies ---
AC = pd.DataFrame({'Nifty50':I['Nifty_50'],'Midcap100':I['NIFTY_MIDCAP_100'],'Smallcap100':I['NIFTY_SMLCAP_100'],'Gold':Ec['GOLDBEES']}).loc['2006-01-01':]
FW = L.fwd_returns(AC, cal, isig, (1,))
Fd = {n:f.reindex(isig) for n,f in L.asset_factors(AC).items()}
start = pd.Timestamp('2008-03-31')
liq = Ec['LIQUIDBEES']; cash1 = L.fwd_returns(pd.DataFrame({'c':liq}),cal,isig,(1,))[1]['c'].fillna((1.06)**(1/12)-1)
cash1[cash1.index<'2007-06-30']=(1.06)**(1/12)-1
for fac,k in (('hi_252',1),('mom_3_0',1),('q5_126',2)):
    bk = L.run_book(Fd[fac].loc[start:], FW[1], k=k, cost=0.001, cash_m=cash1); B[f'AssetRotation_{fac}_top{k}'] = bk['net']
SECT = ['Nifty_Bank','Nifty_IT','Nifty_Pharma','Nifty_FMCG','Nifty_Auto','Nifty_Metal','Nifty_Energy','Nifty_Infra','Nifty_PSU_Bank','Nifty_Pvt_Bank','Nifty_Fin_Service','Nifty_Media','Nifty_MNC','Nifty_PSE','Nifty_CPSE','Nifty_Commodities','Nifty_Consumption','Nifty_Realty','Nifty_Serv_Sector']
Cs = I[SECT]; Fs = {n:f.reindex(isig) for n,f in L.asset_factors(Cs, bench=I['Nifty_500']).items()}
FWs = L.fwd_returns(Cs, cal, isig, (1,))
B['SectorRotation_low_ulcer_top3'] = L.run_book(Fs['low_ulcer_126'].loc['2005-01-31':], FWs[1], k=3, cost=0.001)['net']
B['Gold_buyhold'] = FW[1]['Gold'].loc[start:]
B['Nifty500_buyhold'] = L.fwd_returns(I[['Nifty_500']],cal,isig,(1,))[1]['Nifty_500']
D = pd.DataFrame(B).loc['2008-04-30':].dropna(how='all')
C = D.corr(min_periods=60)
C.to_csv('results/stage13_book_correlations.csv', float_format='%.3f')
pd.set_option('display.width',300); pd.set_option('display.max_columns',30)
short = {c:c[:16] for c in C.columns}
print(C.rename(columns=short,index=short).round(2).to_string())
# --- ETF proxies ---
ins = pd.read_csv('/Users/hemantsoni/Documents/upstox_data_folder/etf_instruments.csv')
nm = ins.set_index('trading_symbol')['name']
dv = (Ec*Ev).rolling(63,min_periods=21).median().iloc[-1]
rows=[]
for sym in Ec.columns:
    s=Ec[sym].dropna()
    if len(s)<500: continue
    rows.append((sym, nm.get(sym,''), s.index[0].date(), len(s), float(dv.get(sym,np.nan))))
E = pd.DataFrame(rows,columns=['symbol','name','start','days','recent_med_value_inr']).sort_values('recent_med_value_inr',ascending=False)
E.to_csv('results/etf_liquid_list.csv',index=False)
pd.set_option('display.max_rows',100); pd.set_option('display.max_colwidth',60)
print(E[E.recent_med_value_inr>2e7].head(60).to_string(index=False))
