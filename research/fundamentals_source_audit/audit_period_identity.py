"""Check filing identity using actual reporting dates, not JSON quarter labels."""
from collections import Counter, defaultdict
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
counts=Counter();samples=defaultdict(list);missing=Counter();missing_symbols=defaultdict(set)
for group,segment in [('main',''),('sme','sme')]:
    for p in sorted((ROOT/'fundamentals_data'/segment).glob('*.json')):
        other=ROOT/'fundamentals'/segment/p.name
        if not other.exists():continue
        maps=[]
        for side,path in [('old',p),('new',other)]:
            doc=json.loads(path.read_text());m=defaultdict(list)
            for fy,y in (doc.get('fiscal_years') or {}).items():
                fs=(y.get('fy_start') or '')[:10]
                try: fy_month=int(fs[5:7]);fy_year=int(fs[:4])
                except ValueError:fy_month=fy_year=0
                for q,qn in (y.get('quarters') or {}).items():
                    for scope in ('standalone','consolidated'):
                        b=qn.get(scope) or {};end=(b.get('period') or {}).get('end','')[:10]
                        if end[:4] not in ('2025','2026'):continue
                        m[(end,scope)].append((fy,q,b.get('filed_date')))
                        if q in ('Q1','Q2','Q3','Q4') and fy_month and fy_year:
                            try: months=(int(end[:4])-fy_year)*12+int(end[5:7])-fy_month;expected=months//3+1
                            except ValueError: continue
                            if expected != int(q[1:]):
                                counts[(group,side,'mismatched_label')]+=1
                                if len(samples[(group,side,'mismatched_label')])<12:samples[(group,side,'mismatched_label')].append((p.stem,fy,q,scope,end,expected))
            for k,v in m.items():
                if len(v)>1:
                    counts[(group,side,'duplicate_period_basis')]+=1
                    if len(samples[(group,side,'duplicate_period_basis')])<12:samples[(group,side,'duplicate_period_basis')].append((p.stem,k,v))
            maps.append(m)
        old,new=maps
        for (end,scope) in old.keys()-new.keys():
            missing[(group,end)]+=1;missing_symbols[(group,end)].add(p.stem)
            if len(samples[(group,end,'missing')])<5:samples[(group,end,'missing')].append((p.stem,scope,old[(end,scope)]))
        for (end,scope) in new.keys()-old.keys():counts[(group,end,'added')]+=1
out={'counts':{str(k):v for k,v in counts.items()},'missing':{str(k):{'blocks':v,'symbols':len(missing_symbols[k])} for k,v in missing.items()},'samples':{str(k):v for k,v in samples.items()}}
(OUT/'updated_period_identity.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
