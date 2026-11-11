"""Raw-bar validation for the optional idle-cash metal ETF sleeve.

Run from this directory: ``python3 test_secondary_etf.py``.
"""
import os

import numpy as np

from csm_aegis_strategy import CSMAegis, load_data
from csm_aegis_backtest import _load_secondary_etf, backtest_event_driven


HERE = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.environ.get("CSM_AEGIS_DATA_FOLDER", "/Users/hemantsoni/Documents/upstox_data_folder/ohlcv_data")


def test_gold_sleeve_uses_only_raw_tradable_etf_bars():
    data = load_data(DATA_FOLDER, cache_dir=os.path.join(HERE, ".cache"))
    strategy = CSMAegis.from_preset("v1.4_low_dd", *data, start="2005-01-01").calculate_factors()
    results = backtest_event_driven(strategy)
    etf = _load_secondary_etf(strategy)["raw"]

    # Gold's own history determines the comparable sample; no fabricated price
    # before the first observed ETF close is permitted.
    assert results["effective_start"] >= etf.close.dropna().index.min()
    assert (strategy.daily_log.Cash >= -1e-10).all()
    assert (results["mult"] < 1.0).any(), "regime leverage must rebalance the ETF sleeve too"
    assert len(strategy.etf_trade_log) > 0
    for trade in results["trades"].itertuples():
        j = strategy.cols.index(trade.Ticker)
        entry_i = strategy.dates.get_loc(trade.Entry_Date)
        assert strategy.fillability_reason(entry_i, j, strategy.fill) is None, trade
        if trade.Exit_Reason != "END_OF_PERIOD":
            exit_i = strategy.dates.get_loc(trade.Exit_Date)
            assert strategy.fillability_reason(exit_i, j, strategy.fill) is None, trade
    for row in strategy.etf_trade_log.itertuples():
        i = strategy.dates.get_loc(row.Date)
        reason = CSMAegis.execution_bar_reason(etf.close.iat[i], etf.volume.iat[i], etf.high.iat[i], etf.low.iat[i], etf.close.iat[i])
        assert reason is None, row
        assert np.isfinite(row.Price) and row.Price > 0 and row.Notional > 0 and row.Cost >= 0

    # Missing/locked ETF days may leave cash temporarily, but they must be
    # visible in the deferred-order log instead of receiving a forward-filled fill.
    deferred = strategy.deferred_order_log
    assert (deferred.Order_Type == "ETF_IDLE_CASH_SWEEP").any()
    assert set(deferred[deferred.Ticker == "GOLDBEES"].Reason).issubset(
        {"STALE_OR_MISSING_PRICE", "NO_VOLUME", "MISSING_OHLC", "CIRCUIT_LOCK"}
    )


if __name__ == "__main__":
    test_gold_sleeve_uses_only_raw_tradable_etf_bars()
    print("SECONDARY-ETF EXECUTION TESTS PASSED")
