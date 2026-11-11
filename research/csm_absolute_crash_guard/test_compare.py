import contextlib
import io
import unittest

import numpy as np
import pandas as pd

from compare import guards, research_engine, IndividualMomentumStrategy


class ResearchChecks(unittest.TestCase):
    def test_guard_does_not_read_future_prices(self):
        rng = np.random.default_rng(13)
        idx = pd.bdate_range('2018-01-01', periods=450)
        benchmark = pd.Series(np.exp(np.cumsum(rng.normal(0, .01, len(idx)))), index=idx)
        full = guards(benchmark)
        for end in (180, 250, 400):
            prefix = guards(benchmark.iloc[:end])
            for name in full:
                pd.testing.assert_series_equal(full[name].iloc[:end], prefix[name])

    def test_exit_day_return_is_not_lost(self):
        dates = pd.bdate_range('2022-01-03', periods=4)
        prices = pd.DataFrame({'STOCK': [100., 100., 90., 90.]}, index=dates)
        strategy = IndividualMomentumStrategy(prices, prices * 1000, opens_df=prices,
                                              use_trailing=False, atr_multiplier=2)
        strategy.positions = pd.DataFrame({'STOCK': [1.]}, index=dates[:1])
        strategy._research_guard = pd.Series([False, False, True, False], index=dates)
        with contextlib.redirect_stdout(io.StringIO()):
            result = research_engine()(strategy, transaction_cost=0, risk_free_rate=0,
                                       hard_stop_from_entry_pct=.9,
                                       hard_stop_from_peak_pct=.9)
        self.assertAlmostEqual(result['net_returns'].iloc[2], -.1)
        self.assertEqual(result['executed_weights'].iloc[2, 0], 0.)


if __name__ == '__main__':
    unittest.main()
