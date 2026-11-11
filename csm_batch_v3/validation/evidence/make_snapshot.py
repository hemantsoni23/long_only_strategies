"""Create a fixed, read-only testing copy outside the source folder.
Use the byte lengths captured before validation and remove all rows after 2026-10-30.
Only copies; never writes to the source. The original source may continue updating.
"""
import json,hashlib,csv,os
from pathlib import Path
E=Path(__file__).resolve().parent
SRC=Path('/Users/hemantsoni/Documents/upstox_data_folder/ohlcv_data')
DST=Path('/private/tmp/csm_batch_v3_validation_snapshot/ohlcv')
DST.mkdir(parents=True,exist_ok=True)
base=json.loads((E/'fingerprint_before.json').read_text())['data'];out=[]
manifest=E/'snapshot_manifest.csv'
prior={r['file']:r['snapshot_sha256'] for r in csv.DictReader(manifest.open())} if manifest.exists() else {}
for name,(length,mtime) in sorted(base.items()):
 src=SRC/name; size=src.stat().st_size
 if size<length:raise RuntimeError(f'Source shrank after initial metadata snapshot: {name}')
 with src.open('rb') as f:data=f.read(length)
 if len(data)!=length or (data and data[-1:]!=b'\n'):raise RuntimeError(f'Unstable or partial source at initial boundary: {name}')
 lines=data.splitlines(keepends=True);header=lines[0];body=[];dropped=0
 for line in lines[1:]:
  date=line[:10].decode('ascii',errors='replace')
  if len(date)==10 and date>'2026-10-30':dropped+=1
  else:body.append(line)
 blob=header+b''.join(body);digest=hashlib.sha256(blob).hexdigest()
 if name in prior and prior[name]!=digest:raise RuntimeError(f'Original prefix changed since snapshot: {name}')
 dest=DST/name;dest.write_bytes(blob)
 out.append({'file':name,'initial_bytes':length,'snapshot_bytes':len(blob),'rows_after_cutoff_removed':dropped,'snapshot_sha256':digest})
with (E/'snapshot_manifest.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
result={'source':str(SRC),'snapshot':str(DST),'csv_files':len(out),'cutoff_inclusive':'2026-10-30','rows_after_cutoff_removed':sum(x['rows_after_cutoff_removed'] for x in out),'creation':'Source initial byte lengths captured before validation; later-dated rows omitted. Earlier byte-prefix integrity cannot be proven for changes before the audit hash.'}
(E/'snapshot_info.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
