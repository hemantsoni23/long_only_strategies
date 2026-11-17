"""Read-only audit of fundamentals JSON continuity and accounting consistency."""
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
import gzip
import math

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'fundamentals_data'
BACKUPS = Path('/Users/hemantsoni/Documents/upstox_data_folder/Fundamentals/output/integrated_backups')
OUT = Path(__file__).resolve().parent
FIELDS = ('revenue_from_operations', 'net_profit', 'basic_eps', 'paid_up_equity_share_capital', 'face_value_per_share')

def num(x):
    if isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x):
        return float(x)
    return None

def fin(b):
    return (b or {}).get('income_statement') or {}

def item(d):
    result = {}
    for fy, y in (d.get('fiscal_years') or {}).items():
        for q, b in (y.get('quarters') or {}).items():
            for scope in ('standalone', 'consolidated'):
                if scope in b and isinstance(b[scope], dict):
                    result[(fy,q,scope)] = b[scope]
    return result

rows=[]; reconc=[]; backups=Counter(); differences=[]; fylabels=Counter(); examples=[]; empty=[]
for path in sorted(list(DATA.glob('*.json')) + list((DATA/'sme').glob('*.json'))):
    group = 'SME' if path.parent.name == 'sme' else 'main'
    doc = json.loads(path.read_text()); sym = doc.get('symbol', path.stem)
    quarters = item(doc)
    backup = BACKUPS / (sym+'.json.gz')
    if group == 'main' and backup.exists():
        backups['files_compared'] += 1
        old = item(json.loads(gzip.decompress(backup.read_bytes())))
        for key, b in old.items():
            period_end=(b.get('period') or {}).get('end')
            if not period_end or period_end > '2024-12-31': continue
            backups['older_blocks']+=1; current=quarters.get(key)
            if current is None:
                backups['missing_old_blocks']+=1
                if len(differences)<30: differences.append((sym,key,'block_missing'))
                continue
            for field in FIELDS:
                a,c=fin(b).get(field), fin(current).get(field)
                backups['historical_field_comparisons']+=1
                if a != c:
                    backups['historical_field_differences']+=1
                    if len(differences)<30: differences.append((sym,key,field,a,c))
    for (fy,q,scope), b in quarters.items():
        per=b.get('period') or {}; end=per.get('end'); start=per.get('start'); inc=fin(b)
        if not end: continue
        row={'symbol':sym,'group':group,'fy':fy,'quarter':q,'basis':scope,'start':start,'end':end,
             'filed':b.get('filed_date'), 'source_url':(b.get('source_filing') or {}).get('url'),
             'submission_type':(b.get('source_filing') or {}).get('submission_type')}
        for k in FIELDS: row[k]=num(inc.get(k))
        if start:
            try: row['days']=(datetime.fromisoformat(end)-datetime.fromisoformat(start)).days
            except ValueError: row['days']=None
        rows.append(row)
    for fy,y in (doc.get('fiscal_years') or {}).items():
        if fy not in ('FY2020-21','FY2021-22','FY2022-23','FY2023-24','FY2024-25','FY2025-26'): continue
        for scope in ('standalone','consolidated'):
            annual=(y.get('annual') or {}).get(scope) or {}; blocks=[(y.get('quarters') or {}).get(q,{}).get(scope) for q in ('Q1','Q2','Q3','Q4')]
            if not annual or any(not b for b in blocks): continue
            try:
                if any(not 80 <= (datetime.fromisoformat(b['period']['end']) - datetime.fromisoformat(b['period']['start'])).days <= 100 for b in blocks): continue
            except (KeyError, TypeError, ValueError): continue
            for field in ('revenue_from_operations','net_profit'):
                a=num(fin(annual).get(field)); vals=[num(fin(b).get(field)) for b in blocks]
                if a is None or any(x is None for x in vals): continue
                total=sum(vals); error=abs(total-a)/max(abs(a),abs(total),1)
                reconc.append({'symbol':sym,'group':group,'fy':fy,'basis':scope,'field':field,
                               'annual':a,'sum_quarters':total,'error':error,'q4':vals[-1],
                               'annual_filed':annual.get('filed_date'),'q4_filed':blocks[-1].get('filed_date'),
                               'q4_source':(blocks[-1].get('source_filing') or {}).get('url')})
print('BACKUP_COMPARISON',dict(backups),'EXAMPLES',differences)
f=pd.DataFrame(rows);f['end']=pd.to_datetime(f['end']);f['year']=f['end'].dt.year
f.to_csv(OUT/'filings_inventory.csv',index=False)
r=pd.DataFrame(reconc);r.to_csv(OUT/'annual_reconciliation.csv',index=False)
print('ROW_COUNTS', f.groupby(['group','year']).size().to_dict())
print('INTEGRATED_SHARE', f.groupby(['group','year']).source_url.apply(lambda x: round(x.notna().mean(),3)).to_dict())
for field in FIELDS:
 print('NONNULL',field, f.groupby(['group','year'])[field].apply(lambda x: round(x.notna().mean(),3)).to_dict())
print('RECONCILIATION')
for (fy,field),g in r[r.group=='main'].groupby(['fy','field']):
 print(fy,field,'count',len(g),'<=1%',round((g.error<=.01).mean()*100,1),'>10%',round((g.error>.1).mean()*100,1),'>50%',round((g.error>.5).mean()*100,1))
print('TOP_LARGE_POST_2025',r[(r.fy.isin(['FY2024-25','FY2025-26']))&(r.error>.1)].sort_values('error',ascending=False)[['symbol','fy','basis','field','annual','sum_quarters','q4','error']].head(25).to_string(index=False))
# Consecutive-quarter revenue jumps >= 20x, separately in each scope.
f=f.sort_values(['symbol','basis','end']);f['prev_end']=f.groupby(['symbol','basis']).end.shift();f['prev_rev']=f.groupby(['symbol','basis']).revenue_from_operations.shift();f['ratio']=f.revenue_from_operations/f.prev_rev
f['gap']=(f['end']-f['prev_end']).dt.days
j=f[(f.gap.between(80,100)) & (f.revenue_from_operations>0) & (f.prev_rev>0)]
for year,g in j[j.group=='main'].groupby('year'):
 print('REVENUE_SPIKES',year,'pairs',len(g),'over20x',int(((g.ratio>20)|(g.ratio<.05)).sum()))
print('POST_TRANSITION_SPIKE_EXAMPLES',j[(j.year>=2025)&((j.ratio>20)|(j.ratio<.05))][['symbol','basis','prev_end','end','prev_rev','revenue_from_operations','ratio']].head(30).to_string(index=False))
print('SOURCE_SUBMISSION_TYPES',f[f.year>=2025].submission_type.value_counts(dropna=False).head(15).to_dict())
