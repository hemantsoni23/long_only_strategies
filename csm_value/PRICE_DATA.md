# CSM Value: price and fundamentals inputs

CSM Value's primary factor is earnings yield: trailing profit divided by market
capitalisation. To calculate historical market capitalisation, the share count
from a filing and the historical price must use the same share units. A 2-for-1
split or 1:1 bonus, for example, halves the price per share and doubles the
number of shares without halving the company's market value. A current
split-adjusted chart price multiplied by an old filed share count can make the
old market cap appear half as large and the earnings yield twice as large.

The strategy uses:

1. `../fundamentals/` by default (including `sme/`; override with
   `CSM_FUNDAMENTALS_DIR`) for financial filings and filed share counts,
   subject to the next-day availability rule.
2. `/Users/hemantsoni/Documents/upstox_data_folder/ohlcv_data/` for price
   signals, universe filters, benchmark, stops and trade-price modelling.
3. `data/nse_monthly_prices.csv` for historical as-traded NSE closes at each
   month-end signal date and reporting-period end. These replace the separate
   user-supplied price-folder requirement for the normal runner.

The monthly data was obtained from NSE's [historical reports and bhavcopy
archives](https://www.nseindia.com/static/resources/historical-reports-capital-market-daily-monthly-archives).
The archived file reports `date, symbol, series, close`. Rows with ambiguous
multiple eligible trading series are excluded. Names are matched by symbol;
there is no complete historical security-master or delisting coverage.

The price files in `data/` are generated data and ignored by Git. To refresh
or recreate the local CSV, run:

```bash
python3 csm_value/fetch_nse_monthly_prices.py
python3 csm_value/run_csm_value_backtest.py
```

The downloader derives month-end trading dates from the existing OHLCV files;
it fetches NSE's archived daily reports only for those dates. Network access
to NSE is required for this separate refresh, not for a normal backtest using
the existing CSV. A failed or missing archive prevents creation of a partial
replacement file. `CSM_UNADJUSTED_PRICE_DIR` remains an optional override for a
verified directory of as-traded daily CSVs; it is not needed with the NSE data.

To catch a possible split or bonus between the financial period end and the
signal date, the strategy compares the NSE-to-Upstox price ratio at both dates
and checks for split-like daily price cliffs. It excludes a stock if the
reference price is absent or the units appear to change. A uniform future
adjustment affects both ratios equally and cancels in their comparison. This is
still a conservative data-quality check, not a complete corporate-action or
security-identity database. Intraday or reversals that leave no detectable
change may be missed; legitimate big price moves can also be excluded.

The report prints the existing 2019-06 to 2021-12 IS and 2022-onward OOS
periods separately. The OOS window has been inspected previously and is not a
blind holdout; the dates are retained for comparability, not newly selected.
The normal runner currently ends on 31 December 2024 at the user's request.

The current engine uses next-session open execution for a monthly signal and
next-session open exits for close-confirmed stops. As requested, its Elendel
accounting convention gives an exited position zero weight on the exit day.
This is a weight-based convention rather than an independently reconciled
cash/share ledger. Opening-auction availability, circuit limits, market impact and
historical filing revisions are not fully reconstructed. The original
Elendel files remain unchanged. Do not treat prior output or the previously
researched 2019–2025 split as a fresh, untouched OOS validation.

The strategy does not rank or restrict the universe by price times volume. The
existing minimum-price, circuit-day and falling-knife gates remain. `top_n`
limits both target selection and actual simultaneously held positions; buffered
exits continue to occupy a slot. The default is 10 positions, selected by
in-sample Calmar; the existing 5% cap per stock remains. To choose another
limit, run `python3 csm_value/run_csm_value_backtest.py --max-positions 15`.
