"""Repeat the SMA run using the original, unmodified backtest accounting."""
from pathlib import Path
import compare

compare.OUT = Path(__file__).resolve().parent / 'original_accounting'
compare.OUT.mkdir(exist_ok=True)
all_guards = compare.guards
compare.guards = lambda benchmark: {'sma200': all_guards(benchmark)['sma200']}
compare.research_engine = lambda: compare.bt._run_event_backtest
compare.main()
