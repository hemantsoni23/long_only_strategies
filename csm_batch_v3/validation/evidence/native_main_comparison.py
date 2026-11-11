"""Compare source main()'s warmed, already-active book with flat-start validation."""
import sys
from pathlib import Path
import pandas as pd
E=Path(__file__).resolve().parent;ROOT=E.parents[1];sys.path.insert(0,str(ROOT));import csm_stock_backtest_v3 as bt
bt.START_DATE='2015-01-01';bt.END_DATE='2025-12-31';s=bt.build_csm();out=bt.run_backtest(s);report=bt.slice_to_report_window(out,bt.START_DATE,bt.END_DATE,bt.INITIAL_CAPITAL);m=bt.metrics(report,bt.RISK_FREE_RATE);start=pd.Timestamp(bt.START_DATE);t=out['trades_df'];before=t[t.Entry_Date<start];cross=before[(before.Exit_Date>=start)];base=pd.read_csv(E/'late_universe_cells.csv').query("cell=='baseline'").iloc[0]
d=pd.DataFrame([{'run':'source main convention (pre-start book allowed)','cagr_pct':m['CAGR'],'sharpe':m['Sharpe0'],'calmar':m['Calmar'],'maxdd_pct':m['MaxDD'],'prestart_entries':len(before),'prestart_positions_crossing_boundary':len(cross),'reported_trade_rows':len(report['trades_df'])},{'run':'flat-start comparison used in reports','cagr_pct':base.cagr_pct,'sharpe':base.sharpe,'calmar':base.calmar,'maxdd_pct':base.maxdd_pct,'prestart_entries':0,'prestart_positions_crossing_boundary':0,'reported_trade_rows':int(base.trades)}]);d.to_csv(E/'native_main_comparison.csv',index=False);print(d.to_string(index=False))
