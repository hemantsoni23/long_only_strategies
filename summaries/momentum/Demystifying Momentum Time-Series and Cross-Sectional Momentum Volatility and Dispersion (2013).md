# Demystifying Momentum: Time-Series and Cross-Sectional Momentum, Volatility and Dispersion

**Johan du Plessis · 2013 · MSc thesis (Stochastics & Financial Mathematics, Univ. of Amsterdam; written at Robeco, supervisors W. Hallerbach, P. Spreij) · Source file `Finance/AbnormalReturnsMomentum_DuPlessis_2013_Thesis.pdf` · Data: FF49 value-weighted industries (monthly; IS Jul-1969–Jun-1994, OOS Jul-1994–Dec-2012) and Robeco MAA 17 asset classes (weekly Wed–Wed excess returns; IS 4-Jan-1979–5-Dec-2002, OOS 5-Dec-2002–17-Apr-2013)**

## Claim / contribution
- Puts cross-sectional (XS) and time-series (TS) momentum in one notation (7 strategy variants), decomposes their expected profits into auto-covariance / cross-serial covariance / mean terms, and tests where the two differ.
- Gives conditions (Sharpe-ratio algebra) under which volatility weighting helps, and shows empirically that **running strategies on vol-normalised asset returns** beats scaling the strategy by its own vol.
- Studies the puzzling negative momentum–dispersion link. Honest thesis: several in-sample conclusions **fail in the hold-out**, which the author flags explicitly (✓/✗ checklist in Ch. 7).

## Setup
MAA universe: 4 equity indices (US, EU, JP, EM), govt bonds (US, EU, JP) + EM debt, US REITs, SMB and HML (US), US IG and HY credit (HY spliced to CDX), oil, gold, USD and JPY cash. Mostly futures-implementable; different market closes ignored (no lag). Industry returns are multiplicative excess over T-bill. No transaction costs anywhere.

**Strategy weights** (formation window $j$, $\bar r=\frac1{N_t}\sum_i r_{i,t-j,t}$, $\tilde r_i=r_{i,t-j,t}-\bar r$):

| Code | Weight $w_{i,t}$ |
|---|---|
| qxs | $\frac1{n_t}\big(\mathbf 1\{\text{rank}>N_t-n_t\}-\mathbf 1\{\text{rank}\le n_t\}\big)$, $n_t=\lfloor N_t/q\rfloor$ ($q=4$ FF49, 3 MAA; 2 in long–short analysis) |
| ulxs | $\tilde r_i/N_t$ (Lo–MacKinlay/Lewellen) |
| slxs | $\frac{2}{N_t}\tilde r_i\big[\sum_k\lvert\tilde r_k\rvert\big]^{-1}$ (meant: gross 1 per leg) |
| sxs | $\frac2N\big(\text{sign}\,\tilde r_i-\frac1N\sum_k\text{sign}\,\tilde r_k\big)$ |
| sts | $\text{sign}(r_{i,t-j,t})/N_t$ |
| ults | $r_{i,t-j,t}/N_t$ (MOP linear TS) |
| slts | $\frac1{N_t}r_{i,t-j,t}\big[\sum_k\lvert r_{k,t-j,t}\rvert\big]^{-1}$ (meant: total gross 1) |

"Global" TS = sign/linear rule on the equal-weighted market applied to all assets. Portfolios rebalanced to the formation weights every month/week; holding periods overlap.

**Linear decompositions** (Lewellen 2002; MOP 2012), $\Omega=\text{Cov}(r_{t-j,t},r_{t,t+k})$:
$$E[r^X]=\underbrace{\tfrac{N-1}{N^2}\text{tr}\,\Omega}_{\text{auto}}-\underbrace{\tfrac1{N^2}(\mathbf 1'\Omega\mathbf 1-\text{tr}\,\Omega)}_{\text{cross}}+\underbrace{\sigma^2_{\mu}}_{\text{mean}},\qquad E[r^T]=\tfrac{\text{tr}\,\Omega}{N}+\tfrac{\mu'\mu}{N}.$$
XS gains from positive auto-cov, **negative** cross-serial cov and cross-sectional variance of means; TS ignores cross terms and gains from $\mu'\mu$ (any common drift). Global TS:
$$E[r^{GT}]=\tfrac{E[r^T]}{N}+\tfrac1{N^2}(\mathbf 1'\Omega\mathbf 1-\text{tr}\,\Omega)+\tfrac1{N^2}(\mathbf 1'\mu\mu'\mathbf 1-\text{tr}\,\mu\mu'),$$
i.e. a down-weighted local TS plus a *short* position in XS's cross-serial and off-diagonal mean terms.

**Two-asset intuition (Prop. 2.1).** XS and TS coincide in up|down formation states and differ only in up|up and down|down states; $r^X-r^T=\pm2r_{i,t}$ on the asset where they disagree. With independent AR(1) assets, $c,\phi>0$, symmetric shocks: $E[r^X-r^T]\le0$. With a pure lead–lag $r_{1,t}=c+\phi r_{2,t-1}+\varepsilon$ and $\phi$ sufficiently negative: $E[r^X-r^T]\ge0$. Large common drift pushes towards TS.

**Signed TS (Hallerbach 2011).** With $S_t=\text{sign}(r_{t-1}r_t)$ independent of $|r_t|$, $P(S=1)=p$: $E[r]=(p-q)E|r_t|$, i.e. profit requires hit rate > 50% (contrast Potters–Bouchaud).

**Volatility weighting (Prop. 2.2).** Model $r_t=\alpha+\gamma\sigma_t+\varepsilon_t\sigma_t$, $\sigma_t$ predictable; weighted $r^*_t=r_t/\sigma_t$.
- $\alpha=0$: $SR(r^*)=\gamma\ \ge\ SR(r)=\gamma/\sqrt{(\gamma^2+1)CV(\sigma)^2+1}$ — the gain grows with the vol-of-vol $CV(\sigma)$, and the vol-weighted rule is optimal among predictable weightings.
- $\gamma\le0$: sufficient condition $\alpha\in[-\gamma E\sigma,\Lambda]$, $\Lambda=\sqrt{\big((\gamma^2\text{Var}\,\sigma+E\sigma^2)E[1/\sigma]^2-1\big)/\text{Var}(1/\sigma)}$. So the vol-independent part of returns must not be too large. Weighting can *induce* a negative return–vol relation ($\alpha/\sigma_t$ term).
- EWMA vol: λ = 0.9836 (≈61 trading days, daily data) for FF49; λ = 0.97 (≈33⅓ weeks) for MAA. Seeds are 21 days / 52 weeks, and the target is 10% annualised.

## Main results (in-sample unless stated)

**Sharpe ratios, J = 12m/52w and 1m/4w formation, K = 1 holding period (Table 3.3):**

| | qxs | slxs | sts | slts | EW market |
|---|---|---|---|---|---|
| FF49 12m | 0.78 | 0.69 | 0.10 | 0.25 | 0.28 |
| FF49 1m | 1.01 | 0.77 | 0.47 | 0.54 | 0.28 |
| MAA 52w | 0.88 | 0.69 | 1.08 | 0.58 | 0.70 |
| MAA 4w | 1.11 | 0.88 | 1.34 | 0.89 | 0.70 |

- XS dominates for industries (robust alpha qxs on sts: 9.66%/yr, p = 0.000 at 12m), TS dominates for MAA (sts on qxs: 2.18%, p = 0.000 at 4w). TS–XS correlations: FF49 0.59 (12m), 0.31 (1m); MAA ≈0.90. The MAA correlation is high even though average pairwise asset correlation is only 0.07 (vs 0.64 for industries). The two strategies simply hold the same positions most of the time.
- Short holding periods are best, and there is no short-term reversal in industries or asset classes. Unscaled linear strategies have extreme kurtosis (MAA ulxs ≈ 112–123), so they are academically useful but impractical. Scaling or quantiles help, i.e. reducing exposure to dispersion helps.

**Decomposition (Table 4.1, % p.a., share of total):**

| | auto | cross | mean | total |
|---|---|---|---|---|
| FF49 12m XS | −0.43 | 0.88 | 0.07 | 0.52 |
| FF49 12m TS | −0.44 | – | 0.49 | 0.05 |
| FF49 1m XS | 0.49 | −0.36 | 0.01 | 0.13 |
| MAA11 52w XS / TS | 0.50 / 0.55 | −0.11 / – | 0.22 / 0.32 | 0.61 / 0.87 |

12m industry XS profits come from lead–lag (negative cross-serial) effects. The 12m industry TS strategy has *negative* auto-covariance and earns only the mean term. Elsewhere auto-covariance dominates, as in MOP rather than Lewellen. The FF49 1m result stays a puzzle: the decomposition favours TS, yet XS has the higher Sharpe.

**Long–short and scenario analysis (2-quantile XS vs sts).**
- Industries: XS wins mainly through **reversal of losers in down|down states** (scenario 4).
- MAA: TS wins through **continuation of positive returns**.
- In both datasets long|long beats short|short, and in industries the short leg even loses. Profits are concentrated in longs.
- XS could be improved by shorting only bottom-quantile assets that also have negative TS signals; the converse does not help TS.
- Hit rates are modestly above 50% and above the independence benchmark. Accuracy and Sharpe are lower in high-vol states, except for industry TS.

**Global vs local TS (Table 4.9, SR local/global):** FF49 12m 0.11/0.10, 1m 0.49/0.40; MAA 52w 1.12/0.48, 4w 1.33/0.98. Only the 3-bond subset is marginally better globally at 52w (0.91 vs 0.90). Global TS down-weights auto-covariance, which is the main profit source.

**Volatility weighting (Tables 5.3–5.4; SR unweighted → own-vol → normalised returns):**

| | unweighted | own vol | normalised |
|---|---|---|---|
| FF49 qxs 12m | 0.77 | 0.94 | 1.12 |
| FF49 qxs 1m | 1.02 | 1.12 | 1.43 |
| FF49 sts 1m | 0.49 | 0.47 | 0.52 |
| MAA qxs 4w | 1.07 | 1.27 | 1.84 |
| MAA sts 4w | 1.33 | 1.53 | 1.99 |
| FF49 EW market | 0.30 | 0.20 | 0.26 |

- Own-vol weighting helps where the strategy's relation to its own vol is negative (most cases). It hurts where the relation is positive (FF49 1m sts, EW market).
- Normalised returns give large, significant robust alphas vs unweighted: MAA qxs 4w 8.39% (t = 6.39), MAA sts 4w 2.67% (t = 6.78), FF49 qxs 1m 3.06% (t = 4.74). Industry TS alphas are insignificant.
- Kurtosis falls consistently. Skew and drawdown effects are mixed.
- The normalisation gain does *not* come from stronger momentum in normalised returns: predictive slopes are weaker. It comes from vol stabilisation and timing, from investing less in the most extreme (volatile) assets, and mostly from periods when TS and XS signals agree.

**Dispersion and market volatility.**
- Naive AR(1) models predict XS profits increasing in lagged dispersion. Empirically the slopes are mostly **negative** (weak), also OOS.
- Momentum is mostly negatively related to market vol, and this persists under normalisation.
- Dispersion is AR(1)-forecastable but less so than vol. Dividing XS positions by forecast dispersion raises SR: MAA qxs 52w 0.88 → 1.02 (actual-dispersion oracle 1.28), 4w 1.08 → 1.28 (1.39). FF49 gains are marginal (12m 0.88 → 0.92).
- Normalising returns lowers the coefficient of variation of dispersion and market vol. OOS: dispersion 0.28 vs 0.39 (FF49), 0.46 vs 0.58 (MAA); market vol 0.24 vs 0.52 and 0.20 vs 0.43.
- Conjecture that the conditional-volatility component of dispersion explains the negative link: holds IS, **fails OOS**. The puzzle remains unexplained.

## Out-of-sample (Ch. 7)
- Momentum is much weaker after 1994/2002. Unweighted OOS SR: FF49 qxs 12m 0.32, 1m 0.17; sts 12m 0.31, 1m 0.52; MAA qxs 52w 0.26, sts 52w 0.50. EW market: 0.48 (FF49), 0.67 (MAA). Only FF49 1m sts beats the market. "Momentum beats the market" and "shorter formation is better" are both rejected.
- The market has shifted towards TS: TS now also beats XS in industries at short holding periods.
- Auto-covariance is no longer the main source. The mean terms become important, and for MAA 52w they are the *only* positive contributor (auto-cov turns negative).
- Confirmed OOS: no short-term reversal (except 1-week formation in MAA), scaling helps linear strategies, longs beat shorts, global TS does not beat local, the negative relation with vol, and dispersion weighting helps (now in all cases).
- Vol weighting still works. Own-vol SR: MAA sts 52w 0.50 → 0.89, FF49 qxs 12m 0.32 → 0.51. Normalised returns: MAA sts 4w 0.60 → 1.00, FF49 sts 1m 0.52 → 0.65. Normalisation is still better on average but not uniformly (MAA qxs 52w: 0.60 own-vol vs 0.55 normalised).

## Critical assessment
- **Convincing:** the decomposition framework and the XS/TS state analysis (they differ only when the market moves one way). Also the robust finding that per-asset vol normalisation beats strategy-level vol scaling, especially for XS, which otherwise loads on the most volatile assets.
- **Fragile:** small universes (49 / ≤17 assets), and dozens of specifications with no multiple-testing adjustment. The decompositions assume stationarity and are unconditional. Many p-values are marginal and robust vs OLS results sometimes disagree. Several IS "findings" reverse OOS: formation length, source of profits, the dispersion–vol story. No costs; MAA assumes synchronous closes.
- **Theory limits:** vol weighting results assume perfectly forecastable $\sigma_t$. Signed-strategy results assume sign independent of magnitude. The author calls the vol–momentum models "infantile".
- **Typos/inconsistencies:**
  - App. B says qxs ranks "in the holding period" (it means the formation period).
  - The slts formula keeps a $1/N_t$ factor, so gross exposure is $1/N_t$, not 1. Reported slts means and SDs (e.g. FF49 slts 12m: 0.09% mean) are on that tiny scale.
  - IS unweighted Sharpe ratios differ slightly between tables (e.g. FF49 qxs 12m 0.78 / 0.77 / 0.88) because vol-estimate seeding changes the sample start.

## Practical relevance for a quant PM
- For multi-asset trend, use **local** TS on **vol-normalised** returns; the global/market-trend variant loses most of the edge. For XS, rank *and* size on normalised returns, or at least use quantile or scaled weights. Never use raw linear weights.
- The TS-vs-XS choice depends on the covariance structure: XS needs negative lead–lag or loser reversal, TS needs own-autocorrelation or common drift. A cheap diagnostic is to run the auto/cross/mean decomposition on your universe, rolling.
- Overlay idea: filter XS shorts by a negative TS signal, since the short side is weak and costly.
- Dispersion scaling (divide by forecast cross-sectional SD) is a modest add-on for asset-class XS. It is dominated by per-asset vol normalisation.
- The OOS decay (post-2002 MAA, post-1994 industries) is a warning against relying on the in-sample Sharpe ratios above 1.
