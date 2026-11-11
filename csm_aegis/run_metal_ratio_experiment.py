"""Run the isolated gold/silver ratio sleeve experiment."""
import argparse
import os

from csm_aegis_metal_ratio_experiment import run_metal_ratio_experiment
from csm_aegis_strategy import DEFAULT_SECONDARY_ETF_DIR


def main(argv=None):
    parser = argparse.ArgumentParser(description="Gold/silver ETF ratio rotation experiment (not production).")
    parser.add_argument("--etf-data-folder", default=DEFAULT_SECONDARY_ETF_DIR)
    parser.add_argument("--lookback", type=int, default=63, help="ratio z-score lookback in sessions")
    parser.add_argument("--z-threshold", type=float, default=1.0, help="monthly switch threshold")
    parser.add_argument("--cost", type=float, default=0.003, help="cost per ETF buy/sell leg")
    parser.add_argument("--output-dir", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "output", "metal_ratio_experiment"))
    args = parser.parse_args(argv)
    results, summary = run_metal_ratio_experiment(args.etf_data_folder, args.lookback, args.z_threshold, args.cost)
    print("\nMETAL SLEEVE EXPERIMENT — long-only rotation, not arbitrage")
    print(f"Signal: monthly {args.lookback}-session z-score, switch at ±{args.z_threshold:.2f}, cost {args.cost:.2%}/leg")
    print("SILVERBEES limits the common sample to its own first session; this is insufficient for production promotion.")
    print(summary.assign(CAGR=lambda x: x.CAGR.map(lambda v: f"{v:.2%}"), Sharpe=lambda x: x.Sharpe.map(lambda v: f"{v:.2f}"), MaxDD=lambda x: x.MaxDD.map(lambda v: f"{v:.1%}"), Calmar=lambda x: x.Calmar.map(lambda v: f"{v:.2f}")).to_string())
    os.makedirs(args.output_dir, exist_ok=True)
    summary.to_csv(os.path.join(args.output_dir, "summary.csv"))
    for mode, result in results.items():
        result["trades"].to_csv(os.path.join(args.output_dir, f"trades_{mode}.csv"), index=False)
        result["deferred"].to_csv(os.path.join(args.output_dir, f"deferred_{mode}.csv"), index=False)
        result["held"].rename("held").to_csv(os.path.join(args.output_dir, f"daily_held_{mode}.csv") )
        result["z"].rename("ratio_z").to_csv(os.path.join(args.output_dir, f"daily_ratio_z_{mode}.csv"))


if __name__ == "__main__":
    main()
