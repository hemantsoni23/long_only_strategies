# Momentum (Annual Review)

**Narasimhan Jegadeesh, Sheridan Titman · 2011 · Annual Review of Financial Economics 3, 493–509 · Source file `Finance/Momentum_JegadeeshTitman_2011.pdf` · Survey of US/international equity momentum, plus the authors' own update of 6/1/6 momentum for 1990–2009**

## Claim / contribution
A short survey by the originators of the J/K strategy. Its arguments:
- Price momentum is too large and persistent to be risk compensation, and is "perhaps the strongest evidence against the efficient markets hypothesis".
- The evidence points to delayed reaction to **firm-specific** information, not to factor serial covariance or dispersion in expected returns.
- Price momentum and earnings momentum (SUE, analyst revisions) are distinct, and neither subsumes the other.
- The **2009 crash (−36.5%)** is largely explained by the strategy's negative market beta after the 2008 decline, together with known time-series predictors.

## Canonical strategy and stylized facts
- **J/K strategy (JT 1993):** at the start of month $t$, rank stocks on past $J$-month returns into equal-weighted deciles and hold winners minus losers for $K$ months, with $J, K \in \{3, 6, 9, 12\}$. Overlapping portfolios. Skipping a week or month between ranking and holding raises returns, because it avoids the 1-week/1-month reversal (Jegadeesh 1990; Lehmann 1990).
- **Horizon structure:** contrarian at 1 week–1 month and at 3–5 years (De Bondt–Thaler 1985); continuation at 3–12 months. The 6/6 strategy made money in every rolling 5-year window from 1965 to 2004. The window starting in 2004 was negative, driven by 2009.
- **International:** similar profits in 12 European countries (Rouwenhorst 1998) and most large markets. Exceptions are in Asia, notably Japan (Griffin–Ji–Martin 2003; Chui–Titman–Wei 2010).
- **Seasonality:** negative in January, significantly positive in every other calendar month. This is the opposite of size, value and reversal effects, which are strongest in January.

## Sources of profits (JT decomposition)
Expected WML profit has three components:
1. dispersion in unconditional expected returns (risk);
2. serial covariance of factor returns (timing via beta tilts);
3. serial correlation in firm-specific returns (delayed reaction).

Evidence against 1 and 2:
- CAPM alphas (JT 1993) and FF3 alphas (JT 2001; Fama–French 1996; Grundy–Martin 2001) stay significantly positive.
- The serial covariance of 6-month equal-weighted index returns is *negative* (−0.0028), so factor autocorrelation cannot drive the profits.
- **Lead–lag in common factors** (JT 1995) would add to momentum only if high contemporaneous betas coincide with high lagged betas. Regressing WML on the squared 6-month VW market return gives a negative coefficient (1965–89), so there is no evidence of this channel.

## Industry momentum
- Moskowitz–Grinblatt (1999): value-weighted industry winners beat industry losers. A "random industry" strategy with the same past returns earns about zero, which they read as industry momentum driving stock momentum.
- Grundy–Martin (2001) counter-evidence: with a contiguous 6/6 design, actual industry momentum earns 0.78%/month (simulated ≈ 0). **With a 1-month skip, industry momentum is insignificant**, while stock momentum earns a significant 0.79%/month (1966–95).
- Interpretation: industry momentum rides first-order portfolio autocorrelation (the lag-1 month), while stock momentum is hurt by the short-term reversal. So industries do not explain stock momentum.

## Behavioral explanations and long-horizon tests
- **Underreaction:** conservatism (BSV 1998), the disposition effect (Grinblatt–Han 2005), anchoring on the 52-week high (George–Hwang 2004). These predict no later reversal.
- **Delayed overreaction:** positive-feedback trading (DeLong et al. 1990); representativeness (BSV); overconfidence plus self-attribution (Daniel–Hirshleifer–Subrahmanyam 1998); news-watchers vs momentum traders (Hong–Stein 1999). These predict a post-holding reversal.
- **Evidence (JT 1993, 2001; 1965–1998):**

| Sample | Cumulative WML at month 12 | Month 36 | Month 60 |
|---|---|---|---|
| 1965–98 | 12.17% | — | −0.44% |
| 1965–81 | 12.10% | 5.25% | −6.29% |
| 1982–98 | 12.24% | 6.68% (insignificant decline) | ≈ 6.68% |

  The reversal supports overreaction models only in the first half. SMB/HML averaged 0.53%/0.48% per month before 1981 and 0.18%/0.33% after.

## Cross-sectional determinants
Momentum is stronger in:
- stocks with low analyst coverage (Hong–Lim–Stein 2000);
- growth vs value stocks (Daniel–Titman 1999, on an overconfidence story);
- stocks with high information uncertainty: analyst dispersion, return and cash-flow volatility (Zhang 2006; Verardo 2009);
- stocks with high revenue volatility and low COGS (Sagi–Seasholes 2007, growth options);
- **high-turnover** stocks (Lee–Swaminathan 2000). This is surprising from a trading-cost angle; possible explanations are differences of opinion or attention.
- Avramov et al. (2007): momentum is confined to low-credit-rating firms. For AAA–BB stocks (96.6% of rated market cap, 78.8% of rated firms) it is insignificant. JT 1993 and Fama–French (2008) find it across size groups.
- Across countries, profits correlate with Hofstede's individualism index (Chui–Titman–Wei 2010).

## Time-series determinants
Regression form: $\mathrm{MOM}_t = g_0 + b_1\,\mathrm{STATE}_{t-1} + e_t$.
- **Macro variables:** momentum is profitable only in expansions (Chordia–Shivakumar 2002). This is not robust to price screens or skip-month returns (Cooper et al. 2004) and fails internationally (Griffin–Ji–Martin 2003).
- **Market state** (Cooper–Gutierrez–Hameed 2004): +0.93%/month after positive 3-year market returns vs −0.37% (insignificant) after negative ones.
- **Return dispersion** (Stivers–Sun 2010), measured as the cross-sectional σ of 100 size/BM portfolios over the prior 3 months: higher RD predicts lower momentum and subsumes market state and macro variables.
- **Volatility × state** (Wang–Xu 2010): −3.01%/month (t = −1.94) in down-market/high-volatility states.
- **Sentiment** (Antoniou et al. 2010): 1.64%/month in optimistic vs 0.56% (insignificant) in pessimistic states. Up/optimistic 1.8% vs up/pessimistic 0.8%. Reversal occurs only after optimistic periods.

## Earnings momentum
$$\mathrm{SUE} = \frac{\text{quarterly EPS} - \text{expected quarterly EPS}}{\sigma(\text{quarterly EPS})},$$
where the expectation typically comes from a seasonal random walk with drift. Analyst-revision momentum:
- Givoly–Lakonishok (1979; 67 firms, 1967–74): up minus down revisions ≈ 5%.
- Stickel (1991, Zacks, 1981–84): similar results.
- Chan–Jegadeesh–Lakonishok (1996, IBES, 1977–93): up minus down revisions **7.7% over 6 months**.

The effects are robust to the revision definition and data source, and persisted after publication. **Two-way 3×3 independent sorts** (CJL 1996, 2000) on 6-month return and SUE or revisions: jointly highest minus jointly lowest = **8.1% over 6 months, 11.5% over 12 months**. No momentum variable subsumes another, so each captures underreaction to a different piece of information.

## Authors' update, 1990–2009 (Table 1)
Design: 6/1/6 (rank on $t-7..t-2$), six overlapping equal-weighted extreme deciles; exclude the smallest NYSE size decile and stocks priced below \$5.

| | Raw WML (% p.a.) | CAPM α | β |
|---|---|---|---|
| Average 1990–2009 | **13.51 (t = 2.90)** | 10.19 (t = 2.30) | ≈ 0 on average |
| Best years | 1999: 67.26; 1998: 41.50; 2000: 36.01 | 2000: 69.70 | 2000: 1.40 |
| Losing years | 1994 −0.32, 2003 −3.50, 2008 −0.32, **2009 −36.50** | 2009: −18.84 | **2009: −0.79** |

Profitable in 16 of 20 years. **2009 decomposition:**
- Raw return −3.4%/month; after adjusting for the in-year beta, −1.56%/month. So beta explains more than half of the loss, analogous to 1933, the only negative decade (the 1930s) in JT 1993.
- Predictive regression (standardized regressors, Jan 1990–Dec 2009):
$$\mathrm{MOM}_t = 1.12 - 0.42\,\mathrm{RD}_{t-1} + 0.90\,\mathrm{MktRet}_{t-36,t-1},\quad t = (-1.03),\ (2.21)$$
  The lagged 3-year market return is significant out of sample. RD has the right sign but is insignificant, even though RD in 2009 was 4.84% vs 3.20% on average.
- Signal-adjusted 2009 profit: −1.5%/month.
- Beta-adjusted version: $\mathrm{MOM}_t - b_t\,\mathrm{MktRet}_t = 0.85 - 0.30\,\mathrm{RD}_{t-1} + 0.76\,\mathrm{MktRet}_{t-36,t-1}$ (t = −0.85, 2.16). The 2009 residual after beta and signals is only 0.19%/month in magnitude.

## Critical assessment
- **Strong points:**
  - The clean decomposition logic.
  - The skip-month industry result (Grundy–Martin), which is often ignored.
  - The out-of-sample 1990–2009 evidence.
  - The simple and useful beta/market-state diagnosis of 2009, consistent with Daniel (2011) and Daniel–Moskowitz.
- **Weak points:**
  - A narrative survey that stays within equities and is short on risk-based or rational counterarguments.
  - The 2009 attribution rests on one year and in-sample CAPM betas fitted within each calendar year (look-ahead), as the authors caution.
  - Equal-weighted deciles overweight small caps.
  - Missing: volatility scaling, residual momentum, and the Novy-Marx 12–7 "echo" finding.
- **Presentation issues:**
  - The text calls the 2009 beta ".79" but it is −0.79 in Table 1.
  - The "adjusted momentum" formula is typeset ambiguously (the regression terms are subtracted from MOM).
  - In the PDF text layer minus signs appear as control characters, so signs above follow the original table.

## Practical relevance for a quant PM
- Use 6/1/6 or 12/1 momentum with a skip month; industry momentum without the skip is mostly lag-1 autocorrelation.
- **Monitor conditional beta.** After market drawdowns WML is structurally short beta and crash-prone on rebounds. Hedge or scale the beta, and condition exposure on the lagged 36-month market return (and dispersion or volatility).
- Combine price momentum with SUE and analyst-revision signals: the 3×3 joint sort roughly doubles the univariate spreads.
- Expect stronger momentum where information is slow or uncertain (low coverage, growth, high dispersion, low credit rating). This also flags where crowding and crash risk concentrate.
