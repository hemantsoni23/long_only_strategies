# Momentum: What Do We Know 30 Years after Jegadeesh and Titman's Seminal Paper?

**Tobias Wiest (Univ. St. Gallen) · 2023 · *Financial Markets and Portfolio Management* 37:95–114 (open access), doi:10.1007/s11408-022-00417-8 · Source file `Finance/Momentum_Wiest_2023.pdf` · Literature survey (60 cited papers, 47 in JF/RFS/JFE); no new estimation**

## Claim / contribution
A compact survey in three strands: (1) construction of momentum strategies and enhancements (time-series, residual, intermediate-horizon, risk-managed); (2) behavioral vs risk-based explanations; (3) *commonality*: industry, style and factor momentum. Its conclusion is that momentum exists everywhere and survives standard risk adjustment, but its origin is unresolved. The most recent evidence (Ehsani–Linnainmaa 2022a; Arnott et al. 2021) says **factor momentum subsumes stock and industry momentum**. That view clashes with *short-term stock reversal*, because monthly factor returns are *positively* first-order autocorrelated.

## Momentum everywhere (Fig. 1, avg monthly WML return)
US equity JT (1965–89), US/Europe/Asia-Pacific ex-Japan (French data, Nov 1990–Dec 2021), mutual funds (Carhart 1963–93: **0.67%/mo**, long best minus worst prior-year funds), commodity futures (Miffre–Rallis), corporate bonds (Jostova et al. 1973–2011), crypto (Liu et al. 2014–20). Plotted values run from 0.41% to 1.22%/mo. Rouwenhorst (1998): 12 European countries, magnitude similar to US. Asness–Moskowitz–Pedersen (2013): momentum in US/UK/EU equities, government bonds, FX and commodities.

## Construction
**JT (1993):** rank on cumulative $J$-month return ($J$ = 3–12), form equal-weighted deciles, hold $K$ months, WML = top minus bottom. A one-month skip is standard to avoid short-term reversal (Jegadeesh 1990). Profits are significant for every $J,K\in\{3,6,9,12\}$.

**Lewellen (2002) decomposition** (1-month formation and hold, weights $w_{i,t}=\tfrac1N(r_{i,t-1}-r_{m,t-1})$):
$$E[\pi^{mom}_t]=\frac{N-1}{N^2}\operatorname{tr}(\Omega)-\frac{1}{N^2}\big[\iota'\Omega\iota-\operatorname{tr}(\Omega)\big]+\sigma^2_\mu ,$$
where $\Omega$ is the lag-1 autocovariance matrix. There are three sources: own autocorrelation (+), cross-serial covariance (negative cross-autocovariances help), and cross-sectional dispersion of expected returns $\sigma_\mu^2$, which needs no time-series predictability.

**Enhancements and alternatives**
| Variant | Key evidence cited |
|---|---|
| Time-series momentum (Moskowitz–Ooi–Pedersen 2012) | Vol-scaled futures on 58 assets, 1965–2009. Pooled regression of next-month return on past 12m: $t>5$. Sign strategy positive at 5% for 52/58 assets. TSMOM spans cross-sectional momentum, attributed to positive cross-asset serial correlation (which lowers CS profits via Eq. 2) |
| Critiques of TSMOM | Goyal–Jegadeesh (2018): the edge is net-long leverage. CS plus a matching market position performs similarly for stocks and better across asset classes, and TSMOM's vol scaling overweights low-return bonds. Huang et al. (2020): asset-by-asset regressions give only **8/55** significant slopes at 10%, and a "long if historical mean > 0" rule earns similar profits, so the edge comes from mean dispersion, not predictability |
| Residual momentum (Blitz–Huij–Martens 2011) | Rank on FF3 residuals of 12-1 returns. Volatility roughly halves; annual **Sharpe 0.45 → 0.90** |
| Intermediate horizon (Novy-Marx 2012) | Sort on $t-12..t-7$: **1.20%/mo** vs **0.67%/mo** for $t-6..t-2$ (1927–2010). Survives FF3 + UMD. Short-term winners/intermediate losers underperform the reverse combination |
| Dynamic momentum (Daniel–Moskowitz 2016) | Weight ∝ conditional Sharpe. Expected return is conditioned on bear-market and high-vol states; variance comes from GJR-GARCH. 1934–2013: **Sharpe 1.20 vs 0.68** for static WML. Consistent with vol scaling in Barroso–Santa-Clara (2015) and Moreira–Muir (2017) |

## Explanations
**Behavioral**
- *Delayed overreaction* (Daniel–Hirshleifer–Subrahmanyam 1998: overconfidence plus biased self-attribution) predicts medium-term continuation and long-run reversal.
- *Initial underreaction* (Barberis–Shleifer–Vishny 1998: conservatism) predicts continuation.
- *Hong–Stein (1999)*: news-watchers with gradual diffusion plus momentum traders give underreaction followed by overreaction, without full irrationality.
- Evidence:
  - Chui–Titman–Wei (2010): top-30% vs bottom-30% individualism countries, **+0.60%/mo** momentum.
  - Hillert et al. (2014): high vs low media-coverage quintile **1.02% vs 0.33%/mo**; the gap is larger with high uncertainty and in individualistic states, and it reverses long-run.
  - Hong–Lim–Stein (2000): momentum is concentrated in small firms and, controlling for size, in low analyst coverage.
  - Zhang (2006): momentum rises with information uncertainty.
  - Antoniou et al. (2013): 6m momentum earns **2.00% vs 0.34%/mo** in high vs low sentiment, stronger with short-sale constraints.
  - Cooper–Gutierrez–Hameed (2004): 1929–95, **0.93%/mo after 3-yr up markets vs −0.37%** otherwise, with long-run reversal.
- Against short-horizon continuation: Novy-Marx (2012), where predictability sits in the intermediate horizon.
- *Anchoring*: George–Hwang (2004) sort on distance to the 52-week high (long/short 30%). Returns are about 2× standard momentum, which suggests price levels matter, not past returns.
- *Disposition*: Grinblatt–Han (2005) use a turnover-weighted reference price. Distance to it fully explains return momentum.

**Risk-based** (APT $\mu_i=\sum_f\beta_i^f\mu^f$). There are two channels:
1. *Persistent risk dispersion* ($\sigma_\mu^2$). Conrad–Kaul (1998) attribute **539%** of 12m-momentum profit to it. Jegadeesh–Titman (2002) show this is small-sample bias (means estimated from under 12 months). Constant expected returns also cannot produce reversal, and momentum survives CAPM/FF3 adjustment (JT 1993; Grundy–Martin 2001; Fama–French 1996). Kelly et al. (2021) do find that conditional, characteristic-based betas cut 12-2 momentum from **8.3% to 4.4% p.a.**
2. *Risk changes with performance*:
   - Johnson (2002): convex price in the growth rate, so winners carry more growth-rate risk.
   - Berk–Green–Naik (1999): growth options and slow project turnover.
   - Sagi–Seasholes (2007): growth options make winners riskier. (The survey writes "stronger in high book-to-market firms because these firms have better growth options". That wording looks internally inconsistent and should be checked against the original.)
   - Pástor–Stambaugh (2003): the liquidity-risk factor explains **~50%** of momentum.
   - Avramov et al. (2007): momentum is insignificant after dropping firms rated below BB, and **3.74%/mo** among B-or-worse.

## Commonality
Cochrane (2011) asks why momentum stocks co-move if momentum is idiosyncratic mispricing. Uncorrelated firm-specific effects would diversify into near-arbitrage.

**Industry and connected-firm momentum**
- Moskowitz–Grinblatt (1999): 20 value-weighted industries, top-3 minus bottom-3 on 6m returns, 6m hold, **0.43%/mo** (7/1963–7/1995), driven by industry serial correlation. Industry-adjusted stock momentum falls to **0.13%** from 0.43%. Profit is strongest at 1m/1m, which contradicts stock-level short-term reversal.
- Grundy–Martin (2001): with a 1-month skip, industry momentum drops to an insignificant **0.16%/mo**.
- Hoberg–Phillips (2018): shocks to TNIC (10-K text) peers take up to 12 months to transmit, vs 1–2 months for standard-classification peers. The effect is stronger for less visible peers (inattention) and robust to the Grundy–Martin critique.
- Grobys–Kolari (2020), 48 industries, 1926–2018:
  - Quintile strategies 1-0-1 / 6-1-1 / 12-1-1 earn **0.62 / 0.57 / 0.80%/mo**. Corr(1-0-1, 12-1-1) = **0.14**, so there are multiple forms. The 1-0-1 strategy has $\alpha$ = **0.56%/mo**.
  - Vol-managed 1-0-1 earns **1.16%/mo** unconstrained, **0.64% / 0.90%** with leverage caps of 1 / 1.5. Skew goes from −0.47 to about none.
  - No Daniel–Moskowitz optionality (crash exposure) in industry momentum.
- Ali–Hirshleifer (2020): momentum on shared-analyst connected firms gives 4-factor $\alpha$ **0.89% (VW) / 1.81% (EW)** per month. It subsumes industry, geographic, customer, supplier and technology spillover momentum, and none of those explain it.
- Style momentum, Chou et al. (2019), asset-growth style:
  - Momentum in the highest vs lowest style-beta stocks: **0.60% vs 0.14%**; the difference of 0.46% is significant at 1%.
  - 25 AG×size portfolios, top 7 minus bottom 7: **0.76%** (3m hold), **0.48%** (12m hold).
  - Stocks that did not change style vs those that did: **0.60% vs 0.31%**.

**Factor momentum.** Ehsani–Linnainmaa decomposition under a linear factor model:
$$E[\pi^{mom}]=\sum_f \operatorname{cov}(r^f_{-t},r^f_t)\,\sigma^2_{\beta^f}+\sum_f\sum_{g\ne f}\operatorname{cov}(r^f_{-t},r^g_t)\operatorname{cov}(\beta^f,\beta^g)+\frac1N\sum_i\operatorname{cov}(\epsilon_{i,-t},\epsilon_{i,t})+\sigma^2_\eta .$$
The four terms are factor autocovariance × beta dispersion, factor cross-serial covariance, residual autocovariance, and mean dispersion.
- Gupta–Kelly (2019):
  - Of 65 factors, **49** have a significant positive AR(1) at 5%.
  - The TS factor-momentum signal is sized by past return / long-run vol, capped at ±2. With a 1-month lookback, **47** factors have positive significant alpha over the raw factor. The combined strategy has **Sharpe 0.84**.
  - Robust to FF5, stock and industry momentum, and STR; it also works internationally.
  - Stock momentum partly explains factor momentum only at 12-1, not at a 1-month lookback. Factor momentum is best at 1 month, exactly where stocks reverse.
- Zhang (2022): TS momentum in the FX dollar and carry factors spans TS and CS currency momentum.
- Ehsani–Linnainmaa (2022a):
  - Across 20 factors, the average return is **51 bp/mo after a positive year vs 6 bp** after a negative one.
  - In the Kozak–Nagel–Santosh sentiment model, $\operatorname{cov}(PC^k_t,PC^k_{t+1})=\lambda_k^2\beta_k^2c_0\sigma^2[(1+R_f^2)\phi-R_f-R_f\phi^2]$. It is positive only for very persistent sentiment ($\phi>0.996$ at a 0.39% monthly rf) and is concentrated in high-eigenvalue PCs, where arbitrage is risky.
  - With 47 factors (1973–2019), momentum in the top-10 PCs explains most low-eigenvalue PC momentum in the first half and all of it in the second.
  - Factor momentum subsumes stock, industry, industry-adjusted and intermediate-horizon momentum. Momentum-neutral factors (weights orthogonalized to past returns) earn *higher* factor-momentum alphas, so causality runs from factors to stocks.
  - Residual momentum's advantage reflects **omitted factor momentum**.
- Arnott et al. (2021), 43 US factors:
  - Cross-sectional factor momentum is above-median minus below-median factors.
  - Industry-neutral factor momentum fully explains industry momentum.
  - Industry-mimicking portfolios built from factor exposures reproduce industry momentum.
  - Momentum in the top-3 PCs of industry-neutral factors subsumes all industry momentum.
- Ehsani–Linnainmaa (2022b, WP): residual momentum = firm-specific + omitted-factor + **betting-against-beta** component, because sorting on CAPM residuals is a BAB sort when the SML is flat. Orthogonalizing short-term residuals to long-run alphas gives **Sharpe 1.23 vs 0.59** for standard residual momentum, with lower correlation to factor momentum. Short-term reversal is purely firm-specific; intermediate momentum comes from firm-specific plus factor momentum.

## Critical assessment
- This is a narrative review, not a meta-analysis. Numbers come from heterogeneous samples, weighting schemes and periods, so they are not comparable across rows. There are no transaction-cost, capacity or post-publication-decay discussions.
- The factor-momentum subsumption result rests on the chosen factor zoo, and the factors themselves embed past-return-correlated characteristics. The survey itself flags the unresolved reversal puzzle (positive factor AR(1) vs negative stock AR(1)).
- Omissions:
  - Momentum crashes are only touched on through Daniel–Moskowitz.
  - Earnings momentum/PEAD and fundamental momentum (Novy-Marx 2015) are not reviewed.
  - Japan's weak momentum is not discussed.
- Editorial slips in the paper:
  - Fig. 2 panels are cited as "Fig. 1a/1b".
  - "from 196 to 2020" for the Arnott et al. sample.
  - The intro describes Daniel–Moskowitz as inverse-*volatility* scaling, but the body correctly says conditional-Sharpe scaling.
  - The Sagi–Seasholes B/M statement (see above).

## Practical relevance for a quant PM
- Plain 12-1 WML is dominated. Consider the intermediate window, factor/industry residualization (but decompose what the residual captures: omitted-factor momentum and a BAB tilt), and conditional-Sharpe or vol scaling. The Sharpe figures above (0.45→0.90 residual; 0.68→1.20 dynamic; 0.59→1.23 beta-neutral residual) are the headline improvements.
- Before labeling a momentum sleeve "idiosyncratic alpha", regress it on a factor-momentum portfolio (TS or CS, top PCs of your factor set). If it is spanned, the book is factor timing, with different capacity and crowding. Stock, industry and factor momentum sleeves may be one bet counted two or three times.
- Factor momentum works best at a 1-month lookback, while stock signals need a 1-month skip. Combine both horizons carefully.
- State dependence (up-market, sentiment, credit rating, uncertainty, coverage) is useful for conditioning exposure. The low-rating and high-uncertainty concentration also means much of the paper premium sits in costly, hard-to-short names.
