# Momentum, Rational Agents and Efficient Markets

**John Crombez (Ghent University / Hogeschool Gent) · *Journal of Psychology and Financial Markets* 2(4), 190–200, 2001 (filename says 2000) · Source file `Finance/AbnormalReturnsMomentum_Crombez_2000.pdf` · Data: IBES × Datastream for MSCI Europe constituents, Mar 1992–Aug 2000 (for dispersion); Belgian Datastream total-market monthly returns 1996–2000 (60 months, for the likelihood)**

## Claim
Behavioural models (DHS 1998, BSV 1998, Hong–Stein 1999) explain momentum by assuming investor irrationality that has never been tested on financial agents. Crombez builds a *normative* benchmark with three ingredients:
1. Bayesian-rational agents.
2. Grossman–Stiglitz efficiency: prices reflect costless public information, while costly information (analysts' models, company access) enters only noisily.
3. Noise in the precision of expert signals.

A simulation shows that slow price adjustment (momentum), and even overshooting, can arise without cognitive failures when analyst forecasts are dispersed. The dispersion is observable even among large, liquid European stocks. Conclusion: behavioural assumptions are not *necessary* and should be demonstrated before they are used.

## Setup
- **Information set.** (i) Historical returns, the likelihood. The uninformed (Hong–Stein) agent's forecast is the sample mean, since $P_t=\mu+P_{t-1}+\varepsilon_t \Rightarrow r_t=\mu\iota+\varepsilon_t$. (ii) The expert consensus, the prior: the one-year consensus earnings-yield forecast (FY1), justified by the valuation identities below.
- **Why expected-return news matters (Assumption 3).**
  - Gordon: $P/D=25\Rightarrow r-g=4\%$, so a 1 pp change in $r$ moves the price about 25% (Cochrane).
  - Ohlson RIM with $P=e_{t+1}/r$ and a 5% earnings yield: a 1 pp change in $r$ moves the price about 17%.
- **Prior scale, or "strength of evidence".** This is the Parkinson extreme-value variance of analyst forecasts:
$$\tau=0.361\,(H-L)^2,$$
  where $H$ and $L$ are the highest and lowest FY1 earnings-yield forecasts (range idea from Kinney–Burgstahler–Martin). **Higher $\tau$ means weaker evidence.** Dispersion is used rather than analyst count, following Griffin–Tversky: *strength* beats *weight* for hard problems. If only one analyst covers a stock, $\tau$ is set to twice the market-portfolio s.d.
- **Bayesian bootstrap regression** (Heckelei–Mittelhammer 1996; roots in Geweke 1986 and Kloek–van Dijk 1978; nonparametric residuals; flexible asset-specific priors instead of Bayes–Stein common shrinkage):
  - $p(\mu|r)\propto p(\mu)\int_0^\infty p(\sigma)f(r|\mu,\sigma)\,d\sigma$, assuming prior independence of $\mu$ and $\sigma$.
  - Draw $\mu_i^*$ from the bootstrap likelihood, then importance-weight by the expert prior:
$$\hat E(\mu)=\frac{\sum_i\mu_i^*p(\mu_i^*)}{\sum_ip(\mu_i^*)},\qquad \mathrm{nse}=\Big[\frac{\sum_i(\mu_i^*-\hat E\mu)^2p(\mu_i^*)^2}{(\sum_ip(\mu_i^*))^2}\Big]^{1/2}.$$
  - $N=5{,}000$ bootstrap draws, with convergence reported as stable. The weight profile $p(\mu_i^*)$ over sorted draws is the "weighing function".

## Empirical dispersion in a liquid universe (Table 1)
The index averages 588 stocks, of which 471 have analyst coverage. Analysts per stock average 16 in 1992, peak at 21 in 1997, and are 19 in 2000. Each month stocks are sorted into deciles (about 50 names) by market value and by CAPM beta, and $\tau$ is averaged within deciles using a robust MAD mean because of extreme outliers.

| Decile | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 | Q8 | Q9 | Q10 |
|---|---|---|---|---|---|---|---|---|---|---|
| $\tau$ by size | 0.02914 | 0.02801 | 0.00331 | 0.00219 | 0.00085 | 0.00040 | 0.00042 | 0.00036 | 0.00028 | 0.00008 |
| $\tau$ by beta | 0.00169 | 0.00158 | 0.00077 | 0.00047 | 0.00077 | 0.00077 | 0.00023 | 0.00093 | 0.00108 | 0.00526 |

- Dispersion falls sharply with size. Q1–Q2 have variance ≈2.85% (s.d. ≈17%), inflated by negative earnings forecasts. Q10 has s.d. ≈0.9%. This is consistent with faster diffusion for large firms (Hong–Lim–Stein).
- Dispersion is high at *both* beta extremes: s.d. ≈4% for the lowest-beta decile and ≈7% for the highest.

## Simulation (Table 2)
Consensus is a +4% next-period return (price 100 → "true" value 104). Only $\tau$ varies, using the size-decile values. The high and low forecasts are symmetric around 4%. The uninformed historical mean is **1.668%** (s.d. 4.17%).

| $\tau$ (source) | expert s.d. | H / L | Bayesian $\hat E(\mu)$ | minus uninformed mean |
|---|---|---|---|---|
| 0 | 0 | 4 / 4 | 4.000% | +2.332 pp |
| 0.00008 (Q10, strong) | 0.894% | 4.744 / 3.256 | **2.262%** | +0.594 pp |
| 0.00085 (Q5, medium) | 2.916% | 6.426 / 1.574 | **1.728%** | +0.060 pp |
| 0.00331 (Q3, weak) | 5.753% | 8.788 / −0.008 | **1.680%** | +0.012 pp |

Q1–Q2 are excluded as too extreme. Even the medium case, whose expert s.d. (2.92%) is below the return s.d. (4.17%), leaves the posterior almost at the historical mean: the weighing function is nearly flat. The author says pessimistic-opinion and alternative-parameter scenarios give the same conclusions (not reported).

## Momentum, crashes, overreaction
- **Two-period diffusion (Table 3).** There is no new information, experts keep valuing the stock at 104, and the agent **halves $\tau$**, i.e. doubles strength, when the consensus persists.

| Price at t=1 | Remaining expert view | $\tau$ | Forecast at t=2 | Price at end of t=2 |
|---|---|---|---|---|
| 102.26 | 1.699% | 0.00004 | 1.671% | **103.97** |
| 101.73 | 2.223% | 0.00043 | 1.693% | 103.45 |
| 101.68 | 2.281% | 0.00166 | 1.671% | 103.38 |

  Only the strong-signal stock reaches about 104 after two periods; the others lag. The author concludes that differences in information diffusion generate momentum, echoing BSV's underreaction without irrationality.
- **Booms vs crashes.** The paper states, without reporting numbers, that analyst agreement is higher in every size decile during market declines. Expert views therefore enter prices faster in down markets: crashes are fast and booms slow.
- **Rational overreaction.** Continuing the weak-signal path to period 3, the remaining expert view is 0.60% but the agent forecasts 1.62% and bids the price to **105.1**, above the "true" 104. With fuzzy expert information the agent behaves almost like the uninformed forecaster (1.668%).
- **Policy implication.** More precise, independent analyst communication, as in Kinney et al.'s finding that US forecast accuracy rose in the 1990s, should speed incorporation and reduce momentum profits.

## Critical assessment
- **What it shows.** It is an existence argument: a rational Bayesian who discounts noisy expert priors moves little. Its empirical contribution is Table 1: analyst dispersion is large and strongly size-dependent even in MSCI Europe. There is **no test of momentum returns**, no cross-sectional link between $\tau$ and realised continuation, and no costs.
- **The "momentum" is largely the historical drift.**
  - In Table 3 every t=2 forecast (1.671–1.693%) is essentially the uninformed mean of 1.668%. An agent ignoring experts entirely would reach $100\times1.01668^2\approx103.37$, virtually the weak path's 103.38.
  - The strong path's arrival at ≈104 comes from the first-period 2.26% plus drift, and the 105.1 "overshoot" is simply continued drift extrapolation.
  - The dynamics therefore show slow *adjustment toward* the expert value, not serial correlation of returns in a cross-section.
- **Conceptual issues.**
  - Prices are updated by "rising by the expected return" rather than jumping to the posterior value, which conflates expected return with price revision. In an efficient market, belief revisions should move prices immediately.
  - The expert prior mixes units: a 4% FY1 earnings yield, essentially an annual quantity, is treated as a next-*month* return and combined with monthly Belgian returns.
  - "Doubling strength" is an ad-hoc learning rule.
  - The likelihood (Belgium) and the dispersion data (MSCI Europe) come from different universes.
- **Inconsistencies in the paper.**
  - The text gives the large-stock decile variance as "0.0008 (s.d. 0.9%)", but Table 1 says 0.00008, which is the value consistent with s.d. 0.9%.
  - Table 2 prints the s.d. as 0.89944% versus the text's 0.8944% ($\sqrt{0.00008}=0.894\%$).
  - Table 2's note says the $\tau$ column is "in percentage points", which contradicts its use as a variance in decimals.
- The observation that dispersion is high among small and extreme-beta stocks is also exactly what behavioural models predict (Hong–Stein, DHS). The mechanism is not discriminating.

## Practical relevance for a quant PM
- The durable, testable idea is to condition momentum on **analyst forecast dispersion** (Parkinson range of FY1). Momentum should be stronger and slower to close where dispersion is high: small caps, extreme betas. This complements Hong–Lim–Stein's coverage conditioning, and the paper leaves it to you to test.
- Use robust (MAD) cross-sectional means for dispersion. Handle negative-earnings names separately, since they dominate raw ranges.
- Treat the simulation numbers as illustrative only; they are not return forecasts.
