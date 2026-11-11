# Great Investors: Their Methods, Results, and Evaluation

Olivier Gergaud and William T. Ziemba. *The Journal of Portfolio Management* 38(4), Summer 2012, pp. 128–147. [Source PDF](../../Finance/UniversalPortfolios_GergaudZiemba_.pdf). The supplied file contains the twenty-page article and a one-page issue abstract. All 21 pages, including the landscape tables and references, were read. Page references below use the printed article pagination.

## Why this matters

The paper examines a specific measurement problem: how to evaluate a manager whose exceptional gains also create high return volatility. A conventional Sharpe ratio puts upside and downside fluctuations into the same denominator. An investor who particularly values infrequent, small losses may prefer a statistic that penalizes only shortfalls. The authors apply the downside symmetric Sharpe ratio, or DSSR, to selected famous investors, Renaissance Medallion, and a screened University of Massachusetts hedge-fund database.

Its contribution is an extension and empirical illustration of an existing measure, previously discussed by Ziemba in 2005, rather than a new trading strategy or a causal explanation of manager skill. The 2012 study supplies additional fund records, comparisons across sampling frequencies, and database rankings. It also includes a fund whose apparently exceptional record was fabricated, making the distinction between a performance statistic and independently verified performance central to interpreting the evidence.

An educated reader can reconstruct the metrics and much of the Medallion example from the printed tables. Reproducing the complete rankings requires the historical fund-level database and several undocumented preprocessing choices. Reimplementing the managers' investment methods is beyond the source: descriptions of Kelly investing, value investing, and short-term trading do not disclose their signals, probability forecasts, position constraints, or execution algorithms. The reproducible object here is an evaluation procedure, with its sensitivity to loss definitions and data quality.

## Evidence structure and what is new

The opening case studies contrast two kinds of wealth paths. Keynes, Berkshire Hathaway, and Quantum exhibit strong long-run growth with substantial interim losses. Princeton Newport and Medallion illustrate much smoother reported paths. The authors interpret the first group as comparatively aggressive growth investors and argue that the second group's performance is inadequately distinguished by a total-volatility denominator.

These cases are selected retrospectively. They do not constitute a random sample of managers, a preregistered comparison, or an out-of-sample investment exercise. Different funds are observed over different historical windows, and some comparisons reuse data and arguments from earlier publications. There is no factor-adjusted alpha regression, benchmark-matched portfolio experiment, transaction-cost simulation, or test that purchasing the highest-DSSR fund predicts subsequent performance.

The broader database contribution uses the University of Massachusetts Center for International Securities and Derivative Markets hedge-fund records. The final tables divide observations into commodity pool operators, commodity trading advisors, funds of funds, and hedge funds. Within categories, the paper ranks selected records by DSSR and compares those rankings and levels with ordinary Sharpe ratios. The main claim is descriptive: at the high-performing end of the selected sample, replacing total volatility with downside risk often produces much larger ratios, especially when there are few negative months.

## A self-contained reconstruction of the performance measures

Let $r_t$ denote a fund's simple net return during observation period $t$, $f_t$ the risk-free return over that same period, and $e_t=r_t-f_t$ the excess return. Let $n$ be the number of valid matched observations. The paper's conventional Sharpe expression is mean return minus a risk-free rate divided by return standard deviation. With a time-varying risk-free series, a consistent implementation is

$$
\bar e=\frac1n\sum_{t=1}^ne_t,\qquad
s_e^2=\frac1{n-1}\sum_{t=1}^n(e_t-\bar e)^2,\qquad
S=\frac{\bar e}{s_e}.
$$

This matches the paper's explicit statement that the Medallion standard-deviation calculations use net returns minus risk-free rates. Using the standard deviation of raw returns instead would be a different convention when $f_t$ varies. All inputs must use the same units; percentage-point returns can be used consistently because numerator and denominator scale together.

For a chosen return series $x_t$ and target zero, define the negative part $x_t^-=\min(x_t,0)$ and downside second moment

$$
d_-^2=\frac1{n-1}\sum_{t=1}^n(x_t^-)^2.
$$

The denominator uses the total number of observations, not merely the number of losses. Positive observations contribute zeros, so both loss frequency and loss severity matter. This is not the variance of losses around their own conditional mean. The paper fixes the downside reference at zero even though its notation uses a symbol resembling a sample mean; centering the shortfalls on the observed positive mean would change the measure.

The symmetry construction reflects the negative tail to create a hypothetical positive tail. Under the verbal convention that total symmetric risk is twice downside variance, the reconstructed risk denominator is

$$
s_{\mathrm{sym}}=\sqrt{2d_-^2},\qquad
DSSR=\frac{\bar r-\bar f}{s_{\mathrm{sym}}},\qquad
DISR=\frac{\bar r}{s_{\mathrm{sym}}}.
$$

The article alternates the abbreviations DISR and DSIR. Its information-ratio variant uses raw mean return in the numerator; it is not the usual active return divided by tracking error relative to a risky benchmark. That distinction must be preserved when comparing it with another system's information ratio.

There is a consequential notation ambiguity on p. 132: the displayed downside expression omits the factor two, while the prose says the total variance is twice downside variance and describes mirroring losses. A replication should explicitly record whether it uses $d_-$ or $\sqrt2d_-$; the former increases every otherwise identical ratio by $\sqrt2$. The formulas above implement the stated mirroring convention. They should not be represented as an unambiguous transcription of every displayed symbol in the paper.

A second choice concerns the series used to identify losses. The general discussion refers to zero net-return losses, whereas the Medallion calculation explicitly uses excess returns in the standard deviations. A positive raw return below the risk-free return is a loss under the latter convention. Therefore record both counts, $\sum_t\mathbf1\{r_t<0\}$ and $\sum_t\mathbf1\{e_t<0\}$, and state which series enters $d_-$. The published monthly loss counts describe the raw-return observations; they should not automatically be used as the excess-shortfall count.

## Properties, edge cases, and interpretation

The authors' intended effect follows directly from the denominator. Hold all negative observations and the number of periods fixed, then increase a positive observation: downside risk remains unchanged while the mean rises. An ordinary standard deviation generally changes as well. This is why a few very large gains can improve the DSSR more dramatically than the conventional Sharpe ratio.

It does not follow that the DSSR must always exceed the Sharpe ratio. It compares a second moment around a target with a variance around a sample mean, and the results depend on the return distribution and normalization. Exhibit 8 supplies a practical counterexample: five of the six displayed funds have smaller downside ratios than ordinary ratios. Symmetry about the zero target would equate the corresponding population second moments only under the appropriate centering; a positively shifted distribution is not symmetric about that target merely because its fluctuations are symmetric around its mean.

If there are no observed shortfalls, $s_{\mathrm{sym}}=0$. A positive numerator then gives an infinite ratio in the extended-real sense. Zero numerator gives an undefined zero-over-zero expression, and a negative numerator with a positive denominator gives a negative ratio. The source's statement that the range begins at zero whenever mean return is no greater than the risk-free return is not the algebraic range of the untruncated ratio. A zero floor would require a separately declared reporting rule.

With only one small loss, the denominator can be extremely small and imprecisely estimated. An enormous ratio does not establish that the unknown loss distribution has a negligible tail. No confidence interval, finite-sample bias correction, or sampling distribution for the DSSR is derived in this article. A ratio also loses information about the ordering of returns: rearranging a series leaves its sample moments and downside count unchanged but can change drawdowns, recovery time, and liquidity pressure substantially.

The article describes the conventional Sharpe ratio as assuming normal returns. More precisely, the ratio can be computed for any distribution with appropriate finite moments. Normality can justify particular distributional interpretations or tests; it is not needed for the arithmetic definition. Choosing downside risk instead expresses a different evaluation preference. The empirical comparisons do not prove that one scalar ranks every investor's utility correctly.

## Sampling frequency and annualization

Compute each frequency's returns from wealth-relative products:

$$
r_{[a,b]}=\prod_{t=a}^b(1+r_t)-1.
$$

A monthly loss may disappear within a profitable quarter. Consequently, the downside second moment of quarterly compounded returns cannot generally be obtained by multiplying a monthly downside second moment by three. This differs from a conventional square-root-of-time approximation for the variance of independent additive returns.

Exhibit 13 labels its T-bill observations as annualized rates even in the monthly and quarterly rows. They must be converted to the fund-return interval before subtraction. Simple prorating, $f_{\mathrm{month}}\approx y/12$ or $f_{\mathrm{quarter}}\approx y/4$, is an approximation; an effective-yield conversion or a bill-price/day-count calculation is another possible convention. The article does not document enough details to determine the exact conversion throughout. Treating an annualized 5% quote as a 5% monthly return would materially distort the comparison.

If one reports an annualized monthly conventional ratio using $\sqrt{12}S_{\mathrm{month}}$, that is a stated scaling convention, with serial dependence and compounding qualifications. An annual DSSR computed from annual observations, a scaled monthly DSSR, and the hybrid quarterly-denominator calculation used below are three different objects. The source's ratios at different frequencies should be reported as such rather than merged into a supposedly frequency-invariant ranking.

## Medallion: the most reconstructible empirical example

Exhibits 11–14, pp. 134–135, report monthly net returns from January 1993 through April 2005, quarterly aggregates, twelve complete calendar-year returns, annualized T-bill observations, a histogram, sorted monthly returns, and a compounded wealth path. There are 148 monthly observations, 49 complete quarters through March 2005, and twelve complete years through 2004. The paper reports 17 negative months, three negative quarters, and no negative complete calendar years. The extra April 2005 observation should enter a monthly calculation but not an unfinished second-quarter or full-year calculation.

The published annual returns are 39.06%, 70.69%, 38.33%, 31.49%, 21.21%, 41.50%, 24.54%, 98.53%, 31.12%, 29.14%, 25.28%, and 27.77% for 1993–2004. These are reported net returns, not gross returns from which another assumed fee schedule should be deducted. The text describes a 5% management fee and 44% incentive fee, but gives no complete historical fee-timing rule suitable for reconstructing gross trading profits. The source's estimate of fund size and later annual returns are historical statements, not current facts.

| Frequency | Ordinary Sharpe reported | DSSR reported | Important convention |
|---|---:|---:|---|
| Monthly | 0.76 | 2.20 | 148 monthly observations |
| Quarterly | 1.09 | 11.6 | 49 complete quarters |
| Yearly | 1.68 | 26.4 | DSSR uses a quarterly risk estimate scaled to a year |

The annual denominator is not calculated directly from annual shortfalls, because no annual net loss is observed. The authors instead multiply the quarterly downside standard deviation by two. This prevents a zero denominator, but the resulting 26.4 is a hybrid estimate combining an annual numerator with a risk estimate from a different sampling frequency. It is not evidence that the observed annual distribution contains enough losses to estimate annual downside risk.

A transparent numerical reconstruction from the rounded printed annual returns and annual T-bill row gives mean excess return 35.9125 percentage points, sample excess-return standard deviation about 21.8363 percentage points, and Sharpe approximately 1.645. Using all 49 printed quarterly returns, the quarterly T-bill row divided by four, and the mirrored downside denominator gives a quarterly Sharpe about 1.093 and DSSR about 11.52; the quarterly downside deviation is approximately 0.6731 percentage points. Combining that risk estimate with the printed annual excess mean gives a hybrid annual DSSR about 26.68. These are this note's calculations under explicit conventions, not new estimates attributed to the authors. They are close to some reported values but do not exactly reproduce all of them, so underlying precision or an undocumented convention remains relevant.

For orientation, compounding the twelve printed complete-year returns produces a wealth multiple of approximately 49.62 before the four additional 2005 months. This agrees with the order of magnitude of the wealth graph that starts at 100, while avoiding confusion between terminal wealth, a cumulative percentage return, and a per-period mean. The paper supplies no inference showing that the difference between ratios is statistically significant or stable in later periods.

## Selected investors and the limits of the Kelly interpretation

The Yale discussion reports a 21.9% return for fiscal 2011 and an endowment value of approximately \$19.4 billion, following a −24.6% fiscal-2009 loss. Over the ten years ending June 2011, the source reports 10.1% annually versus 3.9% for U.S. stocks and 5.1% for bonds. These examples motivate long-horizon evaluation and the importance of endowment spending, illiquidity, and diversified manager selection. They do not supply monthly data, and the authors explicitly decline to compute Yale's DSSR. Exhibit 2 mixes billions-sized 2010–2011 market-value entries with earlier entries under a millions heading, so its units require care.

The Keynes example reports a 9.12% geometric annual return for 1927–1945 versus −0.89% for the U.K. market, with more than half the portfolio lost early in the period. The approximately 80%-Kelly interpretation is inherited from an earlier analysis. Likewise, the inference that Buffett and Soros were full-Kelly investors rests on concentrated holdings and their willingness to tolerate losses. The article does not estimate their subjective return distributions or demonstrate that their observed holdings solve an expected-log optimization. Concentration and volatile wealth paths alone do not identify an optimal Kelly fraction.

Exhibit 8 reports annual performance measures computed from monthly data and arithmetic means:

| Fund or benchmark | Ordinary ratio | Downside ratio |
|---|---:|---:|
| Ford Foundation | 0.970 | 0.920 |
| Tiger Fund | 0.879 | 0.865 |
| S&P 500 | 0.797 | 0.696 |
| Berkshire Hathaway | 0.773 | 0.917 |
| Quantum | 0.622 | 0.458 |
| Windsor | 0.543 | 0.495 |

Berkshire is the sole row whose ratio increases; its downside ratio nearly reaches Ford's. The text reports 58 losing months for Berkshire and 53 for Quantum among 172 observations. Exhibit 9 is explicitly a quarterly-return plot, despite nearby prose discussing monthly observations. These frequencies should not be silently equated. Princeton Newport is reported to have only three monthly losses over approximately twenty years and DSSR 13.8, but the underlying return vector needed to reproduce that result is not printed here.

## Database selection and ranking procedure

The declared screen for Exhibits 21–24 is mean return of at least 1.5% per month and at least 100 months of reported trading. The tables include both funds whose last reports are near February 2010 and funds whose records ended much earlier. They are not estimates over one synchronized common window. Their average-return columns are expressed as gross factors such as 1.018, corresponding to roughly 1.8% per month, not 101.8% net. Exhibit 20 identifies its mean-return statistic as geometric, while the screening prose simply says mean; a faithful rerun should preserve this unresolved arithmetic-versus-geometric distinction.

A reconstruction should retain fund ID, category, share class, inception, last report, observation count, negative count, return series, benchmark rates, and the relevant fee and currency metadata. Calculate the chosen metrics over each declared sample, apply the screen, rank within category, and reproduce the selected table rows. Multiple share classes are separate records in the printed tables: for example, the first three fund-of-funds rows represent closely related TS Multi-Strategy vehicles. They should not be treated as independent manager discoveries without an explicit aggregation rule.

Exhibit 20's reported category means are:

| Category | Months observed | Negative months | Geometric monthly gross factor | Sharpe | DSSR | DISR |
|---|---:|---:|---:|---:|---:|---:|
| Commodity pool operators | 155 | 53 | 1.019 | 1.463 | 4.903 | 5.949 |
| Commodity trading advisors | 179 | 75 | 1.022 | 0.724 | 5.436 | 6.270 |
| Funds of funds | 128 | 26 | 1.016 | 2.328 | 14.542 | 17.222 |
| Hedge funds | 135 | 43 | 1.019 | 1.082 | 6.772 | 7.905 |

These summarize selected fund records, not the performance of investable category portfolios. The source does not document a weighting scheme that would justify interpreting them as returns on aggregate invested capital. A mean of individual loss proportions also need not equal the ratio of mean negative counts to mean history length. Reported dispersion is large: CTA DSSR standard deviation is 8.317 against a mean of 5.436; hedge-fund DSSR standard deviation is 8.682 against a mean of 6.772.

Exhibits 18–19 order funds by ordinary Sharpe and plot either DSSR minus Sharpe or the two levels, together with the proportion of negative months. Local polynomial smoothing illustrates the sharp increase in downside ratios and fall in loss frequency near the high-Sharpe end. Polynomial degree, bandwidth, kernel, boundary treatment, and treatment of infinite ratios are not stated. These plots reveal metric behavior within a selected sample; they are not a formal test that the measure identifies latent ability.

## Exceptional records, internal inconsistencies, and data validation

Logos Trading's reported 157-month record contains 29 losing months, a monthly gross geometric mean rounded to 1.085, ordinary Sharpe 2.773, DSSR 64.40, and DISR 66.72. Its very high downside ratio arises from large gains relative to the observed squared losses; it does not mean losses were absent. The reported dates, total wealth scale, and rounded mean need reconciliation before exact replication. The case-study AUM and the final CTA table also use different values without documenting their valuation dates.

GJ Investment Fund provides an especially short-sample illustration: Exhibit 16 gives ordinary Sharpe 3.217 and DSSR 491.83, with one negative observation and a reported monthly gross geometric mean of 1.155. Its stated interval, November 2008–January 2010, spans fifteen calendar months inclusive, while its observation-count field says thirteen. The displayed wealth multiple 8.708 implies approximately 15.52% per month over fifteen periods but 18.11% over thirteen. This supports a count inconsistency, not a license to silently invent two missing observations. The case study also falls below the 100-month screen for the final rankings.

The FMG example is explicitly presented by the authors as fabricated performance associated with a Ponzi scheme. The reported series has 199 months, no negative returns, Sharpe 12.35, and infinite downside ratios. Its prose gives a geometric mean near 2.3% per month, while Exhibit 17 prints 4.839%. A wealth multiple of 83.91 over 199 periods implies approximately 2.251%, agreeing with the prose's magnitude rather than the table entry. The article's account of enforcement is historical source material; it is not an independently refreshed investigation in this note.

There is another display inconsistency: the final CPO table prints zero DSSR and DISR for FMG despite the explicit infinity in its case study. Zero-loss money-market rows in the hedge-fund table also show zeros. The paper does not explain whether these are placeholder values, a software convention, or transcription errors. A reproduction should encode the mathematical zero-denominator case separately from an ordinary numeric zero and disclose how it is ranked or excluded.

## Replication boundaries and practical takeaways

The minimum executable core is straightforward: align period returns and risk-free inputs, define the loss target, compute means, ordinary volatility and downside second moments, preserve zero-denominator cases, and form ratios with explicit frequency labels. The empirical database exercise additionally requires the original sample vintage, inclusion rules, share-class handling, missing-return policy, return-unit conventions, and historical reporting status. Those are not fully recoverable from the published tables. The article provides neither code nor a complete raw database extract.

The study does not report correction for backfilled histories, survivorship, selective reporting, serial correlation, stale valuations, or multiple comparisons across funds. These are limitations of the evidence supplied, not proof that every record suffers every defect. The authors themselves note that closed outstanding funds and secretive poor funds may be missing. Selecting long histories with high realized means makes the observed tail of performance especially unsuitable for an unconditional statement about manager skill.

For replication beyond the original descriptive exercise, sensitivity to zero raw returns versus zero excess returns, the factor-two convention, common sample windows, and alternative observation frequencies would be useful. Block resampling or an explicit time-series model could quantify ratio uncertainty, but neither is implemented in this paper. Any such extension should be labeled new analysis. Similarly, independent verification of prices, cash flows, valuation procedures, and fund records addresses a different question from the formula's arithmetic and cannot be replaced by a favorable ratio.

The useful conclusion is specific: downside-focused evaluation can expose differences between large positive jumps, frequent ordinary volatility, and realized loss experience that a single conventional Sharpe ratio obscures. It can also become unstable or infinite when the observed loss sample is sparse. The paper's strongest reproducible evidence concerns that measurement behavior. Its rankings and selected wealth paths do not establish a tradable manager-selection rule or disclose the strategies that generated the returns.
