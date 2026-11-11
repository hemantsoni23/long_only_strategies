# Are Options on Index Futures Profitable for Risk Averse Investors? Empirical Evidence

**George M. Constantinides, Michal Czerwonko, Jens Carsten Jackwerth, Stylianos Perrakis · 2010 (draft of July 21, 2010, "Journal of Finance forthcoming", SSRN 1106962, with Internet Appendix) · Source file `Finance/AbnormalReturns_Constanides_2010.pdf` · CME time-stamped quotes on 30-day American options on S&P 500 futures, Feb 1983–Jul 2006 (247 monthly dates); daily index returns 1928–1983 for the return distribution**

## Claim / contribution

Options whose **bid exceeds the Constantinides–Perrakis (2007) stochastic-dominance upper bound** ("good sells") can be written profitably by any risk-averse investor holding the index and cash: out of sample, net of index transaction costs and option bid–ask spreads, with a one-quote delay and early exercise, the option trader's (OT) return **second-order stochastically dominates (SSD)** the index trader's (IT) return. Call upper-bound violations are frequent; put upper-bound and call/put lower-bound violations are too rare for inference. The novelty vs. Constantinides–Jackwerth–Perrakis (2009, European options) is that bound violations are only *signals*; the dominance claim rests on a nonparametric out-of-sample SSD test of realized returns, so misspecification of the bounds makes it conservative rather than invalid.

## Theory (Section I)

Incomplete market, heterogeneous agents; a class of "traders" with increasing concave, state-independent utility over terminal wealth invests in a bond (return $R$) and the index (i.i.d. total return with mean $R_S$, deterministic dividend yield $\gamma$), paying proportional cost $k$ on index trades (options' costs are in their bid/ask). Futures follow cost of carry with bounded, independent basis risk: $F_t=(1+\gamma)^{-(T_F-t)}R^{T_F-t}S_t+\epsilon_t$, $|\epsilon_t|\le\bar\epsilon$. IT starts with $(x_0,y_0)$ in bonds/stock; OT additionally writes one American futures call for proceeds $C$, cannot retrade it, and pays $F_t-K$ from cash if assigned. The **reservation write price** solves $V^{OT}_0(x_0+C,y_0)=V^{IT}_0(x_0,y_0)$; its upper bound, independent of utility, endowment and the holder's exercise policy, is

$$
\bar C(F_t,S_t,t)=\frac{1+k}{1-k}\max\big[N(S_t,t),\,F_t-K\big],
$$

$$
N(S,t)=R_S^{-1}\,E\Big[\max\big\{(1+\gamma)^{-(T_F-t-1)}R^{T_F-t-1}S_{t+1}+\epsilon_{t+1}-K,\;N(S_{t+1},t+1)\big\}\,\Big|\,S_t=S\Big],\quad N(S,T)=0 .
$$

Note the discounting at the **expected index return $R_S$** under the physical distribution, not at $R$. Index costs enter only via $(1+k)/(1-k)$ (≈ 1.01 for $k=0.5\%$) because both traders follow IT's low-turnover policy. With costless futures trading, a put upper bound follows: $\bar P=\bar C-R^{-(T-t)}F_t+K$. Lower bounds exist (CP 2007) but are rarely violated.

## Data and implementation (Section II, Appendices A–B)

- CME tapes: one-month quarterly and serial options (serials start Aug 1987, so the first 19 periods are quarterly); one 40-day period for Oct 1987 to include the crash. 36,921 raw call and 42,881 raw put quotes → 29,822 calls and 30,281 puts after filters (bid ≥ \$0.15, ask ≥ \$0.25; calls $K/F\in[0.96,1.08]$, puts $[0.92,1.04]$; futures quote matched within 15 s; CME flagging rules lose some quotes). Minimum quote size 20 contracts. Index inferred from futures via cost of carry; 3-month T-bill (H.15).
- Return distribution: 1928–1983 daily log returns, shifted so the mean is **4% + T-bill** (not estimated). Volatility by four observable methods; 3rd–4th moments from the preceding 90 days. Table I (volatility prediction error, mean / s.d.):

| Mode | Mean error | St. dev. |
|---|---:|---:|
| Unconditional (1928–83) | 0.0429 | 0.0680 |
| 90-day historical | 0.0095 | 0.0595 |
| ATM IV of previous day, bias-adjusted (~3%) | −0.0005 | 0.0496 |
| EGARCH(1,1), 1928–83 coefficients | 0.0177 | 0.0531 |

  Adjusted IV is best, 90-day second. (The adjusted-IV run loses the first 21 dates → 226 months.)
- Each month a $T$-step (trading days to expiry) recombining lattice with $m$ branches is fitted: equal log-spaced histogram states, affine transform $(a,b)$ and right-tail probability tilt $c$ to match mean, variance and skewness exactly; kurtosis matched by searching $m\le201$ (median relative error 0.003%, max 1.659% over 973 fits). Bounds via backward induction.
- Basis-risk bound $\bar\epsilon=0.5\%$ of the index (95% of 1990–2002 observations).
- **IT policy:** Constantinides (1986)/Perrakis–Czerwonko (2006) no-trade band for $k=0.5\%$, $\sigma=0.1856$, premium 4%, CRRA 2: $y/x\in[1.2026,1.5259]$; each month starts at $y_0=100{,}000$, $x_0=73{,}300$ ($y/x=1.3642$). **OT** uses the same (for it suboptimal) stock policy; if $n$ strikes violate, OT writes $1/n$ call at each (one call in total per index unit) and banks the bids. For put writes OT also sells one future (synthetic short call). Early exercise by the counterparty is modelled with the forward-looking distribution.
- **Tests** on 247 annualized arithmetic monthly returns (all months, including no-trade months where OT = IT). SSD: $D^2_{IT}(z)-D^2_{OT}(z)\ge0$ for all $z$, $D^2_J(z)=\int_{\underline z}^{z}(z-x)\,dF_J(x)$. DD(2000): $H_0$: IT ⪰₂ OT and $H_0$: OT ⪰₂ IT, max/min t-statistics over 20 grid points vs. Stoline–Ury studentized maximum modulus tables. DD(2006): $H_0$: OT does *not* dominate IT vs. $H_A$: OT ⪰₂ IT, restricted-interval min-t with 999 empirical-likelihood bootstrap draws; always 10% left-tail trim, right trim 0/5/10%. First-order serial correlation of returns −0.0267 to 0.0964 (insignificant).

## Pattern of violations (Tables II–IV)

Call bid violations of the upper bound, % of quotes within each $K/F$ bucket:

| Vol. mode | 0.96–0.99 | 0.99–1.01 | 1.01–1.03 | 1.03–1.08 | % of all quotes | Months with violations |
|---|---:|---:|---:|---:|---:|---:|
| Unconditional | 3.3 | 5.8 | 8.6 | 20.6 | 9.4 | 43 / 247 |
| 90-day | 4.8 | 16.1 | 32.2 | 45.4 | 26.9 | 100 / 247 |
| Adjusted IV | 4.1 | 15.2 | 30.5 | 30.3 | 23.7 | 120 / 226 |
| EGARCH | 2.3 | 6.5 | 14.1 | 24.3 | 12.5 | 65 / 247 |

Highest violation *rate* in OTM calls (1.03–1.08); largest *number* in 1.01–1.03, with most violations in the liquid 0.99–1.03 range. Average violation size 5% to 56% of the bound moving from 0.96–0.99 to 1.03–1.08. Violations occur after large index declines when IV is high (Fig. 2); across all four modes they are more frequent when the Baa–Aaa spread, futures open interest and momentum (index / 1-year average) are in the top tercile; other characteristics give mode-dependent patterns. Call upper bound is tighter than the put upper bound (Fig. 1).

## Main results (Table V, one call per index unit)

| Vol. mode | Months | $\hat\mu_{OT}-\hat\mu_{IT}$ (ann.) | DD(2000) p, $H_0$: IT ⪰₂ OT | DD(2006) p, $H_0$: OT ⋡ IT: right trim 0% / 5% / 10% |
|---|---:|---:|---:|---|
| **Call upper bound** | | | | |
| Unconditional | 43 | 0.0031 | <0.01 | 0.244 / 0.024 / 0.000 |
| 90-day | 100 | 0.0043 | <0.01 | 0.166 / 0.007 / 0.002 |
| Adjusted IV | 120 | 0.0066* | <0.01 | 0.119 / 0.029 / 0.000 |
| EGARCH | 65 | 0.0062** | <0.01 | 0.079 / 0.000 / 0.000 |
| **Put upper bound** | | | | |
| Unconditional | 23 | 0.0009 | >0.1 | 0.399 / 0.203 / 0.154 |
| 90-day | 16 | −0.0008 | >0.1 | 1 / 1 / 1 |
| Adjusted IV / EGARCH | 4 / 9 | n/a | | |

(* / ** = mean difference significant at 5% / 1%, one-sided bootstrap, 9,999 draws.) DD(2000) never rejects OT ⪰₂ IT (p > 10%); DD(2006) for IT ⋡ OT gives p = 1. So for calls: OT dominance not rejected, IT dominance rejected, and non-dominance of OT rejected once the right tail is trimmed.

Economic size: the portfolio gains (0.31–0.66% p.a.) are diluted because the call is small relative to the portfolio and because no-trade months count as zero (reported gain = $xn/(n+m)$; violation months are < half the sample, so the conditional gain is > 2×). The selected calls themselves earn **12.3–43.2% per month** to the writer at the bid (significant for 3 of 4 modes), vs. **7.7%** (insignificant) for writing *all* calls at the bid. SSD survives until written-call prices are artificially cut by 10–15%. Restricting to OTM good sells changes little. Short straddles/strangles triggered by call violations (Internet App. D) also dominate (e.g. adjusted IV straddles+strangles: +2.35% p.a., DD(2006) p = 0.020/0.023/0.025) — consistent with overpriced puts, found only indirectly.

## Robustness (Section IV, Internet Appendix)

| Variation | Result (calls) |
|---|---|
| IT holds CRSP VW, MSCI, 60% S&P + 40% REIT, 60/20/20 S&P/HML/SMB, 60/40 S&P/bonds, 60/40 S&P/commodities (Table VI) | OT still dominates; weaker with HML/SMB and commodities at 5% trim (e.g. uncond. 0.126, 0.106), significant at 10% trim |
| 1.5 calls per index unit (Table VII) | gains 0.46–0.99% p.a., dominance holds |
| 2 calls per index unit | gains 0.62–1.32% p.a., dominance holds (5%-trim p 0.031–0.125) |
| 3 calls per index unit | gains 0.93–1.98% p.a., but DD(2000) no longer rejects IT ⪰₂ OT and DD(2006) p ≥ 0.12 → no dominance |
| Buy-and-hold 50% S&P (Table VIII) | virtually identical to Table V |
| CRRA 10 rebalancing (Table F) | SSD tests similar; mean gains shrink to 0.06–0.13% p.a. |
| Start at either band boundary; open option positions in IT (Table E) | unchanged |
| $\bar\epsilon=0$ (Table G) | more violation months (67–195); calls still dominate at 10% trim (adj. IV 0.076 weakest); put writes negative/insignificant |
| Premium 2% or 6% (Table H) | call results as strong as Table V |
| Excluding Oct 1987–Apr 1988 | essentially unchanged |
| Violating calls restricted to $K/F<1.04$, $<1.03$, $<1.02$ (Table I) | 5%-trim p up to 0.094 for $K/F<1.02$; 10%-trim p ≤ 0.004 |

**Alternative rules (Tables IX–X).** Naively writing *all* calls every month: gain 0.60% p.a., DD(2006) p 0.207/0.093/0.007 — weakly supportive; writing all puts: 0.78% p.a. but p 0.280/0.186/0.060; buying calls/puts loses (−4.03%, −2.92% p.a.). Writing only the top 10% or 2.5% most expensive calls by price percentile does not strengthen the result (fewer trades). Bernardo–Ledoit (2000) gain–loss bounds: upper bound with ratio 2 gives results similar to CP; with ratio 4, dominance only for 90-day vol and negative gains for two modes; lower-bound ("good buy") trades are "disastrous" (e.g. −2.48% p.a. unconditional, ratio 2). The authors summarize the naïve rules as working in only one of four cases (writing calls).

## Critical assessment

- **Convincing:** clean long CME tape including 1987, 1998 and 2000–02; realistic frictions (bid prices, index costs, early exercise, one-quote delay); fully out-of-sample bound computation; a preference-free criterion; many robustness checks all pointing the same way for calls.
- **Caveats the summary reader should weigh:**
  - The authors' own simulations (Internet App. C) show **DD(2000) is uninformative here**: with 250 months it rejects IT ⪰₂ OT with probability 1 even when calls are written at fair Black–Scholes prices (Table C1), and rarely rejects OT ⪰₂ IT when it is false (Table C2). The evidence therefore rests on DD(2006).
  - **DD(2006) with right-tail trimming is over-sized for OTM calls** in samples of 250: false-rejection rates at nominal 5% with 5% trimming are 0.106 at $K/S=1.04$ and 0.365 at 1.08; with 10% trimming 0.195–0.366 for $K/S\ge1.02$ (Tables C4–C5). Since violations concentrate at $K/F$ 1.01–1.08 and many headline p-values rely on 10% trimming, the paper's claim that the test is "if anything conservative" holds for power, not size. The $K/F<1.02$ restriction (Table I) leaves 5%-trim p-values of 0.008–0.094 — supportive but weaker.
  - Economic magnitudes at portfolio level are small (0.3–0.7% p.a.); the naïve write-all-calls rule earns a similar mean gain (0.60%) with weaker SSD evidence, so the incremental value of the CP filter lies mostly in dominance/risk shape, not mean return.
  - The mean is imposed (4% + T-bill) and the IV adjustment uses prior prediction errors; the OT is limited to ≤ 1 call per index unit by the theory (bounds are not valid beyond that), and to one month of maturity.
  - Minor inconsistencies: Table H labels Panel A as 2% premium while the text calls Panel A the 6% case; Table F (CRRA 10) mean gains are much smaller than Table V although the text calls the results "virtually identical" (true for the SSD tests only).
- **Interpretation offered:** segmented markets — funds buy OTM puts as insurance, speculators buy OTM calls as leveraged bets, dealers inflate prices (Gârleanu–Pedersen–Poteshman 2009); large arbitrageurs are held back by margins and depth (Santa-Clara–Saretto 2009), so small writers can profit without eliminating the overpricing.

## Practical relevance for a quant PM

- A **covered-call overlay with a pricing filter**: compute each month a physical-measure lattice (mean = rf + assumed premium, vol from bias-adjusted ATM IV, 90-day skew/kurtosis), derive the CP call bound, and write (at most one call per index unit, spread across violating strikes) only when bids exceed it. Signals cluster after sell-offs and in high-credit-spread, high-open-interest states — exactly when margin and gap risk are highest.
- The SSD framing is the right yardstick for option overlays (non-normal, asymmetric payoffs): mean-variance or Sharpe comparisons can mis-rank them. The DD(2006) machinery with paired trimming is reusable, but check size by simulation at the relevant moneyness before trusting trimmed p-values.
- Scaling: evidence holds up to 2 calls per index unit and fails at 3; capacity is limited by the frequency of violations (43–120 of ~247 months) and by liquidity away from ATM.
- Put-selling "because puts are expensive" is not validated directly by the CP put bound (too few violations); evidence for rich puts comes only from call-triggered straddles/strangles.
