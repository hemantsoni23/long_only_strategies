# Fundamentals and OHLCV research rules

These rules govern future research that combines the fundamentals in
`fundamentals_data/` (including `fundamentals_data/sme/`) with daily OHLCV in
`/Users/hemantsoni/Documents/upstox_data_folder/ohlcv_data/`. The objective is
to investigate whether fundamentals-led strategies can improve CAGR and reduce
drawdown; neither outcome is assumed in advance.

## 1. Information availability

- A financial result may be used only **after** its public filing date, never on
  that calendar date. Use the filing date, not the financial period end. For
  example, a result filed on 2 November 2025 is eligible from 3 November 2025;
  if there is no trading session on the eligibility date, the first possible
  use is the next trading session. The strategy's signal and execution rules
  still determine when a trade can actually be made.
- Apply the same next-calendar-day rule to shareholding data using its own
  submission date. Do not assume that shareholding and financial results for
  the same reporting period became public at the same time.
- If a reliable public filing or submission date is missing, do not use that
  observation until its availability can be established. Preserve timestamps,
  including seconds, when parsing, even though the rule excludes the entire
  filing date regardless of the time of day.
- Build every signal from observations already eligible on the signal date.
  Older results, revisions, and changes of reporting basis must not introduce
  information that became public later. The snapshot data may not preserve all
  original filings and revisions; disclose this limitation and exclude or
  separately investigate observations whose history cannot be established.

## 2. Universe

- Start with stocks that have both fundamentals and OHLCV data, including SME
  files. Match symbols carefully and investigate aliases or changes rather than
  assuming every filename match proves security identity.
- At each signal date, use only stocks with sufficient **then-available** data
  for the particular signal and with the OHLCV data required by the strategy.
  Having a JSON file today does not make its future filings available in the
  past. For CSM Value, do not impose a price-times-volume ranking cutoff; its
  other price, circuit-day, and falling-knife eligibility gates remain.
- Current file membership may exclude delisted, renamed or otherwise missing
  stocks. Measure and report this survivorship and mapping limitation; a
  restricted current-file universe is not automatically a point-in-time
  historical universe.

## 3. Signal design and strategy mechanics

- Fundamentals are the primary source of the strategy's main logic or ranking.
  OHLCV is also used for secondary factors or signals, not just trade prices.
  State which input plays each role before testing.
- Preserve the applicable existing OHLCV strategy's flow, signal schedule,
  order of operations, buy and sell timing, and execution assumptions when
  adapting it. Record the specific baseline and any intentional differences
  before running a comparison; do not silently change its mechanics.
- Compare against the selected OHLCV baseline on the same eligible universe,
  dates, execution and cost assumptions so the contribution of fundamentals is
  interpretable. Also disclose how the restricted universe differs from the
  baseline's original universe.
- For CSM Value, use the user-requested Elendel booking convention: an exited
  position has zero weight on its exit day. Disclose this convention, costs,
  and other trading assumptions when reporting results.

## 4. In-sample and out-of-sample testing

- Divide the available fundamentals history chronologically into an
  **in-sample (IS)** development period and an **out-of-sample (OOS)** test
  period. Choose and document the boundaries before testing; none are fixed by
  this document. Observe the public-availability rule in both periods.
- Develop, select and freeze the rules and parameters using IS data. Evaluate
  the frozen strategy on OOS data without using OOS performance to select or
  tune it. If OOS results drive changes, that period is no longer a clean
  holdout for the revised strategy; disclose this and use a new untouched
  period where available.
- History before the OOS boundary may be used to warm up indicators if it was
  already available then; it must not be used to count OOS returns before the
  test begins. Avoid future data in training, rolling calculations, universe
  membership and parameter selection.
- Report IS and OOS results separately, including CAGR, maximum drawdown,
  turnover, costs and coverage, together with the comparable baseline. The
  available history is short and has already informed earlier research, so do
  not call a period genuinely untouched without checking that history.

## 5. Fundamental-data interpretation

- Use actual period start and end dates, reporting-period type and reporting
  basis. An SME result labelled Q2 or Q4 can cover six months; do not treat it
  automatically as a single quarter or sum overlapping periods. Cash-flow
  figures may be cumulative rather than quarterly.
- Keep standalone and consolidated figures, accounting definitions and units
  consistent in a calculation. Account for missing fields, sector-specific
  taxonomies and stale data; do not silently substitute zero for missing facts.
- Reconcile share counts and per-share measures with the price series' split
  and bonus adjustment convention before computing valuation or growth. Audit
  fiscal-year labels, duplicates, filing revisions and abnormal values.

These are research rules, not a selected strategy or a claim of investment
performance. Additional strategy-specific choices should be documented before
running the corresponding experiment.
