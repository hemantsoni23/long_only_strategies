# Momentum Crashes

**Kent Daniel, Tobias J. Moskowitz · 2016 · Journal of Financial Economics (accepted manuscript, doi 10.1016/j.jfineco.2015.12.002; draft of July 25, 2016) · Source file `Finance/AbnormalReturnsMomentum_DanielMoskowitz_2016.pdf` · CRSP US stocks 1927:01–2013:03 (daily and monthly); AMP (2013) data for EU/JP/UK/US equities (1972/74–2013:05), 18 equity index futures, 10 currencies, 10 government bonds, 27 commodities**

Moskowitz discloses an ongoing relationship with AQR Capital.

## Claim / contribution
Momentum's high average return comes with infrequent, persistent **crashes**. These are partly forecastable. They occur in **panic states** (after multi-year market declines, when volatility is high) and coincide with sharp **market rebounds**. The mechanism is that past losers behave like **call options on the market** in bear markets: their up-beta is much larger than their down-beta. WML is therefore effectively **short a call**. The low expected WML return in these states is not explained by market, Fama–French or variance-swap exposure. An implementable dynamic strategy that scales WML by forecast mean over forecast variance roughly doubles the Sharpe ratio of static WML and spans constant-volatility momentum (Barroso–Santa-Clara 2015). This holds across subperiods, four equity regions and four other asset classes.

## Setup
- **WML:** CRSP common stocks (share codes 10 and 11) on NYSE/Amex/Nasdaq, ranked on cumulative return from $t-12$ to $t-2$ (at least 8 valid months). Value-weighted deciles, monthly rebalancing; WML = decile 10 − decile 1.
- **State variables:**
  - $I_{B,t-1}=1$ if the cumulative VW market return over the past 24 months is negative (183 of 1,035 months).
  - $I_{U,t}=1$ if the contemporaneous excess market return is positive (618 months).
  - $\hat\sigma^2_{m,t-1}$ = variance of daily market returns over the prior 126 days.
  - Panic variable $I_{B\sigma^2}\equiv (1/\bar v_B)\,I_{B,t-1}\hat\sigma^2_{m,t-1}$, normalized to average 1 over bear months.
- Betas are estimated from daily data with 10 lags of the market return (sum of the coefficients), because stale prices matter a lot for pre-war losers.

## Main results

**1. Unconditional properties (Table 1, 1927:01–2013:03, annualized).**

| | Loser (D1) | Winner (D10) | WML | Market |
|---|---|---|---|---|
| $r-r_f$ (%) | −2.5 | 15.3 | 17.9 | 7.7 |
| σ (%) | 36.5 | 23.7 | 30.0 | 18.8 |
| CAPM α (%) | −14.7 (t −6.7) | 7.5 (5.1) | 22.2 (7.3) | 0 |
| β | 1.61 | 1.03 | −0.58 | 1 |
| SR | −0.07 | 0.65 | 0.60 | 0.41 |
| Skew, monthly (daily) | 0.09 (0.12) | −0.82 (−0.61) | **−4.70** (−1.18) | −0.57 (−0.44) |

Winners are more negatively skewed than losers, and skewness increases monotonically toward the winner decile.

**2. Anatomy of crashes (Table 2, 15 worst WML months).**
- Worst: 1932:08 −74.36% (market +36.49%) and 1932:07 −60.98% (market +33.63%). Then 2001:01 −49.19%, 2009:04 −45.52%, 1939:09 −43.83%, 1933:04 −43.14%, 2009:03 −42.28%, 2002:11 −37.04%.
- **14 of the 15** occur with a negative lagged 2-year market return. **All 15** occur in months when the market rose.
- The losses are carried by the short leg:
  - Jul–Aug 1932: market +82%, losers **+232%**, winners +32%.
  - Mar–May 2009: market +26%, losers **+163%**, winners +8%. In March 2009 the losers (Citi, BofA, Ford, GM, International Paper) were on average down 84% from their peaks.
- Crashes are multi-month episodes, not jumps. The sustained drawdowns ran Jun 1932–Dec 1939 and Mar 2009–Mar 2013.
- Rolling betas: after big declines, loser betas exceed 3 (up to 4–5 in the 1930s) and winner betas can fall below 0.5.

**3. Conditional betas and optionality (Table 3, monthly regressions of WML).**
$$R_{WML,t}=(\alpha_0+\alpha_B I_{B,t-1})+\big[\beta_0+I_{B,t-1}(\beta_B+I_{U,t}\beta_{B,U})\big]R^e_{m,t}+\varepsilon_t$$

| | (1) | (2) | (3) | (4) |
|---|---|---|---|---|
| $\alpha_0$ (%/mo) | 1.852 (7.3) | 1.976 (7.7) | 1.976 (7.8) | 2.030 (8.4) |
| $\alpha_B$ | | −2.040 (−3.4) | 0.583 (0.7) | |
| $\beta_0$ | −0.576 (−12.5) | −0.032 | −0.032 | −0.034 |
| $\beta_B$ | | −1.131 (−13.4) | −0.661 (−5.0) | −0.708 (−6.1) |
| $\beta_{B,U}$ | | | **−0.815 (−4.5)** | −0.727 (−5.6) |
| adj. R² | 0.130 | 0.269 | 0.283 | 0.283 |

- The unconditional negative beta of WML is entirely a bear-market effect.
- In bear markets WML's beta is **−0.742 when the market falls vs −1.796 when it rises**: a written call.
- **Decile detail (Table 4A):** the loser decile's bear down-beta is 1.560 and its up-beta 2.160 ($\beta_{B,U}=0.600$, t = 4.4). The winner decile's $\beta_{B,U}$ is −0.215. The asymmetry declines monotonically toward the middle deciles.
- **Bull markets (Table 4B):** WML $\beta_{L,U}=-0.242$ (t = −1.3), not significant. The optionality exists only in bear markets and comes mostly from losers.

**4. Ex post vs ex ante hedging.** Grundy–Martin (2001) hedged market and size exposure using *future* betas (current plus next 5 months). Because WML's realized beta is more negative exactly when the market rises, that hedge is strongly upward-biased. An ex ante hedge (lagged 42-day daily beta) does **not** avoid the 1932 crash, underperforms unhedged WML in 1927–39, and is no better than unhedged over the full sample (Fig. 4).

**5. Forecasting the WML mean (Table 5, 1927:07–2013:03, %/month).**
$$R_{WML,t}=\gamma_0+\gamma_B I_{B,t-1}+\gamma_{\sigma}\hat\sigma^2_{m,t-1}+\gamma_{int}I_{B,t-1}\hat\sigma^2_{m,t-1}+\varepsilon_t$$
- Separately, both predictors work: $\gamma_B=-2.626$ (t = −3.8) and $\gamma_\sigma=-0.330$ (t = −5.1).
- Column (4): $\gamma_0=1.973$ (7.1), **$\gamma_{int}=-0.397$ (t = −5.7)**.
- With all terms (column 5): $\gamma_{int}=-0.323$ (t = −2.2); $\gamma_B$ ≈ 0 and $\gamma_\sigma$ is insignificant.
- So the panic *interaction* is what matters.

**6. Variance risk (Table 6, daily data, Jan 1990–Mar 2013, annualized %).**
- WML mean outside panic states: 31.48% (t = 4.7). The panic coefficient is −58.62 (t = −5.2).
- The panic × market beta shift is −0.52 (t = −28.4).
- Adding a VIX-implied S&P variance-swap return: WML loads on it only in panic states (−0.10, t = −4.7; −0.02 otherwise). But α (30.29) and the panic coefficient (−54.83) are essentially unchanged.
- **Conclusion: variance-risk exposure does not explain the premium or its time variation.**
- Appendix B: FF3 interactions do not help either. WML and HML-devil have correlation −0.50. A 50/50 WML + HML-d portfolio still has a panic coefficient of −12.01 (t = −5.2).

## Dynamic strategy
**Weight (maximizes the unconditional Sharpe ratio; Appendix C):**
$$w^*_{t-1}=\frac{1}{2\lambda}\,\frac{\mu_{t-1}}{\sigma^2_{t-1}}.$$
- Conditional volatility is set proportional to the conditional Sharpe ratio. Constant-volatility scaling is optimal only if the Sharpe ratio is constant, and for WML it is not: the mean *falls* when volatility is high.
- $\mu_{t-1}=\hat\gamma_0+\hat\gamma_{int}I_{B,t-1}\hat\sigma^2_{m,t-1}$. In the out-of-sample (OOS) version this uses expanding-window estimates. The OOS slope stays between −0.43 and −0.21 from 1933 on and rises before the 2001 and 2009 crashes.
- $\sigma^2_{t-1}$ is a linear combination of a GJR-GARCH forecast (fitted on daily WML) and the 126-day realized variance; both help (Table D1).
- The OOS strategy in Table 7 uses the 126-day realized variance.

**Leverage profile (full-sample, volatility-matched):**
- cvol weights range from 0.53 (Jun 2009) to 2.18 (Nov 1952).
- Dynamic weights are 3.6× more volatile than cvol weights, ranging from −0.604 (Mar 1938) to 5.37 (Nov 1952), and are negative in 82 months.
- Higher leverage and turnover mean higher costs, as the authors caution.

**Performance (Table 7, 1934:01–2013:03):**

| Strategy | Sharpe | Appraisal ratio vs previous row |
|---|---|---|
| WML (static) | 0.682 | — |
| cvol (scaled by 126-day σ) | 1.041 | 0.786 |
| variance-scaled (by σ²) | 1.126 | 0.431 |
| **dyn, out-of-sample** | **1.194** | 0.396 |
| dyn, in-sample | 1.202 | 0.144 |

- The gain from cvol to OOS dyn is equivalent to adding an orthogonal strategy with SR = $\sqrt{1.194^2-1.041^2}=0.585$. Roughly half comes from variance (rather than volatility) scaling and half from the mean forecast.
- Ordering dyn > cvol > WML holds in every quarter-century subsample (1927–49, 1950–74, 1975–99, 2000–13), including periods without crashes.

**Spanning (Table 8, daily data, all scaled to 23% volatility, α % p.a.):**
- dyn on Mkt + WML: 23.74 (t = 11.99); on FF + WML with panic interactions: 22.04 (11.60).
- dyn on Mkt + cvol: 7.27 (6.86); on FF + cvol, conditional: 6.10 (6.08).
- cvol on Mkt + WML: 14.27 (11.44).
- **cvol on dyn: −0.72 (−0.66) to −0.02.** Dyn spans cvol, but cvol does not span dyn.

## International and other asset classes
Markets use AMP P3−P1 portfolios (top minus bottom third, value-weighted).

**Equity regions (Table 9):**
- Bear-market beta shifts: EU −0.508 (t −7.1), JP −0.527 (−7.0), UK −0.197 (−3.1), US −0.584 (−6.2).
- Optionality $I_BI_UR_m$: EU −0.418, JP −0.367, UK −0.306 (all significant); US −0.086 (not significant in this shorter sample); global equity −0.342.
- Panic coefficient $I_{B\sigma^2}$ (% p.a.) negative and significant everywhere: EU −6.5, JP −9.9, UK −11.4, US −11.1, GE −8.7.

**Other asset classes (Table 10):**
- The bear-market beta falls in all classes: FI −0.362, CM −0.730, FX −1.092, EQ index futures −0.620.
- Optionality is negative in all, but significant only in commodities (−1.102, t −2.5) and in the GAll composite.
- The panic coefficient is negative except for FI, significant for FX (−4.7) and GAll (−4.1).
- Optionality in commodities and FX undermines a pure Merton (1974) equity-as-call explanation.

**Sharpe ratios by market (Table 11A):**

| Market | WML | cvol | dyn |
|---|---|---|---|
| EU (from 1990:06) | 0.462 | 0.886 | 1.130 |
| JP | 0.067 | 0.160 | **0.416** |
| UK | 0.465 | 0.751 | 0.891 |
| US (from 1972) | 0.283 | 0.519 | 0.646 |
| FI | 0.004 | 0.020 | 0.066 |
| CM | 0.587 | 0.686 | 0.803 |
| FX | 0.296 | 0.423 | 0.653 |
| EQ index futures | 0.705 | 0.800 | 0.843 |
| GAll (all combined) | 0.754 | 0.942 | 1.139; fully dynamic combination 1.223 |

- Skewness turns mostly positive under dynamic weighting.
- Dyn has significant alpha vs cvol in nearly every market. cvol's alpha vs dyn is never significant.

## Critical assessment
**Convincing:**
- Long sample and an economically transparent mechanism (conditional beta and convexity of losers).
- A careful demolition of the ex-post-beta hedge.
- A genuinely out-of-sample dynamic rule that nearly matches the in-sample one.
- Replication across 8 further markets and asset classes.

**Fragile / caveats:**
- Crashes are few (essentially 1930s, 2001–02, 2009), so the mean-forecast slope rests on a handful of episodes; the expanding-window slope is unstable before 1933.
- $I_B$ uses a fixed 24-month window, chosen without reported robustness to alternatives.
- The dynamic strategy needs high and sometimes negative leverage (up to 5.4×, min −0.6×). Transaction costs, shorting costs and borrow recalls on distressed losers in panics are ignored.
- Evidence in other asset classes is mostly directional (many coefficients insignificant); fixed-income momentum shows nothing.
- The explanation (risk premium on losers' convexity vs behavioral fear) is left open.

**Inconsistencies in the manuscript:**
- The Table 1 note says WML is "long Decile 1 and short Decile 10" (reversed).
- The text reports WML SR 0.71 and CAPM α 22.3% (t = 8.5), while Table 1 shows 0.60 and 22.2% (t = 7.3).
- The introduction cites bear up/down betas of −1.51 vs −0.70, while Section 3.2 and Table 3 give −1.796 vs −0.742.
- The introduction says the all-asset dynamic strategy has SR 1.19, "four times" static US equity momentum; Table 11 gives 1.139 (GAll) and 1.223 (GAll*) vs 0.283.
- Minor: Table 8 says "wiinner".

## Practical relevance for a quant PM
- Treat WML as **short a market call in bear regimes**. Monitor the loser leg's up-beta and the panic variable $I_B\cdot\hat\sigma^2_m$. The dangerous state is a 2-year market drawdown plus high volatility, followed by a rally.
- **Scale by $\hat\mu/\hat\sigma^2$, not just $1/\hat\sigma$.** Volatility targeting captures most of the gain (0.68 → 1.04). Variance scaling plus a panic-conditioned mean forecast adds about 0.15 SR out of sample and lets exposure go to zero or negative after crashes.
- Don't rely on ex post beta hedges or variance-swap overlays. A static value (HML-devil) blend helps but leaves significant panic exposure.
- Diversify momentum across regions and asset classes and apply dynamic scaling per sleeve. Dynamic scaling revives Japanese momentum (SR 0.07 → 0.42).
- Budget for leverage and turnover: the dynamic weight is 3.6× more volatile than cvol.
