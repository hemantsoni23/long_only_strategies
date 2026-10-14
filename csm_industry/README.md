# csm_industry - D1v industry-led staggered book (research-grade strategy class)

`industry_book_strategy.py::CSMIndustryBook` is a self-contained implementation (no imports from factor_research or Old_live_strategies) of the pre-registered D1v book
(`factor_research/INDUSTRY_BOOK_PREREG.md`, FINDINGS sections 8.3-8.8): top-8 positive-trend Industry_clean baskets (3m, >=10 live U1 members), 2 stocks each by the Zenith composite z(A1)+z(Q5_189) from the SMA200 pool (score="a1" available; Zenith score is the frozen default),
6 overlapping monthly tranches, 0.5x gate below the EW-index SMA200, 15% vol-target overlay, 6.5% on idle cash, 0.3%/side, no stops.

* `python3 test_parity.py` - proves it reproduces the research simulator exactly (cohort weights and daily net returns, max abs diff 0): Zenith score: CAGR 21.19%, Sharpe 1.55, MaxDD -22.24% (whole curve incl. build-up; 20.6% / 1.50 on the fully-built window); A1 score: 19.34% / 1.43 / -23.29% (2005-26, simulator accounting).
* `CSMIndustryBook(...).live_orders()` - target weights, vol scale, cash weight and selected industries for the newest signal row (month-end run; fill next-day close).
* NOT yet: stops/exit rules of the live engines, execution-replay through `csm_value/execution_replay.py`, forward paper-trading (>= 6 monthly cohorts), gold/silver overlay.
Numbers are simulator accounting; plan on ~14-17% CAGR after survivorship / hindsight haircuts (FINDINGS 8.7).
