# Crowding and Momentum
**Authors:** Pedro Barroso, Roger M. Edelen, Paul Karehnke
**Year:** 2017 (draft dated February 2, 2017)
**Journal/Venue:** Working paper (UNSW / UC Davis)
**Source file:** Finance/CrowdingMomentum_BarrosoEdelenKarehnke_2017.pdf (the extracted text omits Tables 2-5; regression results below come from the paper's prose)

## Question

How do the expected level, the unanticipated component, and the uncertainty of capital devoted to momentum shape the mean, volatility and skewness of the momentum factor? The paper derives negative skew (crashes) as an equilibrium outcome of crowding uncertainty, not as an exogenous tail event, and tests the predictions with 13F holdings.

## Model

**Setting.** A single "momentum cycle" between public dividend revelations. Log dividend growth is $\log(X_{j,t+1}/X_{j,t}) = \chi_{t+1} + \iota_{j,t+1}\,\delta_{t+1}/2$, where $\chi$ is a common market shock and $\iota_j\in\{+1,-1,0\}$ tags a random 10% of stocks as future winners/losers. $\delta$ is the long-short differential with variance $\sigma^2_\delta$. With equal-dividend legs, the economy collapses to two assets: the market and a zero-cost momentum portfolio. Let $m_{0\to Rnk}$ be the ranking-period return and $d_1$ the full-cycle differential. The momentum factor return is then
$$m_{Rnk\to 1} = d_1 - m_{0\to Rnk}.$$

**Investors** (common CRRA $\rho>1$; Campbell-Viceira second-order approximation gives mean-variance demand $E[m_{Rnk\to1}]/(\rho\sigma^2_\delta)$ per unit of capital):
- *Informed* ($K_I$) observe $\iota$ and a signal of $d_1$ and trade on $d_1 - m_{0\to Rnk}$.
- *Momentum* ($\tilde K_M$) have no private signal. They hold rational expectations about the price process and condition on $m_{0\to Rnk}$, but not on the realized amount of momentum capital.
- *Counterparty* ($\tilde K_C$) is a reduced-form stand-in for noise trading. A fraction $L_i$ of capital fixates on public information (expects $-m_{0\to Rnk}$), and the rest opts out. $L$ increases with market cap and decreases with a generic illiquidity/adverse-selection characteristic $\lambda$, so $L$ acts as an inverse price-impact parameter.

**Equilibrium.** Momentum traders conjecture $m_{0\to Rnk}=\beta d_1$. The full-information coefficient $\beta = \tilde k_{IM}$ (capital share of informed plus momentum) is infeasible, so they use $\beta^*=E_M[\tilde k_{IM}]$. Define unanticipated momentum capital scaled by informed capital:
$$\tilde\nu = \frac{\tilde k_M - E\,k_M}{k_I}.$$
Then
$$m_{0\to Rnk} = d_1\,\frac{\beta^*}{1-\tilde\nu},\qquad m_{Rnk\to1} = d_1\Big(1-\frac{\beta^*}{1-\tilde\nu}\Big).$$

The core mechanism: momentum traders cannot tell a large ranking-period return driven by strong informed signals from one driven by unexpected crowding. They read crowding as information, $E_M[d_1] = d_1/(1-\tilde\nu)$, and trade *more* aggressively exactly when they should trade less. This positive feedback makes the price response convex in $\tilde\nu$.

**Results.**
1. $\partial m_{0\to Rnk}/\partial\tilde\nu = d_1\beta^*/(1-\tilde\nu)^2$, which is nonlinear and destabilizing. When $\tilde\nu > 1-\beta^* = L\,E_M[\tilde k_C]$, prices overshoot fundamental value and "momentum trading becomes feedback trading resonating with itself."
2. Expected momentum return falls in realized $\tilde k_M$ and in $E\,k_M$. By Jensen on the convex $1/(1-\tilde\nu)$, it also falls in $\sigma^2(\tilde k_M)$.
3. There is an offsetting effect: under crowding uncertainty, the extrapolation intensity $\beta^{*-1}$ is below the average full-information intensity $E[\tilde\beta^{-1}]$. Uncertainty makes momentum traders less aggressive.
4. The effect becomes explosive as a positive capital surprise approaches $k_I$. Extreme moves are more likely when informed capital is low and $\sigma^2(k_M)$ is high.
5. $\sigma^2(\tilde k_M)$ predicts the variance of factor returns.
6. $\sigma^2(\tilde k_M)$ generates **negative skewness**. Positive capital surprises can drive $m_{Rnk\to1}\to-\infty$. Negative surprises are bounded, because with zero momentum capital, returns are limited by $d_1$. This holds even if the capital shocks themselves are symmetric.

Further comparative statics: the premium rises with the momentum portfolio's market cap and falls with its illiquidity, because the same momentum capital erodes more of the residual information in small or illiquid names.

## Empirical design

- **Factor:** Ken French UMD-style decile momentum (12-2, NYSE breakpoints, value-weighted legs), March 1980 to December 2015 (430 months). Annualized mean 13.24% (t = 3.04), volatility 26.08%, Sharpe 0.51, skew -1.43, excess kurtosis 7.84, worst month -45.79%, maximum drawdown -80.36% (2009). The CAPM alpha is 1.28%/month (t = 3.68), above the raw mean of 1.10%/month, and the FF3 alpha is 1.53%/month (t = 4.32), driven by the negative HML loading.
- **Holdings:** Thomson Reuters 13F, 1980Q1 to 2015Q3, merged with CRSP (share codes 10/11).
- **Flow-adjusted net purchases** for institution $i$: $\text{Flow}_{i,t}=K_{i,t}-K_{i,t-1}(1+r_{i,p,t})$. Purchases are measured net of flow-induced scaling with prices held fixed, then signed by $\iota_{j,t}$ (+1 winner decile, -1 loser decile). $\text{Buy}_{i,t}$ uses deciles known at quarter end, i.e., the trade partly precedes classification. $\text{BuyP1}_{i,t}$ uses next-quarter trades in deciles known at the time of purchase.
- **Crowding proxies:** the capital-weighted share of institutions classified as momentum traders. `Buy1qrt` and `Buy1qrtP1` require $\text{Buy}>0$ (resp. $\text{BuyP1}>0$) in the current quarter. `Buy4qrts` and `Buy4qrtsP1` require it in all of the last four quarters (consistent momentum traders).
- **Persistence:** P(momentum trader next quarter | momentum trader now) is about 53% for the 1-quarter measures, falling to about 48% after four quarters. It exceeds 60% for the 4-quarter measures. For comparison, winner-decile stocks stay winners with probability 53% and loser-decile stocks stay losers with probability 62%.
- **Regressors:** the crowding level, the "volatility of crowding" (the uncertainty proxy), and the lagged change in crowding (the surprise proxy). Controls are lagged realized momentum volatility (Barroso and Santa-Clara 2015) and a bear-market indicator (Cooper-Gutierrez-Hameed 2004). The dependent sample starts in September 1981. The volatility-of-crowding estimator is not described in the extracted text, and the earlier summary's attribution of it to AR/GARCH could not be verified.

## Results

**Returns (Table 3, quarterly).** Only the *change* in crowding works. With the other crowding variables included, $\Delta$`Buy4qrts` is negative and significant at 5%, and $\Delta$`Buy4qrtsP1` at 1%. With the volatility and bear-market controls added, the levels are 10% and 1%. In univariate regressions they are 5% and 1%. The 1-quarter measures have the right sign but are insignificant. $\Delta$`Buy4qrtsP1` is significant at 1% in all three specifications and is stronger than either control, and neither control is itself significant in this short sample. Levels and crowding volatility do not predict returns, apart from one weak 10% positive coefficient on crowding volatility, consistent with a risk premium for uncertainty but not robust.

**Volatility (Table 4).** Crowding uncertainty predicts future realized volatility positively, at least at 5% for all four proxies without controls. Lagged realized volatility dominates (t = 10.27; controls-only adjusted $R^2$ = 62.79%). With controls, crowding volatility is subsumed for the 4-quarter measures and survives only one-tailed for the 1-quarter measures (5% and 1%). The best model (`Buy4qrtsP1` plus controls) reaches an adjusted $R^2$ of only 65.77%. Contrary to the model, the crowding *level* predicts *lower* future volatility for three proxies, and this survives controls for the 4-quarter measures. The authors suggest reverse causality: forward-looking momentum capital crowds in when it expects low risk.

**Crashes (Table 5, probit; crash = quarterly return below the 10th percentile, i.e. at most -11.01%).** Lagged volatility is significant at 1% in every specification, and the bear-market indicator has the right sign but is insignificant. With controls, the `Buy1qrt` and `Buy1qrtP1` levels enter positively (5% and 10%), `Buy1qrtP1` crowding volatility enters at 10%, and $\Delta$`Buy4qrts` and $\Delta$`Buy4qrtsP1` enter at 10%. Univariate, $\Delta$`Buy4qrts` is significant at 5% and $\Delta$`Buy4qrtsP1` at 1%. The authors' best crash predictors are lagged momentum volatility and $\Delta$`Buy4qrtsP1`.

## Relation to literature

The model extends Stein (2009), where arbitrageurs don't know aggregate arbitrage capital, from a coordination story to explicit predictions for the first three moments. It is related to Kondor and Zawadowski (2015), on learning about entrants, and Abreu and Brunnermeier (2002), on synchronization risk. Empirically it complements Hanson and Sunderam (2014), who use short interest as a proxy for arbitrage capital, and Lou and Polk's comomentum. It offers a structural reason why Barroso and Santa-Clara's volatility scaling and Daniel and Moskowitz's crash timing work: in the model, the conditions that produce high crash probability also produce high realized volatility. It assumes momentum exists (informed traders under-react) rather than explaining its origin, unlike Hong and Stein (1999), Daniel, Hirshleifer and Subrahmanyam (1998), or Vayanos and Woolley (2013).

## Assessment

- **Convincing:** The theory is elegant. Crashes come from the *signal-extraction* failure of rational momentum traders, not from irrationality. The asymmetry holds with symmetric capital shocks, because the $1/(1-\tilde\nu)$ pole exists only on the crowding-up side. The prediction that crash risk rises when informed capital is thin relative to momentum capital surprises is testable and useful.
- **Fragile:** The sample is about 136 quarterly observations with one dominant crash episode (2009), and significance is scattered across four highly related proxies and many specifications, raising multiple-testing concerns. The volatility result is mostly subsumed by lagged volatility, and the level-volatility sign contradicts the model. "Change in crowding" is a crude stand-in for $\tilde\nu$: it ignores what was anticipated and does not scale by informed capital $k_I$, which the model says matters. The counterparty sector is reduced form. The explosive region depends on the second-order preference approximation, which ignores higher moments, as the authors acknowledge. The measures only cover 13F long positions, with no shorts or hedge-fund leverage.
- **Practical relevance:** A PM would watch the four-quarter change in the capital-weighted share of institutions that are consistent net buyers of winners and sellers of losers, as a slow (quarterly, 45-day-lagged) complement to realized-volatility scaling. It adds little to volatility for risk timing but may carry independent information for the mean. A better implementation would normalize the crowding surprise by a proxy for informed capital and use higher-frequency crowding proxies (short interest, comomentum, ETF/factor-fund flows).
