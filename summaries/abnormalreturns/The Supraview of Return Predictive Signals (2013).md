# The Supraview of Return Predictive Signals
**Authors:** Jeremiah Green, John R. M. Hand, X. Frank Zhang
**Year:** 2013
**Journal/Venue:** Review of Accounting Studies 18:692-730
**Source file:** Finance/AbnormalReturnsReview_GreenHandZhang_2013.pdf

## Question

Instead of proposing a new anomaly, the paper treats the *population* of published cross-sectional return predictive signals (RPS) as the object of study. It asks:
- How many signals are there, and what are their reported return properties?
- How correlated are they?
- What portfolio Sharpe ratio could combining them deliver?
- How much orthogonalization is needed before a "new" signal can be called new?

## Database

- 333 signals first reported between 1970 and 2010, drawn from top accounting, finance and practitioner journals plus SSRN working papers as of 31 Dec 2010. Only the first paper on each signal is coded.
  - Split: 147 accounting-based, 106 finance-based (price-dependent; B/M counts as finance), 78 other (e.g. labor mobility, repurchases, ticker symbol).
  - For scale: this is 4x the McLean-Pontiff (2012) set and 6x Subrahmanyam's (2010) list.
- Discovery grows roughly exponentially, with no sign of slowing by 2010.
- Publication and authorship: 47% of the papers were unpublished at the end of 2010. Accounting faculty write 56% of accounting-signal papers; finance faculty write 79% of finance-signal papers.
- Data: 99% use CRSP, 74% Compustat, 24% I/B/E/S, and 37% some non-traditional source. The average sample length is 305 months.
- Methods:
  - Portfolio construction: 38% of papers sort into deciles.
  - Rebalancing: 56% monthly, 26% annual.
  - Risk adjustment: 91% of papers adjust for risk, but only 12% of those use anything beyond beta, size, B/M and momentum.
- Standardization:
  - Mean returns are annualized without compounding (monthly x 12, daily x 250, and so on).
  - Sharpe ratios are rarely reported, so the authors back them out as $SR \approx t/\sqrt{\text{years}}$. This assumes serially uncorrelated period returns, and it is only done for time-series means.
  - Where a paper reports several robustness variants, the database records their average rather than the best one.

## Facts about published signals (Tables 4-5, Figs. 2-5)

| | Mean | SD | Sharpe | n |
|---|--:|--:|--:|--:|
| Equal-weighted RPS, all | 12.2% | 12.1% | 1.04 (median 0.87) | 237 / 208 |
| Value-weighted RPS, all | 8.1% | 12.2% | 0.70 (median 0.61) | 99 / 87 |
| EW excess market, same windows | 9.5% | 19.1% | 0.50 | |
| VW excess market, same windows | 6.6% | 15.3% | 0.44 | |

(The text rounds the EW mean to 12.1% with n = 239.)

- **EW vs VW:** VW means are about 4 points lower with the same volatility. The mean t-stat is 5.0 for EW vs 3.7 for VW. The authors suggest this is why papers default to EW, since 237 papers report EW returns against 99 VW.
- **Signal types:** Other-based signals are markedly weaker (EW Sharpe 0.81, VW 0.45). Accounting and finance signals look alike.
- **Signals vs the market:** 88% (63%) of signals have a higher Sharpe ratio than the EW (VW) market.
- **Famous signals are below median.** Momentum (Jegadeesh-Titman, 6/6) has EW 11.4% with Sharpe 0.61. Sloan accruals has 10.4% with Sharpe 0.81. The median signal has 10.8% with Sharpe 0.87. Size and PEAD are also below median.
- **No time trend** in the mean, SD or Sharpe of newly discovered signals across the 1970s-2000s; all slope t-stats are below 2. The authors read this as discovery being "academic" (independent of investment value), or as better data and tools offsetting a shrinking pool.
- **Higher-mean signals have higher Sharpe ratios.** Regressing mean on SR gives significantly positive slopes; for EW, $\mu = 2.0\% + 0.10\,SR$. If SD captured risk, Sharpe should be flat or falling in the mean. So either markets are inefficient or SD is an incomplete risk measure.
- **Practitioner truncation:** The factors in J.P. Morgan's US Factor Reference Book (Russell 3000, 1995-2010) top out at Sharpe of about 1.1. The best academic signal reaches 3.1, and 36% (EW) and 14% (VW) of academic signals exceed 1.1. The two sets are not directly comparable: JPM's figures cover a common recent window, while the academic numbers are each paper's in-sample figures.

## Combining signals

Bailey-Lopez de Prado equal-volatility weighting uses weights $x_s = 1/(S\sigma_s)$. With mean individual Sharpe $\overline{SR}$ and mean signed pairwise correlation $\bar\rho$:
$$SR_P = \overline{SR}\sqrt{\frac{S}{1+(S-1)\bar\rho}} \;\xrightarrow{S\to\infty}\; \overline{SR}/\sqrt{\bar\rho}.$$

$SR_P$ is linear in $\overline{SR}$, rises with $S$ at a decreasing rate, and rises with falling $\bar\rho$ at an increasing rate, so correlation matters more than breadth. Example with $\overline{SR}=1.04$: at $S=330$ the portfolio Sharpe is 1.89 when $\bar\rho=0.3$ but 4.52 when $\bar\rho=0.05$.

**Empirical sample.** The authors program 39 signals (26 accounting, 10 finance, 3 other) from CRSP, Compustat and I/B/E/S. Each is a monthly-rebalanced decile long/short, run over Jan 1985 – Dec 2011. The window deliberately mixes pre- and post-publication periods.

- Mean Sharpe is 0.75 (EW) and 0.37 (VW). Five EW and three VW signals have non-positive means.
- **Mean signed pairwise correlation is 0.05** (EW and VW). Mean absolute correlation is 0.29 (EW) and 0.22 (VW). About 47% of pairs are negative; negative pairs average -0.25 and positive pairs +0.33 (EW).
- Five-year rolling averages range 0.01-0.08 (signed) and 0.23-0.38 (absolute), with no trend.
- **Correlation with the market is negative:** mean -0.16 (EW) and -0.17 (VW); 67% (79%) of signals are negatively correlated. Adding a signal portfolio to the market should therefore help.
- **Portfolio Sharpe multipliers.** At $\bar\rho=0.05$, portfolios of 3, 30 and 300 signals should reach 1.65x, 3.50x and 4.33x the mean individual Sharpe.

| Portfolio size | EW best case (published $\overline{SR}$ 1.04) | EW worst case (39-sample $\overline{SR}$ 0.75) | VW best case (0.70) | VW worst case (0.37) |
|---|--:|--:|--:|--:|
| 3 signals | 1.72 | 1.24 | 1.16 | 0.61 |
| 30 signals | 3.64 | 2.46 | 2.45 | 1.29 |
| 300 signals | 4.51 | 3.25 | 3.04 | 1.60 |

- **Monte Carlo check.** Random equal-vol portfolios of the 39 signals (500 draws per size) match the formula. Measured Sharpe is 1.21 (EW) / 0.59 (VW) for 3 signals and 2.43 / 1.22 for 30, against 0.75 / 0.37 for one signal. These are about 30% below what the published Sharpe ratios imply, which the authors attribute to post-publication decay (cf. McLean-Pontiff's roughly 35%).

## Novelty test (Section 4.2, Fig. 9)

A signed correlation near zero can hide large offsetting correlations, so the relevant question is how often a signal keeps a positive alpha when regressed on others.

- Procedure: regress a randomly chosen signal's returns on $N$ other randomly chosen signals from the 39, repeated 500 times, and record the share of intercepts significant at 5%.
- Results: **74% (N=1), 62% (5), 50% (10), 40% (15), 32% (25).**
- Against the 10 best-fitting controls (by adjusted $R^2$), 46% (EW) and 69% (VW) still keep a reliably positive alpha. The text also reports "21 (12) reliably negative intercepts" in this step; the wording is garbled and the two figures are hard to reconcile.
- Authors' conclusion: a new signal should be orthogonalized against *some* but not all existing signals.

## Interpretation and assessment

**Authors' conclusion:** More than 330 signals with low mutual correlation imply either pervasive inefficiency or far more priced risk factors than theory allows. Identifying a small spanning subset is posed as the key open problem. The later factor-zoo and spanning literature (e.g. Harvey-Liu-Zhu; Green-Hand-Zhang 2017) takes this up.

**Robust contributions**
- The population census.
- The EW-vs-VW gap.
- The low average signed correlation (0.05) combined with non-trivial absolute correlation (about 0.25).
- The negative market correlation of long/short signals.
- The breadth-versus-correlation arithmetic, the most portable result. For a PM, $\bar\rho$ among sleeves matters more than adding signals, and diversification caps out at $\overline{SR}/\sqrt{\bar\rho}$.

**Weak points**
- **Published statistics are upward-biased.** The descriptive statistics carry publication selection and in-sample fitting. The "higher mean, higher Sharpe" and "no decay in discovery quality" facts may simply reflect a $t>2$ publication filter applied in every decade.
- **Sharpe ratios are inflated for overlapping returns.** $t/\sqrt{T}$ with non-compounded annualization overstates SR for strategies with overlapping or long holding periods, such as annual rebalancing (26% of papers).
- **The large portfolio Sharpe ratios are gross, equal-vol-weighted figures.** EW decile portfolios are microcap-heavy. There are no transaction or borrow costs, no capacity limit, and no turnover netting. The 0.05 correlation is estimated in the same 1985-2011 sample, and the 39 signals are 2/3 accounting-based.
- **The novelty test is permissive.** A 5% significance threshold for one intercept is not a multiple-testing standard. Random controls from 39 signals do not reflect the most relevant competitors of a new signal, and "46% survive the best 10" uses controls drawn from the same small set.
- **The JPM comparison** is between different samples and periods, and the direction of any bias is unclear.

**Practical use**
- Use the paper as a base-rate reference: published EW Sharpe of about 1.0, decaying about 30-35% after publication, and VW about 0.4-0.7.
- Always report VW and cost-adjusted results.
- Test new signals against the most correlated existing signals (best-subset orthogonalization), not only against FF factors.
- Budget risk across signal sleeves using the $\bar\rho$ arithmetic.
