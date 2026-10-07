import numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore')
from stage14_roadmap import *
P = load_panels(); X = Ctx(P)
dv = X.DV.rolling(63,min_periods=21).median().reindex(sig)
FIN = ['Elendel (control)','I1 tight+persist (mid/small)','I1 tight+persist (liquid)','I2 resid+persist (liquid)','I2 resid+persist (top250)','I3 low-risk (top250)','I4 intraday+ulcer (top250)']
rows=[]
for nm in FIN:
    comps,u = IDEAS[nm]; m = allU[u]; sc = make_score(comps,m).where(m)
    adv_list=[]
    for d in sc.index:
        if d < pd.Timestamp('2022-07-01'): continue
        s = sc.loc[d].dropna()
        if len(s)<60: continue
        pick = s.nlargest(15).index; adv_list.extend(dv.loc[d,pick].astype(float).dropna().values)
    a = np.array(adv_list)
    row={'idea':nm,'picks':len(a),'median_ADV_lakh':np.median(a)/1e5,'p25_ADV_lakh':np.percentile(a,25)/1e5}
    for aum in (5,10,25,50,100):
        pos = aum*1e7/15
        row[f'%pos>5%ADV@{aum}cr'] = float((pos/a>0.05).mean())
    # AUM at which 75% of positions are within 5% of ADV  -> pos = 0.05 * p25 ADV
    row['AUM_cr_75pct_within_5%ADV'] = 15*0.05*np.percentile(a,25)/1e7
    row['AUM_cr_median_within_5%ADV'] = 15*0.05*np.median(a)/1e7
    rows.append(row)
C = pd.DataFrame(rows).set_index('idea'); C.to_csv('results/stage14_capacity_recent.csv',float_format='%.3f')
pd.set_option('display.width',260); pd.set_option('display.max_columns',30)
print(C.round(2).to_string())
