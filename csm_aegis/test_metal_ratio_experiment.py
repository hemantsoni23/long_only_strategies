"""Execution-integrity regression for the isolated gold/silver ratio experiment."""
import os

from csm_aegis_metal_ratio_experiment import _read_etf, run_metal_ratio_experiment
from csm_aegis_strategy import CSMAegis, DEFAULT_SECONDARY_ETF_DIR


def test_ratio_rotation_uses_only_real_etf_bars():
    results, summary = run_metal_ratio_experiment(DEFAULT_SECONDARY_ETF_DIR)
    frames = {ticker: _read_etf(DEFAULT_SECONDARY_ETF_DIR, ticker) for ticker in ("GOLDBEES", "SILVERBEES")}
    assert summary.index.tolist() == ["goldbees", "silverbees", "ratio"]
    assert results["ratio"]["start"] >= frames["SILVERBEES"].index.min()
    assert len(results["ratio"]["trades"]) > 1
    for row in results["ratio"]["trades"].itertuples():
        bar = frames[row.Ticker].loc[row.Date]
        reason = CSMAegis.execution_bar_reason(bar.close, bar.volume, bar.high, bar.low, bar.close)
        assert reason is None, row
    # More conservative cost assumptions cannot improve the same fixed rule.
    _, cost_06 = run_metal_ratio_experiment(DEFAULT_SECONDARY_ETF_DIR, cost=0.006)
    _, cost_10 = run_metal_ratio_experiment(DEFAULT_SECONDARY_ETF_DIR, cost=0.010)
    assert summary.loc["ratio", "CAGR"] >= cost_06.loc["ratio", "CAGR"] >= cost_10.loc["ratio", "CAGR"]


if __name__ == "__main__":
    test_ratio_rotation_uses_only_real_etf_bars()
    print("METAL-RATIO EXPERIMENT TESTS PASSED")
