# Momentum and Mean Reversion Across National Equity Markets
**Authors:** Ronald J. Balvers, Yangru Wu
**Year:** 2006
**Journal/Venue:** Journal of Empirical Finance 13, 24-48
**Source file:** Finance/AbnormalReturnsMomentumMeanReversion_BalversWu_2006.pdf

## Question

Momentum (1-12 month continuation) and mean reversion (3-5 year reversal) are usually estimated separately. If both act on the same assets, each partial model is misspecified. The paper builds a parametric model of country index returns that nests both, derives the omitted-variable biases analytically, and tests whether a combined forecast beats pure momentum and pure contrarian country rotation.

## Model

Log price of country $i$: $p^i_t = \beta_i y_t + x^i_t$, with $y_t$ a global component (may have a permanent part) and $x^i_t$ a **stationary** country-specific component. The identifying assumption, motivated by GDP convergence among developed countries in a Lucas-tree economy, is that country-specific shocks are transitory. World return $r^w_t = y_t - y_{t-1}$, so $r^i_t - \beta_i r^w_t = x^i_t - x^i_{t-1}$.

Transitory component:
$$
x^i_t = (1-\delta_i)\lambda_i + \delta_i x^i_{t-1} + \sum_{j=1}^{J}\rho^i_j\,(x^i_{t-j}-x^i_{t-j-1}) + \eta^i_t .
$$
Hence, with $R^i_t \equiv r^i_t-\beta_i r^w_t$ and $X^i_t \equiv x^i_t-\lambda_i$,
$$
R^i_t = \underbrace{-(1-\delta_i)X^i_{t-1}}_{MRV^i_t} + \underbrace{\rho_i(L)R^i_{t-1}}_{MOM^i_t} + \eta^i_t .
$$
$x^i_t$ is built as the cumulated beta-adjusted return since Dec 1969; $\lambda_i$ absorbs initial mispricing. Special cases: Jegadeesh-Titman momentum ($\delta_i=1$, equal $\rho$, $\beta_i=0$) and the Balvers-Wu-Gilliland (2000) pure mean-reversion model ($\rho=0$, $\beta_i=1$). Unconditional expected $R$ is zero: this is a world CAPM plus predictable transitory deviations.

## Omitted-variable biases (Sec. 2.3)

With equal momentum weights, $MOM_t = \rho(X_{t-1}-X_{t-J-1})$ and $\mathrm{Cov}(MOM, MRV) < 0$ necessarily (a run-up raises momentum and pushes price above trend).
- Omitting momentum: $\mathrm{plim}\, b_{MRV} = -(1-\delta) + \rho\,\mathrm{Cov}(X_{t-1}, X_{t-1}-X_{t-J-1})/\mathrm{Var}(X_{t-1}) > -(1-\delta)$, i.e., reversion looks slower (longer half-life).
- Omitting mean reversion: momentum coefficient is biased down (can flip sign), and choosing $J$ by $R^2$ yields $J \le J^*$: momentum looks shorter-lived.

## Data and estimation

Monthly MSCI gross-dividend USD index returns, 18 developed markets (AUS, AUT, BEL, CAN, DNK, FRA, DEU, HKG, ITA, JPN, NLD, NOR, SGP, ESP, SWE, CHE, GBR, USA), Dec 1969-Dec 1999. ML estimation with pooling restrictions ($\delta_i=\delta$, $\rho^i_j=\rho$, common $\sigma^2_\eta$; $\lambda_i$ country-specific). Trading: rolling re-estimation using prior data only, forecasts from Jan 1980 (1/3 of sample); buy the highest-forecast country (Max1) or three (Max3), short the lowest; **one month skipped** between signal and holding. ETF robustness: 16 iShares/SPDR, Apr 1996-Dec 2003.

## Results

**Full-sample baseline (Table 2, $J=12$):** $\delta = 0.983$ (s.e. 0.002), so $1-\delta = 0.017$; $\rho = 0.023$ (s.e. 0.003). Both larger than in the partial models (pure MR: $1-\delta \approx 0.014$; pure momentum $\rho \approx 0.017$), confirming the bias direction, though smaller in magnitude than the asymptotic formulas imply. MR half-life 40 months alone, 44 months combined (vs 49 in pure MR). $\mathrm{Corr}(MOM, MRV) = -0.35$. Predictable variance: $R^2 = 2.12\%$ (MRV 1.72%, MOM 1.41%, covariance negative); SD of MRV component is 1.15x that of MOM. Impulse responses show momentum lasting beyond 12 months.

**Out-of-sample strategies, 1980-1999 (annualized, $K=1$, $J=12$):**

| Strategy | Max1-Min1 | Max3-Min3 |
|---|---|---|
| Pure momentum (JT) | 11.8% ($t=1.41$) | 10.2% ($t=1.98$) |
| Pure mean reversion | 11.5% ($t=1.70$) | 5.4% ($t=1.53$) |
| Random walk (highest historical mean) | -7.9% | -2.6% |
| Combined | **19.4% ($t=2.99$)** | **11.2% ($t=2.54$)** |

- Over JT's 16 $(J,K)$ cells, combined beats pure momentum in all 42 Max1-Min1 cells and 34/42 Max3-Min3 cells; average Max1-Min1 14.3% vs 7.5%. Combined returns peak at $J=9$-12, consistent with longer momentum once MR is controlled.
- The random-walk strategy (buy highest past-average-return country, Conrad-Kaul) loses money, itself evidence of mean reversion.
- **Factor adjustment (Table 6):** alpha on MSCI world + value-minus-growth, or world + FF SMB/HML, is essentially unchanged (Max1-Min1 $\alpha$ 18.9-19.7%, $t \approx 2.9$); long-short world beta near zero. FX-risk correction "makes little difference" (not tabulated).
- **Turnover/costs:** Max1-Min1 switches 18% of months; at 2% per switch costs about 8.6% p.a., leaving about 10.8%; Max3-Min3 leaves about 4.5%. Pure momentum turns over 39% and is wiped out by costs.
- **Robustness:** all eight pooling variants positive, mostly significant but a few points below the parsimonious baseline; the most flexible ones (country- and lag-specific $\rho$) have double the model-implied expected return but lower realized/expected ratio (overfitting). Consensus of 8 models: 15.4% / 11.1%. Lo-MacKinlay weighted version: 9.6% ($t=2.91$). Forecast start at 1/4 or 1/2 of sample: slightly lower. **ETFs 1996-2003: 4.3% / 5.9%, not significant.** Realized baseline returns are 60% (Max1-Min1) and 47% (Max3-Min3) of the model-implied 32.5% / 23.9%.

## Critical assessment

- **Strong point:** the joint-estimation argument and bias derivation are clean and general; the negative MOM-MRV correlation is mechanical, so any practitioner combining a 12-1 momentum signal with a long-horizon reversal/value signal on the same assets should expect it and estimate weights jointly.
- **Fragile:** headline 19.4% is a single Max1-Min1 position (one long, one short country) over 240 months; $t\approx 3$ is modest, and Max1 results carry country concentration risk. Pooled parameters are estimated on a small panel with slow mean reversion (half-life around 3.5 years), so $\delta$ is imprecise relative to the 30-year sample, and the result that the most parsimonious specification works best suggests signal fragility.
- The only tradeable-instrument test (ETFs) is short and insignificant; the MSCI sample ends in 1999, before the post-2000 decay of country momentum. Transaction costs are assumed, not measured; short-selling costs for indexes are argued away via futures.
- The permanent-global / transitory-local decomposition is an assumption (convergence), not tested; it rules out persistent country-specific re-ratings (e.g., Japan post-1990), which could make MRV signals persistently wrong.
- **Practical relevance:** a useful template for country/sector allocation where a slow anchor (cumulated relative return, effectively a value proxy) and a fast trend coexist. The implementable lesson is the weighting: with $1-\delta \approx 0.017$ and $\rho \approx 0.023$, a 1% excess return raises next-month expected excess return by only about 0.006%, so trend and reversion nearly offset for fresh moves, and the net signal comes from the accumulated deviation relative to recent trend.
