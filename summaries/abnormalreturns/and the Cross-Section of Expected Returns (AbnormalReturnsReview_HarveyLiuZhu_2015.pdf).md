# … and the Cross-Section of Expected Returns — Harvey, Liu & Zhu (2016) — Detailed Quantitative Research Notes

**Campbell R. Harvey (Duke, NBER), Yan Liu (Texas A&M), Heqing Zhu (Oklahoma)** · *Review of Financial Studies* 29(1), 2016 (Advance Access Oct 9, 2015; doi 10.1093/rfs/hhv059) · JEL C12, C52, G12 · Source file: `Finance/AbnormalReturnsReview_HarveyLiuZhu_2015.pdf` · Factor list: http://faculty.fuqua.duke.edu/~charvey/Factor-List.xlsx

---

## Question and contribution

Fama–MacBeth (1973) accepted market beta with $t=2.57$. Since then hundreds of factors have been tested on essentially the same (overlapping, assumed stationary) cross-section, so single-test critical values are invalid. HLZ (i) catalogue the factor zoo, (ii) compute time-varying multiple-testing hurdles from 1967 to 2012 with a projection to 2032, and (iii) build a model that jointly estimates the unobserved number of tried factors $M$, the null fraction $p_0$, and the effect-size distribution, allowing for cross-correlation among factor returns. Conclusion: a new factor needs $t>3.0$ ($p=0.27\%$), and this is probably still too lenient; "most claimed research findings in financial economics are likely false."

Stated caveats: a theory-derived factor deserves a lower hurdle than a mined one (but not $t=2$); the analysis is unconditional; published $t$-stats are taken as econometrically sound.

## Data

- 313 papers (250 published in top finance/economics/accounting journals, 63 SSRN working papers covering 68 factors), 316 factors. Inclusion: papers that propose and test a new factor (plus the first empirical test of a theoretical one); different proxies for the same risk are both kept (e.g. KZ vs Whited–Wu constraints; four idiosyncratic-volatility variants); event studies and small-universe papers excluded.
- Taxonomy: 113 "common" factors (proxies for systematic risk) vs 202 "characteristics"; subcategories financial, macro (common only), microstructure, behavioral, accounting, other. Accounting-based characteristics are the largest single group.
- Discovery rate: ~1 factor/yr in 1980–1991, ~5/yr in 1991–2003, ~18/yr in the last nine years (164 factors, vs 84 in all earlier years).
- Absolute two-sided $t$-stats used (the sign of a long-short is arbitrary). About 20 factors lack reported $t$-stats.

## Framework

For $M$ tests with $R$ rejections, $N_{0|r}$ false rejections:

$$\mathrm{FWER}=\Pr(N_{0|r}\ge 1),\qquad \mathrm{FDR}=\mathbb{E}\!\left[\tfrac{N_{0|r}}{R}\,\middle|\,R>0\right]\Pr(R>0).$$

- **Bonferroni** (single-step, FWER): reject if $p_i\le\alpha_w/M$.
- **Holm** (step-down, FWER): with ordered $p_{(1)}\le\dots\le p_{(M)}$, reject $H_{(1)},\dots,H_{(k-1)}$ where $k$ is the first index with $p_{(k)}>\alpha_w/(M+1-k)$. Always at least as many rejections as Bonferroni.
- **BHY** (step-up, FDR under arbitrary dependence): reject $H_{(1)},\dots,H_{(k)}$ for the largest $k$ with $p_{(k)}\le k\alpha_d/(M\,c(M))$, $c(M)=\sum_{j=1}^M 1/j$ (the Yekutieli dependence penalty; $c(M)\approx 6.3$ at $M=316$).

Toy example (Table 4, 10 tests, all $t$ between 1.99 and 5.34, 5% level): single tests find 10, Bonferroni 3 (cutoff $p=0.50\%$), Holm 4 (0.60%), BHY 6 (0.85%).

Main calibration: $\alpha_w=5\%$, $\alpha_d=1\%$ (FDR is a laxer criterion, so a tighter level is used); $p$-values mapped back to $t$ via the normal. Extrapolation assumes the 2003–2012 factor-production rate continues to 2032.

## Results

### 1. Published factors only ($M=R$; a lower bound)

| | 2012 | 2032 (proj.) |
|---|---:|---:|
| Bonferroni 5% | 3.78 ($p=0.02\%$) | 4.00 ($p=0.01\%$) |
| Holm 5% | 3.64 | slightly below Bonferroni |
| BHY 1% | 3.39 (stable after 2010) | ~3.39 |
| BHY 5% | 2.78 | 2.81 |

Bonferroni/Holm rise monotonically with the number of tests; BHY is non-monotonic before 2000 and then stationary, because the FDR is a proportion that settles as $M$ grows. Headline: minimum ~2.8 even at FDR 5%.

Marked factors (Fig. 3): MRT (beta), HML, MOM, DCG (Yogo), SRV (Adrian–Rosenberg) clear all hurdles; EP, LIQ (Pastor–Stambaugh), CVOL sometimes; SMB, DEF, IVOL, LRV never.

Robustness:
- *Homogeneous subsample* (published ≥2000, Fama–MacBeth, sample covering at least 1970–1995, FF3 controls; 124 factors): Bonferroni 3.54, Holm 3.20, BHY(1%) 3.23, BHY(5%) 2.67.
- *Haircut to 113 common factors*: Holm 3.29 vs 3.64 at 316.
- *Lehmann–Romano FDP control* ($\Pr(\mathrm{FDP}>0.10)\le 0.05$): $t=2.70$.

### 2. Hidden tests, independent $t$-stats (Appendix A)

Assume all tried factors with $|t|>2.57$ are published and fit a truncated exponential to them (MLE $\hat\lambda=1/(\bar t-c)$, $c=2.57$). Implied population mean $|t|$ = 2.07; 71.1% of tried factors unobserved; 238 of 316 factors exceed 2.57, so $\hat M\approx 238/(1-0.711)\approx 824$ (bootstrap median 817); roughly 30% of factors with $t\in(1.96,2.57)$ are hidden. Resulting hurdles (Table A.1, $r=1$): Bonferroni 4.01, Holm 3.96, BHY(1%) 3.68, BHY(5%) 3.18. Doubling the assumed undercount roughly doubles $M$ (~1,650) and adds ~0.2 to Bonferroni/Holm but only ~0.03 to BHY. With plain BH ($c(M)=1$): 3.05 at 5%. The authors' "minimum across scenarios" is 3.18 — this, not the $M=R$ numbers, is the main source of the "$t>3$" rule.

### 3. Model with correlation (Section 4, Table 5)

Each tried strategy has returns normalised to $\sigma=15\%$ p.a., $N=240$ months, contemporaneous pairwise correlation $\rho$ (no serial correlation), and mean

$$\mu_i\sim p_0\,\delta_0+(1-p_0)\,\mathrm{Exp}(\lambda),\qquad T_i=\frac{\bar X_i}{\sigma/\sqrt N}.$$

Publication selection: the sample is assumed to contain a fraction $r$ of factors with $t\in(1.96,2.57)$ and all above 2.57 (baseline $r=1/2$: duplicate the 1.96–2.57 observations). $(\lambda,p_0,M)$ are estimated by simulated minimum distance (5,000 simulated samples) matching the number of discoveries (353 in the augmented sample) and the 20th/50th/90th percentiles of $t$ (2.39, 3.16, 6.34), with GMM-style inverse-variance weights; $\rho$ is calibrated on a grid because it is weakly identified. Thresholds are then found by simulation to hit a target FWER/FDR.

| $\rho$ | $p_0$ | $\lambda$ (%/mo) | $M$ | FWER 5% | FWER 1% | FDR 5% | FDR 1% |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.0 | 0.396 | 0.550 | 1,297 | 3.89 | 4.28 | 2.16 | 2.88 |
| 0.2 | 0.444 | 0.555 | 1,378 | 3.91 | 4.30 | 2.27 | 2.95 |
| 0.4 | 0.485 | 0.554 | 1,477 | 3.81 | 4.23 | 2.34 | 3.05 |
| 0.6 | 0.601 | 0.555 | 1,775 | 3.67 | 4.15 | 2.43 | 3.09 |
| 0.8 | 0.840 | 0.560 | 3,110 | 3.35 | 3.89 | 2.59 | 3.25 |

With $r=2/3$: $M$ = 2,458–5,392, $p_0$ = 0.68–0.92, FWER-5% hurdle 3.44–4.17, FDR-1% 3.30–3.55.

- $\hat\lambda\approx0.55\%$/month in every specification, i.e. true factors average 6.6% p.a., Sharpe 0.44 annual (0.13 monthly). Changing $N$ rescales $\lambda$ but barely moves the thresholds.
- $p_0$ and $M$ rise with $\rho$. At $\rho=0$, 60.4% of the 1,297 *tried* factors are non-null; at $\rho=0.6$, 39.9% of 1,775.
- FWER thresholds are non-monotonic in $\rho$: more nulls push them up, while correlation (fewer effective tests) pushes them down. FDR thresholds rise with $\rho$.
- Summary: $t\approx3.9$ for FWER 5%, $t\approx3.0$ for FDR 1%. These are close to the $M=R$ values, but for a different reason (~1,300+ tests plus correlation, vs 316 tests with no dependence structure).
- **Plausible $\rho$**: the minimised objective is lowest at $\rho=0.2$; S&P Capital IQ (~400 U.S. equity factors, 1985–2014) has average pairwise correlation 0.15; McLean–Pontiff ~0.05; Green–Hand–Zhang 0.06–0.20. Authors' view: ~0.2.
- **How many true factors?** The model implies hundreds of non-null factors, which conflicts with the prior of a handful of systematic risks. The authors reconcile this by noting that ~70% of "true" factors have $SR<0.5$ p.a. (built in by the decreasing exponential density), and concede that $p$-value-based methods cannot tell apart factors that all clear the bar. For further culling they point to Pukthuanthong–Roll (PCA-based criteria) and Harvey–Liu's incremental "lucky factors" framework.

### 4. False discoveries among published factors

Of 296 published significant factors, 158 (Bonferroni), 142 (Holm), 132 (BHY 1%) and 80 (BHY 5%) are false discoveries, i.e. 27%–53%. This is compared with the ~5 statistical common factors found by PCA (Ahn–Horenstein–Wang 2012).

### Why hurdles should rise over time

The low-hanging fruit has been picked (the prior probability of a true discovery falls), the data are finite (CRSP cannot be re-run like a particle collider; the Higgs discovery required $t>5$), and the cost of mining has collapsed, so tried factors now carry weaker priors. Out-of-sample validation is cleaner but not available in real time: hold-out data are observed, and McLean–Pontiff dropped 12 of 97 anomalies that failed even in-sample replication (i.e. 100% decay). Replication studies are rarely published in finance, which biases the literature toward new factors.

## Critical assessment

- **Convincing:** the qualitative result holds across three quite different routes ($M=R$ lower bound, truncated-exponential hidden tests, correlated structural model): classical 1.96 is far too low, and 3.0 is a reasonable floor. The catalogue itself is a lasting public good.
- **Fragile:**
  - The hidden-test models rest on strong functional forms: an exponential $|t|$ or effect-size density, a hard publication cutoff at 2.57, and an ad hoc $r$.
  - $\rho$ is not identified from single $t$-stats. A single equicorrelation ignores clusters (the value/price-scaled family, the IVOL variants), which is exactly where dependence matters.
  - $t$-stats are pooled across heterogeneous samples, periods and methods (FM slopes vs long-short spreads) and treated as tests of one cross-section.
  - $\mu_i$ is drawn independently of $\rho$, and the claim that "true" means non-zero mean conflates a priced risk factor with an anomaly that has positive raw returns.
  - The 27–53% false-discovery figures apply the same procedures to the same sample, not an independent validation.
- **Later debate:** subsequent work (e.g. Bayesian or shrinkage replications) argues the replication crisis is milder once effect-size shrinkage and factor clustering are modelled. The HLZ hurdle is best read as a governance rule of thumb, not a calibrated posterior.
- **For a quant PM/researcher:**
  - The unit of inference is the research programme, so count your own trials (including failures and parameter variants) and apply Holm/BHY to the full log. A signal with $t\approx2.5$ is not evidence.
  - Use FWER-style hurdles (~3.5–4) for the few factors that get large risk budgets or define the risk model; FDR-style (~3.0) for a diversified set of small alphas, where some duds are tolerable.
  - Residualise candidates against existing book factors before testing. Correlation lowers FWER hurdles only modestly unless $\rho$ is extreme.
  - The estimated true-factor Sharpe of ~0.44 gross, before costs and post-publication decay, implies modest net premia, which argues for sparse factor models.
  - Machine-learning searches with many hyperparameters face an even larger effective $M$ than the 316 linear factors counted here.
