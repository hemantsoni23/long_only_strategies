# Facts and Fantasies about Commodity Futures — Detailed Quantitative Research Notes

| Field | Detail |
|------|--------|
| **Authors** | Gary Gorton (Wharton, NBER); K. Geert Rouwenhorst (Yale SOM) |
| **Year / venue** | NBER Working Paper 10595, June 2004, revised March 2006 (published version: *Financial Analysts Journal* 2006) |
| **Source file** | Finance/Futures_GortonRouwenhorst_2004.pdf |
| **Sample** | Equally weighted (EW), fully collateralized index of up to 36 commodity futures, July 1959 – December 2004 (546 months; the abstract says March 2004, the tables run to 2004/12) |

## Question

What are the basic return, risk and correlation properties of commodity futures *as an asset class*? Individual-contract tests of Keynesian normal backwardation (Gray 1961, Dusak 1973, Bessembinder 1992, Kolb 1992) were inconclusive largely because single-contract returns are too noisy; the paper gains power by diversifying across commodities and extending the sample to 45 years (in the spirit of Bodie–Rosansky 1980). The contribution is a set of stylized facts, not a model.

## Mechanics: what a long futures position earns

The futures price embeds the expected future spot price, so expected spot trends are *not* a source of return. The expected payoff to a long position is the risk premium

$$
\mathbb{E}_t[S_T] - F_{t,T},
$$

and the realized payoff is that premium plus the spot surprise $S_T - \mathbb{E}_t[S_T]$. Keynes–Hicks normal backwardation: hedgers (producers) are net short, so speculators demand $F_{t,T} < \mathbb{E}_t[S_T]$ and the futures price drifts up toward the spot as maturity approaches. Oil example (after Weiser 2003): $S_t=30$, $\mathbb{E}_t[S_T]=27$, $F_t=25$; if $S_T=27$ the spot holder loses \$3 while the long futures gains the \$2 premium; if $S_T=26$ the long gains \$1 (premium \$2 minus a \$1 negative surprise).

Two distinctions the paper stresses:
- **Basis vs normal backwardation.** Market "backwardation" means $S_t > F_t$ (positive basis); Keynesian normal backwardation means $F_t < \mathbb{E}_t[S_T]$. A market can be in contango and still pay longs a premium (e.g. $S=30$, $\mathbb{E}[S_T]=34$, $F=32$). By construction the basis equals expected spot change plus the premium, so it is not itself a return source, but it can carry information about the premium.
- **Cost of carry is only an upper bound** (Appendix 2): $F_{t,T} \le e^{r(T-t)}(S_t + w)$ with $w$ net storage cost. The reverse arbitrage requires shorting/borrowing the physical, which inventory holders resist because stock-outs disrupt production, so the inequality is not an equality for commodities.

Leverage is removed by **full collateralization**: each \$1 of futures notional is backed by \$1 of 30-day T-bills (Ibbotson), so total return = futures price return + bill return; the excess return is the futures price return.

## Index construction

- CRB daily data from 1959, plus LME metals (Aluminum, Nickel, Zinc, Lead, Tin; pre-1993 LME prices interpolated between cash and 3-month). 9 commodities at inception (Copper, Cotton, Cocoa, Wheat, Corn, Soybeans, Soy Oil, Soy Meal, Oats); energy enters late (Heating Oil 1978, Crude 1983, Nat Gas 1990, Coal 2001, Electricity 2003).
- Hold the nearest contract that does not expire in the current month; roll on the last business day of the month before expiry. One exchange per commodity (chosen on liquidity). Spot prices are proxied by linear interpolation between the index contract and the next one.
- Equal dollar weights, rebalanced monthly; new commodities enter at equal weight (expanding universe).
- Biases: CRB covers surviving contracts only. The authors argue survivorship is less damaging than in equities because contracts die from lack of volume, not from low returns — direction of bias unclear. Exchange selection by liquidity is a separate selection bias.

## Main results

### Spot vs futures (Table 1)

Annualized, 1959/7–2004/12:

| | Monthly rebal | Annual rebal | Buy & hold |
|--|--|--|--|
| Futures, arithmetic | 10.69 | 11.97 | 11.46 |
| Spot, arithmetic | 8.42 | 7.51 | 4.64 |
| Futures, geometric | 9.98 | 11.18 | 10.31 |
| Spot, geometric | 7.66 | 6.66 | 3.47 |

Inflation ≈ 4.1% p.a. Futures returns are insensitive to the rebalancing rule; spot returns are not, because seasonal spot spikes mean-revert, so rebalancing harvests them (annual-rebalance figures average 12 indices rebalancing in different calendar months, à la Jegadeesh–Titman). Buy-and-hold geometric spot (3.47%) trails inflation, consistent with Prebisch–Singer. Spot and futures indices are highly correlated in the short run (log chart) but diverge in trend: futures earn bill + premium, spot earns the expected spot drift.

### Risk premium vs stocks and bonds (Tables 2–3)

Excess returns over T-bills, annualized monthly data:

| | Commodity futures | S&P 500 | Ibbotson corp. bonds |
|--|--|--|--|
| Mean excess | 5.23% | 5.65% | 2.22% |
| Std dev | 12.10% | 14.85% | 8.47% |
| $t$-stat | 2.92 | 2.57 | 1.77 |
| Sharpe | 0.43 | 0.38 | 0.26 |
| % months > 0 | 55 | 57 | 54 |

Monthly total returns: mean 0.89 / 0.93 / 0.64%, std 3.47 / 4.27 / 2.45%, skewness **+0.71 / −0.34** / +0.37, kurtosis 4.53 / 1.81 / 3.56. The empirical 5% monthly quantile is −4.10% for commodities vs −6.34% for equities. In CPI-deflated cumulative terms commodities and stocks end roughly level after 45 years; commodities won the 1970s, stocks the 1990s.

The premium is measured as the *arithmetic* mean excess return, which the authors (crediting Ingersoll) argue is the right risk-premium measure; geometric/log tests (Kolb 1992; Erb–Harvey 2005) implicitly measure it against a log-utility investor and bias toward rejection. Prior portfolio estimates: Bodie–Rosansky 9.5% p.a. (1950–76); Fama–French 0.45%/month continuously compounded, $t=1.57$ (21 commodities, 1966–84).

### Correlations and tail behaviour (Tables 4–5, Figure 5)

Correlation of EW futures with other assets, overlapping returns, * = 5% significant (Newey–West):

| Horizon | Stocks | Bonds | Inflation |
|--|--|--|--|
| Monthly | 0.05 | −0.14* | 0.01 |
| Quarterly | −0.06 | −0.27* | 0.14 |
| 1-year | −0.10 | −0.30* | 0.29* |
| 5-year | −0.42* | −0.25* | 0.45* |

Stocks and bonds are negatively correlated with inflation at all horizons (stocks −0.15* monthly to −0.25 at 5 years; bonds −0.12* to −0.32* at 1 year), commodities positively. The commodity–stock correlation is statistically indistinguishable from zero except at 5 years, and the 5-year estimates rest on few independent observations (about nine non-overlapping windows).

Conditional on the worst 5% of equity months (S&P −8.98%/month on average), commodities returned +1.03%/month, slightly above their unconditional 0.89%; in the worst 1% (S&P −13.87%) they returned +2.36% — but that is **six observations** (the authors' own caveat). Conversely, in the worst 5% (1%) of commodity months equities averaged −0.99% (−4.10%).

### Inflation components (Table 6, quarterly)

Expected inflation = ex ante 90-day T-bill yield (constant real rate, Fama–Schwert 1977); unexpected inflation = realized minus that; revision = change in the bill yield.

| | Inflation | Δ expected infl. | Unexpected infl. |
|--|--|--|--|
| Stocks | −0.19* | −0.10* | −0.23* |
| Bonds | −0.22* | −0.51* | −0.35* |
| Futures | 0.14 | 0.22* | 0.25* |

Residualizing each asset on unexpected inflation only partly removes the negative cross-asset correlation (quarterly futures–stocks −0.06 → 0; futures–bonds −0.27 → −0.20), motivating the business-cycle channel.

### Business cycle (Table 7)

NBER cycles 1959–2004 (seven full cycles), each expansion and recession split into equal-length early and late halves (following Vrugt 2003). Annualized average returns:

| Phase | Stocks | Bonds | Commodities |
|--|--|--|--|
| Expansion | 13.29 | 6.74 | 11.84 |
| early | 16.30 | 9.98 | 6.76 |
| late | 10.40 | 3.63 | 16.71 |
| Recession | 0.51 | 12.59 | 1.05 |
| early | −18.64 | −3.88 | 3.74 |
| late | 19.69 | 29.07 | −1.63 |

Aggregated to expansion/recession, stocks and commodities look alike; the difference is in phase: commodities do best in late expansion and early recession, exactly when stocks and bonds are below their averages. The authors frame this as diversification of *systematic* risk, but note it is purely descriptive (NBER dates are ex post).

### Basis as a premium signal (Table 8)

Basis $= \dfrac{F_1 - F_2}{F_1}\cdot\dfrac{365}{T_2 - T_1}$ between the index contract and the next. Each month, split the universe into High- and Low-basis halves (EW):

| | High − EW | Low − EW | High − Low |
|--|--|--|--|
| Mean (ann.) | 4.87 | −5.17 | 10.04 |
| Std dev | 6.64 | 6.64 | 13.16 |
| $t$-stat | 4.94 | −5.26 | 5.15 |
| Sharpe | 0.73 | −0.78 | 0.76 |
| % months > 0 | 59 | 39 | 60 |

If premia were constant across commodities and time, sorting on the basis would earn nothing (the basis would only reflect expected spot changes). The profitability of the sort therefore implies time and/or cross-sectional variation in premia that the basis proxies; the decomposition is left open. This contrasts with Fama–French (1987), who found the basis more informative about spot changes than premia in commodity-by-commodity regressions.

### International and equity-proxy checks

- **UK and Japan** (1970–Sep 2004, local currency, deflated by local CPI, MSCI equities and IMF long government bonds): commodities perform similarly to local equities, beat local bonds and local inflation (Figures 7–8, graphical only). Collateral is still US T-bills, so the FX return is embedded.
- **Commodity producer stocks** (17 commodities matched to 4-digit SIC codes in CRSP, EW; 1962/7–2003/12): futures cumulate far more; correlation of producer stocks with futures only 0.40 vs 0.57 with the S&P 500. Producer equities are not a substitute.

### Individual commodities (Appendix 3)

This is where the index result gets its character. Individual-contract annualized std devs are roughly 17–52%; average pairwise correlations with other commodities are only about 0.0–0.17, so equal weighting cuts the index std to about 12%. Individual arithmetic *total* returns range widely (Wheat 3.24%, Corn 2.13%, Oats 2.63%, Rough Rice −1.21%, Gold 4.48% vs Crude 20.67%, Unleaded 24.29%, Heating Oil 18.62%, Copper 15.83%). Since the index's mean bill return is about 5.5% (10.69 − 5.23), several long-lived grain contracts had *negative* average excess returns, and geometric returns are far below arithmetic for volatile contracts (Sugar 11.28% vs 2.12%; Natural Gas 14.50% vs 1.70%). Many contracts are strongly right-skewed with high kurtosis (Oats kurt. 28.7, Nickel 29.0, Propane 36.0).

## Critical assessment

- **Convincing:** the qualitative facts — futures ≠ spot; low or negative correlation with stocks and bonds; positive inflation beta, especially to unexpected inflation and expected-inflation revisions; producer equities are equity beta; basis sorts matter. The basis result ($t\approx5$) is the statistically strongest finding and is the ancestor of the commodity carry factor (Koijen et al., Szymanowska et al.).
- **Fragile — the index premium:** the $t=2.92$ premium is on an EW, monthly-rebalanced index whose constituents are individually noisy and whose average excess is dominated by a subset (energy, metals, livestock) while several grains were negative. With near-zero pairwise correlations, a nontrivial part of the index geometric return is diversification (rebalancing) return rather than average contract-level premium — the point Erb–Harvey (2006) press. The paper's buy-and-hold column (11.46% vs 10.69%) partly addresses this, but it does not report per-contract geometric *excess* returns, which are small or negative for many contracts.
- **Composition drift:** the universe grows from 9 (mostly grains) to ~36 contracts; late-entering energy with short, high-return histories (1980s–2004) and a 20-month Electricity series (−46.7%) all get equal weight. Results are "average commodity, average period", not those of a production-weighted index (GSCI heavy in energy) or anything investable at scale in 1960.
- **Business-cycle and tail results** rest on few events (seven cycles; six worst-1% months) and ex post dating; treat as descriptive.
- **Regime:** the sample predates financialization. Post-2004 correlations between commodities and equities rose sharply (2008), and broad long-only commodity indices delivered poor returns in 2008–2020, so the "equity-like premium" should not be taken as a stable prior; the basis/carry signal has held up better than the passive premium.
- **Practical relevance for a quant PM:** use the paper for the correlation/inflation structure and the carry signal, not as an estimate of the passive long premium. Model commodities as a separate block with inflation-surprise and cycle loadings plus sector and term-structure factors; expect index choice (EW vs production weights), roll schedule and rebalancing to matter at the level of several percent per year.

## Limitations stated or implied by the authors

Survivorship and exchange selection; equal weighting embeds a contrarian rebalancing strategy; front-contract only; constant-real-rate proxy for expected inflation; business-cycle phases dated ex post; firm–commodity matching via SIC codes is crude; foreign-investor results embed USD collateral and FX; sources of premium variation (hedging pressure vs inventories) are left to future work (taken up in Gorton–Hayashi–Rouwenhorst 2007).
