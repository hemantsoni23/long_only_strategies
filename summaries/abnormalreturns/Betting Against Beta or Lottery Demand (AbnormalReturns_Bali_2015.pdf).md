# Betting Against Beta or Demand for Lottery? — Bali, Brown, Murray & Tang (2015) — Detailed Quantitative Research Notes

## Bibliographic Header

| Field | Detail |
|------|--------|
| **Title** | Betting against Beta or Demand for Lottery? |
| **Authors** | Turan G. Bali (Georgetown); Stephen J. Brown (NYU Stern; Melbourne); Scott Murray (Nebraska–Lincoln); Yi Tang (Fordham) |
| **Version** | Working paper, April 2015; recipient of the 2014 Jack Treynor Prize (Q-Group) |
| **Sample** | US common stocks (share codes 10/11) on NYSE/AMEX/Nasdaq with price ≥ $5 at end of month t−1; 594 months, July 1963 – Dec 2012; institutional ownership from 1980; funding-liquidity betas from 1968 (TED) / 1982 (VOLTED) |
| **Source file** | `Finance/AbnormalReturns_Bali_2015.pdf` (main text; the online appendix tables A1–A18 are referenced but not included) |

---

## Question

Frazzini–Pedersen (2014, FP) attribute betting against beta (low-beta stocks earn positive alpha and high-beta stocks negative alpha) to leverage-constrained investors who tilt toward high-beta stocks. The paper proposes a different source for the same price pressure: **lottery demand**. Investors who want large short-horizon upside (Kumar 2009; Barberis–Huang 2008 probability weighting; Barberis–Xiong realization utility) buy stocks with high probabilities of big up-moves. Market beta is one generator of such moves, so lottery demand falls disproportionately on high-beta stocks. This flattens the SML: the intercept rises above $r_f$ and the slope falls below the market premium.

## Variables

- $\beta$: slope of daily excess stock returns on daily market excess returns over the 12 months up to month t (at least 200 days).
- $MAX$: average of the five highest daily returns in month t (at least 15 days). The appendix shows the results hold for $k=1,\dots,5$.
- Controls:
  - characteristics: SIZE, BM, MOM (t−11..t−1), ILLIQ (Amihud), IVOL (1-month FF3 residual volatility);
  - risk measures: COSKEW, TSKEW, DRISK (downside beta), TRISK (bottom-10% tail beta), all from one year of daily data;
  - funding-illiquidity betas: $\beta^{TED}$, $\beta^{VOLTED}$, $\beta^{TBILL}$, $\beta^{FLEV}$ (financial-sector assets / equity), each from 5-year monthly regressions (at least 24 months).
- Inference: portfolio tests use equal weights unless stated, FFC4 alphas and Newey–West (6-lag) t-statistics.

## Main results

### Baseline anomalies
- **β deciles (Table 1):** mean β runs from about 0.00 to 2.02. Excess returns fall from 0.69% to 0.35%/month, with High−Low −0.35% (insignificant). FFC4 α: low-β +0.22% (t = 2.22), high-β −0.29% (t = −2.22), **High−Low −0.51% (t = −2.50)**. The High−Low portfolio loads 0.98 on MKT, +0.58 on SMB, −0.74 on HML and −0.21 on UMD. Decile 1 holds 1.92% of market cap and decile 10 holds 12.86%. β rises with MAX, IVOL, size and momentum.
- **MAX deciles (Table 2):** High−Low return −1.15%/month (t = −4.41); FFC4 α −1.40% (t = −8.95).

### MAX explains BAB
- **Dependent sorts (MAX, then β; Table 3):** High−Low β α = −0.14% (t = −0.85). Controlling instead for SIZE, BM, MOM, ILLIQ, IVOL, any risk measure or any funding-liquidity beta leaves α between −0.36% and −0.59% (t between −2.22 and −3.02). Only MAX removes BAB.
- **Independent 10×10 sorts (Table 5):** averaged across MAX deciles, High−Low β earns −0.03% (t = −0.13), with α −0.15% (t = −0.76). Within β deciles the MAX effect survives: average High−Low MAX α −1.64% (t = −9.99).
- **Orthogonalized sorts (Table 6):** sorting on $\beta^{\perp MAX}$ gives High−Low +0.13% (insignificant) and α +0.05%. Sorting on $MAX^{\perp\beta}$ gives −1.19% (t = −6.72) and α −1.44% (t = −10.62).
- **Fama–MacBeth (Table 4):**
$$R_{i,t}=\lambda_{0,t}+\lambda_{1,t}\beta_{i,t-1}+\lambda_{2,t}MAX_{i,t-1}+\Lambda_t X_{i,t-1}+\epsilon_{i,t}.$$
  - Without MAX, the β slope is 0.06–0.26 (t 0.44–1.08). With MAX it is 0.27–0.47 (t 1.90–2.34), and in the full model 0.47%/month (5.6%/year), i.e. about 0.76%/month between the top and bottom β quintiles.
  - MAX slopes are −0.22 to −0.36 (t −6.2 to −8.5).
  - The IVOL coefficient turns positive once MAX is added, replicating Bali–Cakici–Whitelaw, and becomes insignificant with the funding betas. TSKEW is negative; DRISK is negative in the full specification; all funding-liquidity betas are insignificant.
- **Robustness:**
  - The results hold value-weighted (Tables 7–8) and with β and MAX lagged 2, 3, 6 and 12 months.
  - They hold for alternative betas (Scholes–Williams, Dimson), FP's beta and FP's sample without the price filter (appendix).
  - They hold in expansions and contractions (CFNAI) and are not driven by 2007–09.

### Channel tests
- **Cross-sectional correlation:** $\rho_{\beta,MAX}$ averages 0.30 (median 0.29; range −0.03 to 0.84) and is negative in only 4 of 593 months.
- **Split by $\rho_{\beta,MAX}$ (Table 9):** in above-median months the High−Low β α is −0.72% (t = −2.86). In below-median months the return is −0.01% and α −0.26%, both insignificant. The MAX effect exists in both regimes (α −1.76% vs −1.05%, t = −5.77 in the low regime). High-ρ months have higher aggregate lottery demand: higher market MAX, higher average MAX and higher market volatility.
- **Institutional ownership (Table 10, 1980–2012):** within INST deciles, BAB returns and alphas are large and significant in deciles 1–5 and insignificant in deciles 7–10. The MAX effect likewise decays with INST. FP's leverage story predicts the opposite concentration, since constrained mutual funds and pensions are the institutions, which makes this the paper's sharpest discriminating test.

### Lottery factor FMAX
- **Construction:** 2×3 sort on NYSE-median size and 30/70 MAX breakpoints, value-weighted; **FMAX = average of the two high-MAX portfolios minus average of the two low-MAX portfolios**. Mean −0.54%/month (t = −2.55); FFC4 α −0.67% (t = −5.12).
- **High−Low β portfolio (Table 11):** α is −0.51% (FFC4) and −0.49% (FFC4+PS). Adding FMAX gives **+0.06% (t = 0.35)** and +0.04% (t = 0.22). The FMAX loading is 0.85 (t = 12.49), and the SMB loading becomes insignificant. Both legs lose their alpha: high-β +0.14% (t = 1.37), low-β +0.08% (t = 0.85).
- **FP's BAB factor (Table 12, Aug 1963 – Mar 2012):** α is 0.54% (FFC4) and 0.57% (FFC4+PS). Adding FMAX gives 0.17% (t = 1.23) and 0.22% (t = 1.39), with an FMAX loading of −0.55 (t = −11.84) and adjusted $R^2$ rising from about 22% to 47%. With FMAX included, the "beta-neutral" BAB factor shows a significantly positive market loading.
- **Reverse test:** FMAX α stays significant after adding BAB: −0.35% (t = −2.88) with FFC4+BAB and −0.32% (t = −2.32) with PS added. The spanning is one-directional. FMAX is correlated −0.18 with the Baker–Wurgler sentiment index.

### SML slope equals the market premium (Section 7)
- **Unit-β portfolios:** the paper strips the High−Low β portfolio's non-market factor exposures (SMB, HML, UMD, [PS], FMAX) using its estimated loadings and scales to unit market beta.
  - FFC4+FMAX: mean 0.55%/month (t = 2.16) vs a market premium of 0.46%; difference 0.09% (t = 0.36).
  - With PS: 0.50% (t = 1.88) vs 0.43%; difference 0.06% (t = 0.24).
  - Value-weighted: 0.68% (t = 2.12), difference 0.20% (t = 0.73).
  - $\beta^{\perp MAX}$ sorts: 0.54% (t = 2.14), difference 0.08% (t = 0.31).
- **FM slopes vs the premium:** differences of −0.19% (t = −1.39), −0.03% (t = −0.17) and −0.14% (t = −0.57, against a 1982–2012 premium of 0.61%).
- **Conclusion:** zero slope is rejected and slope = MRP is not rejected. Lottery demand is an overlay on a CAPM-consistent risk–return trade-off.

### Is MAX lottery demand rather than risk? (Section 8)
- High-MAX stocks have higher β, IVOL, DRISK and TRISK and lower COSKEW, all of which should imply *higher* expected returns under risk stories, yet they earn less.
- Stock-level FMAX betas (daily or monthly, with or without MKT) do not price in FM regressions, while MAX stays negative and β positive.
- MAX deciles line up with Kumar's lottery traits, both now and one month ahead:
  - price falls from $70.76 to $14.99;
  - IVOL rises from 0.94% to 4.58%;
  - ISKEW rises from −0.17 to 0.69.
- MAX is persistent: 31% of top-decile stocks stay top-decile next month and 29% after a year.

## Limitations

- **Equal-weighting and the $5 filter:** most headline tests are equal-weighted. Value-weighted versions are reported but in less detail, and the FMAX spanning uses value-weighted factor legs.
- **MAX is mechanically related to β and volatility:** a high-β stock in an up-market month has high MAX by construction, so "controlling for MAX" partly controls for realized beta × market moves. The orthogonalization and lagged-MAX tests help but do not fully separate lottery preference from this mechanical overlap. FP's own construction shrinks betas and uses correlations × volatilities, which the appendix addresses.
- **Weak power:** the SML-slope tests fail to reject slope = MRP with standard errors of about 0.25%/month, so they cannot exclude a moderately flatter SML either. The paper guards against low power by also rejecting zero, but the interval is wide.
- **Leverage constraints not ruled out:** the funding-liquidity proxies are stock-level betas on TED, TBILL, VOLTED and FLEV, which are noisy. Insignificance does not rule out leverage constraints, and the two channels could coexist (Baker–Bradley–Wurgler's benchmarking story is not tested directly).
- **Scope:** US only, with the sample ending in 2012. International and later out-of-sample evidence is outside this paper.

## Assessment

**Convincing:** the one-directional spanning (FMAX explains BAB; BAB does not explain FMAX) and the institutional-ownership split are the strongest pieces, because they discriminate between the stories rather than just showing correlation. The $\rho_{\beta,MAX}$ regime split supports the channel directly. The SML result is a useful reframing for practitioners: the "flat SML" is contamination by a lottery characteristic correlated with β.

**Fragile:** MAX is a one-month realized upside statistic that loads on β, IVOL and short-term reversal. Some of the "explanation" may be one noisy anomaly absorbing another. Treat FMAX as an empirical factor with a behavioral interpretation, not a proven mechanism.

**Practical relevance:**
1. **Hedge FMAX:** a low-beta or BAB sleeve is, to first order, short a lottery factor (High−Low β loads 0.85 on FMAX). If you run low-beta, measure and hedge FMAX, or target low MAX/IVOL directly, rather than low β.
2. **Where the effect lives:** BAB and MAX alpha concentrate in low-institutional-ownership names. Expect little in large, institutionally held universes, and account for borrow and costs on high-MAX shorts.
3. **Beta in expected returns:** after neutralizing MAX, β carries roughly the market premium per unit. In a cross-sectional return model that includes MAX, do not impose a zero or negative price on β.
4. **Timing:** BAB is strongest when $\rho_{\beta,MAX}$ and aggregate lottery demand (market MAX, market volatility, sentiment) are high. This is a conditioning variable for low-beta overlays.

## Relation to literature

The paper responds directly to Frazzini–Pedersen (2014) and Black (1972, 1993) on leverage constraints. It builds on MAX from Bali–Cakici–Whitelaw (2011) and lottery preferences from Kumar (2009), Barberis–Huang (2008) and Barberis–Xiong (2012). It is complementary to Baker–Bradley–Wurgler (2011) and Hong–Sraer (2012) on limits to arbitrage. It also connects to the IVOL puzzle of Ang–Hodrick–Xing–Zhang (2006), whose negative IVOL slope MAX absorbs, and to Stambaugh–Yu–Yuan (2012) on sentiment. International MAX evidence cited: Carpenter–Lu–Whitelaw (China), Annaert et al. and Walkshäusl (Europe), Zhong–Gray (Australia).

## Scholar Index Tags

`BAB`, `lottery`, `MAX`, `beta`, `FMAX`, `SML`, `institutional-ownership`, `funding-liquidity`, `Treynor-prize`, `2015`.
