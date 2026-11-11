"""Read-only comparison of live files with initial audit hashes and captured sizes."""
from pathlib import Path
import csv,json,hashlib
E=Path(__file__).resolve().parent;prior=json.loads((E/'fingerprint_before.json').read_text())['data'];src=Path('/Users/hemantsoni/Documents/upstox_data_folder/ohlcv_data');d={'audit_prefix_matches':0,'audit_prefix_mismatches':0,'audit_size_equals_initial':0,'audit_size_differs_initial':0,'initial_byte_boundary_not_newline':0,'size_changed_since_initial':0}
for r in csv.DictReader((E/'live_data_manifest.csv').open()):
 p=src/(r['symbol']+'.csv');size=int(r['size']);old=prior[p.name][0]
 with p.open('rb') as f:data=f.read(max(size,old))
 if hashlib.sha256(data[:size]).hexdigest()==r['sha256']:d['audit_prefix_matches']+=1
 else:d['audit_prefix_mismatches']+=1
 d['audit_size_equals_initial' if size==old else 'audit_size_differs_initial']+=1
 if old and data[old-1:old]!=b'\n':d['initial_byte_boundary_not_newline']+=1
 if p.stat().st_size!=old:d['size_changed_since_initial']+=1
(E/'live_prefix_verification.json').write_text(json.dumps(d,indent=2));print(json.dumps(d,indent=2))
