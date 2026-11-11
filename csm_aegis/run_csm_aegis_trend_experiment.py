"""Runner for the isolated daily ADX / Supertrend / pivot experiment.

Production files are not changed. Example:
  python3 run_csm_aegis_trend_experiment.py --variant adx
  python3 run_csm_aegis_trend_experiment.py --variant adx_supertrend
"""
import argparse
import ast
import os
import sys
import warnings

from csm_aegis_strategy import PRESETS, load_data
from csm_aegis_backtest import (
    DATA_FOLDER, PANEL_CACHE, REPORT_START, _benchmark, backtest_event_driven,
    print_deferred_summary, print_exit_breakdown, print_reject_summary,
    print_report, print_yearly_returns,
)
from csm_aegis_trend_experiment import CSMAegisTrendExperiment


VARIANTS = {
    "baseline": {},
    "adx": dict(adx_entry_filter=True),
    "supertrend_exit": dict(supertrend_exit=True),
    "pivot": dict(pivot_resistance_filter=True, pivot_stop=True),
    "adx_supertrend": dict(adx_entry_filter=True, supertrend_entry_filter=True, supertrend_exit=True),
    "full_daily": dict(adx_entry_filter=True, supertrend_entry_filter=True, supertrend_exit=True,
                       pivot_resistance_filter=True, pivot_stop=True),
}


def parse_overrides(items):
    out = {}
    for item in items or []:
        key, value = item.split("=", 1)
        try:
            out[key] = ast.literal_eval(value)
        except (SyntaxError, ValueError):
            out[key] = value
    return out


def main(argv=None):
    parser = argparse.ArgumentParser(description="Run isolated daily technical-overlay experiments for CSM Aegis.")
    parser.add_argument("--preset", default="v1.3", choices=list(PRESETS))
    parser.add_argument("--variant", default="adx", choices=list(VARIANTS))
    parser.add_argument("--set", action="append", help="override, e.g. --set adx_threshold=20")
    args = parser.parse_args(argv)
    warnings.filterwarnings("ignore")
    print("Loading daily OHLCV panels ...")
    data = load_data(DATA_FOLDER, cache_dir=PANEL_CACHE)
    options = {**VARIANTS[args.variant], **parse_overrides(args.set)}
    strategy = CSMAegisTrendExperiment.from_preset(
        args.preset, *data, start=REPORT_START, **options
    ).calculate_factors()
    results = backtest_event_driven(strategy)
    print(f"\nEXPERIMENT ONLY — variant={args.variant}; this runner does not modify production strategy files.")
    print("VWAP is intentionally excluded: this run contains daily OHLCV only.")
    print_report(results, strategy, _benchmark())
    print_exit_breakdown(results["trades"])
    print_yearly_returns(results["ret"], _benchmark(), results.get("effective_start", REPORT_START))
    print_reject_summary(strategy)
    print_deferred_summary(strategy)


if __name__ == "__main__":
    main()
