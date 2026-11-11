# Are "Market Neutral" Hedge Funds Really Market Neutral?

**Andrew J. Patton (Oxford / Oxford-Man Institute) · first version Mar 2004, this version 10 Oct 2007 · Source file `Finance/[Patton] - Are Market Neutral Funds Really Market Neutral 2007.pdf` · HFR + TASS monthly net-of-fee returns, live and dead funds, Apr 1993–Apr 2003 (max 121 months); 1,423 funds with ≥12 obs in five self-reported styles; market proxy S&P 500 (MSCI World/Europe in robustness)**

## Claim / contribution

1. "Market neutral" is usually defined as zero correlation/beta, which is inadequate for dynamic, nonlinear hedge-fund payoffs. Patton proposes a hierarchy of neutrality concepts — **mean, variance, VaR, tail, complete** — each tested either against a general alternative or against a one-sided "downside" alternative disliked by a risk-averse investor already long the market (analogy: the option "Greeks").
2. About **one quarter** of self-described market-neutral (MN) funds are significantly non-neutral at 5% (29.2% general joint test, 20.5% downside joint test), which is significant for the category as a whole — but MN is still by far the **most** neutral style (joint-failure rates 50–86% for the other styles).
3. Violations run almost entirely through the **conditional mean** (linear or nonlinear); after controlling for it, variance, VaR and tail tests reject at roughly nominal size (low power given short histories).

Motivation: dollar neutrality is verifiable but says nothing about risk neutrality; lawsuit Weyerhaeuser v. Geewax Terker (settled for \$8m) turned on whether a manager was really "market neutral". Tests also measure the "purity" of portable-alpha strategies.

## Data (Tables 1–2)

Median-fund monthly statistics (funds with ≥12 obs):

| | MN | Equity hedge | Equity non-hedge | Event driven | FoF | S&P 500 |
|---|---:|---:|---:|---:|---:|---:|
| Mean % | 0.68 | 1.00 | 1.05 | 0.86 | 0.69 | 0.85 |
| Std % | 2.35 | 4.35 | 5.89 | 2.52 | 1.88 | 4.52 |
| Skew | 0.02 | 0.20 | 0.04 | −0.17 | −0.03 | −0.54 |
| Kurtosis | 3.80 | 3.96 | 4.02 | 4.56 | 4.23 | 3.26 |
| AC(1) / AC(2) | 0.06 / 0.01 | 0.08 / 0.00 | 0.06 / −0.07 | 0.19 / 0.06 | 0.19 / 0.03 | −0.03 / −0.03 |
| Median # obs | 42 | 44 | 79 | 58 | 40 | 121 |
| # funds (≥12 obs) | 197 | 514 | 79 | 102 | 531 | – |

MN funds: 217 in total (175 live, 42 dead); 171 with ≥18 obs, 150 with ≥24, 59 with ≥66; only 16 have the full 121-month history. Minimum histories used: 18 obs (correlation, rank correlation), 24 (mean/variance), 66 (VaR), 100 (tail).

**Serial correlation:** each fund's returns are filtered with an MA(2) (Getmansky–Lo–Makarov smoothing/illiquidity model) and the residuals used as "true" returns; the MA is re-estimated inside every bootstrap sample so its estimation error is propagated.

## Neutrality concepts, tests and results for MN funds

Notation: $r_{it}$ fund (filtered), $r_{mt}$ market, $\mu_i(r_m)=E[r_{it}\mid r_{mt}]$.

**Correlation neutrality.** Mean correlation 0.025, cross-sectional 5–95% range [−0.52, 0.53]. 28.1% significant at 5%; 23.4% significantly *positive*. Critical rejection proportion: 7.74% under independence across funds (Binomial), **18.75%** under bootstrap cross-fund dependence → the category rejects.

**Mean neutrality:** $E[r_{it}\mid r_{mt}]=E[r_{it}]\ \forall r_{mt}$ (market does not Granger-cause the fund in mean). Implemented by a cubic Taylor approximation (piecewise-linear with estimated kinks has identification problems under the null):

$$
r_{it}=\beta_0+\beta_1r_{mt}+\beta_2r_{mt}^2+\beta_3r_{mt}^3+e_{it},\qquad H_0:\beta_1=\beta_2=\beta_3=0 \ \text{(Wald)}.
$$

Rejected for **28.0%** (150 funds). *Downside mean neutrality*: $H_0: E[\partial\mu_i/\partial r_m\mid r_m\le 0]\le0$, with $\partial\mu_i/\partial r_m=\beta_1+2\beta_2r_m+3\beta_3r_m^2$ evaluated at the sample moments $E[r_m\mid r_m\le0]$, $E[r_m^2\mid r_m\le0]$ (averaging avoids the size distortion of searching over all $r_m$): rejected for **20.0%**. Omitted factors correlated with the market are counted as market exposure by design.

**Variance neutrality** (after removing the cubic mean): $V[r_{it}-\mu_i(r_{mt})\mid r_{mt}]$ constant. Motivated by preferences for skewness (non-increasing ARA) and against kurtosis (decreasing absolute prudence, Kimball), i.e. investors want $\mathrm{Corr}[(r_i-\mu_i)^2,r_m-\mu_m]\ge0$ and $\mathrm{Corr}[(r_i-\mu_i)^2,(r_m-\mu_m)^2]\le0$. Test $\gamma_1=\gamma_2=0$ in

$$
\sigma_i^2(r_{mt},e_{i,t-1})=\gamma_0+\gamma_1r_{mt}+\gamma_2r_{mt}^2+\gamma_3e_{i,t-1}^2\quad(\text{ARCH(1) control}).
$$

Rejected for **4.0%** (downside version, $E[\partial\sigma_i^2/\partial r_m\mid r_m\le0]<0$: also 4.0%). Without the mean control: 8.1% (downside 2.0%).

**VaR (quantile) neutrality**, on standardized residuals $\varepsilon_{it}=(r_{it}-\mu_i)/\sigma_i$ (otherwise mean/variance dependence mechanically creates VaR dependence): Christoffersen-type test of $\Pr[\varepsilon_i\le\widehat{VaR}\mid\varepsilon_m\le\widehat{VaR}]=\Pr[\varepsilon_i\le\widehat{VaR}]$, 10% VaR, market filtered with AR(1)-ARCH(1). 59 funds: **0%** rejections (downside version also 0%); without mean/variance controls 13.8%.

**Tail neutrality:** zero lower-tail dependence,

$$
\tau^L=\lim_{q\to0}\Pr[F_i(r_i)<q\mid F_m(r_m)<q]=0 \quad\text{vs.}\quad \tau^L>0,
$$

tested with Quintos (2003) nonparametric EVT statistic (asymptotic, not bootstrap). Of 28 funds with ≥100 obs, only 15 had enough joint-tail observations; **1 of 15** rejects (6.7%). Contrasts with Brown–Spitzer (2006), who find lower-decile dependence using parametric copulas and i.i.d. assumptions.

**Complete neutrality:** independence, $f(r_i,r_m)=f_i f_m$, i.e. copula density $c\equiv1$. Epstein–Tanny (1980): a "correlation-increasing transformation" moves the copula above $C_I$ in concordance order, and for $u=U(w_ir_i+w_mr_m)$ with concave $U$ and no short sales ($w_i,w_m\ge0$), $\partial^2u/\partial r_i\partial r_m=U''w_iw_m\le0$ → every such investor is correlation averse, so concordance order = expected-utility order. Spearman's $\rho_S$ respects concordance order, so it is used as the scalar test. Mean $\rho_S$ 0.018; **28.1%** significant, **22.8%** significantly positive. Conditioning on the mean model cuts these to 8.6% (5.2%); on mean + variance to 5.2% (6.9%) → mean non-neutrality is the main channel.

**Joint test (§3.7, Appendix).** Declaring a fund non-neutral if it fails any of five 5% tests would have size ≈ 0.23 under independence. Instead, on 1,000 stationary-bootstrap samples with fund and market resampled **separately** (imposing independence while preserving marginals and serial dependence), count the number of the five tests (correlation, mean, variance, VaR, complete) failed; a fund fails jointly if its actual count exceeds the bootstrap 95th percentile (range 0–2, median 1, mean 0.8). Tail test excluded (too few funds). Results: **29.2%** fail the general joint test, **20.5%** the downside joint test; both > 18.75%.

Bootstrap details: Politis–Romano stationary bootstrap; block length from Politis–White applied to returns, squared returns and cross-products, taking the maximum (range 1–10, mean 2.4). Critical proportions for the category use a vector bootstrap on the funds present for the full sample only (16 MN funds): 0.188 for most tests, 0.125 for VaR. Binomial critical proportions: 0.077–0.102 depending on the test.

**HFR Equity Market Neutral index** passes everything: individual-test p-values 0.14–0.75, both joint-test p-values 0.14 → individual exposures offset in aggregate.

## Neutral vs. non-neutral MN funds (Table 3)

Equal-weighted portfolios of MN funds passing (up to 136 funds) vs. failing (up to 35) the downside joint test:

| | Neutral | Non-neutral |
|---|---:|---:|
| Average size (AUM at last obs) | \$57.5m | \$79.3m |
| Average age | 55.4 months | 75.7 months |
| Mean / Std (% per month) | 0.79 / 0.74 | 1.19 / 1.78 |
| Skewness / kurtosis | 0.20 / 3.19 | −0.34 / 3.59 |
| Corr with S&P 500 | −0.08 | 0.78 |
| Corr given $r_m>0$ / $r_m\le0$ | −0.20 / −0.21 | 0.61 / 0.70 |
| Corr given past 6-month market return above / below average | 0.10 / −0.30 | 0.72 / 0.82 |
| Corr with Equity Hedge index | 0.14 | 0.74 |

After controlling for a cubic in the market, the Equity Hedge index is the style index that best explains the non-neutral portfolio (robust t = 5.15 alone; 2.16 and the only significant one when all four style indices enter jointly) → these funds behave like equity hedge. Non-neutral funds earn more but with 2.4× the volatility and negative skew; neutral funds become *more* negatively correlated in down/weak markets, non-neutral ones more positively.

## Cross-style comparison (Table 4) — main result

Proportion of funds rejecting at 5% (Panel I general / Panel II downside):

| Test | MN | Equity hedge | Equity non-hedge | Event driven | FoF |
|---|---:|---:|---:|---:|---:|
| Correlation | 0.281 / 0.234 | 0.543 / 0.560 | 0.857 / 0.870 | 0.656 / 0.700 | 0.482 / 0.510 |
| Mean (cubic) | 0.280 / 0.200 | 0.481 / 0.543 | 0.805 / 0.779 | 0.558 / 0.709 | 0.459 / 0.611 |
| Variance | 0.040 / 0.040 | 0.031 / 0.019 | 0.065 / 0.000 | 0.035 / 0.012 | 0.070 / 0.012 |
| VaR | 0.000 / 0.000 | 0.022 / 0.022 | 0.035 / 0.035 | 0.021 / 0.021 | 0.024 / 0.024 |
| Tail (downside only) | 0.067 | 0.106 | 0.250 | 0.067 | 0.021 |
| Complete (Spearman) | 0.281 / 0.228 | 0.569 / 0.571 | 0.857 / 0.870 | 0.589 / 0.667 | 0.516 / 0.523 |
| **Joint** | **0.292 / 0.205** | 0.539 / 0.562 | 0.857 / 0.844 | 0.611 / 0.700 | 0.497 / 0.538 |

The cubic mean test rejects slightly *less* often than the linear correlation test: extra flexibility costs more in estimation error than it gains with ~40-month samples. Risk-based tests reject at about nominal size for every style. Style-index correlations with the S&P 500 over the sample: MN 0.42, EH 0.68, ENH 0.81, ED 0.68, FoF 0.49.

## Robustness (Tables 5–7, MN funds)

| Variant | Joint (general) | Joint (downside) |
|---|---:|---:|
| Benchmark (S&P 500, USD, MA(2)) | 0.292 | 0.205 |
| MSCI World | 0.269 | 0.240 |
| MSCI World, GBP investor | 0.216 | 0.246 |
| Drop last 6 months (end-game) | 0.230 | 0.212 |
| Drop first 12 months (backfill) | 0.247 | 0.220 |
| MA(0) / MA(4) | 0.281 / 0.275 | 0.257 / 0.175 |
| Live (175) / dead (42) funds | 0.307 / 0.226 | 0.214 / 0.161 |

- Live vs. dead: the only notable difference is downside mean neutrality (live 23.8% vs. dead 3.6%; all but one failing fund is alive).
- Age (Fig. 1): correlation with the S&P 500 rises significantly with the number of observations (robust to dropping two 121-month funds with correlation > 0.9). Candidate explanations: style drift (prospectuses often commit to neutrality only for ~3 years), more test power, or exposure to the late-1990s bull market.
- Sub-samples (Table 7; only funds with full history — 16 MN funds): joint general rejection for MN 0.375 in both Apr-1993–Dec-1998 and Jan-1999–Apr-2003; downside 0.375 → 0.188. EH 0.706 → 0.549, ED 0.857 → 0.500, FoF 0.755 → 0.469, ENH 0.850 → 0.900 (general). The paper's "four of five styles more non-neutral in the first sub-sample" holds for the downside panel; in the general panel MN is flat. Full-history funds reject more often than the full cross-section (MN 0.375 vs. 0.292; ED 1.000 vs. 0.611), consistent with either power or age effects — the paper cannot separate age from market regime.

## Critical assessment

- **Convincing:** the framework (null of independence imposed by separate block bootstraps, MA-filter uncertainty propagated, preference-based one-sided alternatives, a size-controlled joint test and a dependence-robust cross-sectional critical value) is careful and reusable. The main qualitative result — MN funds are the least market-exposed style but a quarter still carry significant, mostly linear, positive exposure — is stable across every robustness variant (joint rates 0.17–0.31).
- **Fragile / caveats:** (i) power is low (median 42 months), so "no evidence" of variance/VaR/tail dependence is weak, and VaR/tail tests are run only on long survivors (survivorship); (ii) the cross-sectional critical value relies on only 16 full-history MN funds; (iii) a single market factor tests a necessary condition only — no size, value, momentum or credit factors; (iv) unconditional tests average over time-varying exposures; (v) apparent tension: the HFR EMN index passes all tests (p ≥ 0.14), yet footnote 21 reports a 0.42 correlation between the "Market Neutral index" and the S&P 500 — likely the paper's own equal-weighted style index rather than HFR's, but it is not clarified; (vi) the abstract's "1,423 funds" is the ≥12-obs count; Table 2 lists 1,619 funds in total; (vii) pre-2008 sample — the 2007 quant crunch and 2008 are not covered.

## Practical relevance for a quant PM

- A ready QA battery for any "neutral" book (own stat-arb, pod, or external manager): MA(2)-filter returns, then linear correlation, cubic-mean Wald test, downside-slope test at $E[r_m\mid r_m\le0]$, Spearman, and a count-based joint test with fund/market resampled independently. Most of the detection power sits in the first two.
- Measure exposure conditional on down or weak markets: non-neutral MN funds' correlation rises to 0.70–0.82 exactly when diversification is needed, while truly neutral ones go negative.
- Diversifying across MN managers restored neutrality at the index level in this sample; single-manager allocations need per-fund testing, with extra scrutiny for older, larger funds (style drift towards equity hedge).
- For portable alpha, test the residual against the investor's existing risk (a composite index of their exposures), as Patton suggests, rather than adding many regressors to short samples.
