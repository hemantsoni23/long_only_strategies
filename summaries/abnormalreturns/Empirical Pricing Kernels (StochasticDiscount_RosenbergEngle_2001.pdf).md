# Empirical Pricing Kernels

**Authors:** Joshua V. Rosenberg (Federal Reserve Bank of New York); Robert F. Engle (NYU Stern)  
**Date:** August 2001 manuscript (published in the Journal of Financial Economics)  
**JEL:** G12, G13, C50 | **Keywords:** Pricing kernels; Risk aversion; Derivatives; Hedging  
**Sample:** Monthly one-month S&P 500 option cross-sections, 1991–1995 (53 usable months); daily S&P 500 returns 1970–1995 for the density model  
**Source file:** `Finance/StochasticDiscount_RosenbergEngle_2001.pdf` (text extract; tables themselves not in the extract, numbers below are those quoted in the text)

---

## 1. Question

Estimate the pricing kernel projected onto S&P 500 return states *date by date*, rather than as a sample average, and ask (i) how "empirical risk aversion" moves over time and with the business cycle, and (ii) whether a time-varying kernel produces better option hedges than a time-invariant one.

Motivation relative to prior work:
- Consumption-based SDF estimation (Hansen–Singleton 1982/83, Chapman 1997, Hansen–Jagannathan bounds) is hampered by NIPA consumption measurement error, seasonal adjustment, and time aggregation.
- Aït-Sahalia–Lo (2000) and Jackwerth (2000) recover projected kernels from options, but build the physical density from an equally weighted four-year histogram of realized returns. That makes beliefs jump discontinuously (the October 1987 crash drops out of the window in November 1991), mis-measures the denominator of the state-price-per-unit-probability, and by averaging over at least a year yields only an *average* kernel that misprices on dates when risk aversion or probabilities deviate from their averages.

## 2. Setup

No-arbitrage pricing $P_t = E_t[M_t X_{t+1}]$ with a general kernel $M_t = M_t(Z_t, Z_{t+1})$. Factoring $f_t(X,Z)=f_t(Z\mid X)f_t(X)$ gives the projection

$$
P_t = E_t\big[M_t^*(X_{t+1})\,X_{t+1}\big],\qquad M_t^*(X_{t+1}) = E_t\big[M_t(Z_t,Z_{t+1})\mid X_{t+1}\big],
$$

which prices any claim on $X$ exactly like $M$, without taking a stand on the state variables $Z$. Projected risk aversion is the normalized slope

$$
\gamma_t^* = -\frac{X_{t+1}\,M_t^{*\prime}(X_{t+1})}{M_t^*(X_{t+1})}.
$$

Under finite horizon and index = wealth, $M^*$ on index returns coincides with the true kernel; in general it is only its projection.

## 3. Estimation

**Criterion.** For options with payoff $g_i(r_{t+1})$, fitted prices are $\hat P_{i,t}(\theta)=\int M^*(r;\theta)\,g_i(r)\,\hat f_t(r)\,dr$, approximated by the average over $J$ simulated returns. The EPK solves

$$
\min_{\theta_t}\ \sum_{i=1}^{L}\big(P_{i,t}-\hat P_{i,t}(\theta_t)\big)^2,
$$

with the scale $\theta_{0,t}$ pinned by pricing the one-month riskless bond, $B_t=E_t[M^*(r;\theta_t)]$.

**Kernel families.**
1. Power: $M^*(r;\theta_t)=\theta_{0,t}\,r^{-\theta_{1,t}}$ ($r$ gross return), so $\gamma^*_t=\theta_{1,t}$ and absolute risk aversion is $\theta_{1,t}/r$ — positive and declining whenever $\theta_{1,t}>0$.
2. Exponentiated generalized Chebyshev polynomial (4 parameters): $M^*=\theta_{0,t}\exp\big[\sum_{n=1}^{N}\theta_{n,t}T_n(x)\big]$, $T_n(x)=\cos(n\arccos x)$, $x=(2r-a-b)/(b-a)$ on the moneyness range $[-10\%,+10\%]$; held flat at its boundary values outside. Chebyshev chosen as near-minimax ($L^\infty$) approximation; the exponential guarantees positivity. The authors note power is only nested in the infinite-order expansion, so a low-order polynomial need not dominate it.

**Physical density.** GJR-type asymmetric GARCH(1,1) with filtered-historical-simulation innovations:

$$
\ln(S_t/S_{t-1})-r_f=\mu+\varepsilon_t,\qquad
\sigma^2_{t|t-1}=\omega_1+\omega_2 I_t+\alpha\varepsilon^2_{t-1}+\beta\sigma^2_{t-1|t-2}+\delta\,\max[0,-\varepsilon_{t-1}]^2 ,
$$

where $I_t$ flags the 1991–95 EPK window (a possible shift in long-run variance). Parameters by QML (normal likelihood); the standardized residuals $\varepsilon_t/\sigma_{t|t-1}$ form the time-invariant innovation pool, rescaled by the current $\sigma$. One-month densities come from 200,000 simulated 20-day paths, updating $\sigma$ along each path. The mean $\mu$ is constant — the authors concede this is inconsistent with time-varying risk aversion but argue it is negligible at a one-month horizon.

**Hedge ratios.** Generalizing Engle–Rosenberg (1995, "GARCH gamma"): reprice the put at $S_t\pm\varepsilon$ (one-day, one-SD moves) and $S_t$ using the updated GARCH density and the *forecast* kernel parameters $E_t[\theta_{t+1}]=\alpha+\beta_1\theta_t+\dots$, then take centered finite differences for delta and gamma. One instrument neutralizes first-order exposure, two instruments first and second order.

## 4. Data

Berkeley Options Database, 1991–1995. End-of-day prices from the last bid–ask midquote between 2:00 and 3:00 pm CT, re-synchronized to the index close by holding the Black–Scholes implied vol fixed (used purely as an interpolation device), then averaged with the put–call-parity counterpart (dividend-adjusted). Filters (partly from Bakshi–Cao–Chen 1997): moneyness $K/S-1\in[-10\%,10\%]$, mid $\in(\$3/8,\$50)$, IV between 5% and 90%, no-arbitrage bounds, monotonicity and vertical-spread conditions, at least 8 options per date. One cross-section per month with maturity closest to 20 trading days (16–24 allowed; exactly 20 in 39 of the 53 months). Only OTM puts and OTM calls are used; 8–13 options per date, none with moneyness above +6% and fewer below −6%.

Daily S&P 500 returns 1970–1995: annualized mean (price only) 7.55%, SD 14.79%, negative skew, excess kurtosis, some serial correlation.

## 5. Results

**Density model.** GARCH ≫ ARCH (LR $p<0.0001$); asymmetry significant (robust $t=2.41$ on $\delta$); the regime dummy is insignificant; a GARCH components model (Engle–Lee) adds nothing. Standardized residuals pass Ljung–Box ($p=0.74$) and ARCH-LM ($p=0.70$), with skewness −0.36 and excess kurtosis 4.26; moves below −5σ occur 6 in 10,000 days and below −10σ 3 in 10,000, versus under 1 in 1,000,000 under normality. June 1991–1995 one-month densities: annualized σ 15.55, 13.03, 11.74, 9.98, 10.88%; skewness −0.36 to −0.47; kurtosis 5.06–5.73. Over the full sample, conditional vol ranges 6.75%–112.86% (peak around October 1987).

**Kernel fit.** Average pricing-error SD per date: polynomial \$0.09 (min \$0.03, max \$0.24) vs power \$0.63 (min \$0.28, max \$1.34). With 8–13 options and 4 parameters, part of the polynomial's advantage is simply degrees of freedom.

**Shape.** Power kernels are monotone decreasing with a slope that varies month to month. Polynomial kernels put more value on large negative states and less on large positive states than power; the left-tail state price per unit probability is especially volatile (time-varying crash-insurance demand), and there is a region of increasing marginal utility for small positive returns. The average polynomial kernel resembles Aït-Sahalia–Lo's: steeply rising for large losses, falling for large gains, non-monotone in between. Its implied absolute risk aversion is negative between −4% and +2% and increasing for returns above −4%, qualitatively matching Jackwerth's post-crash estimates — an early documentation of what later became the "pricing kernel puzzle". The power family cannot produce this by construction.

**Empirical risk aversion (ERA $=\theta_{1,t}$, power).** Mean 7.36, range 2.26–12.55, first-order autocorrelation 0.45 (monthly).

**Business-cycle link (Table 7).** ERA regressed on the lag of ERA, the ATM implied-minus-GARCH vol spread, and one-month percentage changes in: Baa–30y Treasury credit spread, 30y–3m Treasury slope, 3m yield, S&P 500 return, and per-capita real nondurables+services consumption growth.
- Credit spread: coefficient 9.95, significant; the authors read it as a 1 bp widening raising ERA by 0.0995. Univariate correlation 0.50 ($p=0.0004$).
- Term slope: insignificant in the multiple regression; univariate correlation −0.36 ($p=0.0129$).
- Lagged ERA and the vol spread are significant and positive.
- The 3m yield, S&P return, and consumption growth are insignificant, but all signs are consistent with counter-cyclical risk aversion.

The authors interpret this as support for habit models (Campbell 1996; Campbell–Cochrane 1999: risk aversion falls with the surplus-consumption ratio) and as a preference-based reading of Fama–French (1989) counter-cyclical risk premia, conditional on ERA tracking Arrow–Pratt RRA.

## 6. Hedging tests

Design: hedge a \$100 position in an OTM put (moneyness closest to −3%, not above) with an ATM put ($|K/S-1|\le1\%$), the index, or both; options with 16–24 days to expiry, one-day horizon, 243 observations. Time-invariant (TI) kernels use the average of the 53 monthly parameter vectors. EPK parameters are forecast with a one-lag linear model estimated on the 133 consecutive-day pairs in the hedging sample (adjusted $R^2$ 12%–52% across parameters); for power, $\hat\theta_{1,t+1}=2.26+0.69\,\theta_{1,t}$, adjusted $R^2$ 50%, mean forecast 7.49 (SD 1.87). Comparison by a Diebold–Mariano-type $t$-statistic on squared hedging-error differentials with Newey–West errors.

| Instrument | EPK power | TI power | Note |
|---|---|---|---|
| ATM put | **\$11.10** | \$11.21 | $t=2.82$; lowest SD overall |
| S&P 500 index | \$12.11 | \$12.41 | index hedges worse for every spec |
| ATM put + index | \$11.29 | — | best dual hedge, still worse than ATM-only |

- Time variation lowers hedge-portfolio SD by 1–3%; significant in 3 of 6 comparisons, marginal in 1.
- Power beats polynomial for every instrument, both time-varying and TI; significant at 5% in 5 of 6 pairwise comparisons (not tabulated).
- Adding instruments hurts when hedge ratios are estimated with error.

The authors' own conclusion is that the evidence on functional form is "mixed": polynomial prices better, power hedges better.

## 7. Assessment

**Convincing.**
- Replacing the rolling histogram with a conditional GARCH/FHS density is the right fix for the denominator of $q/f$, and the specification tests support it.
- The fit-versus-hedge split is a genuine out-of-sample lesson: extra shape parameters fit the smile but inject noise into finite-difference Greeks. Mark with flexible kernels, hedge with parsimonious ones (or shrink the shape parameters).
- The Chebyshev EPK reproduces the non-monotone kernel of Aït-Sahalia–Lo and Jackwerth under a much better physical density, so the "puzzle" is not purely an artifact of the four-year histogram.

**Fragile.**
- *Short, benign sample.* 53 monthly observations, 1991–95, a window with no NBER recession after March 1991. "Counter-cyclical" is identified from mild credit-spread fluctuations with about eight regressors. The correlations are suggestive, not structural.
- *Meaning of ERA.* $\theta_{1,t}$ absorbs any misspecification of $\hat f_t$: the constant $\mu$, filtered innovations, and missing jump or variance-risk premia. Its co-movement with the implied-minus-GARCH vol spread is partly mechanical, since both measure how rich options are relative to the P-model. A rise in ERA is therefore "options expensive relative to GARCH", not necessarily a preference shock.
- *Regression specification.* Levels of ERA are regressed on one-month changes in the indicators, and the "per basis point" reading of the 9.95 credit coefficient depends on how the percent units are defined. Treat the magnitude loosely.
- *Look-ahead in the hedging test.* The TI benchmark uses the full-sample average of parameters, and the EPK AR(1) is fitted on the hedging sample itself. The gains are small (about 1–3%) and period-specific.
- *Narrow coverage.* A single maturity and a ±10% moneyness window, with the kernel flat outside it. Deep-tail state prices, which matter most for crash insurance, are not identified.

**Practical relevance for a quant PM/researcher.**
- The recipe (filtered-HS GARCH P-density, option-implied Q prices, a low-dimensional kernel fitted with a bond constraint) gives a monthly or daily risk-aversion or variance-premium index.
- That index is usable as a conditioning variable, for example alongside credit spreads.
- For derivatives books, the paper argues for letting the kernel slope vary with conditions when computing Greeks. The payoff is modest but statistically detectable, and hedging an OTM put with the ATM put beats hedging it with the index.

## 8. Relation to literature

- Aït-Sahalia–Lo (2000) and Jackwerth (2000): same projected-kernel object. This paper adds a conditional P-density, a monthly time series, and hedge-based validation.
- Engle–Rosenberg (1995), "GARCH gamma": the source of the hedge-ratio method.
- Campbell–Cochrane (1999) habits and Fama–French (1989): the paper supplies option-market evidence consistent with counter-cyclical risk aversion and premia.
- Hansen–Singleton and Chapman: consumption-based alternatives the paper sidesteps. Consumption growth is insignificant in Table 7, consistent with the paper's premise about noisy NIPA data.
