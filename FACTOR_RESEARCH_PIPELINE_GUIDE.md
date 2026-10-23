# Indian Market Factor Research & Implementation Pipeline Guide

**Date:** 2026-10-20  
**Scope:** Architecture and standard operating procedure for computing Information Coefficient (IC), Information Ratio (ICIR), Newey-West t-stats (NW-t), and Horizon Decay on the Indian stock universe (5,000+ symbols, ETFs, and Indices).  
**Runner Script:** [`evaluate_new_momentum_factors.py`](file:///Users/hemantsoni/Documents/long_only_strategies/factor_research/evaluate_new_momentum_factors.py)  
**Core Framework Modules:**  
- Data ingestion & caching: [`data.py`](file:///Users/hemantsoni/Documents/long_only_strategies/factor_research/data.py)  
- Factor definitions: [`factors.py`](file:///Users/hemantsoni/Documents/long_only_strategies/factor_research/factors.py)  
- Statistical evaluation engine: [`evaluate.py`](file:///Users/hemantsoni/Documents/long_only_strategies/factor_research/evaluate.py)  
- Batch scanner: [`run_scan.py`](file:///Users/hemantsoni/Documents/long_only_strategies/factor_research/run_scan.py)  

---

## 1. The Standard Evaluation Framework (Formulas & Protocol)

Every quantitative factor or entry logic must clear the following statistical hurdle before advancing to a portfolio backtest:

```
Raw Factor Signal F(t) ──► Cross-Sectional Universe Mask U(t) ──► Forward Returns R(t+1 -> t+1+h)
                                                                             │
             ┌───────────────────────────────────────────────────────────────┤
             ▼                                                               ▼
  Spearman Rank IC(t, h)                                          Quantile Sorting
             │                                                               │
             ├─► Mean IC & ICIR (Mean / Std)                                 ├─► Top 20% Excess vs Market
             ├─► Newey-West t-stat (lag = h - 1)                             ├─► Q5 - Q1 Spread
             ├─► Hit Rate (% months IC > 0)                                  └─► Win-Rate vs Universe Median
             ├─► Discovery (<=2014) vs Holdout (>=2015)
             └─► Incremental IC vs Live Baseline (Elendel / Zenith)
```

### 1.1 Forward Return Horizon & Execution Realism
To prevent lookahead bias and reflect real execution dynamics in Indian equities:
- **Signal Observation ($t$):** Evaluated at the **month-end close**.
- **Execution ($t+1$):** Fills occur at the **next trading day's close** (T+1 execution lag, conservative proxy).
- **Forward Horizon ($h$):** Measured across $h \in \{1, 2, 3, 6, 12\}$ months:
  $$R_{i, t, h} = \exp\left( \ln P_{i, \text{entry}(t+h)} - \ln P_{i, \text{entry}(t)} \right) - 1$$
- **Data Cleaning:** Unadjusted corporate action spikes ($R < -40\%$ or $R > +300\%$) are masked to 0.0 to prevent bad prints from corrupting rank correlations.

### 1.2 Spearman Rank Information Coefficient (IC)
Each month $t$, we compute the rank correlation between the cross-sectional factor values $F_{i,t}$ and the forward returns $R_{i,t,h}$:
$$\text{IC}_{t, h} = \frac{\sum_{i=1}^N (r_{i, F} - \bar{r}_F)(r_{i, R} - \bar{r}_R)}{\sqrt{\sum (r_{i, F} - \bar{r}_F)^2 \sum (r_{i, R} - \bar{r}_R)^2}}$$
- **Rule of Thumb:** Mean $\text{IC} > 0.03$ is tradeable; $\text{IC} > 0.07$ is strong.

### 1.3 Newey-West Autocorrelation-Adjusted t-Statistic (NW-t)
Because forward returns overlap for horizons $h > 1$ (e.g., 3-month returns sampled monthly), standard error of the mean IC is severely underestimated by classic t-tests ($t = \frac{\mu}{\sigma / \sqrt{N}}$). The Newey-West estimator corrects for this serial correlation:
$$S = \gamma_0 + 2 \sum_{j=1}^{h-1} \left(1 - \frac{j}{h}\right) \gamma_j, \quad \text{SE}(\bar{\text{IC}}) = \sqrt{\frac{S}{N}}, \quad t_{\text{NW}} = \frac{\bar{\text{IC}}}{\text{SE}(\bar{\text{IC}})}$$
- **Hurdle:** A valid signal must achieve $t_{\text{NW}} \ge 3.0$ on the full panel.

### 1.4 Horizon Period & Factor Decay Curve
Plotting $\text{IC}_h$ across $h = 1, 2, 3, 6, 12$ months determines the natural holding period:
- **Peak Horizon (`peak_h_ic`):** The forward window where IC reaches its maximum.
- **Fast vs Slow Factors:** Signals peaking at 1 month with fast decay (e.g., short-term reversal or tightness) require monthly rebalancing; signals peaking at 6–12 months (e.g., 52-week-high proximity, trend persistence) support low-turnover quarterly or staggered rebalancing.

### 1.5 Discovery vs Holdout Split
Every factor is strictly audited across two independent regimes:
- **Discovery Period ($\le 2014$):** 2003 – 2014 bull/bear/rebound cycles.
- **Holdout Period ($\ge 2015$):** 2015 – 2026 out-of-sample window.
- **Hurdle:** The factor must be positive in both sub-periods. Factors that show $\text{IC} > 0.10$ before 2014 but turn negative after 2015 are rejected.

### 1.6 Incremental IC vs Live Baseline (`corr_elendel`)
A factor may have an IC of 0.08, but if its cross-sectional rank correlation with your live book (`csm_elendel` / `csm_zenith`) is 0.90, it adds zero new value.
- Regress factor ranks on live baseline ranks: $F_t^{\text{rank}} = \alpha + \beta B_t^{\text{rank}} + \varepsilon_t$.
- Compute **Incremental IC** as the rank correlation between residual $\varepsilon_t$ and forward return $R_{t,h}$.
- **Hurdle:** Incremental $\text{IC} > 0$ with incremental $t_{\text{NW}} > 2.0$.

---

## 2. Tested Universes for Indian Equities

The pipeline applies four distinct liquidity and quality filters (defined in `evaluate.build_universes`):
1. **`U1_liquid1000`:** Price $> ₹20$, top-1,000 by 63-day median daily traded value, $\le 5$ circuit-locked days ($H = L$) in the last 63 trading days (averages ~700 names/month).
2. **`U2_live_trend`:** $U1 \cap \text{Close} > \text{SMA}_{200}$ (matches the exact pool ranked by your live momentum books).
3. **`U3_top300`:** Price $> ₹20$, top-300 most liquid names by median daily traded value (large/mid-cap institutional capacity).
4. **`U2z_zenith_univ`:** $U2$ with the top 20% highest 21-day single-day spikes excluded (Low-MAX M3 filter).

---

## 3. How to Run the Evaluation Runner

The standalone script [`evaluate_new_momentum_factors.py`](file:///Users/hemantsoni/Documents/long_only_strategies/factor_research/evaluate_new_momentum_factors.py) computes all these metrics for the novel factor blueprints:

```bash
cd /Users/hemantsoni/Documents/long_only_strategies/factor_research
python3 evaluate_new_momentum_factors.py
```

### What It Outputs:
- Detailed CSV reports per universe:
  - `factor_research/results/new_factors_U1_liquid1000.csv`
  - `factor_research/results/new_factors_U2_live_trend.csv`
  - `factor_research/results/new_factors_U3_top300.csv`
- Master summary comparison: `factor_research/results/master_new_factors_summary.csv`

---

## 4. How Data Ingestion & Caching Works

The source data in `/Users/hemantsoni/Documents/upstox_data_folder/ohlcv_data` contains 5,200+ stock CSVs. To avoid parsing thousands of CSVs repeatedly, `data.py` converts them into aligned, memory-efficient Parquet files in `factor_research/.cache/`:
- `close.parquet`, `open.parquet`, `high.parquet`, `low.parquet`, `volume.parquet`
- `index_data_close.parquet`, `etf_ohlcv_data_close.parquet`

If you ever add new CSVs or want to update the history to the latest date:
```bash
cd /Users/hemantsoni/Documents/long_only_strategies/factor_research
python3 data.py   # Rebuilds the parquet panels in ~20 seconds
```
*(Requires a Python environment with `pandas`, `numpy`, and `pyarrow` installed).*
