# Momentum Investing and Business Cycle Risk: Evidence from Pole to Pole

**John M. Griffin, Xiuqing Ji, J. Spencer Martin · 2003 · *Journal of Finance* 58(6), 2515–2547 · Source file `Finance/AbnormalReturnsMomentum_Griffin_2003.pdf` · 40 countries: US CRSP NYSE/AMEX from 1926, plus 39 Datastream markets with ≥50 stocks (10 from 1975, 23 by 1990), ending Dec 2000; local-currency returns**

## Claim
If momentum were a premium for macroeconomic or business-cycle risk, it should co-move across integrated markets, load on macro factors, be forecast by macro instruments, and lose money in bad states. Internationally none of these holds. Momentum (i) barely correlates across countries, (ii) is unrelated to the Chen–Roll–Ross (CRR) factors, (iii) is not captured by the Chordia–Shivakumar (2002) conditional forecasting model, (iv) is positive in both good and bad GDP and market states, and (v) **reverses** within 1–2 years, including outside January. Point (v) is inconsistent with existing risk-based models (Conrad–Kaul, Berk–Green–Naik, Johnson) and more in line with behavioural ones.

## Strategy
The 6/6 strategy with a one-month skip: rank on months $t-7\ldots t-2$, go long the top quintile and short the bottom quintile, equal-weighted, and hold for $t\ldots t+5$ with six overlapping vintages. Quintiles are used because many markets are small; deciles are used for the US, UK and Japan in some tests. A no-skip variant (rank $t-6\ldots t-1$) is used to compare with Moskowitz–Grinblatt and Chordia–Shivakumar. Regional series are equal-weighted averages of country WML series.

## 1. Momentum around the world (Table I; %/month)
| | Skip (t−7..t−2) | No skip | Since 1990 |
|---|---|---|---|
| Africa (2 mkts) | 1.63 | 1.42 | – |
| Americas ex-US | 0.78 | 0.50 | 0.42 |
| Asia | 0.32 (insignificant) | 0.13 | 0.02 |
| Europe | 0.77 (≈9.24% p.a.) | 0.70 | 0.61 |
| US (1926–2000) | 0.59 (t≈3.3) | | |
| Developed ex-US | 0.73 (8.74% p.a.) | | 0.59 |
| Emerging | 0.27 (insignificant) | | |

- The mean is positive in 2/2 African, 5/6 American, 10/14 Asian and 14/17 European markets. Japan is ≈0 (0.02, t≈0.1).
- Relative to the local index, winners *and* losers often outperform (a small-stock effect). In Europe, losers underperform.
- Momentum has not died out since 1990 (developed-market average 0.59%).

**Co-movement (Table II).** Average intraregional pairwise correlation of country WML: Africa 0.012, Americas 0.077, Asia 0.106, Europe 0.088. Average interregional pairwise correlation is 0.032 (highest US–Europe, 0.139); regional-index pairs average 0.103. By contrast, market indices correlate 0.331 (pairwise) and 0.469 (regional). If momentum is a risk premium, the risk must be largely country-specific. The authors add that WML correlations are even overstated, because WML carries market beta after up-markets.

## 2. Unconditional macro model: Chen–Roll–Ross (17 markets, Table III)
$$WML_{j,t}=\alpha_j+\beta_{UI,j}UI_{j,t}+\beta_{DEI,j}DEI_{j,t}+\beta_{UTS,j}UTS_{j,t}+\beta_{MP,j}MP_{j,t}+\varepsilon_{j,t},$$
$$E[WML_{j,t}]=\sum_k\hat\beta_{k,j}\hat\gamma_{k,j,t}.$$
Factors: unexpected inflation, change in expected inflation (Fama–Gibbons), term spread (>10y govt yield minus 3m bill), and industrial-production growth. The default premium is omitted because non-US credit markets are too thin. Risk premia $\gamma$ come from country-level Fama–MacBeth regressions on 25 size/BM portfolios (US, UK, Japan) or 9 portfolios elsewhere; each country needs at least 3 years of data.
- **3-factor model (no MP):** only 8/51 loadings are significant at 5%, and the average adj. $R^2$ is **0.012** (compare 0.75/0.86 for FF3 on loser/winner deciles in Fama–French 1996). World: observed WML 0.67% vs model $E[WML]$ −0.03%; the gap (0.70%) is significant (t(DIFF)≈4.45). US: 0.86 vs 0.04. $E[WML]$ is scattered around zero across countries.
- **With MP** (shorter samples): adj. $R^2$ 0.015 and $E[WML]$ 0.18% (insignificant). The gap is still significant in 6 countries. The MP loading is negative and significant in 2 countries, which would make momentum *less* risky when output grows.
- Robustness: 5-year rolling betas give $R^2$ 0.014 and $E[WML]=-0.42\%$; using US factors for all countries does no better.

## 3. Conditional model: Chordia–Shivakumar (Table IV, Figure 1)
Stock-level rolling regressions over $t-60\ldots t-1$ on lagged instruments:
$$R_{i,t}=c_{i0}+c_{i1}DIV_{t-1}+c_{i2}TERM_{t-1}+c_{i3}YLD_{t-1}+e_{i,t}.$$
DEF is dropped, which does not change CS's US results in the authors' replication. The MSCI dividend yield starts in Dec 1988, so non-US forecasts start in 1991. A stock's predicted return compounds the one-step-ahead fits from the six most recent estimations. Test: in 16 countries with enough stocks for 3×3 sorts (≥10 stocks per cell), double-sort on past return and predicted return, and ask which one predicts future returns over $t\ldots t+5$.
- **No skip, momentum sorted first (Panel A), world ex-US:** $P_{hi}-P_{lo}$ is −0.22, 0.13 and 0.45 (significant) in the low/mid/high momentum terciles. It is significantly positive only in Switzerland and the US. $M_{hi}-M_{lo}$ is −0.06, 0.40* and 0.60* across predicted-return terciles and is significant in 6 countries. Reversing the sort order (Panel B) gives similar results (Switzerland 0.93, US 0.35).
- **With the skip month (Panels C/D):** world $P_{hi}-P_{lo}$ is 0.02 and 0.11 (insignificant), while $M_{hi}-M_{lo}$ is 0.38 in both panels (significant). The model's apparent power comes largely from not skipping a month, i.e. from microstructure and short-term reversal.
- **Portfolio level (Figure 1):** the correlation between model-predicted and realised country WML is positive in 8 markets, zero in 2 and negative in 12. Predicted profits are negative in more markets than they are positive.

## 4. Momentum in economic states (Table V)
Model-free test in the spirit of Lakonishok–Shleifer–Vishny: a risk premium should earn low returns in bad states.

**GDP growth (22 OECD markets, real seasonally adjusted quarterly GDP; nominal for Korea and Turkey):**
| %/month | GDP<0 | GDP>0 | GDP quartiles (low → high) |
|---|---|---|---|
| Americas ex-US | 1.18 | 0.61 | 0.41, 0.66, 0.93, 0.76 |
| Asia | 0.11 | 0.14 | |
| Europe | 0.28 | 0.76 | 0.64, 0.53, 0.80, 0.69 |
| US | 0.31 (t 0.38) | 0.92 (t 5.58) | 0.90, 1.58, 0.25, 0.65 |
| Developed ex-US | **0.59 (t 3.09)** | 0.74 (t 8.73) | 0.56, 0.73, 0.76, 0.79 |
| World | 0.32 (t 1.54) | 0.64 (t 7.67) | 0.56, 0.62, 0.48, 0.68 |

- Momentum is positive in 17/22 markets during negative-GDP periods.
- Petkova–Zhang argue that bad news arrives early in a recession. In the *first half* of negative-GDP spells, momentum still earns 1.24% (US, significant) and 0.26% (non-US).
- GDP regressed on current and lagged momentum shows no relation, echoing Liew–Vassalou.
- Chordia–Shivakumar's US result (0.53 in expansions vs −0.72 in NBER contractions) is reconciled: with the skip month, the contraction return becomes insignificant.

**Market states (value-weighted local index):**
| %/month | Market <0 | Market >0 |
|---|---|---|
| Africa | 1.55 | 1.28 |
| Americas ex-US | 0.76 | 0.76 |
| Asia | 0.55 | −0.10 |
| Europe | 0.68 | 0.76 |
| US | 1.04 | 0.32 |
| Developed | 0.77 | 0.64 |
| Emerging | 0.56 | −0.01 |

- WML is negative in only 5/40 markets during down markets, versus 14/40 during up markets.
- By market-return quartile: developed ex-US 0.62, 0.84, 0.69, 0.69; US 1.23, 0.99, 1.24, **−1.11** (US momentum loses in the strongest up-markets, i.e. rebounds).
- Using a dividend-yield forecasting model for *expected* market returns, world momentum is significantly positive in both high and low expected-return periods (0.89% in the top dividend-yield quartile).
- Industrial-production states give similar results.

## 5. Post-holding reversals (Table VI, Figure 2), horizons up to 60 months
Theory predictions: Conrad–Kaul implies profits persist at all horizons. Berk–Green–Naik profits turn negative only in about year 5. Johnson (2002) and Grinblatt–Han profits decay but never turn negative. The behavioural models (DHS, BSV, Hong–Stein) allow reversal, but at an unspecified horizon.

| %/month | $t..t+5$ | $t+6..t+11$ | $t+12..t+17$ |
|---|---|---|---|
| Africa | 1.63 | 0.00 | −0.92 |
| Americas ex-US | 0.78 | −0.45 | −1.07 |
| Asia ex-Japan | – | −0.49 | −1.22 |
| Europe | 0.77 | 0.31 | −0.36 |

- Profits are also negative in $t+18..t+23$. Cumulative profits peak at 6–10 months, then a sharp correction takes them **negative in year 2**. The reversal is faster and stronger than in the US.
- Januaries are negative in all regions except Africa across the three post-holding windows (world ex-US −1.08, −1.81, −1.56).
- **Excluding January**, US cumulative profits dissipate only slightly and never turn negative (consistent with Grinblatt–Moskowitz: US reversal is a January/tax effect). Europe, the Americas and Asia still reverse strongly.

## Critical assessment
- **Convincing.** The breadth of the evidence (40 markets), the near-zero cross-country correlations, the robust positive returns in bad states, and above all the diagnosis of the skip month (the Chordia–Shivakumar "explanation" is largely a short-term-reversal artefact) make standard macro-risk stories untenable.
- **Fragile or caveats:**
  - Negative-GDP samples are short, so state-conditional means have low power (e.g. US GDP<0 t = 0.38).
  - Realised states mix expected and unexpected risk.
  - Datastream coverage for many emerging markets begins in the 1990s.
  - Equal-weighted quintiles in small markets are dominated by small, illiquid stocks, and there are no transaction costs.
  - Only standard linear macro models are tested; the authors concede that an untested form of macro risk cannot be excluded. Behavioural models "win" partly because they specify no reversal horizon.
- **Asia/Japan** show essentially no momentum, a notable exception that the paper documents but does not explain.
- **Typo:** in the Table IV discussion the skip-month ranking window is written "$t-1\ldots t-2$"; it should be $t-7\ldots t-2$.
- **Numerical caveat:** table cells in the JSTOR scan are rotated images, so a few numbers above were read by OCR. All headline numbers are also stated in the paper's text.

## Practical relevance for a quant PM
- Momentum is largely a **country-local** phenomenon with weak cross-country correlation (≈0.03–0.10). Country-neutral global momentum therefore diversifies well, but do not expect a common macro driver or hedge.
- Always skip a month. Without the skip, microstructure and one-month reversal contaminate both returns and any "conditional risk" attribution.
- Holding past about 6–10 months is costly outside the US: cumulative profits reverse in year 2. Keep holding periods short and turnover-aware, and consider long-horizon reversal as an overlay.
- Momentum does not reliably lose in recessions or down markets. US momentum's worst quartile is the strongest up-market months, which foreshadows the later crash literature (rebounds after bear markets).
- Expect weak or zero momentum in Japan and much of Asia.
