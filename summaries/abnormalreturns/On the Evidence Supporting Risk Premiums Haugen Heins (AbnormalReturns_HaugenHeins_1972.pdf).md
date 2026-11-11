# On the Evidence Supporting the Existence of Risk Premiums in the Capital Market (Haugen–Heins 1972/1975) — Detailed Quantitative Research Notes

**Authors:** Robert A. Haugen, A. James Heins | **Year:** 1972 (working paper, University of Wisconsin; SSRN 1783797) | **Published as:** "Risk and the Rate of Return on Financial Assets: Some Old Wine in New Bottles," *JFQA* 10(5), 1975 | **Source file:** `Finance/AbnormalReturns_HaugenHeins_1972.pdf` (scanned working paper; OCR is noisy, figures illegible, a few table digits uncertain)

## Question and thesis
Does the ex-post evidence of the late 1960s (Sharpe 1965, Douglas 1969, Jensen 1969, Soldofsky–Miller 1969, Black–Jensen–Scholes, Miller–Scholes) actually support a positive reward for risk in the *stock* market? The paper argues that four methodological problems can each manufacture an apparent risk premium where none exists, then runs a test designed to avoid them. Result: over long samples the cross-sectional relation between return and risk ($\sigma$ or $\beta$) among NYSE stock portfolios is significantly **negative**. The authors conclude that a search for new theories of relative asset pricing is in order. This is one of the earliest documentations of the low-volatility/low-beta anomaly.

## Part II: four pitfalls in earlier tests

### A. Sample period (bull–bear bias)
Assume the single-index/CAPM generating process over horizon-length periods,
$$r_{j,t}=a_j+\beta_j p_t+e_{j,t},\qquad a_j=E(r_f)(1-\beta_j),$$
so $\bar r_j=a_j+\beta_j\bar p+\bar e_j$. Substituting into the cross-sectional covariance between $\hat\beta_j$ and $\bar r_j$, with $\hat\beta_j\approx\beta_j$ and the residual term small for well-diversified portfolios, the cross-sectional slope is
$$b_\beta\approx\underbrace{[E(p)-E(r_f)]}_{\text{true slope}}+\underbrace{[\bar p-E(p)]}_{\text{estimation error}}.$$
A sample in which the market beat expectations overstates the premium; one in which it disappointed understates it. (The scanned text says "in a bear market, where on average results exceed expectations" — an evident slip; the logic is bull = overestimate.) Their point: the existing tests sampled heavily from 1953–1968, a bullish stretch in which the geometric average return on all NYSE stocks was 15.09% per year. The only remedy is long samples under an assumption of stationarity.

### B. Survivorship ("posterior selection")
Samples drawn at the end of the period and traced backward keep only survivors, and survivors look like low-risk, high-return firms. Illustration: 150 stocks drawn at random from the 1926 NYSE list, each replaced by another random NYSE stock on delisting, annual returns through 1969. Only 60 of 150 survived continuously:

| Group | Avg continuously compounded geometric mean | Avg std. dev. |
|---|---:|---:|
| 90 broken series | .040 | .557 |
| 60 continuous survivors | .073 | .264 |

Mutual-fund analogue (Nantell 1971): funds alive in 1954 but missing from Sharpe's sample had mean .10 / s.d. .21 vs .12 / .16 for Sharpe's surviving funds over matched periods. Miller–Scholes' replication of Lintner (stocks listed continuously 1946–66) and Compustat-based studies (Arditti, Douglas; Lintner's 301 Compustat firms) are criticized on the same grounds.

### C. Pooling segmented markets (bonds and stocks)
Sharpe's and Jensen's mutual-fund samples include balanced/income funds, and Soldofsky–Miller pool bonds, preferreds and common stock. If institutional and regulatory constraints raise bond prices relative to stocks, pooling produces a positive risk–return slope driven by the between-market difference, with no reward for risk *within* stocks. Regan's (1972) dissertation, using 10-stock NYSE portfolios and bond portfolios over 1927–1968, finds two clusters with statistically different intercepts and slopes. Once bond-heavy observations are removed (Sharpe re-run on logged annual relatives, keeping funds with less than one-third in fixed income), the significant positive relations disappear, and for Jensen and Soldofsky–Miller they become significantly **negative** (their Table 3; the coefficients are not legible in the scan). Side point: Sharpe regressed arithmetic means on $\sigma$; with positively skewed returns, sample mean and sample variance are positively correlated even without any true relation (the Miller/Jensen point), so logs are used.

### D. Non-stationarity
Monthly continuously compounded returns on all NYSE stocks (Fisher Link Relative index, February 1926–December 1971) show clearly shifting variance before 1946 and roughly stable variance over 1946–1971. Daily S&P 500 returns (1959–1963) are not stationary even within that period, and variance jumps coincide with sharp price declines. The effect on cross-sectional tests has no clear sign, but it motivates focusing on 1946–71.

## Part III: the test
- **Universe and portfolios:** stocks listed on the NYSE in 1926, CRSP data, no survival screen. 114 equal-weighted portfolios of 25 stocks each (the number was limited by computer time). A monthly performance relative is the average of the 25 stock relatives, so the portfolios are rebalanced to equal weight monthly. A delisted stock is replaced at delisting by another NYSE stock.
- **Statistics per portfolio:** geometric mean (continuous compounding) and s.d. of monthly returns; $\beta$ against the average return of all CRSP stocks; skewness and kurtosis. Computed over 1926–71, 1946–71 and nine five-year windows (the last is six years).
- **Diversification check:** correlations of portfolio returns with the market average are .90–1.00 for all 114, so $\sigma$ and $\beta$ rank portfolios almost identically. Raw returns rather than excess returns are used; a footnote argues the resulting bias is small.
- **Null of no risk premium:** over a long window with $\bar p\approx E(p)$, there should be zero cross-sectional covariance between return and $\sigma$ or $\beta$. Over short windows the slope should be positive in bull markets and negative in bear markets.

## Results

**Table 4 — long periods (cross-section of 114 portfolios)**

| | 1926–71 | 1946–71 |
|---|---:|---:|
| Geometric mean on s.d.: slope | −.0353 | −.0945 |
| t | −4.87 | −5.82 |
| Geometric mean on $\beta$: slope | −.0031 | −.0043 |
| t | −4.79 | −5.42 |
| Average portfolio return (monthly) | .0094 | .0089 |
| Average portfolio s.d. (monthly) | .0893 | .0460 |

For 1946–71, the arithmetic mean is also negatively related to $\sigma$ ($t=-2.97$), and
$$\bar r = .015 - .098\,\sigma - .039\,\text{SKEW} - .004\,\text{KURT}\qquad t:\ (11.33)\ (-6.01)\ (-0.48)\ (-1.43).$$
Volatility survives the controls, and skewness and kurtosis are insignificant.

**Table 5 — five-year windows** (portfolio return regressed on risk; the table title says variance, the text says standard deviation), compared with whether market performance beat the previous ten years (S&P 425 industrials):

| Period | b | t | Market vs prior 10y |
|---|---:|---:|:--:|
| 1926–30 | −.035 | −0.73 | − |
| 1931–35 | −.045 | −1.70 | − |
| 1936–40 | −.098 | −5.58 | − |
| 1941–45 | +.212 | +7.12 | + |
| 1946–50 | −.162 | −4.08 | − |
| 1951–55 | −.234 | −4.46 | − |
| 1956–60 | −.101 | −2.55 | − |
| 1961–65 | +.292 | +6.35 | + |
| 1966–71 | −.041 | −1.33 | − |

In every window the sign of the slope matches the sign of the market surprise measured against the prior decade, as the bias formula predicts. The OCR of the market-return and "change" columns is too garbled for exact values, so only the signs reported by the authors are shown. A separate annual-return experiment on the 150 random stocks (1926–69) gives the same pattern: negative over long periods, alternating sign across bull and bear subperiods.

**Kurtosis as a symptom of shifting variance:** portfolio kurtosis is 2.7–3.9 over 1946–71 but 12–25 over 1926–71. The authors read this as evidence that monthly returns are close to Gaussian with time-varying variance rather than intrinsically fat-tailed. This anticipates the ARCH/stochastic-volatility view (they credit Hsu and Wichern for the idea).

Rough magnitude (my arithmetic, not the paper's): in 1946–71 a one-standard-deviation spread in portfolio $\sigma$ is small, but the slope implies that moving from $\sigma=.046$ to $.092$ per month lowers the monthly geometric mean by about $.0945\times.046\approx .43\%$, around 5% per year.

## Assessment
- **Convincing:** The bull–bear decomposition is simple and correct, and Table 5's sign pattern is a sharp test of it. The design already reflects later best practice: forward-looking sampling from 1926, delisting replacement, diversified portfolios to reduce errors-in-variables, and separation of stocks from bonds. The negative long-run slopes on both $\sigma$ and $\beta$, with $|t|\approx 5$, are the original low-risk anomaly result, predating Haugen–Baker (1991, 1996), Ang et al. (2006) and Frazzini–Pedersen BAB.
- **Fragile:**
  - The dependent variable in the headline is the geometric mean, which mechanically falls with variance ($\bar g\approx\bar r-\sigma^2/2$). The arithmetic-mean result is weaker ($t=-2.97$), and the half-variance drag explains part of the $\sigma$ slope.
  - Portfolios are random 25-stock groups, not sorted on risk. The cross-sectional dispersion in $\beta$ and $\sigma$ is therefore narrow, and the slopes are driven by modest risk differences.
  - The 114 portfolios are not independent: each is formed from the same 1926 universe with replacement draws.
  - OLS $t$-stats ignore cross-sectional correlation of residuals, so they are likely overstated.
  - Returns are raw, not excess, and there are no size or industry controls. A small-firm effect running the other way (Banz 1981) could interact with this.
  - Using "market vs prior 10 years" as a proxy for $\bar p-E(p)$ is crude, and it is a signs-only test with nine observations.
- **Practical relevance:** For a quant researcher, two lessons remain current. (1) Any short-window estimate of a beta or volatility premium is dominated by the realized market surprise; check it against the market regime before believing it. (2) The low-risk effect is a century-old, out-of-sample regularity in US equities. Its strength depends on whether one measures geometric or arithmetic returns, which matters for long-only unlevered investors compared with levered BAB implementations.
