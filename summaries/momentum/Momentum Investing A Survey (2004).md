# Momentum Investing: A Survey

**Laurens Swinkels · 2004 · *Journal of Asset Management* 5(2), 120–143 · Source file `Finance/AbnormalReturnsMomentum_Swinkels_2004.pdf` · literature survey (plus a Table 1 computed from Ken French's data, US 1927–2002)**

## Contribution
A compact survey of the cross-sectional (relative-strength) momentum literature up to 2003, organised around (i) how momentum is *measured* (WRSS vs decile sorts, overlapping portfolios, regression equivalence), (ii) an *algebraic decomposition* of the momentum payoff (Lo–MacKinlay → Conrad–Kaul → Lewellen → Jegadeesh–Titman factor version → Moskowitz–Grinblatt industry/country → Chan–Hameed–Tong currency terms), (iii) conditioning characteristics (size, industry, country, turnover, analyst coverage), (iv) risk-based vs behavioural explanations, and (v) transaction costs. No new data beyond Table 1; conclusion: "research on this topic still has momentum" — no explanation is settled.

## Definitions and measurement
Momentum is defined as positive cross-sectional covariance of successive relative returns:
$$E\Big\{\tfrac1N\sum_{i=1}^N (R_{i,t-1}-\bar R_{t-1})(R_{i,t}-\bar R_t)\Big\}>0. \tag{1}$$
This is an empirical regularity, not by itself evidence of inefficiency (no pricing model assumed).

- **WRSS** (weighted relative strength strategy, Lo–MacKinlay/Conrad–Kaul): zero-investment weights $w_{i,t-1}=R_{i,t-1}-\bar R_{t-1}$; sample analogue of (1). Weakness: weights scale with cross-sectional dispersion, so in high-dispersion months a few extreme (often tiny) stocks dominate; noisy and costly to implement (Figure 1).
- **Decile/quantile sorts**: equal (or value) weight within top/bottom 10% (sometimes 20–30%); drop extremes-driven weighting; top/bottom 20–30% give lower spreads than deciles (momentum concentrated in extremes).
- **Inference with $K>1$ holding periods**: (a) non-overlapping blocks (few obs.), (b) overlapping returns + Newey–West, (c) Jegadeesh–Titman **overlapping portfolios** — each month hold $K$ sub-portfolios formed in months $t,\dots,t-K+1$; monthly returns non-overlapping, so a plain t-test is valid if WML monthly returns are not autocorrelated. Skipping a week/month between formation and holding reduces bid–ask bounce; effect on (6,6) returns usually small.
- **Regression equivalence**: panel $Y_{i,t}=\beta X_{i,t}+\varepsilon_{i,t}$. With $Y,X$ = current and lagged cross-sectionally demeaned returns, the OLS numerator is the sample analogue of (1). With $X$ = $D$ group dummies from the lagged ranking, Fama–MacBeth estimates equal the time-averaged portfolio returns and the FM variance equals the usual long–short portfolio variance; WLS in the cross-sectional step gives value weighting. Sorting discards information and collapses with multiple sorts; Nijman–Swinkels–Verbeek (2004) use a portfolio-holdings regression to separate country/industry/stock momentum with interactions.

## Decomposition of the payoff
Let $\pi_t=\frac1N\sum_i w_{i,t-1}(R_{i,t}-\bar R_t)$.

1. **Conrad–Kaul (1998)**: $R_{i,t}=\mu_i+\varepsilon_{i,t}$ with no serial (cross-)correlation ⇒ $E\pi_t=\sigma^2_\mu\equiv\frac1N\sum_i(\mu_i-\bar\mu)^2$. Momentum = dispersion in unconditional means. JT (2001): this implies profits growing linearly with holding horizon, which the data do not show.
2. **Lewellen (2002)**, allowing serial and cross-serial correlation:
$$\pi_t=\sigma^2_\mu+\frac{N-1}{N^2}\sum_i\varepsilon_{i,t-1}\varepsilon_{i,t}-\frac1{N^2}\sum_i\sum_{j\ne i}\varepsilon_{i,t-1}\varepsilon_{j,t},$$
i.e. in expectation $\sigma^2_\mu+\frac{N-1}{N^2}\mathrm{tr}\,\Gamma-\frac1{N^2}(\iota'\Gamma\iota-\mathrm{tr}\,\Gamma)$, $\Gamma$ = lag-1 autocovariance matrix. Lewellen's evidence: **negative cross-serial covariances** (a high return on $j$ predicting low return on $i$ — overreaction to other firms' news), not own autocorrelation, drive momentum; Cheng–Hong (2002) show this is also consistent with underreaction.
3. **Jegadeesh–Titman one-factor version**: $R_{i,t}=\mu_i+\beta_i\tilde R^e_{m,t}+\eta_{i,t}$, with $\mu_i=R_f+\beta_iE\{R^e_{m}\}$ and $E\{\eta_{i,t}\eta_{j,t-1}\}=0$ for $i\ne j$:
$$\pi_t=\sigma^2_\mu+\sigma^2_\beta\,\mathrm{Cov}\{R^e_{m,t-1},R^e_{m,t}\}+\frac1N\sum_i\eta_{i,t-1}\eta_{i,t}.$$
JT attribute momentum to the third (idiosyncratic autocorrelation) term, but that conclusion is partly imposed by assuming away cross-serial covariance. Multi-factor (e.g. FF3) generalisation: $\sum_k\sigma^2_{\beta_k}\mathrm{Cov}\{R^e_{k,t-1},R^e_{k,t}\}$, assuming no cross-autocorrelation between factors.
4. **Industry/country** (Moskowitz–Grinblatt 1999): $\eta_{i,t}=\sum_l\theta_{i,l}\tilde R_{z_l,t}+\nu_{i,t}$ with industry factors orthogonalised to risk factors; with additive country + industry effects (Heston–Rouwenhorst), split $L=L_1+L_2$; interacting country×industry gives $L_1\times L_2$ components.
5. **Currency** (Chan–Hameed–Tong 2000; Bhojraj–Swaminathan 2001): with $R_{i,t}\approx r_{i,t}+e_{i,t}$ (local + FX return), four cross-product terms: local–local, FX(t−1)–local(t), local(t−1)–FX(t), FX–FX.

**Full decomposition (eq. 8):**
$$\pi_t=\sigma^2_\mu+\sum_{k=1}^K\sigma^2_{\beta_k}\mathrm{Cov}\{\tilde R^e_{k,t-1},\tilde R^e_{k,t}\}+\sum_{l=1}^L\sigma^2_{\theta_l}\mathrm{Cov}\{\tilde R_{z_l,t-1},\tilde R_{z_l,t}\}+\text{(3 FX cross terms)}+\frac{N-1}{N^2}\sum_i\nu_{i,t-1}\nu_{i,t}-\frac1{N^2}\sum_i\sum_{j\ne i}\nu_{i,t-1}\nu_{j,t},$$
under no lead–lag cross-covariance between distinct factors, between factors and industry/country factors, and between factors and lagged residuals. Swinkels flags estimating all components on a large international stock sample as open research.

## Empirical facts collected
**Table 1 (French data; "momentum" = UMD, (11,1) with 1-month skip, size-controlled; % per month, autocorrelation-corrected t in brackets):**

| Sample | Market | Size | Value | Momentum |
|---|---|---|---|---|
| 1927–2002 | 0.62 [3.25] | 0.22 [1.87] | 0.40 [3.10] | **0.78 [5.33]** |
| 1927–41 | 0.45 [0.65] | 0.40 [1.02] | 0.15 [0.31] | 0.47 [0.47] |
| 1942–62 | 1.11 [4.26] | 0.11 [0.76] | 0.50 [3.03] | 0.77 [6.13] |
| 1963–89 | 0.41 [1.57] | 0.27 [1.45] | 0.50 [3.12] | 0.80 [4.45] |
| 1990–2002 | 0.45 [1.32] | 0.07 [0.25] | 0.34 [0.97] | 1.13 [3.15] |

Over the full sample, momentum beats the equity premium in both mean and t-stat. The paper says momentum has the highest mean in every subperiod except 1942–62, where the market's 1.11 is higher but momentum's t-stat is still the largest. Note that in 1927–41 its t (0.47) is actually below size's; momentum is weak pre-1941.

**Table 2 (US WML, % per month, 6-month-type strategies):** JT93 0.95 (t 3.07, 1965–89, EW deciles); Conrad–Kaul 0.36 (4.55, WRSS); Moskowitz–Grinblatt 0.43 (4.65, VW 30%); Hong–Lim–Stein 0.53 (2.61, EW 30%); Lee–Swaminathan 1.05 (4.28); JT01 1.23 (6.46, 1965–98); Chordia–Shivakumar 1.51 (6.52); Griffin et al. 0.58 (3.31, 1927–2000, EW 20%). Dispersion reflects sample period (pre-1941 weak), Nasdaq/low-price/small-cap screens, EW vs VW, and breakpoints.

**International:** Rouwenhorst (1998) Europe 1980–95, (6,6) 1.16%/month (t 4.02), significant in 11/12 countries; Rouwenhorst (1999) 20 emerging markets 1982–96: 0.39% (t 2.68), cross-country-average 0.58% (t 3.96), significant in only 6 countries; Griffin et al. (2003) find emerging winners ≈ losers 1986–2000. Country-index momentum: Richards 0.57%/month insignificant; Chan et al. (2000) 0.46% (t 2.35); Bhojraj–Swaminathan significant in 38 and 16-developed-country samples.

**Characteristics:**
- *Industry*: Moskowitz–Grinblatt say industry momentum explains stock momentum; others disagree — Lee–Swaminathan: industry adjustment cuts 12.5% → 10.1% p.a. (−20%); Grundy–Martin: industry momentum ≈ half of stock momentum. MG's result seems to hinge on the skip month and 30% (vs 10%) breakpoints. Nijman et al. (2004, Europe): stock-level > industry > country (≈0); strongest in small growth stocks.
- *Size*: stronger in small caps (JT01); Hong–Lim–Stein: none in largest 30% by cap, stronger with low analyst coverage (controlling for size), reversals in the smallest decile. MG: 9.3% (EW) vs 5.2% (VW) p.a. for tertile portfolios.
- *Earnings*: Chan–Jegadeesh–Lakonishok (1996): earnings momentum (SUE, announcement return, analyst revisions) and price momentum are distinct.
- *Turnover*: Lee–Swaminathan — high-turnover stocks show more momentum; "early-stage" (long low-volume winners, short high-volume losers) 16.7% vs "late-stage" 6.8% p.a. in year 1; confirmed in Germany (Glaser–Weber).

## Explanations
**Risk.** CAPM beta (JT93) and unconditional FF3 (Fama–French 1996) fail; FF3 adjustment *raises* alpha because WML loads negatively on SMB/HML (JT01). Ang–Chen–Xing downside-risk factor explains part. Conditional versions:
- Wu (2002): time-varying betas $R^{wml}_t=\alpha+M_{t-1}'\gamma_m R^{mkt}_t+M_{t-1}'\gamma_sR^{smb}_t+M_{t-1}'\gamma_hR^{hml}_t$ (Shanken 1990) — $\gamma$ significant but $\alpha\neq0$ still; a time-varying-risk-premium GMM version ($E\{\tilde R^e_{m,t}|M_{t-1}\}=\delta M_{t-1}$) does price momentum but leaves exposures unidentified.
- Chordia–Shivakumar (2002): stock-by-stock $R_{i,t}=\alpha_i+\beta_iM_{t-1}+\varepsilon_{i,t}$ on 60-month rolling windows; sorting on predicted returns absorbs much of momentum. Griffin–Ji–Martin (2003) counter: the prediction model's average adj. $R^2\approx5\%$, and CRR-style regressions of WML on contemporaneous macro factors leave the intercept intact.
- Johnson (2002): rational model with persistent dividend-growth-rate shocks.
Verdict: unconditional models fail; conditional models have many parameters and may be spurious.

**Behavioural.** Swinkels' evaluation criteria: plausible psychology, consistency with other stylised facts, and new testable (out-of-sample) predictions. Models: Daniel–Hirshleifer–Subrahmanyam (overconfidence + biased self-attribution → continued overreaction, later reversal); Barberis–Shleifer–Vishny (conservatism + representativeness → underreaction, then overreaction after streaks); Hong–Stein (news-watchers vs momentum traders; slow diffusion → prediction confirmed by Hong–Lim–Stein on size/analyst coverage); Barberis–Shleifer style investing (style momentum and later reversal; partly supported by Lewellen). Without new testable predictions, the models remain descriptive.

## Transaction costs
Most papers report break-even costs versus round-trip ~1%. Korajczyk–Sadka (2004), long-only winners vs market, (5,6) with skip: gross 59 bp/month (EW) and 33 bp (VW); net of effective spread 41/22 bp, of quoted spread 35/17 bp. Price-impact models (Breen–Hodrick–Korajczyk convex; Glosten–Harris affine, slightly larger capacity) give break-even fund size <$200m for EW and ~$1bn for VW; a liquidity-weighted momentum portfolio reaches ~$1.1bn (NYSE) and ~$5bn (NYSE/AMEX/Nasdaq). Lesmond–Schill–Zhou (2004): JT01 portfolios net 7.12% p.a. (t 2.57) with effective spread+commission vs 4.40% (t 1.59) with the LDV cost estimate; JT93 portfolios insignificant under both.

## Critical assessment
- The value is the unified decomposition (eq. 8) tying each empirical claim to a term: Conrad–Kaul ↔ $\sigma^2_\mu$, JT ↔ own idiosyncratic autocovariance, Lewellen ↔ cross-serial terms, MG ↔ industry factor autocovariance. Each attribution rests on orthogonality assumptions, which the survey states but does not test.
- It is a survey: no replication across studies, and Table 1 uses UMD (11,1) rather than JT (6,6), so it is not strictly comparable to Table 2.
- Typos/inconsistencies in the paper: "WRRS" in Table 2 (= WRSS); multi-factor assumption written as "$\mathrm{Cov}\{R^e_{k,t-1},R^e_{l,t}\}$ for $k\ne l$" (missing "= 0"); "$L_1\times L_1$ components" should read $L_1\times L_2$; the assumption list writes "$\forall k,i$" for the industry-residual condition.
- Predates the crash-risk, risk-managed-momentum and factor-momentum literatures.

## Practical relevance for a quant PM
- Use the decomposition as a diagnostic: estimate how much of your WML is industry/factor autocovariance vs stock-specific (residual momentum), and whether cross-serial (lead–lag) effects matter.
- Weighting matters: WRSS concentrates in extreme, small, illiquid names in high-dispersion regimes; rank or decile weights are more robust.
- Implementable momentum is mostly a mid/large-cap, VW, cost-aware construct. Capacity estimates are on the order of $1bn per strategy (2004 costs), and EW academic numbers overstate what is attainable.
- Expected premium of ~0.8%/month (UMD, 1927–2002) with a weak 1927–41 period; the strength of the effect is regime-dependent.
