# Crestline signal-over-time and holding-period diagnostics - definitions (written 2026-10-12 BEFORE any number was computed)

Subject: the core score of `crestline_v2_4.py` = z(close/252d high) + z(share of last 189 days above SMA50), computed on the strategy's own ranking pool (price floor, liquidity rank 1-1000, circuit filter, stale filter), back-adjusted prices, 2006-03 .. 2025-12.
Signals on a 5-bar grid (993 dates). Forward return = open of the next bar -> close h bars later (the strategy's fill convention), gross of cost; delisted names stay flat at the last price.
Horizons h = 5, 10, 20, 40, 60, 90, 120, 180, 252 bars. IC = Spearman(score, fwd return) across the pool at each date; ICIR = mean IC / std IC; hit = share of dates with IC > 0;
t = Newey-West HAC t of the mean IC with lag = ceil(h/5) (overlapping returns). Also each leg alone (HP, TP) and the top-25 / top-decile payoff versus the pool mean (excess return, HAC t).

## Windows
* Non-overlapping 3-year blocks by signal date: 2006-03..2008, 2009-11, 2012-14, 2015-17, 2018-20, 2021-23, 2024-25 (partial; long horizons truncated by the end of data).
* Rolling 3-year windows starting each 1 Jan 2006..2022.

## Verdict rule for "the core idea works over time" (fixed now, on h = 60 and h = 120)
* WORKING in a block: mean IC > 0 and HAC t >= 2.0 at that horizon.
* WEAK: mean IC > 0 but t < 2.0.  BROKEN: mean IC <= 0.
* Overall verdict: WORKING over time if >= 6 of the 7 blocks are WORKING at h=120 AND >= 5 of 7 at h=60, with no BROKEN block; DECAYING if the mean IC of the last two full blocks (2018-20, 2021-23) is < 50% of the mean of the first two (2006-08, 2009-11) at either horizon; otherwise MIXED. Both labels can apply and will be reported.
* A 3-year block holds ~150 grid dates but only ~3 independent 120-bar returns per year, so t-stats are the honest yardstick and are reported next to every IC.

## Holding-period diagnostics (v2.4 trade logs, all six schedule anchors pooled; cash 6.5%)
1. Holding-time distribution (trading days) by exit reason; share of trades shorter than 20/40/60/120 trading days; capital-weighted average hold.
2. Counterfactual: for the same entries, return from the entry open to close at +20/60/120 bars with no stops (cost 0.6% round trip) versus the realised net return; realised return per held day versus counterfactual.
3. Post-exit drift by exit reason: return from the exit open to +20/60/120 bars minus the pool-mean return over the same bars (excess), mean/median/% positive.
4. Winner capture: entries whose no-stop 120-bar return exceeds +30% ("big winners"): share stopped out before day 60, average realised vs counterfactual; realised/MFE ratio for trades with MFE >= 30%.
5. Signal state at exit: rank of the stopped name at the latest grid date before the exit; share of stop exits still ranked <= 25 and <= 50, and their post-exit excess versus names no longer ranked.
6. Pure-signal hold-H portfolios (no stops): top-25 equal weight, K = H/20 staggered sub-portfolios, 0.3% per side, fully invested vs. bear-gated (cash at 6.5% when the benchmark is below its SMA200 at formation), H in {20,40,60,90,120,180,252}: CAGR, vol, Sharpe vs 6.5%, MaxDD - compared with the actual stop-based strategy. This isolates what the signal earns when held to its horizon.

No parameter is tuned here and nothing is adopted; this is diagnosis. Any strategy change that follows needs its own pre-registration.

## Definition fix logged before running Part 2 (not a tuning choice)
Item 6 horizons were written as {20,40,60,90,120,180,252}. Staggered K = H/20 sub-portfolios need H to be a multiple of 20 bars, so 90 -> 100 and 252 -> 240. Everything else as written.
