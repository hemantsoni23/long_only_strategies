"""Compare the new and previous JSON corpora without changing either one."""
from collections import Counter, defaultdict
from datetime import datetime
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'csm_value'))
from fundamentals_loader import _parse_filed

FIELDS = ('revenue_from_operations', 'net_profit', 'basic_eps',
          'paid_up_equity_share_capital', 'face_value_per_share')
aggregate = Counter()
counts = defaultdict(Counter)
changes = Counter()
examples = defaultdict(list)
all_revised = []
reconciliation = defaultdict(Counter)

def blocks(d):
    result = {}
    for fy, node in (d.get('fiscal_years') or {}).items():
        for q, qnode in (node.get('quarters') or {}).items():
            for basis in ('standalone','consolidated'):
                b=qnode.get(basis)
                if isinstance(b,dict) and (b.get('period') or {}).get('end'):
                    result[(fy,q,basis)] = b
    return result

for group in ('main','sme'):
    segment = '' if group == 'main' else 'sme'
    old_dir=ROOT/'fundamentals_data'/segment
    new_dir=ROOT/'fundamentals'/segment
    for path in sorted(new_dir.glob('*.json')):
        symbol=path.stem
        try:
            d=json.loads(path.read_text())
            old_path=old_dir/path.name
            old=json.loads(old_path.read_text()) if old_path.exists() else {}
        except Exception as exc:
            examples[(group,'read_error')].append((symbol,str(exc)))
            continue
        a=blocks(old);b=blocks(d)
        counts[group]['files']+=1
        seen=set()
        for key,blk in b.items():
            per=blk.get('period') or {}; end=per.get('end',''); start=per.get('start','')
            try:
                dt=datetime.fromisoformat(end[:10]); days=(dt-datetime.fromisoformat(start[:10])).days
            except (ValueError,TypeError):
                continue
            year=dt.year
            if year not in (2025,2026): continue
            seen.add(year)
            c=counts[(group,year)]; c['blocks']+=1
            if 80<=days<=100: c['quarter']+=1
            elif 150<=days<=195: c['half_year']+=1
            else:c['other_duration']+=1
            f=blk.get('source_filing') or {}; kind=f.get('submission_type');c['revisions']+=int(kind=='Revision')
            filed=_parse_filed(blk.get('filed_date'))
            if filed is None:c['bad_filed_date']+=1
            else:
                lag=(filed-dt).days
                if lag<0: c['negative_lag']+=1
                if lag>120:
                    c['lag_gt120']+=1
                    if kind=='Revision': c['revision_gt120']+=1
            inc=blk.get('income_statement') or {};facts=inc.get('other_facts') or {}
            if inc.get('net_profit') is None and facts.get('ProfitLossForThePeriod') is None and facts.get('ProfitLossFromOrdinaryActivitiesAfterTax') is None:c['missing_profit']+=1
            if inc.get('paid_up_equity_share_capital') is None or inc.get('face_value_per_share') is None:c['missing_share_fields']+=1
            prev=a.get(key)
            if prev is None:
                changes[(group,year,'added')]+=1
                if len(examples[(group,year,'added')])<8:examples[(group,year,'added')].append((symbol,key))
            else:
                changes[(group,year,'existing')]+=1
                for field in FIELDS:
                    if (prev.get('income_statement') or {}).get(field)!=inc.get(field):
                        changes[(group,year,'field_changed',field)]+=1
                        if len(examples[(group,year,'field_changed')])<8:examples[(group,year,'field_changed')].append((symbol,key,field,(prev.get('income_statement') or {}).get(field),inc.get(field)))
                if prev.get('filed_date')!=blk.get('filed_date'):changes[(group,year,'filed_changed')]+=1
        for year in seen: counts[(group,year)]['symbols']+=1
        for key,blk in a.items():
            end=(blk.get('period') or {}).get('end','')
            if end[:4] in ('2025','2026') and key not in b:
                changes[(group,int(end[:4]),'missing_in_new')]+=1
                if len(examples[(group,int(end[:4]),'missing_in_new')])<8:examples[(group,int(end[:4]),'missing_in_new')].append((symbol,key))
        for fy,node in (d.get('fiscal_years') or {}).items():
            if fy not in ('FY2024-25','FY2025-26'):continue
            for basis in ('standalone','consolidated'):
                ann=(node.get('annual') or {}).get(basis) or {}
                qs=[((node.get('quarters') or {}).get(q) or {}).get(basis) or {} for q in ('Q1','Q2','Q3','Q4')]
                if not ann or not all(qs):continue
                try:
                    if any(not 80 <= (datetime.fromisoformat(x['period']['end'])-datetime.fromisoformat(x['period']['start'])).days<=100 for x in qs): continue
                except (KeyError,ValueError,TypeError):continue
                for field in ('revenue_from_operations','net_profit'):
                    vals=[(x.get('income_statement') or {}).get(field) for x in [*qs,ann]]
                    if any(not isinstance(v,(int,float)) for v in vals):continue
                    total=sum(vals[:4]);annual=vals[4];err=abs(total-annual)/max(abs(total),abs(annual),1)
                    stat=reconciliation[(group,fy,field)];stat['n']+=1;stat['within1pct']+=int(err<=.01);stat['over10pct']+=int(err>.1)
                    if err>.1 and len(examples[(group,fy,field,'outlier')])<8: examples[(group,fy,field,'outlier')].append((symbol,basis,round(err,4)))

out={'counts':{str(k):dict(v) for k,v in counts.items()},'changes':{str(k):v for k,v in changes.items()},
     'examples':{str(k):v for k,v in examples.items()}, 'reconciliation':{str(k):dict(v) for k,v in reconciliation.items()}}
(OUT/'updated_folder_audit.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
