# Presidential Address: Discount Rates — Cochrane (2011) — Detailed Quantitative Research Notes

| Field | Detail |
|------|--------|
| **Title** | Presidential Address: Discount Rates |
| **Author** | John H. Cochrane (Chicago Booth; NBER); AFA President 2010 |
| **Journal** | *Journal of Finance* 66(4), August 2011, pp. 1047-1108 |
| **Type** | AFA Presidential Address: survey and research agenda |
| **Source file** | Finance/AbnormalReturnsDiscountRates_Cochrane_2011.pdf (Drive id `0B-6kBz0I0dMsMGM2NVB4Y3oyWWs`; extracted text ends partway through Appendix A.6, so the later appendix tables were not seen) |

## Thesis

Fama (1970) organized the field around the "expected" part of expected discounted cashflows (informational efficiency). Cochrane argues the "discounted" part should organize it now. Three claims:
1. Essentially all variation in aggregate valuation ratios is variation in expected returns, not expected cashflows.
2. The cross-section of expected returns has become a "zoo" of factors that needs a new data reduction, probably via characteristics-based panel regressions.
3. Theories should be classified by what drives discount rates and which data pin them down. Applications (portfolio choice, performance evaluation, capital budgeting, accounting, compensation, macro) change once discount rates are allowed to vary.

The paper is explicitly "more an agenda than a summary."

## I. Time-series facts

**Short-horizon regression (Table I; CRSP VW excess return on $D/P$, annual 1947-2009):**

| Horizon | $b$ | $t(b)$ | $R^2$ | $\sigma[E_t(R^e)]$ (%) | $\sigma[E_t(R^e)]/E(R^e)$ |
|---|---|---|---|---|---|
| 1 year | 3.8 | 2.6 | 0.09 | 5.46 | 0.76 |
| 5 years | 20.6 | 3.4 (Hansen-Hodrick) | 0.28 | 29.3 | 0.62 |

A 1pp rise in $D/P$ forecasts a return nearly 4pp higher, so prices rise about 3pp more than the dividend yield alone implies. Expected returns vary by about as much as the "puzzling" 6% premium itself. $R^2$ is the wrong metric for economic significance; the right one is $\sigma(E_t R)$.

**Present-value decomposition.** Campbell-Shiller with $dp_t=d_t-p_t$ and $\rho\approx0.96$:

$$dp_t \approx \sum_{j=1}^{k}\rho^{j-1}r_{t+j} - \sum_{j=1}^{k}\rho^{j-1}\Delta d_{t+j} + \rho^k dp_{t+k}.$$

Regressing each term on $dp_t$ gives $1 \approx b_r^{(k)} - b_{\Delta d}^{(k)} + \rho^k b_{dp}^{(k)}$, i.e., a variance decomposition of $dp$ into return news, cashflow news and a "rational bubble".

**Table II (annual 1947-2009):**

| Method | $b_r^{(k)}$ | $b_{\Delta d}^{(k)}$ | $\rho^k b_{dp}^{(k)}$ |
|---|---|---|---|
| Direct, $k=15$ | 1.01 | -0.11 | -0.11 |
| VAR-implied, $k=15$ | 1.05 | 0.27 | 0.22 |
| VAR, $k=\infty$ | 1.35 | 0.35 | 0.00 |

"What we expected to be zero is one; what we expected to be one is zero." Dividend-growth coefficients are small, insignificant, and have the wrong sign (high prices, if anything, precede *lower* dividend growth). No standard errors are reported. Cochrane's defense is that when the point estimates are 1 and 0, asking people to believe 0 and 1 because they cannot be rejected is "a tough sell." The $dp$ variance is all discount rate, but up to half of the *price-change* variance still comes from current dividends.

**Pervasiveness.** The same pattern holds across markets: a yield or valuation ratio maps roughly one-for-one into expected excess returns, not into the expected cashflow or price change. Examples: term spreads forecast bond returns rather than rate changes; credit spreads forecast returns more than defaults; interest differentials forecast FX returns rather than depreciation; sovereign debt levels forecast returns; and price/rent ratios forecast housing returns. Table III (houses 1960-2010 vs stocks 1947-2010): $r_{t+1}$ on $dp_t$ gives $b=0.12$ ($t=2.52$, $R^2=0.15$) for houses vs 0.13 ($t=2.61$, $R^2=0.10$) for stocks; the dividend/rent-growth slopes are small; $dp$ persistence is 0.90 and 0.94. All these premia are high in recessions.

**Multivariate challenge.** Which predictors survive jointly, what is the factor structure of expected returns across asset classes, and what covariances justify them? Cochrane-Piazzesi is the template: one factor captures 99.9% of expected bond-return variance, priced only by the level factor.

**cay and the term structure of risk premia (Table IV, 1952-2009, cay standardized):** $r_{t+1}=0.12\,dp_t+0.071\,cay_t$ ($t$ = 2.14, 3.19), $R^2=0.26$, $\sigma(E_t r)=8.99\%$, ratio to mean 0.91. cay barely forecasts dividend growth, and its own AR coefficient is only 0.65. Long-run coefficients from the VAR are $r^{lr}$: 1.29 on $dp$ and 0.033 on cay; $d^{lr}$: 0.29 and 0.033. By the identity, the cay coefficients on long-run returns and long-run dividend growth must be equal. cay therefore moves expected returns from the distant to the near future ("a shock to the term structure of risk premia") and leaves long-run attribution unchanged. The impulse responses make this concrete: a $\Delta d$ shock is a pure cashflow shock (prices jump permanently), while a $dp$ shock is almost a pure discount-rate shock. Despite a transitory price component in the multivariate system, univariate returns remain almost uncorrelated, so stocks are *not* safer in the long run.

General lesson (Appendix A.4): adding a variable $z$ gives $0=c^{lr}_r-c^{lr}_d$. Extra predictors can only *raise* the share of $dp$ variance attributed to returns; they cannot shift it toward dividends. Appendix Table AI (Welch-Goyal predictors: cay, equity issuance share, stock variance, I/K, default spread) repeats the pattern: one-year $R^2$ rises to about 0.10-0.19, but the variables mean-revert fast and long-run expected-return variance still dominates. Adding the change in $dp$ (a second lag) raises the one-year $R^2$ from 0.09 to 0.15 and forecasts dividend growth ($t=3.27$).

## II. Cross-section

- **Value (FF 10 B/M portfolios, 1963-2010).** Mean excess returns rise from growth to value while CAPM betas are flat, and the HML loading $h_i$ lines up with means. "Beta without expected return is just as much a puzzle, and as profitable, as expected return without beta" (Frazzini-Pedersen). FF3 is a data reduction: theories need only explain the HML premium, so testing deep models on the 25 FF portfolios is weak. Comovement is the core FF result: where there is mean there must be comovement, or Sharpe ratios would be unbounded. Hence pure "fad" stories that do not produce common movement are insufficient.
- **The zoo.** Momentum, accruals, issuance, beta arbitrage, credit, timing, carry, put writing and liquidity provision each raise three questions: which characteristics are independent, whether each corresponds to a factor, and whether $K<N$ factors span them.
- **Method.** Portfolio sorts are nonparametric cross-sectional regressions and cannot be run 27 ways, so we need panel regressions $R^{ei}_{t+1}=a+b'C_{it}+\varepsilon$. The companion step models covariances as functions of characteristics, $\mathrm{cov}_t(R^{ei}_{t+1},f_{t+1})=g(C_{it})$, and tests $E(R^e\mid C)=g(C)\lambda$. By the managed-portfolio theorem, time-series and cross-sectional versions are the same object. The maintained assumption is that moments are stable functions of characteristics, not of security names. Within-portfolio time variation in B/M forecasts returns more strongly than cross-portfolio variation, and recent changes in B/M also forecast.
- **Economic magnitude via sorts.** An annual autocorrelation of 0.1 ($R^2=0.01$) applied to last year's winners, who rose 100%, yields a 10% momentum portfolio return.
- **Back to prices.** Cochrane asks why the field became "asset expected returning" and treats betas as exogenous. Market-to-book should be the left-hand variable. Long-run returns satisfy $\sum\rho^{j-1}r_{t+j}=\sum\rho^{j-1}\Delta d_{t+j}-dp_t$, so long-run betas are cashflow betas. The price/return error mapping is asymmetric. At a 2% yield, a permanent 10 bp/month expected-return error is a 12% price error. Momentum, being short-lived and small in autocorrelation, probably matters little for price levels. Conversely, tiny i.i.d. price errors create spurious mean reversion in multiply-differenced series; forward spreads, for example, are triple differences of prices.

## III. Theories (classified by main ingredient and the data that pin down discount rates)

1. **Fundamental investors, few frictions.**
   - (a) Macro: consumption (habits, long-run risks, rare disasters, durables), incomplete markets and cross-sectional risk (Constantinides-Duffie), outside income, investment/production and general equilibrium. These tie discount rates to quantities.
   - (b) Behavioral: wrong expectations. Any distorted probability is equivalent to a discount factor, $\pi^*_s=\pi_s m_s/\sum\pi_s m_s$, so "rational vs behavioral" in the abstract is vacuous. Models get bite only from restrictions tied to other data, and behavioral work mostly ties prices to other prices. Survey expectations may be risk-neutral expectations.
   - (c) Finance: factor models are data reduction for relative pricing, with deep theories explaining why the factors are priced.
2. **Frictions.**
   - (a) Segmented markets: limited risk-bearing of local investors, downward-sloping demand.
   - (b) Intermediated markets: leveraged, delegated managers, fire sales, liquidity spirals. These need direct data on intermediary balance sheets and on who is active in each market, and an account of why deep-pocket capital arrives only with a lag.
   - (c) Liquidity: idiosyncratic, systemic, or a trading/"moneyness" value of securities.

Efficiency "basically won": none of these is fundamentally about slow cashflow-information diffusion. Informational efficiency is easy to achieve (one informed trader suffices), whereas eliminating segmentation requires everyone to change their portfolios.

## IV. The 2008 crisis through these lenses

- The habit surplus-consumption ratio tracks the P/D ratio through 1990-2010 reasonably well.
- Q theory, $1+\alpha\,i_t/k_t=Q_t$, links I/K to market-to-book and P/D in both the tech boom and the crisis. These are 100%-$R^2$ models, easy to reject formally, but the broad fit is good.
- The crisis showed a coordinated rise in systematic risk premia across all asset classes, including unintermediated ones (e.g., the BAA-AAA spread tracking the S&P). Cochrane argues this favors macro and risk-bearing explanations. Behavioral mechanisms explain anomalies in individual assets but not pervasive common premia or covariance; segmentation models struggle with broad indexable markets.
- Arbitrage violations (Citigroup CDS-bond basis, covered-interest-parity/FX-swap deviations) support intermediary models, but they were small relative to overall price moves. Cochrane's view: macro explains the level, frictions explain the spreads.
- Speculative: a trading-value (liquidity) premium as the low discount rate in "bubbles." NASDAQ Tech's 1998-2001 price rise and fall coincided with its dollar-volume rise and fall, as in every labeled bubble.

## V. Applications

- **Portfolio theory.**
  - The average investor holds the market, so durable advice must rest on differences across investors (outside income, hedging demands). Multifactor efficiency implies a three-fund theorem.
  - Zero-alpha hedge portfolios matter more than priced factors for most investors (the "steelworker" should short a steel portfolio).
  - Mean-variance with time-varying moments misleads. Worked example: a 60% equity share at 18% volatility, with volatility rising to 70% in late 2008, implies a 4% share unless the expected excess return rose from 4% to 60%.
  - Under quadratic utility over consumption streams (Cochrane 2008), optimal payoffs combine an indexed perpetuity and a claim to aggregate dividends on a long-run mean/variance frontier. State variables drop out and a long-run CAPM re-emerges, with outside income adding a second factor. An indexed perpetuity (or annuity) is the long-horizon risk-free asset.
- **Performance evaluation.** "There is no alpha": only beta you understand and beta you do not, and beta you should buy versus beta you already hold. Equity-market-neutral hedge fund returns look like short out-of-the-money puts, and "exotic beta" is alpha to a client who cannot access it.
- **Corporate finance, accounting, regulation.** The textbook CAPM plus a constant 6% premium is wrong on three counts: the premium varies by about its mean, pricing is multifactor, and discount rates differ by horizon. Characteristics- or comparables-based relative pricing may beat beta models for capital budgeting. Price declines driven by discount rates do not raise default probabilities (they raise risk-neutral ones), which bears on hold-to-maturity accounting, slow capital-structure adjustment and capital rules. Stock-based pay loads executives with discount-rate risk they cannot control.
- **Macro.** Recessions are mostly about risk premia and credit spreads, not "the" interest rate. The Fed's crisis response mostly targeted premia. Q-theory adjustment costs matter for dynamics. In the fiscal-theory valuation equation $B_t/P_t=E_t\sum_j m_{t,t+j}\,s_{t+j}$, a flight to quality lowers the discount rate on government debt, linking "rising risk premia" to "falling aggregate demand."

## Assessment

- **Robust and useful:** Framing predictability through the present-value identity is the lasting contribution. It converts a 9% $R^2$ into "all P/D variance is expected-return variance" and shows why adding short-lived predictors changes the term structure of premia, not long-run attribution. For a PM, the operational content is:
  - valuation-ratio signals are slow, low-$R^2$ but economically large;
  - $\sigma(E_t R)\approx$ mean premium, so a constant-premium assumption is a first-order error;
  - long-run and short-run forecast implications must be checked jointly through the identity.
- **Fragile:**
  - Evidence is annual US data, 1947-2009 (about 60 observations), with no standard errors in Table II.
  - Stambaugh-type small-sample bias and out-of-sample instability of $D/P$ forecasts (Goyal-Welch) are acknowledged only in passing.
  - The dividend series reinvests dividends within the year, which mechanically improves $D/P$ as a return forecaster.
  - Housing results rest on smoothed price indices.
  - The crisis section is illustrative graphs, not tests.
- **Research program:** The characteristics-panel approach (means and covariances both as functions of $C_{it}$) anticipated much of the subsequent machine-learning and IPCA-style asset-pricing literature. The call to model prices and long-run payoffs, rather than one-period returns, remains largely unanswered. The "no alpha, only understood/non-understood beta" view is the right lens for evaluating factor-replicable managers.
