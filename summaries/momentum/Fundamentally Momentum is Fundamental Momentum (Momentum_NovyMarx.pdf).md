# Fundamentally, Momentum Is Fundamental Momentum — Novy-Marx (working paper) — Detailed Quantitative Research Notes

**Author:** Robert Novy-Marx (Simon School, University of Rochester) · **Year:** working paper, references through 2014 · **Venue:** working paper (JEL G12) · **Source file:** `Finance/Momentum_NovyMarx.pdf`

**Sample:** US equities, January 1975 – December 2012 (start dictated by quarterly Compustat earnings/RDQ coverage); subsamples 1/75–12/93 (roughly the CJL period) and 1/94–12/12.

---

## Claim

Price momentum is not an independent anomaly; it is a noisy expression of earnings (fundamental) momentum. Three layers of evidence:

1. **Cross-section (Fama–MacBeth):** earnings surprises subsume $r_{2,12}$.
2. **Time series (spanning):** UMD has a *negative* alpha on the earnings-momentum factors; the earnings factors have large alphas on UMD. Holds in large caps, net of costs, and for volatility-managed versions.
3. **Conditional construction:** price momentum *inside* earnings momentum is harmful — it contributes volatility and crash risk but no mean. Earnings momentum purged of past returns has lower vol, positive skew, and higher Sharpe.

The target is Chan–Jegadeesh–Lakonishok (1996), who concluded each variable has separate power. Novy-Marx argues their evidence rests on a 3×3 independent sort that is too coarse (within an earnings tertile, sorting on past return still spreads earnings surprises), and their FM tests use 6–12 month forward returns, percentile-rank regressors (which weakens the SUE signal), and no controls. Chordia–Shivakumar (2006) reached the same conclusion, but identified mostly off small caps.

---

## Variables

- **Past performance** $r_{2,12}$: return over months $t-12$ to $t-2$.
- **SUE:** most recent year-over-year change in quarterly EPS (Compustat EPSPXQ, basic, excl. extraordinary items), scaled by the SD of earnings innovations over the last 8 announcements (at least 6 required). Announcement dates from RDQ.
- **CAR3:** market-adjusted return from day $-1$ to $+1$ around the most recent announcement.

Average cross-sectional rank correlations: $\rho(r_{2,12},\text{SUE})=29.1\%$, $\rho(r_{2,12},\text{CAR3})=13.7\%$, $\rho(\text{SUE},\text{CAR3})=19.9\%$. SUE correlates more with the prior year's return than with the announcement reaction: most of the EPS news is in prices before the announcement. This is the mechanism by which $r_{2,12}$ proxies for fundamentals.

---

## 1. Fama–MacBeth (Table 1)

Monthly returns (%) on characteristics; controls $\ln ME$, $\ln B/M$, GP/A, $r_{0,1}$; regressors trimmed at 1/99%. t-stats in brackets.

| | (1) Full | (2) Full | (3) Full | (4) Early | (5) Early | (6) Late | (7) Late |
|---|---|---|---|---|---|---|---|
| $r_{2,12}$ | 0.59 [2.84] | | 0.15 [0.70] | 0.80 [3.79] | 0.30 [1.28] | 0.38 [1.05] | −0.00 [−0.00] |
| SUE | | 0.27 [17.0] | 0.26 [19.2] | | 0.30 [16.4] | | 0.21 [11.2] |
| CAR3 | | 5.84 [19.7] | 5.75 [20.4] | | 6.63 [15.2] | | 4.87 [13.9] |

Adding earnings surprises cuts the $r_{2,12}$ coefficient by about three quarters and kills its significance; adding $r_{2,12}$ leaves the SUE/CAR3 coefficients essentially unchanged. Controls behave as usual: $\ln B/M$ 0.30–0.46, GP/A 0.74–0.93 (t 3.8–6.8), $r_{0,1}$ −2.8 to −8.1. Note that $r_{2,12}$ is already insignificant on its own in the late sample (0.38 [1.05]).

**By size (Table A3):**
- **Large caps** (above the NYSE median): $r_{2,12}$ 0.51 [2.13] alone and 0.32 [1.33] with surprises. SUE 0.06 [4.41] and CAR3 3.18 [7.10].
- **Small caps** (NYSE deciles 3–5): 0.60 → 0.11.
- **Microcaps:** 0.61 → −0.01.

Caveat: in large caps in the late sample, the SUE coefficient is only 0.04 [1.68] and CAR3 is 1.25 [2.14], so earnings surprises are much weaker there too.

---

## 2. Spanning tests (Table 2)

SUE and CAR3 factors are built like UMD: 2×3 sorts on NYSE median size × NYSE 30/70 breakpoints of the surprise measure. The factor is the equal-weighted average of the value-weighted large-cap and small-cap high-minus-low legs. The regression is

$$y_t=\alpha+\beta' X_t+\varepsilon_t,\qquad X_t\in\{\text{FF3}\}\ \text{or}\ \{\text{FF3, other two momentum factors}\}.$$

**Panel A: y = UMD (monthly %)**

| | Mean | FF3 α | α on FF3+SUE+CAR3 | $\beta_{SUE}$ | $\beta_{CAR3}$ | adj. $R^2$ |
|---|---|---|---|---|---|---|
| Full | 0.64 [3.03] | 0.85 [4.05] | **−0.48 [−2.55]** | 1.18 [10.9] | 0.84 [6.09] | 40.6% |
| 75–93 | 0.82 [3.67] | – | −0.03 [−0.13] | 0.90 | 0.34 | 25.4% |
| 94–12 | 0.46 [1.29] | – | **−0.60 [−2.16]** | 1.35 | 1.03 | 50.1% |

(The "Early" and "Late" columns of the original table are raw means, specifications 4 and 6.)

**Panels B/C:** SUE mean 0.59 [7.14], α on FF3+UMD+CAR3 0.38 [5.31]. CAR3 mean 0.53 [8.42], α on FF3+UMD+SUE 0.37 [6.18]. Both are significant in both halves, with returns about 50% larger in the early half. The loadings are asymmetric: UMD loads 1.18 on SUE, while SUE loads only 0.18 on UMD. Earnings factors are about 6% vol against about 15.6% for UMD, so a large UMD-on-SUE beta is expected.

Figure 1: at 10% vol scaling, SUE and CAR3 grow a dollar far more than UMD over 1975–2012.

The paper links this to Hou–Xue–Zhang: HXZ's ROE factor prices momentum portfolios because ROE embeds post-earnings-announcement drift (PEAD), not because of the profitability level (Novy-Marx 2015, "How can a q-theoretic model price momentum?").

---

## 3. Within-size-quintile tests (Table 3)

Within each NYSE size quintile the paper forms top/bottom-30% value-weighted WML, SUE and CAR3 strategies, and regresses each on FF3 plus the other two strategies from the same quintile.

| Size quintile | 1 (small) | 2 | 3 | 4 | 5 (large) |
|---|---|---|---|---|---|
| % of market cap | 3.5 | 4.4 | 6.9 | 13.2 | 72.0 |
| Mean WML | 1.43 [5.48] | 0.88 [3.95] | 0.69 [3.06] | 0.47 [1.97] | 0.35 [1.48] |
| WML α | **−1.47 [−5.79]** | −0.13 | −0.04 | 0.08 | 0.18 [0.83] |
| Mean SUE | 1.50 [15.6] | 0.76 | 0.53 | 0.26 | 0.26 [2.46] |
| SUE α | 0.94 [9.84] | 0.41 | 0.44 | 0.18 | 0.29 [2.83] |
| Mean CAR3 | 1.29 [14.8] | 0.76 | 0.46 | 0.32 | 0.20 [2.12] |
| CAR3 α | 0.79 [9.03] | 0.60 | 0.35 | 0.28 | 0.15 [1.66] |

- Price momentum is insignificant relative to earnings momentum in every quintile, and strongly negative in microcaps.
- All ten earnings-strategy alphas are positive and significant at 5%, except large-cap CAR3 (10%).
- In the top quintile, even raw WML is insignificant (t = 1.48).

---

## 4. Conditional strategies (Section 3, Tables 4–5)

**Construction.** Within large/small halves, match stocks into groups of $n$ on the control variable. Within each group, go long the highest and short the lowest on the primary variable. Under independence, the expected rank of the max of $n$ uniforms is $n/(n+1)$, so $n=6$ gives 85.7%/14.3%, close to the 85/15 average ranks of a 30/70 tertile sort. (The paper prints 6/7 = "85.3%", 1/7 = "15.3%", which is a typo.) Because the two variables are correlated, $n=7$ is used so that the spread in the primary variable matches the univariate sort. Factors are the equal-weighted average of the value-weighted large- and small-cap legs.

The alternative triple-matched construction (Tables A5, A7) matches name diversification instead and gives consistent, if anything stronger, results.

**Figure 2 (rank spreads).** UMD's long–short spread in SUE rank is about one third of its spread in $r_{2,12}$ rank. SUE's spread in $r_{2,12}$ rank is about one third of UMD's. The conditional factors have essentially zero spread in the control variable.

**Table 4 (monthly %).**

| y | Mean | α vs. other-type factor | Key loadings |
|---|---|---|---|
| UMD | 0.64 [3.03] | 0.25 [3.95] vs UMD\|SUE; 0.09 [1.38] vs UMD\|SUE + SUE\|r | $\beta_{UMD\mid SUE}=0.86$ [71.4], $\beta_{SUE\mid r}=0.28$ [6.68] |
| SUE | 0.59 [7.14] | 0.04 [0.86] vs both conditional factors | $\beta_{SUE\mid r}=0.81$, $\beta_{UMD\mid SUE}=0.17$ |
| UMD\|SUE | 0.45 [1.93] | −0.23 [−3.18] vs UMD; −0.07 [−0.99] vs UMD+SUE | $\beta_{SUE}=-0.35$ [−7.64] |
| SUE\|$r_{2,12}$ | 0.58 | 0.25 [4.68] vs SUE; 0.22 [4.74] vs SUE+UMD | $\beta_{UMD}=-0.15$ [−12.4] |

- Stripping earnings news from UMD cuts its mean by about one third (to t = 1.93).
- Stripping price momentum from SUE leaves the mean intact and adds a large information ratio.
- UMD\|SUE is effectively *short* earnings momentum relative to UMD.

**Table 5 (higher moments, full sample, monthly data).**

| | MKT | UMD | SUE | UMD\|SUE | SUE\|$r_{2,12}$ |
|---|---|---|---|---|---|
| Vol (%) | 15.8 | 15.6 | 6.1 | 17.3 | 5.1 |
| Skew | −0.64 | −1.50 | −1.74 | −1.05 | **+0.46** |
| Excess kurtosis | 2.10 | 11.4 | 15.0 | 8.37 | 0.96 |
| Max loss, 10% vol (%) | 37.2 | 40.7 | 33.7 | 42.3 | **16.6** |
| Sharpe (annual) | 0.48 | 0.49 | 1.16 | 0.32 | **1.35** |

The crash and negative skew of plain SUE, including its spring-2009 drawdown (Fig. 3), come from its incidental past-return tilt. Once that tilt is neutralized, the drawdown disappears.

---

## 5. Constant-volatility strategies (Section 4, Table 6)

**Construction.** Following Barroso–Santa-Clara, each dollar-neutral strategy is levered each month by $\sigma^{\text{target}}/\hat\sigma_{t-1}$. Here $\hat\sigma_{t-1}$ is realized daily vol over the previous month, and the target is set so average leverage is about 1.

The paper rejects Daniel–Moskowitz's conditional-mean version because it uses full-sample fitted parameters, raising look-ahead concerns. Figure 4: leverage of all momentum strategies and of a constant-vol market strategy moves together, falling in 2000–01 and after 2008. Novy-Marx reads this as momentum volatility being tied to market-wide uncertainty, contrary to BSC's "momentum-specific risk".

**Results.**
- **Constant-vol UMD:** 0.85%/mo [6.34], at about 9.8% vol versus 15.6% for plain UMD. Its α on plain UMD+FF3 is 0.47 [5.65].
- **UMD α on the constant-vol factors:** relative to constant-vol SUE and CAR3 plus FF3, α = 0.02 [0.18], with $\beta_{SUE}=0.86$ [9.23] and $\beta_{CAR3}=0.57$ [5.33]. Subsamples: 0.14 [0.58] early, −0.07 [−0.43] late.
- **Constant-vol SUE:** 0.62 [9.96], α 0.36 [5.84] on the full set.
- **Constant-vol CAR3:** 0.54 [10.1], α 0.35 [6.22].

So vol management raises the Sharpe of both types, but constant-vol price momentum is still fully spanned by constant-vol earnings momentum.

---

## 6. Transaction costs (Appendix A, Tables A1–A2)

**Costs.** Effective spreads are estimated following Novy-Marx–Velikov (2014), using a Hasbrouck Gibbs-sampler Roll model. These are small-trader estimates that ignore price-impact convexity.
- Standard SUE turns over more than twice a year per side, costing about 35 bps/mo.
- UMD and CAR3 turn over about 3× a year, costing about 50 bps/mo.
- Vol targeting adds about 25 pp of leverage change per month, or about 25 bps/mo more, which eats most of its gross gain.

**Mitigation.** A buy/hold band: enter at the top/bottom NYSE quintile, exit when the stock leaves the top/bottom two quintiles. This cuts UMD turnover by about 50%, SUE by about one third and CAR3 by about one quarter.

**Net results (monthly %).**

| | Net mean | α on FF3 + other two net factors | Late-sample mean |
|---|---|---|---|
| UMDnet | 0.45 [2.03] | 0.01 [0.03] | 0.30 [0.80] |
| SUEnet | 0.32 [3.40] | 0.24 [3.22] | 0.22 [1.47] |
| CAR3net | 0.19 [2.50] | 0.10 [1.46] | 0.11 [0.84] |

After costs, the gross UMD result of a significantly *negative* α becomes a zero α: the tracking portfolio loads heavily on two costly factors.

**Ex-post MVE Sharpe ratios (Table A2, annual).**
- **Standalone:** UMDnet 0.33, SUEnet 0.55, CAR3net 0.41.
- **All three momentum factors together:** 0.57.
- **FF3 alone:** 0.81, rising to 1.16 with SUEnet and 1.19 with all three.
- **Late sample:** SUEnet 0.34, FF3 + all three 0.85.

UMDnet's MVE weight is about 0 whenever SUEnet is available.

---

## Critical assessment

**Convincing**
- The spanning results are one-directional and hold across subsamples, size quintiles, vol-managed versions and net-of-cost versions. That is hard to get by chance.
- The conditional-strategy design, which matches the primary-variable spread and checks it in Fig. 2, is cleaner than CJL's 3×3.
- The skewness result is the most practically important finding: SUE\|$r_{2,12}$ has +0.46 skew and a 16.6% worst loss, against −1.74 and 33.7% for plain SUE (at equal vol).

**Fragile or under-examined**
- *Spanning is not the same as explaining.* UMD's R² on SUE/CAR3 is only about 41%. What the tests show is that the *mean* of UMD is spanned. UMD still carries a large unpriced common component, which the paper concedes when it says past returns matter for realized-return comovement.
- *Weak statistics recently.* The earnings anomaly itself decays sharply after 1993, in large caps and net of costs:
  - late-sample SUEnet t = 1.47 and CAR3net t = 0.84;
  - large-cap late-sample SUE FM coefficient t = 1.68.
  
  "Earnings momentum subsumes price momentum" is strongest where both are weakest in economic terms. Late-sample UMD is itself insignificant (t = 1.29), which makes the negative α easier to obtain.
- *Uncorrected sampling error.* Sharpe and MVE comparisons are ex post and in-sample, with no standard errors on Sharpe differences.
- *Design choices not stress-tested.*
  - SUE uses a seasonal random walk scaled by innovation SD, and CAR3 is market-adjusted only; there is no analyst-forecast SUE and no characteristic-adjusted CAR.
  - Each factor uses only the most recent surprise, so signal staleness at $r_{2,12}$ horizons is not examined. Surprises from several quarters back, which drive part of $r_{2,12}$, are not included.
  - There is no out-of-US evidence.
- *Mechanism is asserted, not tested.* The claim that past returns proxy for pre-announcement incorporation of fundamentals rests on rank correlations. It does not rule out price momentum reflecting non-earnings news (industry momentum, analyst revisions), which the SUE/CAR3 factors may partly absorb through correlation.
- *Typos in the draft:* "fails to generate abnormal returns relative to the price momentum factors" should read *earnings* momentum factors; UMD's mean is given as both 64 and 65 bps; the Fig. 6 caption is pasted from a different paper (ROE/PEAD factors).

**Practical relevance for a quant PM**
- In a multi-factor alpha model with a PEAD/SUE sleeve, a standalone 12-1 momentum signal adds little expected return. Its role is as a *risk* factor (comovement, crash exposure), not an alpha factor.
- Neutralize $r_{2,12}$ (or UMD beta) in PEAD books. Going by Table 5, this roughly halves the worst drawdown at constant vol and turns skew positive, at no cost in mean.
- Conversely, stripping SUE from a momentum book leaves mostly the crash component: UMD\|SUE has a Sharpe of 0.32.
- Vol targeting helps gross performance but doubles turnover-related cost. Use banded rebalancing (buy/hold spreads) before relying on it.
- Capacity: net of costs and in the top size quintile, the edge is thin (large-cap SUE α about 29 bps/mo gross). Treat the headline small-cap numbers as upper bounds.
