# Characteristics of Risk and Return in Risk Arbitrage — Mitchell & Pulvino (2000) — Detailed Quantitative Research Notes

**Mark Mitchell** (HBS), **Todd Pulvino** (Kellogg) · Manuscript October 2000, forthcoming *Journal of Finance* · Source file: `Finance/riskrbitrage_mitchellpulvino.pdf`

---

## Question

Prior studies report enormous merger-arbitrage returns: >100% annualized for cash tenders (Dukes et al. 1992; Jindra–Walkling 1999), 26% with beta 0.39 for Canadian 1997 deals (Karolyi–Shannon), ~12.5% excess for U.S. deals 1978–1996 (Baker–Savasoglu). Three candidate explanations: (1) genuine inefficiency; (2) transaction costs and practical limits (including the event-time annualization artifact — e.g. a 9.5% three-day gain on Zycon annualizes to 1,903%); (3) compensation for a non-linear, crash-state risk that linear models mismeasure. The paper separates (2) and (3) with calendar-time portfolios.

## Data and construction

- All CRSP firms delisted for mergers 1963–1998 plus unsuccessful bids reported in DJNS/WSJ: 9,026 transactions; terms hand-collected from news. Restricted to 100% cash (mergers and tenders) and simple stock swaps: **4,750 deals**. Excluded complex deals do not differ significantly on premium, failure probability, size, etc.
- Table I: **73% of deals are cash** (not a success rate); mean duration 59.3 trading days (39.2 for failures, 64.2 for successes); mean target equity \$391M, acquirer \$1.55B. Cash share rises sharply from the late 1970s (82–94% in the 1980s) and falls in the 1990s (41–62%).
- Positions open at the close of the day after announcement (excludes the takeover premium) and close at delisting or the day after failure is announced. Revised bids and competing bidders are treated as new transactions. Stock deals: long target, short $\Delta$ acquirer shares; short proceeds earn the risk-free rate (worth ~2%/yr; not available to most individuals).
- Figure 1: median spread of eventually failed deals stays wide (~15%) and jumps to >30% at termination; successful-deal spreads decline smoothly to zero — failure risk is largely priced.

**Two return series.**
- **VWRA:** target-value-weighted calendar-time average of all active deals, no costs, unlimited capital (comparable to prior studies; equal weighting gives 18.08%).
- **RAIM** (risk-arbitrage index manager): \$1M seeded in 1963, invests in every deal, no leverage, ≤10% of capital per deal, position sizes capped so that Breen–Hodrick–Korajczyk price impact is ≤5% on target and acquirer ($\Delta P/P=\beta\,NTO$, orders split into 10 trades), NYSE-regulated commissions before 1975 then \$0.10/\$0.05/\$0.04 per share. No attempt to pick deals.

## Results

### Aggregate performance (Table II, 1963–1998)

| Series | CAGR | Ann. SD | Monthly Sharpe |
|---|---|---|---|
| VWRA | 16.05% | 9.29% | 0.288 |
| RAIM | 10.64% | 7.74% | 0.161 |
| CRSP VW | 12.24% | 15.08% | 0.126 |
| T-bills | 6.22% | 0.73% | — |

The 5.41% VWRA–RAIM gap: ~1.5% direct costs, ~1.5% price impact, ~2.5% position-size limits from illiquidity. RAIM has only three losing years (1966 −4.03%, 1968 −2.88%, 1973 −7.45%); in 1974 it made 12.93% against a −27.86% market.

### Linear models (Table III)

| Sample | Series | α (monthly) | β_MKT | Adj. R² |
|---|---|---|---|---|
| All 432 months | RAIM CAPM | 0.0029** | 0.123*** | 0.057 |
| | RAIM FF3 | 0.0027* | 0.105*** (SMB 0.122**) | 0.076 |
| | VWRA CAPM | 0.0074*** | 0.054 | 0.006 |
| Mkt−rf < −3% (76 mo.) | RAIM CAPM | 0.0260*** | 0.507*** | 0.306 |
| | RAIM FF3 | 0.0206*** | 0.404*** | 0.396 |
| | VWRA CAPM | 0.0368*** | 0.519*** | 0.219 |
| Mkt−rf < −5% (35 mo.) | RAIM CAPM | 0.0232 | 0.483** | 0.222 |

CAPM alpha: 74 bp/mo (9.25%/yr) for VWRA vs 29 bp/mo (3.54%/yr) for RAIM. The positive SMB loading reflects long small targets / short large acquirers.

### Piecewise-linear market model (Table IV)

$$R_{RA}-r_f=(1-\delta)\left[\alpha_L+\beta_L(R_M-r_f)\right]+\delta\left[\alpha_H+\beta_H(R_M-r_f)\right],\qquad \delta=\mathbf 1\{R_M-r_f>\text{thr}\}$$
with continuity at the threshold; threshold −4% minimizes SSR.

| Sample | $\alpha_H$ | $\beta_L$ | $\beta_H$ | Adj. R² |
|---|---|---|---|---|
| RAIM 1963–98 | 0.0053*** | 0.492*** | 0.017 | 0.124 |
| VWRA 1963–98 | 0.0101*** | 0.476*** | −0.068 | 0.065 |
| RAIM 1963–79 | 0.0025 | 0.385*** | −0.021 | 0.044 |
| RAIM 1980–89 | 0.0095*** | 0.583*** | 0.099 | 0.233 |
| RAIM 1990–98 | 0.0054*** | 0.469*** | −0.029 | 0.127 |

Equality of up/down betas rejected at 0.001 (Jagannathan–Korajczyk test). In normal markets RAIM earns ~53 bp/mo over T-bills with zero beta; below −4% it behaves like half a unit of the market. The intercepts are put premia, not alphas.

### Mechanism: deal failure and form of payment

- **Probit (Table V, 4,740 deals)**, failure defined as a *negative arbitrage return* (so downward revisions that still close count as failures). Marginal effects: contemporaneous market −0.44 (**), lagged market −0.46 (***), two-month lag insignificant; a 5% market decline raises failure probability by ~2.25 pp. Hostile +12.9 pp (***), tender +6.5 pp, LBO +4.9 pp, cash +4.7 pp, log target size −1.5 pp; premium insignificant. Pseudo-R² 0.04 — failures are mostly idiosyncratic. Alternative: a 5% market drop raises the monthly fail/active ratio from 0.050 to 0.059 (+18%).
- **Cash vs stock (Table VI, 1975–98):** down-market beta **0.77** for cash deals vs **0.15** for stock deals (up-market betas 0.10 and −0.08). In a stock deal the short acquirer leg hedges the market, so a market fall does not make the acquirer overpay; in a cash deal the fixed cash price becomes too high after a crash and the acquirer walks. The crash exposure is therefore concentrated in cash deals — the opposite of the intuition that stock deals carry more market risk.
- **Deal flow** (number or value of announced deals) is not a robust return determinant.

### Sensitivity (Table VII, annual RAIM return; the kink survives every scenario, $\beta_L$ 0.43–0.58, $\beta_H\approx0$)

| Scenario | Return |
|---|---|
| Base (direct + indirect costs, 10% cap, \$1M) | 10.64% |
| Indirect costs only | 12.01% (direct costs ≈ 1.37%/yr) |
| No costs | 13.50% (impact ≈ 1.49%/yr; vs VWRA 16.05% ⇒ practical limits ≈ 2.5%) |
| Double price impact | 8.13% |
| No interest on short proceeds | 8.62% (−2.02%) |
| 20% / 5% per-deal cap | 10.05% / 9.15% |
| \$10M starting capital | 6.85% (−3.79%) |

Scale effects are exaggerated by thin 1960s deal flow, but point to capacity limits.

### Contingent-claims valuation

Replicate one month of \$100 in RAIM with a T-bill of face $100(1+r_f+\alpha_H)$ and a short position in $\beta_L=0.492$ one-month index puts struck at $100(1+\text{thr}+r_f)=\$96.51$ ($r_f$ = 51 bp/mo). With Black–Scholes, $\sigma=15\%$, $r=6.3\%$: put = \$0.40, replicating cost \$100.33 ⇒ **excess return 33 bp/mo ≈ 4.0%/yr**.

- Using actual S&P 500 put implied vols (1987–1996, ~4% OTM): **~29 bp/mo (3.5%/yr)** — lower because implied vol exceeds realized (post-1987 skew, cf. Jackwerth).
- Annual-horizon piecewise regression: beta 0.17 in both states, implied excess 3.6%/yr — the kink is a monthly phenomenon.
- **VWRA with the same method: 82 bp/mo (10.3%/yr), *higher* than its 9.25% CAPM alpha.** So non-linearity does not explain the large alphas of earlier studies; **transaction costs and practical limits do**. CAPM errors are small except where the kink is severe (e.g. cash deals in the 1980s, CAPM understates by ~1%/yr; stock deals in the 1990s overstate by 0.35%/yr).
- Without interest on short proceeds (individual investors) the excess return is ~2%/yr.

### Hedge funds (Tables VIII–IX, HFR merger-arbitrage index 1990–1998, net of fees)

- Same kink out of sample: HFR $\alpha_H=61$ bp, $\beta_L=0.60$, $\beta_H=0.10$ (adj. R² 0.46) vs RAIM over the same period 54 bp, 0.47, −0.03. Robust to thresholds of −3% and −5%. Active funds look like short a fraction of a put **and** long ~0.10 calls — plausibly from collar deals and leverage.
- Monthly correlation RAIM–HFR: 0.36 overall, **0.66 in down months, −0.02 in up months**; individual funds show the same split. Quarterly, the correlation is 0.38 even in up quarters. RAIM is a good benchmark for crash behavior and quarterly returns, not for monthly up-market noise.
- Proposed evaluation: three parameters from the piecewise regression — a superior manager has a lower down-beta, higher up-beta and higher intercept than RAIM.

## Assessment

**Convincing.**
- Deal-level calendar-time construction removes both hedge-fund database biases and the event-time annualization artifact that inflated earlier estimates.
- The kink is robust across subperiods, cost assumptions, position limits and in actual hedge-fund returns, and it has a clear mechanism (market-driven failures, concentrated in cash deals).
- The cost decomposition is concrete and matches practitioner intuition.

**Fragile or open.**
- The headline 4% depends on a calibrated price-impact model estimated on 1993–97 data and applied back to 1963, on the rebate assumption, and on Black–Scholes pricing of the put (the implied-vol version gives 3.5%).
- The threshold is chosen in-sample; $\beta_L$ is estimated from 76 months, a handful of which (1973–74, 1987, 1990, 1998) do the work.
- Failure defined as any negative return mixes breaks with renegotiations; the probit has little explanatory power (pseudo-R² 0.04).
- The residual 4% is attributed to liquidity provision in crashes but not tested against alternatives (funding constraints, limited arbitrage capital).
- Sample ends in 1998; post-2000 deal mix (more stock, collars, regulatory/antitrust risk) may shift the cash/stock exposure.

**For a quant PM/researcher.**
- Merger arb is roughly a zero-beta carry trade plus a short position in about half a one-month index put struck ~4% OTM. Low full-sample beta (≈0.1) and vol (≈8%) understate tail risk; stress-test with $\beta\approx0.5$ in sharp selloffs and for correlated breaks.
- The crash exposure sits in **cash** deals (down-beta 0.77); stock-for-stock with a properly sized acquirer short is close to market-neutral (0.15).
- Net-of-cost excess returns are single digits, sensitive to short rebates and capacity (\$10M vs \$1M start costs 3.8%/yr in the simulation).
- Evaluate managers against a piecewise or option-replicating benchmark, not CAPM alpha or Sharpe. Given the concave payoff, adding merger arb to other short-volatility sleeves concentrates crash risk.
