"""Read-only source-file audit. Hashes content, removes no data, writes only evidence."""
from pathlib import Path
import csv, hashlib, json, math
from datetime import date,timedelta
from collections import Counter
ROOT=Path(__file__).resolve().parent; SOURCE=Path('/Users/hemantsoni/Documents/upstox_data_folder/ohlcv_data')
paths=sorted(SOURCE.glob('*.csv')); manifest=[]; anomalies=[]; counts=Counter(); first='9999'; last='0000'
for ix,p in enumerate(paths):
    before=p.stat(); digest=hashlib.sha256(); records={}; prior_date=None; raw=0
    def lines():
        with p.open('rb') as h:
            for line in h:
                digest.update(line)
                yield line.decode('utf-8-sig')
    try:
        for row in csv.DictReader(lines()):
            raw+=1; d=row.get('datetime','')[:10]
            try: c=float(row['close'])
            except (ValueError,TypeError,KeyError): counts['invalid_close']+=1;continue
            if not d or not math.isfinite(c) or c<=0: counts['nonpositive_or_missing']+=1;continue
            if prior_date and d<prior_date:counts['out_of_order']+=1
            if d in records:counts['duplicate_dates']+=1
            records[d]=c;prior_date=d
    except Exception as e: counts['file_errors']+=1;print('FILE ERROR',p.name,repr(e),flush=True)
    after=p.stat()
    if (before.st_size,before.st_mtime_ns)!=(after.st_size,after.st_mtime_ns):counts['changed_while_scanning']+=1
    days=sorted(records); n=len(days)
    if n:
        first=min(first,days[0]);last=max(last,days[-1]);previous=None
        for d in days:
            c=records[d]
            if previous is not None:
                ratio=c/previous-1
                if ratio<=-.4 or ratio>=3:anomalies.append((abs(ratio),p.stem,d,ratio))
            previous=c
    manifest.append({'symbol':p.stem,'first':days[0] if n else '', 'last':days[-1] if n else '', 'valid_dates':n,'raw_rows':raw,'size':after.st_size,'mtime_ns':after.st_mtime_ns,'sha256':digest.hexdigest()})
    if (ix+1)%1000==0:print('files scanned',ix+1,flush=True)
cutoff=(date.fromisoformat(last)-timedelta(days=183)).isoformat();old=[r for r in manifest if r['last'] and r['last']<cutoff]
summary={'source':str(SOURCE),'files':len(paths),'first':first,'last':last,'stale_cutoff':cutoff,'last_seen_before_cutoff':len(old),'last_seen_pct':len(old)/len(paths)*100,'extreme_close_changes':len(anomalies),'counts':dict(counts),'largest_jumps':[{'symbol':s,'date':d,'return_pct':r*100} for _,s,d,r in sorted(anomalies,reverse=True)[:20]]}
with (ROOT/'data_manifest.csv').open('w',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=list(manifest[0]));writer.writeheader();writer.writerows(manifest)
(ROOT/'data_audit.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2),flush=True)
