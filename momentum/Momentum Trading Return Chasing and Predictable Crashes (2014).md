# Momentum Trading, Return Chasing, and Predictable Crashes
**Authors:** Benjamin Chabot, Eric Ghysels, Ravi Jagannathan
**Year:** 2014
**Journal/Venue:** Federal Reserve Bank of Chicago Working Paper WP 2014-27 (SSRN 2539800)
**Source file:** Finance/Momentum_ChabotGhyselsJagannathan_2014.pdf

## Question

Momentum earns large alpha yet crashes periodically, and it did so in Victorian London (no hedge funds, no delegated quant money) as well as in the CRSP era. Are crash states predictable in both eras, is the predictability tied to how easily momentum traders can get capital (margin leverage then, return-chasing "blind capital" now), and why would skilled managers stay invested when crash risk is visibly high? The proposed answer: crashes are the limits-to-arbitrage mechanism that keeps the premium alive — they periodically destroy the capital that would otherwise arbitrage it away.

## Data and portfolios

- **London 1866–1907:** hand-collected closing bid/ask quotes for 1,808 equities (610,421 prices, 39,090 dividends) from *The Money Market Review* / Wetenhall's official list, filled from *The Economist*; dividends and shares from the *Investor's Monthly Manual*. Returns are 28-day (not monthly), capital calls treated as negative dividends; debt-like "stock", preference and debenture issues excluded. Shorting was cheap: fortnightly LSE settlement with contango/backwardation carry, and no capital-gains tax.
- **CRSP 1927–2012:** Fama–French UMD factor and an "FF7030" portfolio (value-weighted top three minus bottom three momentum deciles).
- London analogues are built the same way (2x3 size/prior-return sorts; 7030 decile portfolio).
- Because book equity is unavailable pre-1907, an alternative three-factor model uses market, a median-split size factor, and a dividend-yield HML (top 30% yielders minus non-payers). In CRSP it gives the same alpha as FF3, which validates it for London.

## Unconditional results (Table 1)

| | CRSP UMD | CRSP 7030 | London UMD | London 7030 |
|---|---|---|---|---|
| Mean (per period) | 0.69% | 0.55% | 0.30% | 0.27% |
| Std. dev. | 4.8% | 5.1% | 2.24% | 2.6% |
| Skewness | -3.03 | -2.89 | -1.55 | -1.39 |
| Ann. Sharpe | 0.50 | 0.37 | 0.48 | 0.37 |
| Alpha (alt. 3-factor) | 1.01% | 0.89% | 0.52% | 0.49% |

All alphas are significant at 1%. Momentum loads negatively on market (about -0.2 to -0.45) in both eras. Sharpe ratios are nearly identical across eras; the CRSP series is far more negatively skewed. The authors attribute this to delegated management adding run-type crash risk on top of the leverage-constraint risk that existed in both eras.

## Dating bull and bear markets (Table 2)

The Lunde–Timmermann (2004) algorithm runs on the cumulative momentum price. Symmetric thresholds switch bull to bear after a 5% (or 10%) fall from the running local maximum, and back after a 5% (10%) rise from the local minimum.

| | CRSP UMD | CRSP 7030 | London UMD | London 7030 |
|---|---|---|---|---|
| # bears, 5% | 63 | 68 | 19 | 21 |
| avg duration (months) | 3.7 | 4.9 | 7.3 | 7.9 |
| avg cumulative loss | 13.6% | 14.8% | 10.2% | 11.7% |
| # bears, 10% | 30 | 36 | 7 | 9 |
| avg cumulative loss | 20.6% | 21.6% | 15.8% | 16.9% |

A 5% momentum bear occurs roughly every 15–16 months in CRSP and every 25–28 months in London. London bears are rarer and shallower, though they last longer.

## Hazard model

The model is a continuous-time proportional hazard with Weibull baseline in bull-market age $t$, $h(t\mid X)=h_0(t)\exp(X_t'\beta)$ with $h_0(t)=\rho t^{\rho-1}$. It is discretized à la Prentice–Gloeckler (1978), giving a complementary log-log form for the probability that the bull market ends in month $t$:
$$
\Pr_t = 1-\exp\!\left\{-\exp(X_t'\beta)\,\big[t^{\rho}-(t-1)^{\rho}\big]\right\},
$$
estimated by ML over bull-market months at risk. Covariates are the risk-free rate $r_{f,t}$ and the cumulative momentum and market returns from $t-12$ to $t-1$. Bull-market age enters only through $\rho$. The estimated $\rho$ (about 0.85–1.10 in CRSP, 0.69–1.10 in London, with large SEs) is not distinguishable from 1, so there is essentially no duration dependence: bull markets do not "get old".

**Table 3, key coefficients (SEs):**

- **$RET^{mom}_{t-12\to t-1}$** is positive and significant in every specification in both eras. CRSP UMD: 2.50 (0.92) at 5%, 6.06 (1.39) at 10%. London UMD: 7.74 (1.97) at 5%, 9.26 (3.56) at 10%. This is the robust result: strong recent momentum raises crash odds.
- **$RET^{mkt}_{t-12\to t-1}$** has opposite signs across eras. In CRSP it is negative, about -1.6 to -2.0 and mostly significant, so the relevant state is momentum outperforming the market. In London it is positive and significant only for the 7030 portfolio (6.9 at 5%, 13.6 at 10%). The authors' story is that in CRSP a strong market makes momentum relatively less attractive to return-chasing flows (less crowding). In London a rising market should raise collateral values, which would cut forced-selling risk. The positive London sign therefore does not obviously fit the collateral story, and the paper's explanation here is loose.
- **$r_{f,t}$** is strongly negative in London (-57.6 (12.2) for UMD at 5%; -81.7 (26.0) for 7030 at 5%), so cheap margin credit predicts crashes. In CRSP it is insignificant, with estimates of both signs.
- **Fit:** in-sample AUC is 0.65–0.68 at the 5% threshold and 0.76–0.80 at 10% in CRSP, and 0.75–0.80 in London. A bootstrap from memoryless resampled returns (to correct in-sample AUC inflation above 0.5) rejects no predictability at 1% in all specifications. London estimates rest on only 6–20 bear events.

## Conditional returns (Table 4)

Bull-state months are sorted by past 1-year momentum return decile:

- In CRSP UMD, the one-month bull-to-bear transition probability is about 3–10% in deciles 1–9 and jumps to 24.1% in decile 10 (7030: 21.7%). The annualized Sharpe of staying invested falls to 0.23 in decile 10 (7030: 0.60), against roughly 0.6–1.7 elsewhere.
- Conditional on the bull persisting, however, next-month return is highest in decile 10 (3.9% vs 1.4–2.3%). That is the manager's dilemma: exiting avoids the crash (average -9.9% crash month in decile 10) but gives up the best bull-state returns.
- London shows only a mild top-decile effect (10.8–11.1% vs 0–11% in other deciles). The top-decile crash concentration is mainly a CRSP phenomenon.

## Managed-portfolio illustration

Define relative performance $RP_t=\sum_{s=t-K}^{t-1}(r^{mom}_s-r^{mkt}_s)$ with $K=36$, motivated by long-run reversal. Hold UMD when the percentile rank of $RP_t$ is below a threshold and hold T-bills otherwise. Always-invested UMD has Sharpe 0.66 over 1950–2012 and 0.45 over 1930–2012. Exiting above the 75th percentile gives 0.83 and 0.65. The paper does not say clearly whether percentile ranks are computed on an expanding window or the full sample, so look-ahead cannot be ruled out.

## Why managers stay in: model and simulation

**Two-period, two-manager game.** Skilled managers observe a hidden good/bad state; investors do not. The momentum gross return is $R_{up}>1$ or $R_{down}<1$, with $p_{UG}>p_{UB}$. Investors split $\$2$ equally in period 1. In period 2 they send all existing and new money to the best performer if momentum was up, and only $f<1$ of new savings if it was down. Fees are a share $\delta$ of profits, and $(R_{down}+f)R_{up}<1+f$ ensures a period-1 loss means zero fees.

In period 2 investing is always optimal. In period 1, with $R_{up}=1.02$, $R_{down}=0.75$, $p_{UG}=0.99$, $f=0.5$, $\delta=0.2$ and $\pi_{ij}=0.5$, the manager prefers momentum to cash in the bad state whenever $p_{UB}>0.426$. That means he stays in even with a crash probability up to about 57%. At a 10% bad-state crash probability all equilibrium conditions hold (Table 5). Investors understand this behavior and still delegate.

**Simulation calibrated to CRSP.** Returns come from an 11-state Markov chain: 10 bull deciles from Table 4 plus a bear state that replays an entire historical bear episode. Each run lasts 100 years and the last 25 are kept, with 5,000 replications and 100 funds per run.

- Fees are 2/20 with a high-water mark.
- Each month investors move 1% of AUM from bottom-quartile to top-quartile funds.
- Strategy-level flows equal 20% of momentum's trailing 1-year excess over the market.

A type-$k$ fund goes to cash when past-year momentum exceeds the $k$-th percentile. With a share $\alpha$ of funds conservative (types 70–80) and the rest aggressive (types 90–100), conservative funds earn 28–68% of an always-invested fund's profits at $\alpha=0.9$ and 10–38% at $\alpha=0.1$ (Table 6). Aggressive types dominate across $\alpha$. Timing that raises Sharpe for the investor lowers fees for the manager.

## Assessment

- **Convincing:** the out-of-era replication is the real contribution. A 40-year hand-built London sample with similar Sharpe, significant alpha, and crash hazards that rise with trailing momentum performance is hard to call data mining or a hedge-fund artifact. The complementary log-log hazard on Lunde–Timmermann-dated states is a clean, portable way to turn "crash" into a forecastable event.
- **Fragile:**
  - Everything is in-sample: the hazard fits, the Table 4 deciles, and possibly the managed-portfolio percentiles.
  - Table 4 is non-monotone below decile 10, so the signal is essentially a top-decile flag.
  - London inference rests on fewer than about 20 events.
  - Table 6 is very noisy (non-monotone in type, some ratios above 1 for types 93–99), so "aggressive beats conservative" is qualitative.
  - The "blind capital" channel is never measured directly; flows are imputed from returns.
  - The Victorian collateral story sits awkwardly with the positive London market coefficient.
  - The model is partial equilibrium: crowding does not feed back into returns.
- **Relation to the literature:** complements Daniel–Moskowitz (crashes follow bear markets and occur in market rebounds; the negative CRSP market coefficient matches) and Barroso–Santa-Clara (volatility scaling). This paper's signal, trailing momentum outperformance, is a crowding proxy rather than a volatility or option-like beta proxy. It extends the authors' earlier Chabot–Ghysels–Jagannathan (2009) NBER paper on Victorian momentum cycles.
- **Practical use:** a top-decile trailing-UMD (or UMD-minus-market) flag is a cheap crash overlay to test alongside volatility scaling and DM's bear-market/market-variance rule, but it should be validated out of sample. The incentive result is a useful reminder that crowding into a recently hot factor can be privately rational for managers while being bad for LPs.
