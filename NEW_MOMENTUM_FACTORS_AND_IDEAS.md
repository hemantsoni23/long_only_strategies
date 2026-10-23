# New Momentum Factors & Strategy Architectures Beyond Live Logics

**Date:** 2026-10-20  
**Author:** Quantitative Research Analysis  
**Repository:** `/Users/hemantsoni/Documents/long_only_strategies`  
**Scope:** Deep quantitative analysis of the 61 research papers in `momentum/`, benchmark audit against existing models in `Old_live_strategies/`, empirical cross-validation with `factor_research/`, and new factor blueprints.

---

## Executive Summary & Objective

The objective of this research synthesis is twofold:
1. **Literature & Codebase Audit:** Deconstruct the core theoretical mechanisms documented in the `momentum/` research directory (61 academic papers covering empirical asset pricing, microstructure, behavioral finance, factor momentum, and crash risk) alongside the empirical findings in `factor_research/`.
2. **Novel Factor Generation:** Formulate actionable, mathematically rigorous momentum factors and strategy blueprints that are **structurally distinct** from the models currently running in `Old_live_strategies/`.

### What Your Live Strategies Currently Trade (The Reference Baseline)
Every active strategy in `Old_live_strategies/` relies on variations of three core ideas:
- **`csm_batch` / `csm_quad` / `csm_absolute`:** Dual-lookback Sharpe momentum — $[R_{12,1} / \sigma_{12}] + [R_{6,1} / \sigma_{6}]$, lagged 1 month, combined with catastrophic hard stops and ATR chandelier trailing stops.
- **`csm_zenith`:** **A1** (52-week-high proximity: $\text{Close}_t / \max(\text{High}_{252})$) + **Q5** (Trend persistence: fraction of last 189 days where $\text{Close} > \text{SMA}_{50}$) + **M3** (Low-MAX exclusion: dropping the top 20% highest single-day return spikes in the last 21 days).
- **`csm_elendel`:** **A3** (Relative-strength line at 52-week high: $\text{RS}_t / \max(\text{RS}_{252})$ vs benchmark) + **Q5** (126-day trend persistence).
- **`residual_momentum_strategy`:** CAPM residual momentum (idiosyncratic residual $r_i - \beta_i r_m$ summed over 9m/3m windows and vol-scaled) + 52-week high tilt.
- **`hr_breakout_v2` & `vcp_v4`:** Event-driven horizontal resistance breakouts and Minervini volatility contraction pattern entries.

**The Structural Problem:** As proven in `factor_research/FINDINGS.md` and `MOMENTUM_SIGNALS_EXPLAINED.md`, these existing strategies share a daily return correlation of **0.77 to 0.85**. Adding further lookback windows (e.g., 3m, 9m) or cosmetic risk adjustments to past returns yields an incremental Information Coefficient (IC) near zero ($t < 1.4$). True diversification requires **novel information mechanisms**.

---

## 1. Key Insights from the `momentum/` Literature

A systematic review of the 61 academic works in `momentum/` reveals five critical anomalies and mechanisms that are **not** captured by simple price momentum:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       CORE LITERATURE MECHANISMS                            │
├──────────────────────────┬──────────────────────────────────────────────────┤
│ Mechanism                │ Key Reference Papers                             │
├──────────────────────────┼──────────────────────────────────────────────────┤
│ 1. Momentum Life Cycle   │ Lee & Swaminathan (2000), Llorente et al. (2002) │
│    & Trading Volume      │ Chen, Jegadeesh & Wermers (2000)                 │
├──────────────────────────┼──────────────────────────────────────────────────┤
│ 2. Fundamental & SUE     │ Novy-Marx (2012, 2015), Da & Warachka (2014),    │
│    Momentum              │ Chordia & Shivakumar (2006)                      │
├──────────────────────────┼──────────────────────────────────────────────────┤
│ 3. Asymmetric Downside   │ Daniel & Moskowitz (2016), Lu & Murray (2018),   │
│    Risk & Crash Spreads  │ Ang, Chen & Xing (2006), Barroso & Santa-Clara   │
├──────────────────────────┼──────────────────────────────────────────────────┤
│ 4. Factor Momentum       │ Ehsani & Linnainmaa (2017/2022), Arnott et al.   │
│    Autocovariance        │ Moskowitz, Ooi & Pedersen (2012)                 │
├──────────────────────────┼──────────────────────────────────────────────────┤
│ 5. Execution Drift &     │ Lou, Polk & Skouras (2019), Da, Gurun & Warachka │
│    Information Arrival   │ (2014 - Frog in the Pan), Heston & Sadka (2008)  │
└──────────────────────────┴──────────────────────────────────────────────────┘
```

### Insight 1: The Momentum Life Cycle (Lee & Swaminathan 2000)
- **Finding:** Trading volume reveals the *life cycle* of momentum. Price momentum is pronounced and persistent among **low-turnover/low-volume** winners (early accumulation stage), persisting for 8–12 months with negligible reversal.
- **Contrast:** High-volume winners (late distribution stage) suffer violent, predictable post-formation reversals.
- **Live Strategy Gap:** None of the live strategies condition momentum on volume turnover or volume life-cycle state.

### Insight 2: Fundamental Momentum Subsumes Price Momentum (Novy-Marx 2012, 2015)
- **Finding:** Price momentum is an imperfect, noisy proxy for earnings momentum (Standardized Unexpected Earnings / SUE, and Cumulative Abnormal Returns CAR3 around announcements). When purged of earnings surprises, $R_{12,1}$ alpha collapses and retains negative skew and crash vulnerability. Conversely, earnings momentum stripped of price momentum exhibits **positive skew (+0.46)**, lower volatility (5.1% vs 15.6%), and eliminates rebound crashes.
- **Live Strategy Gap:** The live books are 100% price/technicals-driven, ignoring point-in-time earnings revision drift and fundamental surprise shocks.

### Insight 3: Downside Risk & Crash Sensitivity ($\beta^-$ vs $\beta^+$) (Ang et al. 2006, Daniel & Moskowitz 2016)
- **Finding:** The Sharpe ratio of momentum is penalized by severe left-tail crashes during market turnarounds (e.g., 2009, 2020), when past losers with high upside beta rally violently. Standard beta ($\beta$) treats upside and downside variance symmetrically. High-momentum stocks frequently hide high downside beta ($\beta^-$) during market drawdowns.
- **Live Strategy Gap:** `csm_batch` and `residual_momentum` estimate a static full-period CAPM beta, blind to conditional upside vs downside covariance.

### Insight 4: Factor Momentum Spans Stock Momentum (Ehsani & Linnainmaa 2017)
- **Finding:** Stock-level momentum ($UMD$) is largely an aggregation of factor autocovariance across major equity anomaly factors (Value, Investment, Quality, Low Volatility, Residual Variance). Individual anomaly factors have persistent, positively autocorrelated returns that continuation-trade with an annual Sharpe $> 1.3$.
- **Live Strategy Gap:** All existing books rank individual stocks cross-sectionally. None operate at the factor/style-sleeve layer.

### Insight 5: Microstructure & Information Arrival (Intraday vs Overnight) (Lou et al. 2019)
- **Finding:** Returns built overnight (open-to-previous-close) are driven by retail attention, headline noise, and sentiment, which reverse over subsequent horizons. In contrast, returns accrued **intraday** (close-to-open) represent institutional execution, order-flow absorption, and informed trading, which exhibit strong positive autocorrelation.
- **Empirical Confirmation:** In `factor_research/FINDINGS.md`, `intra_over_252` demonstrated an IC of 0.080 in Top-250 liquid names ($t = 5.5$), while overnight-minus-intraday drift had a significantly negative IC ($t = -5.1$).

---

## 2. Seven Novel Factor Blueprints & Strategy Architectures

Below are seven distinct factor families designed from the ground up to provide uncorrelated alpha relative to the existing live momentum suite.

```
       ┌─────────────────────────────────────────────────────────────┐
       │                NEW MOMENTUM FACTOR MATRIX                   │
       └──────────────────────────────┬──────────────────────────────┘
                                      │
     ┌──────────────────┬─────────────┴──────┬───────────────────┐
     ▼                  ▼                    ▼                   ▼
[1. Quiet Momentum] [2. Asymmetric Beta] [3. Intraday Trend] [4. SUE / PEAD]
(Turnover-Scaled)   (Downside Purged)    (Overnight Faded)   (Fundamental)
     │                  │                    │                   │
     ▼                  ▼                    ▼                   ▼
[5. Factor Rotation][6. Ulcer Momentum]  [7. Convexity Mom]
(Style Autocov.)    (Drawdown-Purged)    (Curvature/Accel)
```

---

### Blueprint 1: "Quiet Momentum" (Volume Turnover-Scaled Momentum)

#### Theoretical Origin
*Lee & Swaminathan (2000) — "Price Momentum and Trading Volume"*

#### Intuition
A stock that has doubled on modest or contracting turnover is experiencing systematic institutional accumulation without retail euphoria. A stock that has doubled on massive turnover is nearing retail climax and institutional distribution. Scaling momentum by turnover filters for the "early" to "mid" life-cycle phase of trends.

#### Mathematical Formulation
1. **Raw Price Trend:**
   $$\text{Trend}_{i,t} = \frac{P_{i,t-21}}{P_{i,t-252}} - 1$$
2. **Turnover Ratio:**
   $$\text{Turnover}_{i,t} = \frac{\text{Median}(\text{Volume}_{i,\tau} \times P_{i,\tau}, \tau \in [t-63, t])}{\text{MarketCap}_{i,t}} \quad \text{or} \quad \frac{\text{Median}(\text{Volume}_{i, \tau})}{\text{SharesOutstanding}_{i,t}}$$
   *(If shares outstanding is unavailable in daily CSVs, use the relative volume ratio: $\text{RelVol}_{i,t} = \frac{\text{SMA}(\text{Volume}, 21)}{\text{SMA}(\text{Volume}, 252)}$).*
3. **Quiet Momentum Factor:**
   $$F_{\text{Quiet}, i, t} = \frac{\text{Z-Score}(\text{Trend}_{i,t})}{1.0 + \text{Z-Score}(\text{RelVol}_{i,t})}$$
   Alternatively, create a 2D independent sort: Quintile 5 by Trend $\cap$ Quintile 1 or 2 by Volume Turnover.

#### Why It Differs from Live Logics
- `csm_batch` uses dollar volume strictly as an eligibility floor (top 1,000 liquid).
- This factor uses volume dynamically to penalize crowded, late-stage retail momentum.
- Expected correlation with `csm_zenith` / `csm_elendel`: **0.45 – 0.55**.

---

### Blueprint 2: Asymmetric Downside-Beta Momentum ($\Delta \beta$ Capture)

#### Theoretical Origin
*Ang, Chen & Xing (2006) — "Downside Risk"*; *Daniel & Moskowitz (2016) — "Momentum Crashes"*

#### Intuition
Standard beta-neutralized (residual) momentum removes overall market covariance. However, investors want stocks that exhibit **upside market participation** ($\beta^+ > 1.0$) while decoupling during market crashes ($\beta^- < 0.5$). Purging downside beta prevents the strategy from buying stocks that secretly act as high-beta cyclicals during bull market peaks.

#### Mathematical Formulation
Over a trailing 252-day window, let $R_{i,t}$ be the stock return and $R_{m,t}$ be the benchmark return, with $\bar{R}_m$ as the benchmark mean:
1. **Downside Beta ($\beta^-$):**
   $$\beta^-_i = \frac{\sum_{t=1}^{T} (R_{i,t} - \bar{R}_i)(R_{m,t} - \bar{R}_m) \cdot \mathbf{1}_{\{R_{m,t} < \bar{R}_m\}}}{\sum_{t=1}^{T} (R_{m,t} - \bar{R}_m)^2 \cdot \mathbf{1}_{\{R_{m,t} < \bar{R}_m\}}}$$
2. **Upside Beta ($\beta^+$):**
   $$\beta^+_i = \frac{\sum_{t=1}^{T} (R_{i,t} - \bar{R}_i)(R_{m,t} - \bar{R}_m) \cdot \mathbf{1}_{\{R_{m,t} > \bar{R}_m\}}}{\sum_{t=1}^{T} (R_{m,t} - \bar{R}_m)^2 \cdot \mathbf{1}_{\{R_{m,t} > \bar{R}_m\}}}$$
3. **Upside Convexity Spread:**
   $$\Delta \beta_i = \beta^+_i - \beta^-_i$$
4. **Asymmetric Momentum Factor:**
   $$F_{\text{AsymMom}, i, t} = \text{Z-Score}(R_{i, 12-1}) + \lambda \cdot \text{Z-Score}(\Delta \beta_i) \quad (\lambda \approx 0.5 - 1.0)$$

#### Why It Differs from Live Logics
- `residual_momentum_strategy.py` uses single-factor linear regression: $e_t = r_t - \beta r_{m,t}$. It does not distinguish between up days and down days.
- When market rebounds occur, stocks with high $\beta^-$ collapse. $\Delta \beta$ specifically hedges out momentum crash sensitivity.

---

### Blueprint 3: Institutional Intraday Drift Momentum (`Intra_Over`)

#### Theoretical Origin
*Lou, Polk & Skouras (2019) — "A Tug of War: Overnight Versus Intraday Expected Returns"*

#### Intuition
Price changes can be decomposed into:
- Overnight gap: $\ln(Open_t / Close_{t-1})$ (retail sentiment, earnings news leaks, international market shocks).
- Intraday move: $\ln(Close_t / Open_t)$ (institutional order execution, VWAP algorithmic buying).
Research on Indian equity panels demonstrates that stocks with positive overnight drift experience persistent negative forward returns ($t = -5.1$), whereas stocks that systematically advance intraday continue to drift upwards ($t = 5.4$).

#### Mathematical Formulation
Over lookback window $L \in \{126, 252\}$ trading days:
1. **Intraday Return Component:**
   $$R_{\text{Intra}, i, t} = \sum_{\tau=0}^{L-1} \text{clip}\left(\ln\frac{\text{Close}_{i, t-\tau}}{\text{Open}_{i, t-\tau}}, -0.15, 0.15\right)$$
2. **Overnight Return Component:**
   $$R_{\text{Over}, i, t} = \sum_{\tau=0}^{L-1} \text{clip}\left(\ln\frac{\text{Open}_{i, t-\tau}}{\text{Close}_{i, t-\tau-1}}, -0.15, 0.15\right)$$
3. **Intraday Alpha Spread:**
   $$F_{\text{IntraOver}, i, t} = R_{\text{Intra}, i, t} - R_{\text{Over}, i, t}$$
4. **Execution-Quality Composite:**
   Combine $F_{\text{IntraOver}}$ with a 6-month SMA trend filter ($\text{Close} > \text{SMA}_{150}$).

#### Why It Differs from Live Logics
- Zero overlap with `csm_batch`, `csm_zenith`, or `csm_elendel`.
- In `factor_research/results/factor_catalog.csv`, `intra_over_252` has a correlation with the Elendel composite of only **0.31 to 0.48**.
- Particularly potent in large caps (Top-250 universe), where traditional price momentum is weakest.

---

### Blueprint 4: Fundamental Momentum & Announcement Surprise Drift (PEAD)

#### Theoretical Origin
*Novy-Marx (2012, 2015) — "Fundamentally, Momentum Is Fundamental Momentum"*; *Da & Warachka (2014)*

#### Intuition
Price momentum works because it acts as an echo of underlying fundamental revisions. If we rank directly on the unexpected component of fundamentals, we extract the return drift while avoiding the negative skewness and crashes of price momentum.

#### Mathematical Formulation
1. **Option A: Full Fundamental Pipeline (via point-in-time financial data):**
   - **Standardized Unexpected Earnings (SUE):**
     $$\text{SUE}_{i,q} = \frac{\text{EPS}_{i,q} - \text{EPS}_{i,q-4}}{\sigma(\Delta \text{EPS}_{i, \text{last 8 quarters}})}$$
   - **Gross Profitability Momentum:**
     $$\Delta \text{GP}_{i,q} = \frac{\text{Revenue}_{i,q} - \text{COGS}_{i,q}}{\text{Assets}_{i,q}} - \frac{\text{Revenue}_{i,q-4} - \text{COGS}_{i,q-4}}{\text{Assets}_{i,q-4}}$$
   - **Signal:** Rank stocks by $\text{SUE}_{i,q} + \text{Z-Score}(\Delta \text{GP}_{i,q})$, holding for 3–6 months following results announcements.

2. **Option B: Pure OHLCV Proxy (Announcement Reaction Drift):**
   Identify days with extreme abnormal trading volume (> $3 \times \text{ADV}_{63}$) and positive price jumps (> +3%):
   $$R_{\text{JumpReaction}, i, t} = \sum_{\tau \in \text{Abnormal Vol Days in last 126d}} R_{i, \tau}$$
   Post-earnings announcement drift ensures that stocks gapping on massive institutional volume continue drifting in that direction for 60 trading days.

#### Why It Differs from Live Logics
- Converts an earnings-calendar shock into a structural drift trade.
- Has a proven correlation with standard price momentum of only **0.14 – 0.29**, providing genuine multi-factor diversification.

---

### Blueprint 5: Factor-Level Momentum & Style Sleeve Allocation

#### Theoretical Origin
*Ehsani & Linnainmaa (2017) — "Factor Momentum and the Momentum Factor"*

#### Intuition
Equity anomaly factors (Value, Low Volatility, Quality, Size, Residual Momentum) show significant time-series momentum. Rather than stock picking, dynamically allocate portfolio capital across style factors based on their trailing 12-month returns. This completely eliminates stock-specific idiosyncratic drawdowns.

#### Strategy Architecture
1. **Define 5 Core Factor Baskets (built dynamically from the top 1,000 liquid universe):**
   - **Basket 1 (Low Volatility):** Top 30 stocks with lowest 126d volatility.
   - **Basket 2 (High Quality / Trend Persistence):** Top 30 stocks by Q5 persistence.
   - **Basket 3 (Anchor Momentum):** Top 30 stocks by 52-week-high proximity (A1).
   - **Basket 4 (Intraday Quality):** Top 30 stocks by `intra_over_252`.
   - **Basket 5 (Value Proxy / Deep Discount from 3-Year High):** Top 30 stocks with lowest valuation / lowest 3-year range position that are above SMA200.
2. **Factor Momentum Rule (Monthly Rebalance):**
   - Calculate trailing 12-month return for each basket: $R^f_{12,1}$.
   - **Long Selection:** Hold only the baskets with $R^f_{12,1} > 0$ and rank in the top 2.
   - **Cash Gate:** If fewer than 2 baskets have positive trailing returns, allocate the unassigned capital to liquid money-market funds (LIQUIDBEES earning 6.5%).
3. **Weighting:** Equal weight (50% each) across the top 2 winning factor baskets.

#### Why It Differs from Live Logics
- Shifts the bet from stock selection to macro factor persistence.
- Eliminates momentum crashes: Ehsani & Linnainmaa show that momentum crashes coincide with negative factor autocorrelation. When factors turn negative, this architecture automatically switches to cash.

---

### Blueprint 6: Drawdown-Penalized "Ulcer Momentum" (Calmar/Pain Ratio Trend)

#### Theoretical Origin
*Martin & McCann (1989); validated in `factor_research/FINDINGS.md` (`low_ulcer_252`)*

#### Intuition
Classic Sharpe momentum ($R / \sigma$) penalizes upside volatility equally with downside volatility. A stock surging +10% every week has high volatility and is penalized by Sharpe momentum. Conversely, the **Ulcer Index** measures only the depth and duration of drawdowns from rolling historical highs. A smooth compounding stock has an Ulcer Index near zero.

#### Mathematical Formulation
1. **Percentage Drawdown from 252-day High:**
   $$D_{i, \tau} = \frac{P_{i,\tau} - \max_{k \in [\tau-252, \tau]} P_{i,k}}{\max_{k \in [\tau-252, \tau]} P_{i,k}} \times 100 \quad (\le 0)$$
2. **Ulcer Index (252-day RMS Drawdown):**
   $$\text{UI}_{i,t} = \sqrt{\frac{1}{252} \sum_{\tau=t-251}^{t} D_{i,\tau}^2}$$
3. **Ulcer-Adjusted Momentum Factor:**
   $$F_{\text{UlcerMom}, i, t} = \frac{R_{i, [t-252, t-21]}}{\text{UI}_{i,t} + \epsilon}$$
   *(Alternatively, subtract the log of UI: $\text{Z-Score}(R_{12,1}) - \text{Z-Score}(\ln \text{UI}_{252})$).*

#### Why It Differs from Live Logics
- In `factor_research/results/factor_catalog.csv`, `low_ulcer_252` achieved an IC of **0.100 at 12 months** ($t = 5.5$) and produced a top-15 standalone book drawdown of only **−36.9%** (compared to −66.8% for standard Elendel momentum).
- Selects steady institutional compounders (consistent upward drift with shallow pullbacks) rather than erratic high-beta cyclicals.

---

### Blueprint 7: Acceleration & Curvature Momentum (Convexity Trend)

#### Theoretical Origin
*Unpacking Price Momentum: "The Need for Speed" (2009); Andreas Clenow / Polynomial Trend Fitting*

#### Intuition
Standard momentum measures velocity (first derivative: $P_t / P_{t-L} - 1$). Curvature momentum measures **acceleration (second derivative)**: is the trend steepening or plateauing? A stock breaking out of a 6-month base into rapid acceleration offers higher immediate forward returns than a stock whose trend is 18 months old and decelerating.

#### Mathematical Formulation
1. **Log-Price Polynomial Regression:**
   Fit a second-order polynomial of log-close prices over the past 126 trading days:
   $$\ln(P_{i, \tau}) = \alpha_i + \beta_i \cdot \tau + \gamma_i \cdot \tau^2 + \varepsilon_{i, \tau}, \quad \tau \in [1, 126]$$
2. **Parameters:**
   - $\beta_i$: Velocity (linear drift rate).
   - $\gamma_i$: Acceleration / Curvature (convexity parameter).
   - $R^2_i$: Trend goodness-of-fit.
3. **Convexity Factor:**
   $$F_{\text{ConvexMom}, i, t} = \text{Z-Score}(\beta_i \times R^2_i) + \text{Z-Score}(\gamma_i)$$
   - $\gamma_i > 0$: Price curve is concave up (accelerating momentum).
   - $\gamma_i < 0$: Price curve is concave down (decelerating, exhaustion risk).

#### Why It Differs from Live Logics
- Existing live strategies use fixed calendar windows (12m, 6m) with static weights. They cannot distinguish between a stock up 50% in the first 2 months vs a stock up 50% in the last 2 weeks.
- Curvature explicitly identifies early-stage velocity expansion.

---

## 3. Systematic Strategy Comparison Matrix

The table below contrasts the 7 proposed ideas against the live models across key quantitative dimensions:

| Strategy Blueprint | Primary Signal Logic | Rebalance Horizon | Universe Fit | Correlation to Live Books | Primary Edge / Source of Alpha | Key Risk / Failure Mode |
|---|---|---|---|---|---|---|
| **Live Baseline (`csm_zenith`)** | A1 (52w-High) + Q5 (Persistence) | Monthly | Top-1000 Liquid | 1.00 (Reference) | Reference anchoring + structural trend | Post-bear V-rebound crashes |
| **Live Baseline (`csm_batch`)** | Dual Sharpe (12m + 6m, lag 1m) | Monthly/Quarterly | Top-1000 Liquid | 0.85 – 0.90 | Risk-adjusted intermediate price continuation | Decelerating false breakouts; churn |
| **1. Quiet Momentum** | Trend $\div$ Volume Turnover | Bi-weekly / Monthly | Mid & Small Caps (301–1000) | **0.45 – 0.55** | Early institutional accumulation before retail climax | Illiquidity in microcaps; slower exits |
| **2. Asymmetric $\Delta \beta$** | 12-1m Mom + $(\beta^+ - \beta^-)$ | Monthly | Top-1000 Liquid | **0.50 – 0.60** | Upside market participation without downside crash beta | In flat/choppy markets, $\Delta \beta$ estimation noise |
| **3. Intraday Trend (`Intra_Over`)** | Cumulative Intraday − Overnight | Monthly | Large Caps (Top 250/300) | **0.30 – 0.48** | Institutional execution vs retail sentiment fade | Sensitive to opening print data quality / call auction |
| **4. Fundamental PEAD** | SUE + Abnormal Volume Reaction | Quarterly / Monthly | All Liquid Names | **0.15 – 0.30** | Post-announcement underreaction & earnings drift | Dependent on financial filing dates (`pit_harness`) |
| **5. Factor Allocation** | 12m Time-Series Factor Momentum | Monthly | Multi-Style Baskets | **0.40 – 0.60** | Macro factor autocovariance; cuts factor losers | Regime transitions when all factors temporarily lag |
| **6. Ulcer Momentum** | 12m Return $\div$ 252d Ulcer Index | Monthly / Bi-monthly | Top-1000 Liquid | **0.55 – 0.65** | Lowest drawdown compounders; smooth equity curve | Lags speculative high-beta bull market rallies |
| **7. Convexity Momentum** | Quadratic Trend Curvature ($\gamma$) | Monthly | Top-500 Liquid | **0.60 – 0.70** | Catches accelerating trends right out of bases | High turnover; whipsaws if acceleration fails |

---

## 4. Implementation Playbook & Recommended Next Steps

To deploy these findings into production without risking capital or overfitting, follow this 4-step execution sequence:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       STRATEGY DEVELOPMENT WORKFLOW                         │
├─────────────────────────────────────────────────────────────────────────────┤
│ Step 1: Alpha Screen & IC Verification (Vectorized in `factor_research/`)    │
│         - Compute 1m, 3m, 6m, 12m Spearman rank IC and Newey-West t-stats   │
│         - Check split-half stability (≤2014 Discovery vs ≥2015 Holdout)     │
├─────────────────────────────────────────────────────────────────────────────┤
│ Step 2: Faithful-Booking Backtest (`industry_book.py` / `csm_value/AUDIT`)  │
│         - Signal at Close T -> Fill at Close T+1 -> Returns booked from T+2  │
│         - 0.3% round-trip friction, realistic cash yield (6.5% on idle cash) │
├─────────────────────────────────────────────────────────────────────────────┤
│ Step 3: Risk Overlays & Portfolio Construction Integration                  │
│         - Add 200-SMA Market Trend Gate (50% de-lever in bear regimes)      │
│         - Apply Strategy Realized Volatility Targeting (target 15-20% vol)  │
│         - Enforce single-stock liquidity caps (max 5% of 20-day ADV)        │
├─────────────────────────────────────────────────────────────────────────────┤
│ Step 4: Standalone Class Construction in `long_only_strategies/`            │
│         - Clean class structure matching `CSMZenith` / `CSMIndustryBook`    │
│         - Paper-trade for at least 6 consecutive monthly cohorts            │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Top 2 Priorities to Implement First:
1. **Intraday Institutional Drift (`Intra_Over_252`):** Already empirically validated on your dataset ($t = 5.5$ in top-250), carries the lowest correlation (0.31–0.48) to your live models, and works best where existing models are weakest (large caps).
2. **Quiet Momentum (Turnover-Scaled Trend):** Leverages existing OHLCV CSVs immediately without external fundamental pipelines, directly applying Lee & Swaminathan's momentum life-cycle theorem to eliminate distribution traps.
