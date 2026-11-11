# New Facts in Finance — Cochrane (1999) — Detailed Quantitative Research Notes

**John H. Cochrane** (University of Chicago GSB; consultant, FRB Chicago; NBER) · 1999 · *Economic Perspectives*, Federal Reserve Bank of Chicago · companion to "Portfolio advice for a multifactor world" (same issue) · Source file: `Finance/NewFactsInFinance_Cochrane_1999.pdf` (Drive id `1Vkiygbx-5MDvjLTi8Lc0rQmjy4N6qS6z`)

## Scope and thesis
This is a survey, not an estimation paper. The pre-1985 consensus rested on three claims: (1) the CAPM explains cross-sectional average returns; (2) returns are unpredictable (random walk for stocks, the expectations hypothesis (EH) for bonds, uncovered interest parity (UIP) for FX, roughly constant volatility); (3) active managers do not beat passive benchmarks after adjusting for beta. Each has been revised: multifactor models, long-horizon predictability, time-varying bond and FX premia, time-varying volatility, and fund "persistence" that turns out to be style rather than skill.

The unifying theme: **a price variable (P/D, B/M, the yield-curve slope, the interest differential) reveals slow-moving expected returns, because the offsetting adjustment the old view requires (dividend growth, future short rates, depreciation) is absent or sluggish.** The premia plausibly reward exposure to recessions and financial distress. Cochrane argues this enlarges the set of priced risks without necessarily giving up informational efficiency. Momentum is the exception: it does not fit this template.

## Cross-section: CAPM vs. multifactor
Time-series regression $R^i_t-R^f_t=\alpha_i+\beta_{im}(R^m_t-R^f_t)+\beta_{iA}F^A_t+\dots+\varepsilon^i_t$. The pricing restriction is $E[R^i-R^f]=\beta_{im}\lambda_m+\beta_{iA}\lambda_A+\dots$, and alpha is the residual average return (Box 1).

- **Size (Figs. 1–2, NYSE size deciles plus government and corporate bonds, 1947–96).** Against the VW market, the CAPM fits broadly. Small firms earn a few percent too much (Banz 1981), which is statistically significant but "within the range statisticians can argue about"; a cross-sectional OLS fit roughly halves the effect. With the EW NYSE as proxy, the effect disappears and the slope is if anything too shallow. The size anomaly is sensitive to the market proxy.
- **Value (Figs. 3–4, FF 25 size×B/M).** The highest portfolios earn about 3x the average excess return of the lowest, unrelated to market beta. Within a size group, higher B/M means higher return but *lower* beta, so the CAPM is "a disaster" on these portfolios.
- **FF3 (Fig. 5)** puts the 25 portfolios close to the 45° line. The worst fit is growth stocks, whose average returns barely vary with size beta.
- **APT argument.** FF (1993) time-series $R^2$ are 90–95%. A large alpha with $R^2$ near 1 would be a near-arbitrage (very high Sharpe on the residual), so high $R^2$ nearly forces the factor model to price these portfolios. The flip side: FF3 also prices other price-based sorts (E/P, 5-year sales growth, 5-year reversal), but those sorts also have high $R^2$ on HML/SMB, so this is weak independent evidence. Industry portfolios (lower $R^2$) are priced worse. FF3 fails on momentum despite high $R^2$.
- **Why multiple factors (Merton ICAPM).** Most investors have labor or business income that falls in recessions, so among assets with equal market beta, those that do badly in recessions must pay more. Candidate factors: the market; recession or labor-income events; return-forecasting state variables; and factor-mimicking portfolios (the projection of any factor on returns carries the same pricing information). A factor only earns a premium if it hurts the *average* investor; risks that merely transfer between investors are not priced. "Empirical success varies inversely with theoretical purity." Macro factors (labor income: Jagannathan–Wang 1996; industrial production and inflation: Chen–Roll–Ross 1986; investment growth: Cochrane 1996) line up with average returns but price the 25 portfolios worse than HML/SMB.
- **Interpreting HML.** Value stocks are typically distressed; the premium would compensate for aggregate distress (credit crunch, flight to quality), not idiosyncratic bankruptcy. Heaton–Lucas (1997): the typical stockholder is a small-business proprietor, exposed to exactly that risk. Liew–Vassalou (1999): $GDP_{t\to t+4}=a+0.065\,MKT_{t-4\to t}+0.058\,HML_{t-4\to t}$ ($t=3.09$, $2.83$), so a 10% HML return adds 0.5 pp to the next year's GDP forecast. Fig. 6 shows no obvious link between HML/SMB and macro events. Both have roughly zero market beta.
- **Premium decay (Fig. 6, vol-matched cumulative log₂ returns).** In FF's 1960–90 sample, HML goes from 0.62 below the market to 0.77 above, i.e. $2^{0.62+0.77}\approx 2.6$x the market's cumulative return. Over the full plotted sample HML ends where the market does. From 1990 to 1999 the market beats HML by $2^{0.77}=1.71$x. SMB drops sharply around 1980, when the small-firm effect became known. Caveat: decade-long droughts have happened before (small stocks in the 1950s).

## Time series: predictability

**Stocks (Table 1).** Regression $R^{VW}_{t\to t+k}-R^{TB}_{t\to t+k}=a+b\,(P_t/D_t)+\varepsilon_{t+k}$; GMM standard errors corrected for heteroskedasticity and overlap:

| Horizon | $b$ | s.e. | $R^2$ |
|---|---:|---:|---:|
| 1 yr | −1.04 | 0.33 | 0.17 |
| 2 yr | −2.04 | 0.66 | 0.26 |
| 3 yr | −2.84 | 0.88 | 0.38 |
| 5 yr | −6.22 | 1.24 | 0.59 |

Mechanism: $R_{t+1}=a+bx_t+e_{t+1}$, $x_{t+1}=c+\rho x_t+\delta_{t+1}$. A small one-period $b$ and $R^2$ with a persistent $x$ (large $\rho$) imply large long-horizon coefficients and $R^2$ (the "Chicago temperature in spring" analogy). Because D/P does not forecast dividend growth, it forecasts returns roughly one-for-one: a 1 pp higher dividend yield means about 1 pp higher expected return. A run of good returns that raises prices is bad news for future returns, as with bonds. Shiller (1981) and LeRoy–Porter (1981) volatility tests are essentially the same fact (Cochrane 1991). The 1996–99 run-up had already halved the estimated D/P predictability.

**Momentum and reversal (Table 2, from FF 1996 Table 6; NYSE deciles, buy winners / short losers):**

| Strategy | Period | Formation months | 10−1, %/month |
|---|---|---|---:|
| Reversal | Jul 1963–Dec 1993 | 60–13 | −0.74 |
| Momentum | Jul 1963–Dec 1993 | 12–2 | +1.31 |
| Reversal | Jan 1931–Feb 1963 | 60–13 | −1.61 |
| Momentum | Jan 1931–Feb 1963 | 12–2 | +0.38 |

FF3 explains reversal (long-term losers behave like value stocks) but not momentum: FF3 predicts high returns for momentum losers, which load on value. Momentum essentially disappears in 1931–63 while reversal is stronger there. The arithmetic of small predictability: individual-stock volatility is about 40%/yr (about 12% per month), and the top decile of a normal lies 1.76σ above the mean (winners up about 80% and losers down about 60% over the prior year). A monthly forecast $R^2=0.0025$ gives a predictable component with σ ≈ $\sqrt{0.0025}\times 12\% = 0.6\%$, so each extreme decile earns about 1% relative to the mean and the long–short about 2%/month. A Carhart UMD factor "explains" momentum but is ad hoc, since it prices only portfolios sorted on its own characteristic.

**Short-horizon autocorrelation (Table 3, CLM 1997, 1962–94):** daily ρ₁ is 0.18 (VW) and 0.35 (EW); monthly ρ₁ is 0.043 (VW) and 0.17 (EW). Implementation: Carhart (1997) finds momentum not exploitable after costs. Moskowitz–Grinblatt (1999) find most of the gains come from shorting small illiquid losers, with a large share in November (ahead of December tax-loss selling).

**Why momentum is theoretically awkward.** Price-based predictability comes from positive autocorrelation in *expected* returns, which produces *negative* autocorrelation in realized returns (a rise in the discount rate lowers the price). Getting positive realized autocorrelation needs expected-return shocks correlated with falling expected dividend growth, or an impulse response that turns negative at long horizons. Momentum's forecast variable is fast-moving, so its $R^2$ falls with horizon; its economic content comes from sorting into extreme portfolios. Cochrane's own lean: momentum "isn't there, it isn't exploitable, or it represents a small illiquidity."

**Bonds (Boxes 2, Tables 4–5, CRSP annual 1953–97).** Average one-year holding returns on zero-coupon bonds of maturity 1–5 years are 5.83, 6.15, 6.40, 6.40 and 6.36% (standard deviations 2.83 to 6.58%), so the EH looks fine unconditionally. Fama–Bliss regressions:
- (A) Change in the one-year yield $N$ years ahead on the forward–spot spread: slope −0.10, 0.37, 0.41, 0.77 for $N=1..4$ (EH predicts 1). The adjusted $R^2$ is negative at $N=1$.
- (B) One-year excess holding return on the forward–spot spread: slopes 1.10, 1.46, 1.30, 1.31 (EH predicts 0), $R^2$ 0.16, 0.19, 0.10, 0.07.
A 1 pp higher forward rate means about 1 pp higher expected one-year return on the long bond, not higher future short rates. Short rates are nearly unforecastable at one year, so bond returns are forecastable. The EH works better at 4+ years. $R^2$ builds with horizon toward about 30% (Fama–French 1989). The term spread also forecasts stock returns and business cycles.

**FX (Table 6: Hodrick 2000, Engel 1996, Meredith–Chinn 1998).** Unconditionally, average depreciation and interest differentials line up (DM −1.8 vs −3.9; GBP 3.6 vs 2.1; JPY −5.0 vs −3.7; CHF −3.0 vs −5.9 %/yr), and the gaps are not statistically significant. Fama (1984) regressions $s_{t+1}-s_t=a+b(r^f_t-r^d_t)$, where UIP predicts $b=1$: 1975–89 slopes −3.1, −2.0, −2.1, −2.6 ($R^2\approx0.03$); 1976–96 slopes −0.7, −1.8, −2.4, −1.3. This is the forward-discount puzzle: high-rate currencies tend to *appreciate*. $R^2$ peaks at 30–40% around six-month horizons (Bekaert–Hodrick 1992). At a 10-year horizon the slopes are 0.8, 0.6, 0.5, so long-run UIP roughly holds. The profitable signal is a rate that is high *relative to its usual level*, not a high rate as such.

**Volatility (stated, not tabulated).** Volatility clusters, rises after large price drops, and bond volatility is higher when rates (and possibly spreads) are high.

## Mutual funds
- Carhart (1997) survivor-bias-free data, 1962–96 (funds with TNA > $25m and > 25% in stocks): average CAPM alpha **−1.23%/yr** (Fig. 7). Dispersion of fund average returns is almost as large as across individual stocks, so funds make concentrated bets.
- Style: funds sorted into thirds by HML beta; the top-third cutoff is only h = 0.34. Self-described value funds had market betas near 1 and underperformed the S&P 500 by about 1% (Lakonishok–Shleifer–Vishny 1992). The share of funds with SMB beta > 1 rose from 14% (pre-1990) to 22% (full sample); for HML beta > 1, from 12% to 23%.
- Persistence (Table 7, funds ranked on the prior year's return): monthly excess returns next year are 0.75% for the top 1/30 and −0.25% for the bottom 1/30, a spread of about 1%/month. CAPM alphas are 0.27% vs. −0.74%. Four-factor (MKT, SMB, HML, PR1YR) alphas are −0.11% vs. −0.64%/month. Persistence is momentum in the stocks held, not manager skill. Only the losers' persistence (large negative alphas) survives.
- Tension Cochrane flags: if HML nearly doubles the market Sharpe ratio (FF 1993), funds should cluster above the market line. That they don't fits an "overlooked strategy" story, which contradicts an equilibrium risk-premium story; if the premium was overlooked, it should not last.

## Catastrophe insurance
Convergence trades (e.g., LTCM's 29.5- vs. 30-year Treasury bet, which is a liquidity spread, not arbitrage) and short out-of-the-money puts earn small, steady premia and lose large amounts in panics (Hsieh–Fung 1999). Value, carry and term strategies share this profile: distressed firms fail together in a panic, high-rate currencies devalue in global crises, and long bonds are hit by inflation. Implication: in-sample premia may be *overstated*, because the 50-year sample contained no devastating panic.

## Measurement caveats (Cochrane's)
- With σ = 16% and T = 25 years, the standard error of a mean return is 16/√25 ≈ 3%/yr, so a 2-s.e. band of ±6 pp is about as large as the premia being estimated.
- Predictability rests on very few independent observations: the term spread changes sign roughly once per business cycle, D/P crosses its mean about once a generation, and the rates history is dominated by the single rise and fall around 1980.
- Several premia (HML, SMB, D/P predictability) shrank after publication.

## Assessment
- **Durable contributions:** (i) a single organizing principle, price ratios as expected-return proxies with missing offsetting adjustments, that covers D/P, the term spread, carry, value, size and long-term reversal; (ii) the $R^2$-builds-with-horizon arithmetic and the extreme-portfolio arithmetic for momentum, both of which quantify how economically large effects can hide behind tiny short-horizon $R^2$; (iii) separating performance attribution (where ad hoc factors are fine) from economic explanation (where they are not).
- **Dated or fragile:** long-horizon $R^2$ from overlapping observations in about 50 years of data is fragile (small-sample bias with a persistent regressor, and weak out-of-sample performance of D/P after 1999). The prediction that momentum would not survive was wrong on existence and right on fragility (crashes, strong dependence on small illiquid shorts). HML's post-publication decline, visible already here, continued. The FX section rests on four currencies.
- **For a quant PM/researcher:** evaluate managers and books on multifactor alphas, including momentum, as attribution; treat value, carry and term premia as compensation for crash or recession states with left-tail exposure, and size them assuming the sample understates tail frequency; treat conditional signals as "rich or cheap relative to their own history" (the FX result); require about 25+ years of data before believing any premium estimate. Read with the companion article for the portfolio-choice implications.
