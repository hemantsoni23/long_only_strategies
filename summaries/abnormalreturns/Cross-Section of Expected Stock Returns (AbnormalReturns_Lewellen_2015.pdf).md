# The Cross-Section of Expected Stock Returns — Lewellen (2015) — Detailed Quantitative Research Notes

## Bibliographic Header

| Field | Detail |
|------|--------|
| **Title** | The Cross-section of Expected Stock Returns |
| **Author** | Jonathan Lewellen (Dartmouth College and NBER) |
| **Journal** | *Critical Finance Review*, 2015, Vol. 4, pp. 1–44 |
| **DOI** | 10.1561/104.00000024 |
| **Sample** | CRSP common stocks merged with Compustat annual; 1964–2013 (forecast tests 1974–2013); subgroups: all-but-tiny (> NYSE 20th pct ME), large (> NYSE median) |
| **Method** | Out-of-sample expected returns = past Fama–MacBeth slopes × current characteristics |
| **Source file** | `Finance/AbnormalReturns_Lewellen_2015.pdf` |
| **Drive file_id** | `0B-6kBz0I0dMsQmJidFZOQm9Jd3c` |

---

## Question

Many characteristics are significant in-sample, but two practical questions are open: (1) how much cross-sectional variation in expected returns can be predicted *in real time*, and (2) are FM-based expected-return estimates unbiased, i.e. do realized returns load on them with slope one? Portfolio sorts (one or two pre-chosen characteristics) and standard FM tests answer neither. The exercise also mimics an investor who did not know ex ante which of many candidate characteristics would work, and offers characteristic-based cost-of-equity estimates as an alternative to implied cost of capital and to CAPM/FF3 (Fama–French 1997, Simin 2008, Levi–Welch 2014). Closest antecedents: Haugen–Baker (1996), Hanna–Ready (2005), which use 1-year slope windows and short-lived predictors (1-month reversal) and study trading profits, not forecast accuracy.

## Data and specifications

All predictors are slow-moving (levels or flows over at least a year). Market data are used immediately; accounting data with a 4-month lag. Characteristics (not returns) are winsorized at 1/99 monthly. Stocks need size, B/M, and 12-month momentum. Breakpoints at end-2013: NYSE 20th pct $693m, median $2,757m. All-but-tiny is roughly half the sample (avg N ≈ 1,706 of 3,955), large roughly a quarter (876).

- **Model 1:** LogSize, LogB/M, Return$_{-2,-12}$.
- **Model 2:** + LogIssues$_{-1,-36}$, Accruals (Sloan), ROA, LogAG.
- **Model 3 (15 vars):** + DY, LogReturn$_{-13,-36}$, LogIssues$_{-1,-12}$, Beta$_{-1,-36}$ (weekly), StdDev$_{-1,-12}$ (daily), Turnover$_{-1,-12}$, Debt/Price, Sales/Price.

B/M uses the *latest* market equity (monthly-updated), not the Fama–French June/December convention.

## Method

Monthly FM regressions $r_{i,t} = a_t + g_t' X_{i,t-1} + e_{i,t}$, 596 months (1964:05–2013:12), NW(4) t-stats. Forecast for month $t$:
$$F_{i,t} = \bar a_{t-1} + \bar g_{t-1}' X_{i,t-1},$$
with $\bar g$ the 10-year rolling (primary) or cumulative-since-1964 average of past slopes (also 1-, 3-, 5-, 7-year windows). Validation: out-of-sample FM regression of $r_{i,t}$ on $F_{i,t}$; an unbiased forecast has slope $b = 1$. Decile sorts on $F$ give an economic reading.

**Interpretation of $b$ (fn. 3).** Relative to a null forecast equal to the cross-sectional mean $\bar F$, $\mathrm{MSE}(\bar F) - \mathrm{MSE}(F) = (2b-1)\,\mathrm{var}_{cs}(F)$, so $F$ beats the null iff $b > 0.5$. For the shrinkage forecast $\bar F + s(F - \bar F)$ the MSE gain is $(2bs - s^2)\mathrm{var}_{cs}(F)$, maximized at $s = b$. The predictive slope is therefore the optimal shrinkage weight, and $b>0$ means some weight on $F$ helps.

## Results

### In-sample FM slopes (Table 2, monthly %, all stocks)

| | Model 1 | Model 2 |
|---|---|---|
| LogSize | −0.13 (t −2.80) | −0.13 (−3.38) |
| LogB/M | 0.54 (7.07) | 0.44 (6.26) |
| Mom | 1.06 (5.70) | 0.88 (5.32) |
| Issues36 | | −0.39 (−3.77) |
| Accruals | | −1.44 (−5.66) |
| ROA | | 1.34 (2.54) |
| LogAG | | −0.78 (−6.40) |

Size, B/M and AG are weaker among larger stocks; issuance and ROA stronger (ROA 2.57, t 4.38 in all-but-tiny). In Model 3 only beta is at least marginally significant in all three groups (t 1.73–3.05, positive); StdDev is strongly negative for all-but-tiny/large (t −4.63/−3.76) but not all stocks; Turnover (−3.68) and Sales/Price (3.10) matter only in the full sample; DY, long-term reversal, 12m issuance and Debt/Price are insignificant (t between −1.38 and 0.65).

- **Timely B/M matters:** using FF-style B/M lowers the Model 1 slopes from 0.54 to 0.31 (B/M) and 1.06 to 0.74 (momentum), because timely B/M is more negatively correlated with momentum, so each hedges the other.
- **2009:** dropping it raises the momentum slope to 1.24; the April 2009 monthly slope was −33.58, and the 2009 average −7.41 (losers rebounded).
- **Slope decay:** 10-year rolling slopes (Figure 1) shrink toward zero over time but rarely change sign, which anticipates forecasts that are too dispersed.
- **FM R² is not predictive power:** it measures contemporaneous variance explained by characteristic portfolios. In a world where the CAPM holds exactly with no idiosyncratic risk and all expected returns are equal, beta has FM R² of one and zero predictive power. The appropriate pooled, demeaned R² is 0.0012–0.0024, 20–50 times below FM R².

### Distribution and predictive slopes of monthly forecasts (Table 3, 1974–2013)

| Sample | CS std of $F$ (rolling, M1/M2/M3) | Predictive slope, rolling M1/M2/M3 | Cumulative M1/M2/M3 |
|---|---|---|---|
| All | 0.76 / 0.80 / 0.87 | 0.77 / 0.80 / 0.74 | 0.82 / 0.81 / 0.63 |
| All-but-tiny | 0.51 / 0.58 / 0.63 | 0.62 / 0.64 / 0.57 | 0.61 / 0.67 / 0.68 |
| Large | 0.44 / 0.48 / 0.53 | 0.66 / 0.65 / 0.44 | 0.60 / 0.71 / 0.72 |

t-statistics are 8.6–13.4 for all stocks and 3.6–7.2 for the subsamples. Slopes are reliably below one (minimum t of 2.45 against one for all stocks, 2.08 for the subsamples). The p10–p90 range is roughly 0.3% to 2.1% monthly for all stocks, a spread of about 2%/month; low-end forecasts for many large stocks are at or below the T-bill rate (0.41%/month average). Implied shrinkage toward the cross-sectional mean is about 20–35%. Estimation noise in slopes explains only 0.05–0.06 pp of forecast std for Models 1–2 (0.09–0.13 for Model 3; fn. 2), slightly less than the errors-in-variables reading of the slopes; the rest reflects slope drift. The composite forecast is a stronger predictor than any single characteristic.

### Model comparison (Table 4)

Forecast correlations across models are 0.65–0.87. The Model 2 residual on Model 1 has std 0.26–0.38% and predicts returns (slopes 0.67–0.84, t 4.67–6.46): accruals, issuance, ROA and AG add real but modest information. The Model 3 residual on Model 2 is weak (slopes 0.52 / 0.30 / 0.09, t 3.13 / 1.37 / 0.44 for all / all-but-tiny / large), so the extra eight variables add essentially nothing for larger stocks.

### Window length (Table 5)

Even 1-year windows work (slopes 0.36–0.79 across all specifications; 27/36 above 0.5), but shorter windows give more dispersed, noisier forecasts, and longer windows generally do better. Short-window performance partly reflects slope autocorrelation at lag 1 (average 0.10, gone by lag 2). Skipping a month between the estimation window and the forecast month barely affects 10-year forecasts (e.g., 0.77 to 0.76) but hurts 1-year ones (0.70 to 0.56). Dropping 2009–2013 raises 5-year Model 1 slopes substantially (0.59 to 0.74 for all stocks, 0.36 to 0.63 for all-but-tiny).

### Decile portfolios (Tables 6–7, Model 3, 10-year rolling)

| Sample | Pred H–L | Realized EW H–L (t, ann. SR) | Realized VW H–L |
|---|---|---|---|
| All | 3.09 | 2.36 (10.21, 1.65) | 1.54 (t 5.03) |
| All-but-tiny | 2.24 | 1.26 (5.26, 0.85) | 1.16 |
| Large | 1.87 | 1.00 (3.70, 0.61) | 0.93 |

Model 1 gives predicted/realized EW spreads of 2.70/2.19 (all stocks); VW 1.21. Realized/predicted ≈ 0.76, matching the regression slope. Realized returns are nearly monotone in predicted returns. For comparison, the market's excess return was 0.60%/month (SR 0.45). FF3 alphas of H–L are close to raw spreads (EW all 2.32, t 10.46; VW large 1.04, t 3.62), and both legs contribute: large-stock VW top decile +0.53 (t 3.08), bottom −0.51 (t −3.37). Carhart four-factor alphas are smaller: EW 2.04 / 0.68 / 0.43, VW 0.83 / 0.46 / 0.29 (the last insignificant), so much of the large-cap spread is momentum.

### Time variation (Figure 2)

The 10-year rolling predictive slope hovers around 0.8 (all) and 0.6 (larger stocks) until 2008, peaking near one in the early 2000s. Over the final decade (2004–2013) average slopes collapse to 0.38 (all), 0.15 (all-but-tiny), and −0.37 (large); the yearly large-stock slope hits −2.03 in 2009. H–L returns stay positive in that decade (EW 1.20%, VW 0.71%/month). The author cannot tell whether the decline is permanent or a crisis/momentum-crash artifact.

### Longer horizons (Tables 8–9)

Direct FM regressions on 6- and 12-month returns: same signs; B/M, momentum and ROA lose significance, while issuance, accruals, AG (and, in Model 3, DY) become *more* significant (12m, Model 2 all stocks: Accruals −13.77, t −4.98; AG −9.69, t −8.31; Issues −7.46, t −6.70). Alternatively, monthly forecasts are extrapolated assuming geometric mean reversion of the cross-sectional deviation with monthly persistence 0.9 (observed 0.90–0.94):
$$F_{ik} = k\bar F_1 + (1 + 0.9 + \dots + 0.9^{k-1})(F_{i1} - \bar F_1).$$
12-month forecasts have cross-sectional std of 5.4–9.2% (all), 3.6–5.8% (all-but-tiny), and 3.0–5.4% (large). Predictive slopes are 0.54–0.91 (all; t 3.69–8.70), 0.27–0.63 (all-but-tiny), and 0.22–0.68 (large). Model 2 with cumulative slopes is best (0.91, t 8.70, extrapolated); Model 3 rolling for large stocks is worst (0.22). Implied shrinkage: about 10–30% (all), 40–55% (all-but-tiny), 35–60% (large); the conclusion summarizes this as 20–50% for annual forecasts.

## Assessment

- **Convincing:** it is a genuinely real-time test with no look-ahead in variable selection weights. Slopes of 0.6–0.8 with t-stats near 10 are unusually strong out-of-sample evidence, in contrast with time-series equity premium forecasting (Goyal–Welch). The MSE interpretation turns the slope directly into an optimal shrinkage coefficient.
- **Fragile or limited:**
  - The candidate list is chosen with hindsight: Models 1–2 are known winners; only Model 3 imitates ignorance.
  - Predictability in large caps deteriorated sharply after 2004, driven by momentum crashes, and four-factor alphas for large-stock VW spreads are insignificant.
  - No transaction costs; equal-weighted all-stock spreads are dominated by micro-caps.
  - OLS FM slopes are equal-weighted across stocks, so they are driven by small stocks.
  - The shrinkage factors are themselves estimated ex post over the full sample.
  - Linear, additive specification with no interactions.
- **Practical use:**
  - Long-window (10-year or cumulative) averaged FM slopes act as a strong regularizer; 1-year windows chase transitory slope autocorrelation.
  - A lean set (Model 1–2) captures almost all the signal. Extra weak variables add dispersion but not information, especially in large caps.
  - Shrink composite forecasts toward the cross-sectional mean by roughly one minus the OOS slope, and more for large caps and long horizons.
  - Evaluate models by OOS predictive slope or pooled demeaned R², never FM R².
  - Characteristic-based expected returns are a credible cost-of-equity input, with dispersion of about 0.8%/month (all stocks) or 0.5% (large).
  - Use timely B/M jointly with momentum.

## Scholar Tags

`expected-returns`, `Fama-MacBeth`, `out-of-sample`, `cost-of-capital`, `composite-signals`, `shrinkage`, `1964-2013`, `Critical-Finance-Review`.
