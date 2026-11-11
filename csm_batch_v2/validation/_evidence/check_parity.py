from pathlib import Path
import json
import pandas as pd
P=Path(__file__).resolve().parent
r=pd.read_csv(P/'reference_runner/equity_curve.csv',index_col=0,parse_dates=True).iloc[:,0];e=pd.read_csv(P/'parity_equity.csv',index_col=0,parse_dates=True).iloc[:,0]
result={'reference_rows':len(r),'replay_rows':len(e),'same_dates':r.index.equals(e.index),'max_abs_equity_difference':float((r-e).abs().max())};(P/'parity.json').write_text(json.dumps(result,indent=2));print(result)
if not result['same_dates'] or result['max_abs_equity_difference']>1e-10:raise SystemExit('Replay did not reproduce the strategy runner.')
