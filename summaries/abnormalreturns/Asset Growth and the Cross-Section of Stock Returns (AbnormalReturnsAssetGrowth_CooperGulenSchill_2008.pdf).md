# Asset Growth and the Cross-Section of Stock Returns — Cooper, Gulen & Schill (2008) — Detailed Quantitative Research Notes

## Bibliographic Header

| Field | Detail |
|------|--------|
| **Title** | Asset Growth and the Cross-Section of Stock Returns |
| **Authors** | Michael J. Cooper (Utah); Huseyin Gulen (Purdue); Michael J. Schill (Virginia Darden) |
| **Journal** | *Journal of Finance*, Vol. LXIII, No. 4, August 2008, pp. 1609–1651 |
| **Sample** | NYSE/Amex/Nasdaq nonfinancial firms, CRSP–Compustat; returns July 1968–June 2003 |
| **Key variable** | $\mathrm{ASSETG}_t = (A_{t-1}-A_{t-2})/A_{t-2}$, total assets (Compustat item 6), fiscal years ending in calendar $t-1$ and $t-2$ |
| **Source file** | Finance/AbnormalReturnsAssetGrowth_CooperGulenSchill_2008.pdf |
| **Drive file_id** | `0B-6kBz0I0dMsbmVfbVdsUFhjMlk` |

Previously circulated as "What best explains the cross-section of stock returns? Exploring the asset growth effect."

---

## Question

Event studies show low returns after asset-expanding events (acquisitions, SEOs, debt issues, bank loans) and high returns after contracting events (spinoffs, repurchases, debt prepayments, dividend initiations); cross-sectional work finds the same for capex (Titman-Wei-Xie), accruals (Sloan), sales growth (LSV), NOA (Hirshleifer et al.), net external financing (Richardson-Sloan) and share growth (Pontiff-Woodgate). CGS ask whether the comprehensive measure -- total asset growth -- subsumes these fragments and whether the resulting effect is risk or mispricing.

## Data and design

- Nonfinancial firms (SIC 6000-6999 excluded); firm must be on Compustat 2 years (backfill). Characteristics formed end of June $t$ from fiscal year $t-1$; BM uses December $t-1$ price (Davis-Fama-French book equity); MV end of June.
- Decile sorts on ASSETG each June, held July $t$–June $t+1$, EW and VW, overall and within NYSE 30/70 size groups.
- Asset growth is large and dispersed: mean (median) about 19% (8%) per year; cross-sectional s.d. about 60%, 95% in the last decade. Median ASSETG in decile 10 is 83.6%, decile 1 is -21.2%. Growth is persistent: deciles 10 vs 1 grew 21.7% vs 0.4% the previous year.
- High-growth firms: lower BM (0.43 vs 0.82), higher ROA and E/P, higher accruals and issuance, very high past 36-month returns but below-average past 6-month returns; similar leverage. Corr(ASSETG, BM) = -0.18, corr(ASSETG, size) = 0.02 -- not simply a value or size sort. Median capitalization of extreme deciles is comparable to size deciles 3 (low growth) and 6 (high growth).

## Portfolio results (Table II)

Pre-formation, high-growth firms earned much higher returns: VW monthly spread (high minus low) of 3.34%, 2.92%, 1.93%, 1.50% in years -2 to -5. Post-formation the sign flips:

| Year 1 | Decile 1 (low) | Decile 10 (high) | High − low | t |
|---|---|---|---|---|
| EW raw, %/mo | 1.99 | 0.26 | −1.73 | −8.45 |
| VW raw, %/mo | 1.48 | 0.43 | −1.05 | −5.04 |
| EW FF3 α | 0.76 (t=3.28) | −0.87 (t=−5.81) | −1.63 | −8.33 |
| VW FF3 α | 0.24 (t=1.65) | −0.46 (t=−3.74) | −0.70 | −3.84 |

EW returns are perfectly monotone across all ten deciles. In VW, most of the alpha is on the short (high-growth) side. Alpha-difference t-stats use joint GMM with HAC covariance and the delta method.

FF3 alpha spread by size group (%/mo): small EW −1.77 (t=−9.12), VW −1.14 (−6.46); medium EW −0.60 (−2.85), VW −0.55 (−2.45); large EW −0.86 (−3.12), VW −0.81 (−2.91), i.e. about 10%/yr in large caps.

- **Persistence:** cumulative years 1-5 spread −87.99% EW (t=−8.63), −49.67% VW (t=−4.25); average 5-year FF3 alpha spread −0.73%/mo EW (t=−10.96), −0.39% VW (t=−2.73).
- **Carhart 4-factor:** −1.48% EW (t=−7.45), −0.60% VW (t=−2.84); large VW −0.63% (t=−2.13).
- **Consistency:** low beats high in 32/35 years EW (91%; the 3 losses are 1984, 1985, 1996 at −1%, −5%, −2%) and 71% of years VW. FF3 alpha spreads are significant in 1968-80, 1981-90 and 1991-2003, except VW 1968-80 (−0.35%, t=−1.69); the effect is strongest in the last subperiod, i.e. not decaying within the sample.
- **Sharpe ratios** of annual spread returns: 1.19 EW, 1.07 VW vs HML 0.37, SMB 0.13, UMD 0.73.
- **Robustness:** price screens (\$3, \$5), assets ≥ \$10m, March formation; excluding firm-years with an IPO/SEO/acquisition (SDC) in $t-1$ (dropped for $t-1$ to $t+2$) leaves large VW alpha spread −0.92%/mo (t=−3.72).

## Cross-sectional regressions (Table III)

Fama-MacBeth regressions of **annual** compounded returns (chosen to limit microstructure bias in monthly closing prices), with t-stats corrected for first-order autocorrelation in yearly slopes by $\sqrt{(1+\rho)/(1-\rho)}$. Controls: BM, MV, 6-month and 36-month lagged returns.

- Base model, all firms: ASSETG $t=-6.52$, the strongest regressor; by size −5.18 (small), −3.80 (medium), −3.60 (large). BM loses significance in all large-firm models; MV and 6-month momentum are weak.
- Against other growth variables (all firms): with 5-yr sales growth, ASSETG $t=-7.41$ vs 5YSALESG −0.27; with capital investment −6.05 vs −3.32; with NOA/A −6.10 vs −2.43; with accruals −5.65 vs −4.00. In large firms, CI, sales growth and accruals are insignificant once ASSETG is included. (NOA/Lag A is mechanically NOA/A × A/Lag A, so only NOA/A is used.)
- Lagged growth (L2ASSETG) and a weighted 5-year growth rank (years −5 to −2) are also negative and significant; 1-year ASSETG remains strongest.
- Subperiod monthly-return regressions: ASSETG t = −3.98, −4.46, −6.14 vs BM 1.40, 2.12, 2.23. Winsorizing at 1/99% raises ASSETG to $t=-9.47$; monthly-return FM gives −7.36; dropping utilities, keeping negative-book firms, dropping assets < \$10m change nothing.

## Balance-sheet decomposition (Table IV)

Accounting identities, each change scaled by lagged total assets:
$$\mathrm{ASSETG}=\Delta\mathrm{Cash}+\Delta\mathrm{CurAsst}+\Delta\mathrm{PPE}+\Delta\mathrm{OthAssets}=\Delta\mathrm{OpLiab}+\Delta\mathrm{RE}+\Delta\mathrm{Stock}+\Delta\mathrm{Debt}.$$

- Investment side (all firms, univariate t): cash −0.03 (never significant in any size group), noncash current assets −4.80, PPE −3.91, other assets −3.34; jointly, current assets and PPE dominate.
- Financing side: debt −6.59, operating liabilities −4.00, stock −1.88, retained earnings −0.83 (not significant). Growth financed internally is not penalized; external financing is.
- The dominant component shifts with size: in small firms, current assets and debt; in large firms, PPE (t=−2.62) and stock financing (t=−3.27; debt −1.79).
- No single component matches total ASSETG, except that in large firms Δstock subsumes ASSETG (t=−2.25 vs −0.56) when both are included. Removing share growth from asset growth, the Fama-French (2008) variant, gives only $t=-0.73$ in large firms vs −3.60 for ASSETG -- the equity-financed part carries the large-cap effect.

## Issuance and repurchases (Table V)

Adds Daniel-Titman 3-year ISSUANCE ($\log(ME_t/ME_{t-3})-r_{t-3,t}$), SEO and repurchase dummies (prior 2 years; 1982-2002 sample for dummies).
- All firms: ASSETG t=−5.86 vs ISSUANCE −2.99; with all four, ASSETG −4.54 and the others insignificant. With 2-year-lagged variables, ASSETG (−2.85) subsumes all issuance measures.
- Large firms reverse the ranking: ISSUANCE −3.98 vs ASSETG −1.91; SEO (−4.29) and repurchase (+3.52) dummies are strong only in large firms. Dropping ISSUANCE, ASSETG is again significant (−2.24). Corr(ISSUANCE, ASSETG) is 0.19/0.33/0.39 in small/medium/large firms.
- Adding A/MV (book vs. market scaling of growth) changes nothing. Both variables are strongest at 1-3 year construction horizons; neither subsumes the other.

## Risk vs. mispricing

Against risk (investment-based models of Berk-Green-Naik, Carlson-Fisher-Giammarino, Zhang, Liu-Whited-Zhang):
- Conditional CAPM with betas linear in dividend yield, default spread, term spread and T-bill leaves a spread-portfolio alpha of 1.65%/mo (t=8.02).
- These models tie the investment effect to size and BM, so FF3 should absorb it; instead residual spreads are 8%/yr VW and 20%/yr EW.
- High-growth deciles earn 5.2% (VW) and 3.1% (EW) per year vs an average T-bill of about 6.3%: a zero or negative risk premium.
- High-growth returns rise from year 1 to year 5 (+1.08%/mo EW, +0.83% VW) while growth remains positive, whereas these models predict falling expected returns as firms keep investing.

For mispricing:
- Operating margin (EBITDA/sales) peaks around the sort year for high-growth firms and troughs for low-growth firms, then reverts (Fig. 4) -- LSV extrapolation.
- Earnings-announcement test (La Porta et al. 1997): 3-day EAD vs non-EAD mean daily returns are 0.27% vs 0.11% for low growth (diff t=3.41) and −0.10% vs 0.00% for high growth (t=−3.59), roughly monotone across deciles: investors are surprised by subsequent earnings.
- During 1984-89, a period of heightened takeover discipline (Titman-Wei-Xie), the spread shrinks (EW −0.86%, t=−2.56; VW −0.46%, t=−1.51), consistent with an empire-building component.
- Market-state link: the high-low growth-rate spread loads on lagged 36-month market return (t=4.80), and the return spread loads on the lagged growth-rate spread (t=2.17) -- read as manager/investor overconfidence after booms.

Conclusion as stated: low-growth firms earn +9.1%/yr risk-adjusted, high-growth −10.4%, a 19.5% EW spread and 8.4% VW spread; "most consistent with the interpretation that investors overextrapolate past gains to growth."

## Assessment

- **Strong:** simple, pre-specified, non-mined variable; very high t-stats; monotone deciles; survives in large caps; horse races against the leading growth anomalies; annual-return FM with autocorrelation correction is conservative. The decomposition explains *why* the aggregate wins: it averages over components whose relevance shifts with size.
- **Fragile or open:** (1) The rejection of q-theory is informal. Liu-Whited-Zhang and later Hou-Xue-Zhang (2015) and Fama-French (2015, CMA) price the effect with an investment factor, which converts the "anomaly" into a factor without resolving the risk/mispricing debate; the conditional CAPM with four instruments is a weak straw man. (2) VW long-leg alpha is only 0.24% (t=1.65); the VW effect is mainly the short side, where borrow cost and short constraints matter and which the paper does not cost. (3) Large-cap predictability is largely equity issuance, not organic investment, so the "comprehensive" claim is weakest where capacity is. (4) EW magnitudes are dominated by small firms. (5) US 1968-2003 only.
- **For a quant PM:** ASSETG is effectively the CMA signal; test incremental value over CMA/issuance rather than trading it standalone. Use winsorized or ranked ASSETG (winsorizing raises t from −6.5 to −9.5). In large caps, separate the stock-financing component. Annual rebalance suffices: the signal is slow (5-year persistence) and turnover is low. The shrinking spread in periods of strong governance and the boom-dependence of the growth spread suggest the premium is state-dependent and larger after strong markets.
