# A Now-Casting Model for Canada: Do U.S. Variables Matter?

**Daniela Bragoli & Michele Modugno · 2017 · *International Journal of Forecasting* 33, 786–800 (doi:10.1016/j.ijforecast.2017.03.002) · Source file `Finance/NowcastingDynamicFactorModels_BragoliModugno_2017.pdf` · 17 series (12 Canadian monthly, 4 U.S. monthly, quarterly Canadian GDP); estimation from Jan-1992, pseudo-real-time evaluation 2006Q1–2016Q3**

## Claim / contribution

1. A small, "market-moving" mixed-frequency dynamic factor model (DFM) for Canadian real GDP growth (QoQ) whose accuracy is comparable to the Bank of Canada, OECD and the Bloomberg consensus.
2. Adding four timely U.S. indicators (ISM manufacturing PMI, nonfarm payroll change, industrial production, capacity utilization) improves Canadian nowcasts "dramatically", because Canada lacks timely production data (no IP / capacity-utilization series).
3. A restricted state-space specification that makes Statistics Canada's **monthly GDP** a state variable and links quarterly GDP to it via the Mariano–Murasawa aggregation, instead of treating monthly GDP as a generic indicator.
4. News decomposition of every forecast revision into release surprises × model weights.

Canada-specific motivation: quarterly GDP comes ~60 days after quarter end (vs. ~4 weeks US/UK, ~6 weeks euro area/Japan); monthly GDP comes ~60 days after the month (January GDP available in March). Monthly GDP is at basic prices, quarterly at market prices (incl. net taxes on products), so the two are related but not identical. The U.S. took about 70% of Canada's total trade in 2015.

## Data and release calendar (Table 1)

Variables chosen by market relevance (Bloomberg usage %, Forex Factory L/M/H ratings), not by optimization; prices, financial, nominal and sectoral series are excluded because earlier work found they do not help (Bańbura–Modugno 2014; Luciani 2014).

| Series | Release (day, months after ref. period) | Transformation | Bloomberg relevance |
|---|---|---|---:|
| US ISM manufacturing PMI | day 5, +1 | level | 94.6 |
| US nonfarm payroll change | day 5, +1 | level (thous.) | 99.1 |
| US industrial production | day 15, +1 | Δln MoM | 86.6 |
| US capacity utilization | day 15, +1 | Δ | 60.6 |
| Canada Ivey PMI | day 5, +1 | level | 15.4 |
| Canada employment | day 8, +1 | Δ | 30.8 |
| Canada dwelling starts | day 9, +1 | Δln MoM | 82.0 |
| Canada building permits; imports; exports | day 5, +2 | Δln MoM | 71.8; –; – |
| Canada mfg shipments; mfg orders; motor vehicle sales | day 15, +2 | Δln MoM (vehicles: Δln YoY, not SA) | –; –; 0.0 |
| Canada wholesale; retail sales | day 20, +2 | Δln MoM | 51.3; 74.4 |
| Canada monthly GDP | day 28, +2 | Δln MoM | 84.6 |
| Canada real GDP (quarterly, target) | day 28, +2 | Δln QoQ | 92.3 |

"+2 months, day 5" means roughly a five-week lag (the paper: permits and trade ~5 weeks; sales and orders 6–7 weeks). Start dates differ (Ivey PMI Jan-2001, monthly GDP Jan-1997, wholesale Jan-1993, shipments/orders Jan-1992), so the panel is unbalanced at the start and ragged at the end. Series are standardized after transformation. PMIs enter in levels because the survey question is already a month-on-month comparison.

## Model

Generic DFM (eqs. 1–3), standardized stationary monthly data $y_t$:

$$
y_t=\Lambda f_t+e_t,\qquad f_t=A_1f_{t-1}+\dots+A_pf_{t-p}+u_t,\ u_t\sim N(0,Q),\qquad e_{i,t}=\rho_ie_{i,t-1}+v_{i,t},\ v_{i,t}\sim N(0,\sigma_i^2).
$$

Common and idiosyncratic shocks are uncorrelated at all leads/lags (Doz–Giannone–Reichlin approximate factor model; limited cross-correlation allowed asymptotically, diagonal in the likelihood). Chosen specification: **one factor** (Bai–Ng IC), **VAR(2)** (AIC), AR(1) idiosyncratic terms.

**Canada-specific restriction (Box I / Appendix A.3).** Let $y^m_t$ be monthly GDP growth, $f_t$ the single factor extracted from the other $n-2$ monthly series $x_t$. Then $(y^m_t,f_t)$ follow a bivariate VAR(2),

$$
\begin{bmatrix}y^m_t\\ f_t\end{bmatrix}=\begin{bmatrix}a_{11}&a_{13}\\a_{21}&a_{23}\end{bmatrix}\begin{bmatrix}y^m_{t-1}\\ f_{t-1}\end{bmatrix}+\begin{bmatrix}a_{12}&a_{14}\\a_{22}&a_{24}\end{bmatrix}\begin{bmatrix}y^m_{t-2}\\ f_{t-2}\end{bmatrix}+\begin{bmatrix}u^y_t\\ u^f_t\end{bmatrix},
$$

(coefficient labels as in the printed matrix), with measurement equations

$$
y^m_t = y^m_t\ \text{(observed state)},\qquad x_t=\Lambda_m f_t+e_t,\ e_t=Pe_{t-1}+v_t\ (P\ \text{diagonal}),
$$

$$
y^q_t=\lambda_q\,(y^m_t+2y^m_{t-1}+3y^m_{t-2}+2y^m_{t-3}+y^m_{t-4})+(\epsilon^q_t+2\epsilon^q_{t-1}+3\epsilon^q_{t-2}+2\epsilon^q_{t-3}+\epsilon^q_{t-4}),\qquad \epsilon^q_t=\rho_q\epsilon^q_{t-1}+v^q_t.
$$

So quarterly GDP loads **only** on monthly GDP (one scalar $\lambda_q$ times the fixed 1-2-3-2-1 Mariano–Murasawa weights) plus an aggregated AR(1) discrepancy that absorbs the basic-vs-market-price gap. The factor affects quarterly GDP only through the VAR, i.e. by forecasting unreleased months of monthly GDP. The state stacks five lags each of $y^m$, $f$, $\epsilon^q$ plus $e_t$ (the printed box also carries a redundant zero row).

**Estimation.** Quasi-ML via EM adapted to arbitrary missing-data patterns (Bańbura–Modugno 2014): initialize with OLS on principal-component factors, then iterate Kalman smoother (E-step) and restricted regressions that account for the factors being estimated (M-step) to convergence. Re-estimated recursively in the evaluation; only data available at each date are used.

## News decomposition

With information set $\Omega_v$ and new releases $x_{k_j,t_j}$, $j=1,\dots,J_{v+1}$:

$$
P[y^q_t\mid\Omega_{v+1}]-P[y^q_t\mid\Omega_v]=\sum_{j=1}^{J_{v+1}}b_{v+1,j}\,\underbrace{\big(x_{k_j,t_j}-P[x_{k_j,t_j}\mid\Omega_v]\big)}_{\text{news } I_{v+1,j}} ,
$$

with $B_{v+1}=\mathrm{Cov}(y^q_t,I_{v+1}\mid\Omega_v)\,\mathrm{Var}(I_{v+1}\mid\Omega_v)^{-1}$ (the paper calls eq. 6 a generalization of the Kalman update to asynchronous data). "Impact" of a series is defined as weight × news standard deviation (s.d. rather than mean, since mean news ≈ 0 and to drop the sign). Caveat for implementers: the identity holds for fixed parameters and no data revisions; in a recursive exercise revision and re-estimation effects need separate accounting.

## Evaluation design and benchmarks

- Prediction period per target quarter: first forecast 90 days before the quarter starts, updated at every release until GDP comes out ~150 days after the quarter start → a 240-day window (forecast → nowcast → backcast).
- Real-time vintages from the OECD Real-Time Data and Revisions Database: **8 series effectively real-time** (7 with vintages + unrevised Ivey PMI), **9 series use the last vintage** (revisions ignored). So "real time" is only approximate.
- Benchmarks: (i) same DFM **without** the U.S. series; (ii) a bridge equation (BE): AR model forecasts the missing months of monthly GDP, aggregate to quarterly, then map to quarterly GDP via a regression of quarterly on aggregated monthly GDP; (iii) Bank of Canada MPR (Jan/Apr/Jul/Oct); (iv) OECD Economic Outlook (twice yearly, "March and September" per the paper); (v) Bloomberg survey (published once ≥3 respondents, ~2 weeks before release, revised until 24h before; the Fig. 2 point is the day before the preliminary GDP release).

## Main results

**Fig. 2 (RMSFE vs. days from quarter start):** the model without U.S. data has higher RMSFE than the model with U.S. data at *every* point of the 240-day window; the with-U.S. model is on average as accurate as BoC, OECD and Bloomberg at their dates. Fig. 1: the with-U.S. model tracks the Great Recession collapse much better. No numerical RMSFE table is given (only the graph), and no crisis-excluded result.

**Table 2 — Diebold–Mariano: mean(squared error of benchmark − squared error of with-U.S. model), HAC s.e. in parentheses; positive = U.S. model better; evaluated at the first Canadian release (Ivey PMI) of each month.**

| | Forecast: BE | Forecast: no-US | Nowcast: BE | Nowcast: no-US | Backcast: BE | Backcast: no-US |
|---|---|---|---|---|---|---|
| month 1 | 0.08 (0.06) | 0.05 (0.05) | 0.24 (0.15) | 0.18 (0.12) | 0.04 (0.03) | 0.03 (0.02) |
| month 2 | 0.13 (0.11) | 0.10 (0.10) | 0.30 (0.15) | 0.24 (0.12) | 0.01 (0.01) | 0.00 (0.00) |
| month 3 | 0.11 (0.14) | 0.10 (0.12) | 0.14 (0.08) | 0.09 (0.05) | – | – |

All differences are non-negative; gains are largest in the nowcast phase (month 2 ≈ 2 s.e.), small in the forecast phase and vanishing in the backcast once monthly GDP is in. The paper marks significance in bold (lost in text extraction); t-ratios from the rounded entries are at most ≈2.0.

**Table 3 — Patton–Timmermann (2012) monotonicity tests** (forecast errors $\Delta e\ge0$, mean squared forecast $\Delta f\ge0$, forecast–target covariance $\Delta c\ge0$): p-values 0.5006, 0.4957, 0.4974 → monotone improvement with more information is not rejected.

**Table 4 — model news vs. Bloomberg surprises (mean, s.d.), selected:**

| Series | Model mean | Model s.d. | Bloomberg mean | Bloomberg s.d. |
|---|---:|---:|---:|---:|
| US ISM PMI | −0.182 | 1.865 | 0.026 | 1.755 |
| US nonfarm payrolls (thous.) | −24.862 | 259.530 | 7.977 | 101.579 |
| US capacity utilization | 0.024 | 0.544 | 0.043 | 0.613 |
| Canada Ivey PMI | −0.459 | 7.117 | −0.892 | 6.753 |
| Canada dwelling starts | −0.248 | 9.754 | −0.528 | 12.171 |
| Canada monthly GDP | −0.065 | 0.256 | 0.012 | 0.225 |

The authors' "well-specified" check is only |mean| < 2 s.d. (a scale check, not a test of zero-mean news). The model is comparable to the consensus for most series but clearly worse on payrolls (s.d. 2.5× Bloomberg's). Units are mixed (some growth rates in decimals, e.g. US IP news s.d. 0.008, others in percent).

**Table 7 / Fig. 3 — which releases move the nowcast** (A = avg weight, B = news s.d., C = impact = A·B; months m1/m2/m3 of the nowcast quarter):

| Release | C m1 | C m2 | C m3 | weight A (m1→m3) |
|---|---:|---:|---:|---|
| US ISM PMI | 0.111 | 0.108 | 0.057 | 0.060 → 0.030 |
| US industrial production | 0.102 | 0.060 | 0.048 | 9.814 → 7.327 |
| US capacity utilization | 0.090 | 0.064 | 0.049 | 0.136 → 0.102 |
| US nonfarm payrolls | 0.043 | 0.092 | 0.030 | 0.000 (rounded; units = thousands) |
| Canada employment | 0.061 | 0.058 | 0.035 | 0.001 |
| Canada mfg orders | 0.051 | 0.061 | 0.045 | 0.010 → 0.011 |
| Canada exports | 0.052 | 0.053 | 0.045 | 1.279 → 1.333 |
| Canada mfg shipments | 0.056 | 0.050 | 0.044 | 0.024 → 0.026 |
| Canada Ivey PMI | 0.028 | 0.017 | 0.018 | 0.004 → 0.002 |
| Canada retail sales | 0.003 | 0.005 | 0.004 | 0.337 → 0.386 |
| Canada monthly GDP | 0.064 | 0.084 | **0.169** | 0.236 → 0.319 → 0.721 |
| Canada quarterly GDP | 0.054 (single value) | | | 21.820 |

U.S. data dominate in month 1 (ISM also in month 2); monthly GDP matters only in month 3, when its weight triples. The Ivey PMI, despite high Forex relevance, carries little information; retail sales almost none.

## Model selection (Appendix A.1)

Bai–Ng IC for 1–4 factors: sample 1 (balanced 2001Q1–2005Q4, N=15, T=59) 0.15/0.24/0.43/0.58; sample 2 (N=14, T=156) 0.18/0.33/0.56/0.77; sample 3 (N=14, T=285, includes the evaluation period) 0.13/0.25/0.46/0.68 → one factor everywhere. AIC for VAR lags 1–4: −1.55/−1.98/−1.84/−1.95 → 2 lags (narrowly over 4). Inconsistency: the prose says sample 2 has "15 observations", the table says T=156. Sample 3 uses evaluation-period data, so it is not a purely ex-ante choice.

## Critical assessment

- **Convincing:** the timing mechanism. The U.S. gain is concentrated where theory says it should be (early in the quarter, before Canadian hard data), and vanishes in the backcast. The monthly-GDP restriction is a neat, parsimonious way to use a partial measurement of the target.
- **Fragile / caveats:** (i) statistical evidence is modest — 43 quarters, DM t-ratios ≤ ~2, much of the RMSFE gap plausibly driven by 2008–09; (ii) 9 of 17 series use final vintages, which flatters any model relative to BoC/OECD/Bloomberg; (iii) comparison with institutional forecasts is only graphical, with forecasts made at very different dates and information sets; (iv) no sensitivity of results to the factor count or lag order, to the market-relevance selection rule, or to adding other U.S. series (e.g. retail sales, which prior Canadian models used); (v) EM tolerances, BE lag order, HAC kernel/bandwidth and the GDP vintage used as "out-turn" are not reported, so exact replication needs code.
- "Model forecasts as good as professionals" rests on average accuracy in a small sample; the authors' stronger conclusion that judgmental soft information adds little is not formally tested.

## Practical relevance for a quant PM

- A clean template for a release-aware macro signal: store both reference and release dates, run one joint state-space model, and attribute each revision to surprises. Surprise × weight gives an ex-ante map of which prints should move the GDP nowcast (for Canada: ISM, U.S. IP, capacity utilization and payrolls early in the quarter; monthly GDP late).
- Cross-border information flow: for small open economies tightly linked to a larger one (Canada, Mexico), the larger economy's timely data can front-run domestic data — relevant for CAD rates/FX and Canadian equity sector views, though the paper provides no trading evidence.
- Model news can be benchmarked against consensus (Bloomberg) surprises; the model is not systematically better at predicting individual releases, so its value lies in aggregation, not in beating the consensus release by release.
