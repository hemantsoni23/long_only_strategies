import importlib.util
from pathlib import Path
from types import SimpleNamespace
import unittest

import numpy as np
import pandas as pd

spec=importlib.util.spec_from_file_location('validation_research',Path(__file__).with_name('validate.py'))
research=importlib.util.module_from_spec(spec);spec.loader.exec_module(research)


class ValidationTest(unittest.TestCase):
    def test_identical_return_streams_have_zero_bootstrap_difference(self):
        r=np.linspace(-.002,.003,252)
        b=research.bootstrap(r,r,n=20,block=21,seed=1)
        np.testing.assert_allclose(b['cagr_delta_percentiles_2_5_50_97_5'],0,atol=1e-12)
        np.testing.assert_allclose(b['drawdown_delta_percentiles_2_5_50_97_5'],0,atol=1e-12)

    def test_absolute_signal_gate_has_no_future_dependency(self):
        dates=pd.bdate_range('2019-01-01','2022-03-31')
        prices=pd.DataFrame({'A':100+np.arange(len(dates))*.1},index=dates)
        first=research.signal_absolute(SimpleNamespace(prices=prices))
        changed=prices.copy();changed.loc['2022-01-01':]*=3
        second=research.signal_absolute(SimpleNamespace(prices=changed))
        pd.testing.assert_frame_equal(first.loc[:'2021-12-31'],second.loc[:'2021-12-31'])


if __name__=='__main__':unittest.main()
