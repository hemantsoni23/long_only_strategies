import importlib.util
from pathlib import Path
from types import SimpleNamespace
import unittest

import numpy as np
import pandas as pd

spec=importlib.util.spec_from_file_location('live_research_study',Path(__file__).with_name('study.py'))
study=importlib.util.module_from_spec(spec)
spec.loader.exec_module(study)


class LiveSignalTest(unittest.TestCase):
    def test_later_prices_do_not_change_prior_live_strategy_signals(self):
        dates=pd.bdate_range('2018-01-01','2021-02-26')
        t=np.arange(len(dates),dtype=float)
        prices=pd.DataFrame({'A':100+t*.1,'B':100+t*.08,'C':100+t*.06},index=dates)
        labels=prices.resample('ME').last().index
        results=pd.DataFrame({'symbol':['A'],'filed':[pd.Timestamp('2020-01-15')],
                              'oneoff_share':[.2],'sg_np':[.3]})
        def calculate(close):
            s=SimpleNamespace(prices=close,highs=close*1.01,factors=pd.DataFrame(1.,index=labels,columns=close.columns),
                benchmark=pd.Series(1+t*.0001,index=dates),_results_in=results,results_max_age_days=140)
            return study.calc_signals(s)
        orig=calculate(prices);later=prices.copy();later.loc['2021-01-01':]*=3
        changed=calculate(later)
        for name in orig:
            pd.testing.assert_frame_equal(orig[name].loc[:'2020-12-31'],changed[name].loc[:'2020-12-31'])

    def test_blended_score_keeps_fundamental_eligibility_and_neutral_missing(self):
        idx=[pd.Timestamp('2020-12-31')]
        base=pd.DataFrame([[1.,2.,np.nan]],index=idx,columns=list('ABC'))
        a3=pd.DataFrame([[np.nan,0.9,1.0]],index=idx,columns=list('ABC'))
        result=study.rank_value(base,{'a3':a3},'value_a3')
        self.assertAlmostEqual(result.loc[idx[0],'A'],.75*.5+.25*.5)
        self.assertTrue(pd.isna(result.loc[idx[0],'C']))


if __name__=='__main__':unittest.main()
