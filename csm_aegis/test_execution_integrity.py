"""Execution-integrity regression test for CSM Aegis.

Every booked entry/exit must use a raw, positive-volume, non-circuit OHLC bar.
Unfillable exits must remain pending rather than receive a forward-filled price.
Run from this directory: ``python3 test_execution_integrity.py``.
"""
import os

import numpy as np

from csm_aegis_strategy import CSMAegis, load_data
from csm_aegis_backtest import backtest_event_driven


HERE = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.environ.get("CSM_AEGIS_DATA_FOLDER", "/Users/hemantsoni/Documents/upstox_data_folder/ohlcv_data")


def test_bar_classifier():
    cases = (
        ((100.0, 1.0, 101.0, 99.0, 100.0), None),
        ((100.0, 0.0, 101.0, 99.0, 100.0), "NO_VOLUME"),
        ((100.0, 1.0, 100.0, 100.0, 100.0), "CIRCUIT_LOCK"),
        ((np.nan, 1.0, 101.0, 99.0, 100.0), "STALE_OR_MISSING_PRICE"),
        ((100.0, 1.0, np.nan, 99.0, 100.0), "MISSING_OHLC"),
    )
    for values, expected in cases:
        actual = CSMAegis.execution_bar_reason(*values)
        assert actual == expected, (values, actual, expected)


def test_booked_fills():
    data = load_data(DATA_FOLDER, cache_dir=os.path.join(HERE, ".cache"))
    strategy = CSMAegis.from_preset("v1.3", *data, start="2005-01-01").calculate_factors()
    results = backtest_event_driven(strategy)
    trades = results["trades"]

    # END_OF_PERIOD is a mark, not an executable exit. All other transaction
    # records must pass the identical raw-bar validation used by the engine.
    for trade in trades.itertuples():
        j = strategy.cols.index(trade.Ticker)
        entry_i = strategy.dates.get_loc(trade.Entry_Date)
        assert strategy.fillability_reason(entry_i, j, strategy.fill) is None, trade
        if trade.Exit_Reason != "END_OF_PERIOD":
            exit_i = strategy.dates.get_loc(trade.Exit_Date)
            assert strategy.fillability_reason(exit_i, j, strategy.fill) is None, trade

    deferred = strategy.deferred_order_log
    assert len(deferred) > 0, "fixture should exercise deferred fills"
    assert set(deferred.Order_Type) == {"EXIT"}
    assert {"STALE_OR_MISSING_PRICE", "CIRCUIT_LOCK"}.issubset(set(deferred.Reason))


if __name__ == "__main__":
    test_bar_classifier()
    test_booked_fills()
    print("EXECUTION-INTEGRITY TESTS PASSED")
