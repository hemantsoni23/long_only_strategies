# The Fundamentals of Commodity Futures Returns — Detailed Quantitative Research Notes

| Field | Detail |
|------|--------|
| **Authors** | Gary B. Gorton (Wharton, NBER); Fumio Hayashi (NBER); K. Geert Rouwenhorst (Yale SOM) |
| **Year / venue** | NBER Working Paper 13249, July 2007 (JEL G1, G11, G12) |
| **Source file** | Finance/Futures_GortonHayashiRouwenhorst_2007.pdf |
| **Sample** | 33 commodity futures (CRB + LME; the Gorton–Rouwenhorst universe minus electricity, gold, silver), 31 of them with monthly inventory data; Dec 1969 – Dec 2006; CFTC positions 1986–2006 |

## Question and claim

What drives time-series and cross-sectional variation in commodity futures risk premia? The paper's answer is the **state of physical inventories**, as the Theory of Storage predicts, not Keynesian "hedging pressure". Contributions: (i) a monthly inventory panel for 31 commodities over 37 years; (ii) direct evidence of a negative, convex basis–inventory relation; (iii) evidence that low inventories, and price signals that proxy for them (basis, 12-month futures momentum, 12-month spot change), predict higher futures excess returns; (iv) a predictive test that rejects hedging pressure measured from CFTC positions.

## Theory

Two identities, which the authors stress are not mutually exclusive (Fama–French 1988):

$$
F_{t,T} - S_t = S_t r_t + w_t - c_t \qquad\text{(storage: interest + storage cost − convenience yield)}
$$
$$
F_{t,T} - S_t = \big[\mathbb{E}_t(S_T) - S_t\big] - \pi_{t,T},\qquad \pi_{t,T} \equiv \mathbb{E}_t(S_T) - F_{t,T}.
$$

The storage identity has content only through the claim that $c_t$ is decreasing and convex in inventories; the second identity simply defines the premium.

**Model (Appendix A).** A two-period Deaton–Laroque (1992) economy (random harvest $z_1$, depreciation $\delta$, non-negative inventories $I_0 \ge 0$) extended with (a) a fully collateralized futures market, (b) risk-averse speculators with utility $U$ over $W = e_0 + N(\Gamma_1 - F)$, and (c) inventory holders who face a reduced-form bankruptcy cost $g(z_1, I_0, NF)$ decreasing in each argument, which creates hedging demand. First-order conditions:

$$
\mathbb{E}[U'(\Gamma_1 - F)] = 0,\qquad \mathbb{E}[\Gamma_1 - F] = -\mathbb{E}[g'_N] > 0 .
$$

So $F$ sits below the expected spot price (normal backwardation). Because $\mathrm{Var}(\Gamma_1)$ decreases in $I_0$ (DL Lemma 4), a fall in inventories raises the premium longs require. Under the assumption of constant marginal bankruptcy costs, $F$ falls, or rises less than $\Gamma_0$, so the basis $\Gamma_0 - F$ widens. The equilibrium number of contracts $N$ can move either way, so the model does not sign the relation between inventories and open interest or hedging. The authors' interpretation is that the futures premium is *inherited* from a spot-market premium on holding inventory.

Predictions: (1) the basis falls in inventories, at an increasing rate near stock-out; (2) the premium falls in inventories; (3) because inventories are slow to rebuild, past price shocks signal current scarcity, which produces momentum in futures excess returns. Prediction (3) is argued informally and is not derived in the two-period model.

## Data and construction

- **Returns:** at each month-end, hold the nearest contract that does not expire in the following month; excess return $(F_{t+1,T} - F_{t,T})/F_{t,T}$. A commodity enters at the latest of: first inventory month, 12 months after futures listing, Dec 1969 (Natural Gas forced to Dec 1990). There are 7 commodities at the start.
- **Basis:** $(F_1/F_2 - 1)\cdot 365/(D_2 - D_1)$, nearest vs next contract; positive = backwardation.
- **Inventories:** LME warehouse stocks, USDA (terminal elevator grain stocks, cold storage), DOE Monthly Energy Review (non-SPR crude, distillates, gasoline, working gas, propane), NYBOT/NYMEX warehouse stocks. Sugar and Rough Rice have none; Feeder Cattle uses Live Cattle cold-storage beef shifted 3 months ahead. "Normal" inventory $I^*$ is a Hodrick–Prescott trend of log inventories with $\lambda = 160{,}000 \times 81$ (retains cycles of roughly 30+ years); the state variable is $I/I^*$.
- **Stylized facts (Table 1):** EW index excess 5.48% p.a. (geometric 4.58%, std 13.5%, skew 0.91, kurtosis 8.71). 26 of 33 commodities have positive arithmetic mean excess returns, 21 positive geometric; negative arithmetic means include Corn −5.42%, Rough Rice −6.35%, Cotton −4.10%, Aluminum −2.06%. Average pairwise correlation is only 0.12 (0.40 with the index). The average basis is **−2.10%**, i.e. contango on average, negative for two-thirds of commodities, yet the long side earns a premium: the practitioners' "roll yield" is not the risk premium.
- **Inventory dynamics (Table 2):** de-trended, de-seasonalized inventories are very persistent (median AR(1) > 0.90, minimum Soy Meal 0.71). Seasonal $R^2$ ranges from about 0 for industrial metals to 0.61 for Soybeans, 0.70 Pork Bellies and 0.79 Natural Gas.

**Figure 1 caveat.** Across commodities, average basis explains 52% of the variance of average excess returns (1990/12–2006/12), but the authors show this is partly mechanical: with zero ex ante premia, a supply shock raises spot more than futures, so realized returns and basis rise together. Only predictive tests identify premia.

## Results

### Basis vs inventories (Figure 3, Table 3)

For every commodity the average basis is higher in months with $I/I^* < 1$ than with $I/I^* > 1$, significantly so for most (dependence-robust t-stats, Appendix C). A cubic spline with one knot at $I/I^* = 1$ plus month dummies, with slopes evaluated at $I/I^* = 1$ and $0.75$ (Newey–West, 12 lags; group estimates by pooled OLS on the unbalanced panel):

| Group | Slope at 1 (t) | Slope at 0.75 (t) | Difference (t) |
|--|--|--|--|
| Metals | −5.1 (−2.46) | −11.8 (−6.01) | 6.7 (4.70) |
| Softs | −19.3 (−5.65) | −25.7 (−8.37) | 6.4 (4.93) |
| Grains | −21.4 (−5.10) | −25.1 (−5.02) | 3.7 (1.39) |
| Meats | −59.8 (−7.03) | −60.2 (−6.27) | 0.4 (0.12) |
| Energies | −154.6 (−7.61) | −149.6 (−4.15) | −5.0 (−0.16) |

Slopes at normal inventory are negative for all but one commodity (Soy Meal). Magnitudes follow storability: metals are cheap to store and hold large buffers, so they have flat slopes, while bulky energy and perishable meats have steep ones. Convexity is clear for metals and softs (Copper −3.2 → −15.3, difference t = 5.64) but not for meats or energy. Energy inventories rarely reach 0.75 × normal, so those slopes are polynomial extrapolation. Results are unchanged using the interest-adjusted basis.

### Inventories and premia (Tables 4–5)

Predictive regressions of monthly excess returns on lagged $I/I^*$ plus month dummies give mostly negative but imprecise slopes. Group-pooled estimates are significant only for Meats (−2.82, t = −2.22), with Energy marginal (−8.71, t = −1.75).

Half-portfolio sorts on $I/I^*$ (returns relative to the EW index, annualized):

| Period | Low − High | t | % months Low > High |
|--|--|--|--|
| 1969/12–2006/12 | 8.06 | 3.19 | 56.5 |
| 1986/1–2006/12 | 7.25 | 2.34 | — |
| 1990/12–2006/12 | 8.75 | 2.82 | — |

The Low-inventory half has a much higher basis (+4.61 vs −7.78; t = 14.51) and higher prior-12m futures returns (15.31 vs 0.41; t = 6.45), but **no higher realized volatility** (23.86 vs 23.40; t = −1.15). Commercials are more net short in High-inventory names (−11.71% vs −7.97% of open interest). Caveats the authors state: unknown publication lags and revisions in inventory data can create spurious predictability, and $I/I^*$ is not comparable across commodities.

### Price-based sorts (Tables 6–8)

Monthly half-portfolio sorts, EW, annualized returns relative to the EW index:

| Sort | High − EW | Low − EW | High − Low (t) | Std H−L | 1990/12–2006/12 H−L (t) |
|--|--|--|--|--|--|
| Basis | 5.42 (t 3.98) | −4.82 (t −3.44) | 10.23 (3.73) | 15.58 | 11.57 (4.08) |
| 12m futures return | 6.54 | −6.82 | 13.36 (4.93) | 16.99 | 15.36 (4.60) |
| 12m spot change | 6.73 | −7.12 | 13.85 (4.95) | 17.19 | 16.03 (4.47) |

Implied High−Low Sharpe ratios are about 0.65–0.80. All three long legs select below-normal inventories. For the basis sort, High vs Low inventory deviation is −14.9% vs +15.3% (t = −17.08), prior futures return t = 12.93, spot change t = 10.45; the inventory separation is weaker for spot momentum (t = −2.77). The returns of the High Basis and High Momentum portfolios correlate 0.87. Sorting on the **de-meaned** basis (each commodity's full-sample mean removed) still gives 10.13% (t = 3.52). So the basis premium is mainly *time-series* variation in scarcity, not a static bet on hard-to-store commodities. Longer look-back windows increase the inventory dispersion of the momentum portfolios, which motivates the 12-month window (and the annual seasonality).

### Hedging pressure (Tables 9–10, CFTC 1986–2006)

Commercials are net short on average, about 10% of open interest rather than the ~100% a pure Keynesian story would imply, with a monthly std of about 15% and AR(1) between 0.59 (Coffee) and 0.92 (Palladium). Commercials are net long in Corn, Feeder Cattle, Lean Hogs and Milk. Regressing monthly excess returns on commercials' net position:
- **Contemporaneous:** strongly negative slopes (commercials add shorts as prices rise), average $R^2$ about 10% (up to 0.40 in first differences for Corn).
- **Lagged:** insignificant almost everywhere, average $R^2$ below 1%. Sorting portfolios on lagged hedging pressure produces no return spread (unreported).

Non-commercials behave like momentum traders: they are more long in High-momentum and High-basis names. The authors could not replicate De Roon–Nijman–Veld (2000), whose predictive result they believe is contemporaneous; their own results agree with Wang (2003). Conclusion: positions respond to prices and inventories but do not predict premia.

### What inventories do not explain

Regressing High-Basis excess returns on Low-Inventory excess returns leaves an intercept of 2.4% p.a. (t = 1.58, which the paper calls significant although it is not at conventional levels). For High-Momentum the intercept is 4.0% (t = 2.27). The components of basis and momentum returns orthogonal to inventories span each other (intercept ≈ 0). This points to one common priced factor beyond measured inventories, or to inventory mismeasurement.

## Critical assessment

- **Convincing:** the basis–inventory link is robust across ~30 commodities and matches storability intuition. The de-meaned-basis result cleanly separates time-series scarcity from cross-sectional storability. The hedging-pressure test is simple and decisive: contemporaneous vs lagged $R^2$ of 10% vs under 1%. This paper gives the economic rationale for commodity carry and momentum factors.
- **Mechanism only partly supported:** the model's channel is low inventories → higher future spot variance → higher premium, yet realized volatility is essentially the same across inventory-sorted portfolios (t = −1.15) and only slightly higher for High Basis (t = 2.13). The premium is not linked to any measured systematic risk (the authors concede asset-pricing reconciliation is out of scope), so risk-based and limits-to-arbitrage or behavioural readings of momentum remain open.
- **Look-ahead in $I/I^*$:** the HP trend is two-sided, so $I^*_t$ uses future inventories, on top of the unmodelled publication lags. The direct inventory sorts are therefore not implementable as stated; the price-based sorts are the investable evidence.
- **Statistics:** the cross-section is small (7 names in 1969, about 31 by 2006) with half-portfolio sorts. The t-statistics are Newey–West on single portfolio series, and three highly correlated signals are presented as confirming evidence although they are closer to one test. Transaction costs, roll timing and capacity are ignored.
- **Model:** two periods with reduced-form bankruptcy costs and zero cross-partials. The momentum prediction is informal, and the open-interest prediction is ambiguous by construction, which makes the positions evidence hard to falsify.
- **Practical relevance for a quant PM:** treat basis (carry), 12m futures momentum and YoY spot change as noisy, correlated proxies for one scarcity state. Combine rather than stack them, since they correlate at about 0.87. Normalize basis within storability groups, because slopes differ by an order of magnitude between metals and energy. Use CFTC positioning for crowding and risk monitoring, not as a return forecaster. Expect the premium to be regime-dependent; post-2006 carry and momentum returns were weaker than the 10–15% gross spreads reported here.
