"""Verify every read-only validation snapshot file against its recorded SHA-256."""
import csv,hashlib,json
from pathlib import Path
E=Path(__file__).resolve().parent;root=Path('/private/tmp/csm_batch_v3_validation_snapshot/ohlcv');manifest=list(csv.DictReader((E/'snapshot_manifest.csv').open()));bad=[]
for r in manifest:
 p=root/r['file']
 if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest()!=r['snapshot_sha256']:bad.append(r['file'])
actual={p.name for p in root.glob('*.csv')};expected={r['file'] for r in manifest}
d={'expected_files':len(expected),'actual_files':len(actual),'hash_mismatches_or_missing':len(bad),'extra_files':len(actual-expected),'ok':not bad and actual==expected}
(E/'snapshot_verification.json').write_text(json.dumps(d,indent=2));print(json.dumps(d,indent=2))
if not d['ok']:raise SystemExit(1)
