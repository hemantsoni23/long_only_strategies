# The Non-Linear Market Impact of Large Trades: Evidence from Buy-Side Order Flow

**Authors:** Nataliya Bershova and Dmitry Rakhlin, AllianceBernstein. **Version:** July 2013 working-paper PDF, SSRN abstract 2197534. **Source:** `Finance/marketimpact_BershovaRkhlin_2013.pdf`, 49 pages. References below are to printed/PDF pages. **Research type:** empirical study of institutional equity execution, with an order-flow pricing model and post-trade relaxation estimates.

## Main contribution and interpretation

Bershova and Rakhlin use identifiable institutional parent orders to test a relationship between the distribution of order sizes, the shape of market impact, and the price remaining after execution. Their main evidence supports three linked observations over their filtered intraday sample: the central portion of the order-size distribution resembles a power law with cumulative tail exponent around $3/2$; impact grows approximately as the square root of execution duration; and the post-reversion price is close to the volume-weighted average execution price. That last result is a direct test of the fair-pricing condition, rather than an inference based solely on fitting an impact curve.

The paper also contributes a duration-dependent method of measuring post-trade impact and a description of relaxation with two regimes. A quick initial decline is approximately power law during the first ten minutes; larger orders subsequently show a slower exponential phase. A fixed post-completion observation time can therefore compare small orders whose temporary effect has already dissipated with larger orders whose effect is still relaxing. That measurement difference matters when estimating whether persistent impact is linear or concave in size.

The source calls the remaining intraday displacement “permanent impact.” This note preserves that terminology when reporting the paper but treats it as an operational endpoint, measured within roughly an hour after completion for most of the core analysis. It is not proof of a price effect that persists indefinitely. The study deliberately avoids overnight observations in its main sample. It also removes orders with unusually large adverse-selection or post-trade moves, which makes the resulting clean relaxation patterns conditional on substantial selection.

The authors present the findings as support for the Farmer–Gerig–Lillo–Waelbroeck theory, abbreviated FGLW. That interpretation is strongest for the joint empirical pattern in the bulk of the sample. It is weaker as a universal structural account: the largest orders have thinner tails than Pareto, logarithmic impact can fit them better, and the relaxation dynamics are not supplied by the original equilibrium model. The paper explicitly identifies those deviations and does not claim its dataset settles every no-manipulation question.

## The FGLW mechanism being tested

The theoretical review considers informed institutional investors, liquidity or day traders, and competitive market makers. Informed investors receive a common signal $\alpha$ about future value. Day traders contribute independent zero-mean noise signals. Metaorders combine the resulting demand and are executed in equal-sized slices of quantity $\kappa$. Market makers know the distribution of total metaorder sizes but do not know the realized size of the order currently being worked (pp. 5–8).

Write $\widetilde S_t$ for the transaction price after $t$ slices, $P_t$ for the conditional probability that the order continues, and $S_{t+1}$ for the price after reversion if it stops at that point. The martingale condition is

$$
P_t(\widetilde S_{t+1}-\widetilde S_t)+(1-P_t)(S_{t+1}-\widetilde S_t)=0.
$$

A positive expected price increment if the order continues must be balanced by a negative price adjustment if it stops. Equivalently, the ratio of the continuation increment to the completion reversal is $(1-P_t)/P_t$. For a sufficiently heavy-tailed size distribution, surviving orders become more likely to continue as their age rises. The incremental surprise of another slice falls, generating concave cumulative impact.

The second assumption is fair pricing: conditional on the completed order size, the average execution price equals the post-trade price. With equal-sized slices this is

$$
\frac1N\sum_{i=1}^{N}\widetilde S_i=S_{N+1}.
$$

The theory links this condition and the martingale restriction to the metaorder-size distribution. For a probability mass function behaving as $p_N\propto N^{-(\beta+1)}$, the cumulative tail exponent is $\beta$. At large execution age, peak impact scales as $t^{\beta-1}$ when $\beta\ne1$, with logarithmic growth at the boundary $\beta=1$. Persistent impact has the same exponent and a coefficient smaller by a factor $1/\beta$:

$$
I_{\mathrm{peak}}(t)\propto t^{\beta-1},\qquad
I_{\mathrm{perm}}(t)\sim\frac1\beta I_{\mathrm{peak}}(t).
$$

Thus $\beta=3/2$ yields square-root peak and persistent impact and a two-thirds persistent fraction. This is a joint prediction involving both order-size statistics and prices. Merely observing a square-root curve would not uniquely validate the mechanism, since other microstructure models also generate concavity.

The equal-slice framework relates execution count, total size, and duration. Real orders do not literally follow identical schedules, so the empirical sample imposes trading-rate restrictions designed to make average size approximately proportional to duration. Duration-based impact estimates should be read with that design in mind, not generalized to arbitrary participation-rate policies.

## Core sample construction and its consequences

The proprietary data are single-day market orders executed by AllianceBernstein's buy-side desk from January 2009 through June 2011 in U.S. equities, spanning approximately 50 institutional funds. Initial inclusion requires a fill rate above 80%, duration longer than ten minutes, participation rate between 5% and 50%, and order size between 0.1% and 30% of median daily volume, or MDV. Stocks with MDV below 300,000 shares are excluded. Orders must arrive after 10 a.m. and finish by 3 p.m., avoiding opening volatility and retaining at least an hour to study reversal (pp. 8–9).

The trade rate must be between 0.01% and 0.1% of MDV per minute. This eliminates extremely aggressive orders and very slow orders, including cases where abundant liquidity or binding price limits could make large orders appear unusually inexpensive. It produces a cone-shaped admissible region in size-duration space. Within this region, average order size is approximately linear in duration, and average participation remains roughly between 15% and 19% across the range covering 99% of trades.

The original selected sample contains 12,501 orders. The main post-trade sample falls to 10,166 after outlier and reversion filters. Appendix 1 trims the top and bottom 1% of impact and shortfall, leaving shortfall between approximately -88 and 187 basis points and total impact between -137 and 288 basis points. It then removes unusually adverse slippage relative to available VWAP and a 10% participation-weighted benchmark, plus extreme first-hour reversal observations (pp. 44–45).

Available VWAP runs from arrival to the close. Orders with slippage above 110 basis points, the top 5% of that distribution, are removed; many are sells with large subsequent rebounds. The 10% participation-weighted-price filter excludes slippage above 46 basis points, again approximately the top 5%. Finally, reversion outside a two-standard-deviation range removes roughly the top and bottom 5% of persistent-impact values. The total reduction is around 20%, not the sum of every listed percentage because filters can overlap.

These filters make the intended object clear: typical order-induced price trajectories with a discernible reversal pattern. They also limit causal and external interpretation. Removing event-driven trades and extreme subsequent moves conditions on outcomes related to information content. An unfiltered cost model for all institutional trading could therefore have different averages, tail risk, and measured persistent fractions. The source's strong language about fair pricing should be interpreted alongside this selection process.

Table 1 reports mean duration 42 minutes, median 27 minutes, mean size 1.4% MDV, median 0.8%, mean participation 16%, median 14%, and average spread 5.1 basis points. Mean MDV is six million shares and median MDV three million; the narrative's reference to three million reflects the typical median scale rather than the table's mean. Mean high-low daily volatility is 2.7%. These orders are much smaller than the multi-day institutional positions examined separately in Appendix 2.

## Size and duration distributions

The authors compare 60 candidate distributions using Kolmogorov–Smirnov goodness-of-fit rankings. Pareto ranks 18th for size and 14th for duration, with fitted cumulative exponents 1.56 and 1.64 respectively. Pareto is therefore a useful approximate description, not the best fitting family across the entire distribution. Lognormal and inverse-Gaussian distributions rank above it, largely because of differences in the tails (pp. 9–12).

A log-log density fit in the central size range of approximately 1% to 20% MDV has slope -2.4759, standard error 0.0511, and $R^2$ about 96%. The implied cumulative exponent is approximately 1.48. It is important to distinguish a density exponent around 2.5 from a survival-tail exponent around 1.5; subtracting one is what aligns the empirical estimate with the theoretical convention.

The upper 5% tail, around sizes above 7% MDV, does not support a Pareto extrapolation. The exponential-tail test does not reject a lognormal approximation at the 5% level, while the generalized-Pareto test rejects the tested Pareto form. Table 2 reports 220 excesses and 1,000 bootstrap samples. The paper notes that filtering and sample construction complicate precise tail inference; these tests should not be read as an unconditional law governing all institutional demand.

Several mechanisms can explain the thinner observed upper tail. Orders are restricted to complete within one day, so late arrivals cannot become arbitrarily long executions. Table 3 shows average duration declining from 58 minutes for 10 a.m. arrivals to 26 minutes for 2 p.m. arrivals. Portfolio managers may also cancel costly orders instead of continuing to trade through adverse prices. Finally, one manager's order-size distribution can differ from the aggregate across managers. These considerations motivate the second dataset rather than being dismissed as irrelevant noise.

## Impact estimators and fitted shapes

Let $S_0$ denote the arrival midpoint, $S_T$ the midpoint at the last fill, $\bar S$ the volume-weighted execution price, and $\epsilon$ the buy/sell sign. The paper defines peak impact and realized impact by

$$
I=\epsilon\frac{S_T-S_0}{S_0},\qquad
J=\epsilon\frac{\bar S-S_0}{S_0}.
$$

Persistent impact replaces $S_T$ with a post-reversion price whose measurement window depends on order duration. The definitions are signed arithmetic returns rather than a fitted spread-cost measure. Midpoints at arrival and completion reduce bid-ask-bounce contamination of the peak response, while the realized-price measure includes where the fills actually occurred (p. 13).

Three models relate impact to duration $T$, measured in minutes, and daily stock volatility $\sigma$, estimated from a 30-day trailing average of Parkinson volatility:

$$
I=b\sigma T+u,\qquad I=b\sigma T^\gamma+u,\qquad I=b\sigma\log T+u.
$$

The paper uses nonlinear least squares and Bayesian information criterion, termed Schwarz information criterion in the text. For peak impact, the power specification gives $b=0.0225$ with standard error 0.0018 and $\gamma=0.4713$ with standard error 0.0196. Its $R^2$ is 29%, compared with 24% for the linear model and 28% for the logarithmic model. BIC is 89,139.7 for power, 89,234.16 for log, and 89,741.92 for linear (Table 4, p. 33).

The power fit is best by those reported comparisons and is close to square root, although its exponent is not fixed at one-half. Individual impact remains highly noisy: explaining 29% of cross-order variation is useful but far from a deterministic law. The fitted coefficients also depend on the paper's volatility and time units, so they must not be transferred to a different annualization convention without conversion.

Ten approximately equal-count duration buckets reveal that a logarithmic curve fits the largest orders better than a pure square root. Each bucket receives equal weight in that graph rather than inverse-variance weighting. This emphasizes the shape across duration groups but assigns relatively noisy long-duration groups comparable graphical influence. The authors connect the flattening to increasing order-flow predictability and to portfolio managers' cancellation options (pp. 14–15).

For a power trajectory $I(t)=bt^\gamma$, uniform execution implies average impact

$$
J(T)=\frac1T\int_0^T bt^\gamma\,dt=\frac{I(T)}{1+\gamma}.
$$

At $\gamma=1/2$, this equals two-thirds of peak impact. For an idealized logarithmic trajectory, the average lies approximately a constant amount below the endpoint, so temporary reversal need not rise proportionally with size. The logarithmic calculation is an asymptotic intuition; its behavior at zero requires a regularized time origin in an implementation.

## Defining the post-reversion endpoint

The authors first compute five-minute VWAPs after the last fill. Reversion at elapsed time $X$ is the sign-adjusted difference between that interval's VWAP and the last-fill midpoint, divided by the arrival midpoint:

$$
R_X=\epsilon\frac{\operatorname{VWAP}_{T+X}-S_T}{S_0},\qquad R_0=0.
$$

Negative values denote reversal. For example, the ten-minute observation averages prices over minutes five through ten, rather than using a single quote exactly ten minutes after completion. This smooths microstructure noise while retaining a time profile (p. 16).

All 10,166 core orders have a one-hour profile; only 7,918, around 78%, remain available at two hours. Mean peak impact is 19.4718 basis points and realized impact is 13.9800. Mean reversal reaches -6.3581 basis points at 50 minutes and remains near -6.2 basis points at one hour. At 120 minutes it is -5.4236 basis points, but the sample has changed and standard errors have increased. A comparison of later averages therefore should not automatically be interpreted as renewed impact for a fixed set of orders (Table 5, p. 34).

For the principal persistent-price estimate, the orders are grouped into durations below 20 minutes, between 20 and 45 minutes, and above 45 minutes, with 3,585, 3,527, and 3,054 observations respectively. The authors use successive tests to find the first five-minute interval whose reversion is statistically indistinguishable from all subsequent intervals within the first hour. The resulting relaxation thresholds are 15, 30, and 40 minutes. Persistent price is then the VWAP from that threshold through minute 60 (p. 17).

This rule explicitly permits larger orders to require more relaxation time. It also uses the sample's observed trajectory to choose the endpoint and involves multiple comparisons. The source does not describe a separate validation sample or a multiplicity correction. A reproduction should replicate the rule before evaluating alternatives, and should not interpret failure to distinguish successive averages as proof that no slower decay remains.

## Fair pricing, persistent impact, and source inconsistencies

The persistent-impact power exponent is 0.4722, standard error 0.0351, again close to one-half. BIC favors power over log and linear, with values 101,806.5, 101,832.1, and 102,000.1 respectively. Explanatory power is only around 11%, lower than for peak impact because later prices contain more unrelated noise (Table 6, p. 38).

There is a material internal discrepancy in the source's scale coefficient. Table 6 prints the persistent-impact power coefficient as 0.0105, but Figure 9 on the same page labels the curve $0.0150\sigma T^{0.4722}$. The latter matches the narrative's persistent-to-peak ratio around $0.66\pm0.09$, while dividing 0.0105 by 0.0225 would not. Visual inspection confirms that this discrepancy is in the PDF, not merely text extraction. The exponent and model comparison are consistently reported; the scale coefficient should be verified against the authors' data before calibration.

There is also a notational reversal in the displayed ratio formula on page 19: the surrounding explanation and numerical results clearly concern persistent impact divided by peak impact, even though the displayed symbols are inconsistent. This note uses the economic direction of the ratio supported by the reported means and discussion.

The direct fair-pricing test is easier to interpret. Mean realized impact is 13.9800 basis points and mean persistent impact is 13.1677. Their difference is 0.8123 basis points, with standard error 0.4335 and a 95% interval from -0.0374 to 1.6621. Thus equality is not rejected at the stated confidence level, although the interval permits a small economically nonzero difference (Table 7). The ratio of the reported mean persistent impact to the mean peak impact is approximately 0.676.

The paper argues that concave peak impact plus fair pricing implies concave persistent impact. That is sound within the operational endpoint and execution assumptions. It does not directly contradict every theorem requiring linear permanent mechanical impact, because those results concern different assumptions about liquidity, admissible round trips, and genuinely lasting effects. The authors discuss those distinctions but do not supply a new general no-manipulation theorem.

## Two stages of relaxation and the O-U estimation

To study the trajectory more finely, minute-by-minute reversal is normalized by estimated peak impact, approximately $0.0225\sigma_i\sqrt{T_i}$. This uses an expected denominator rather than each order's noisy realized peak. All normalized trajectories therefore start at zero and are comparable in scale. The text initially constructs six log-spaced duration groups and merges statistically similar adjacent groups into four (pp. 21–24).

The final tabulated buckets are 11–13, 14–29, 30–78, and at least 79 minutes, with mean durations 12, 20, 47, and 126 minutes. Earlier narrative boundaries differ slightly from these final figure/table labels, so the published final bucket definitions should be treated as the reproducible target while documenting that discrepancy. Table 8 contains 1,178, 3,359, 2,841, and 1,099 observations, a smaller subset than the 10,166-order main sample; the PDF does not fully reconcile that further reduction.

The first ten minutes are described by relatively rapid power-law relaxation. For the four buckets, reported power-decay exponents are approximately 0.97, 0.87, 0.46, and 0.22. The corresponding power-phase shares of total relaxation are 100%, 72%, 55%, and 32%. The initial reversal magnitude is about three basis points for the smaller groups and four to five basis points for larger groups, compared with a spread around five basis points. For small orders, most or all measurable transient impact disappears in this first stage.

For the later stage, the authors fit normalized reversal $R_{i,n}$ using an Ornstein–Uhlenbeck process,

$$
dR_{i,n}=-\theta(R_{i,n}-\mu)\,dn+\widetilde\sigma_i\,dB_{i,n}.
$$

Here $\mu$ is the asymptotic normalized reversal level, which is negative, and $\theta>0$ is the speed of mean reversion. It is the reversal endpoint, not the remaining impact fraction. For a one-minute step, the conditional mean has the form $e^{-\theta}R_{i,n}+\mu(1-e^{-\theta})$, with Gaussian innovation variance determined by the O-U diffusion scale and $\theta$.

To choose the end of active relaxation, the authors fit five-minute sliding windows backward from the end of the available post-trade horizon. They inspect when the estimated $\mu$ first reaches a local minimum marking the end of monotone decay. The resulting thresholds are 12, 28, 41, and 62 minutes. The O-U model is then estimated over the post-ten-minute interval through the relevant threshold. Alternative stability criteria give shorter thresholds, showing that estimated completion time is method dependent.

Table 8 reports O-U speeds 0.21, 0.08, 0.06, and 0.04 per minute, with standard errors 0.008, 0.002, 0.001, and 0.001. Its O-U endpoint estimates are -0.27, -0.27, -0.34, and -0.25, with standard errors 0.046, 0.031, 0.024, and 0.033. These should be distinguished from the descriptive endpoint levels -0.30, -0.30, -0.38, and -0.35 also shown in the table and emphasized in the narrative. The largest group's numerical discrepancy is meaningful when calibrating a model.

The residual checks show approximately Gaussian standardized residuals except for fat tails; roughly 98% lie within -2 to 2. The largest residual first-order autocorrelation is about 0.1. These checks support the O-U model as a local approximation, not a globally exact stochastic process for stock prices. The regime boundary, permanent level, and diffusion normalization are estimated from the same finite windows and interact with each other.

## Aggregated multi-manager evidence

Appendix 2 uses separate TCA-vendor aggregates from 2010–2011. The vendor first aggregates client allocations by stock and day into signed imbalances. Stock-days with absolute imbalance above 5% MDV enter the initial set. Consecutive qualifying days are stitched into multi-day orders, with total size normalized by MDV on the first day. Both gross and net-of-contra-side sizes are reported (pp. 45–49).

After vendor-side tail filtering, there are 11,114 large-cap and 25,548 mid-cap observations. Small caps are excluded because the required cleaning could not be reliably performed without access to the underlying records. Large-cap orders average 57.2% MDV gross and 41.5% net, last 2.8 days, and have realized impact 74.8 basis points against peak impact 104.6. Mid-cap orders average 67.1% MDV gross and 51.6% net, last three days, and have realized impact 66.9 basis points against peak impact 92.2.

Full-sample impact exponents are approximately 0.5342 for large caps and 0.4337 for mid caps. Power specifications marginally outperform logarithmic alternatives in the full samples. For the largest 20%, logarithmic impact has a modest BIC advantage. Tail tests favor lognormal over Pareto in those upper quintiles, while the central portions remain approximately power law. The authors report that temporary reversal for these larger, multi-day trades completes by the close of the next day, and that realized and persistent impacts are not statistically distinguishable.

This exercise broadens the evidence beyond one manager, but its stitched objects are not independently identified parent orders. Thresholding daily imbalance and combining consecutive days changes the distribution being measured. The appendix is best viewed as a robustness comparison across aggregation schemes, not a completely independent replication of the proprietary intraday design.

## Implications and reproducibility limits

For transaction-cost modeling, the useful lesson is that impact shape, order-size distribution, and post-trade measurement horizon must be estimated together. A constant 30-minute endpoint can mix temporary and persistent effects differently across sizes. A square-root model works reasonably well for the central sample, while the largest orders and the decay phase require additional structure. The shortfall-to-peak relation is economically informative because it tests whether the average execution price matches the subsequent market level.

An exact reproduction would require parent-order and fill records, start and finish midquotes, minute-level or finer trades for interval VWAPs, MDV histories, Parkinson-volatility inputs, and all filter definitions. It should retain before-and-after sample counts at every stage, preserve side signs, and report both filtered and unfiltered results. It should also verify the table/figure coefficient inconsistencies and resolve the final relaxation-bucket sample before using the published numbers as production parameters.

The paper's strongest contribution is the direct connection between identifiable buy-side orders and the joint shape of execution and reversal. Its main limitation is that clean intraday fair pricing is measured in a selected sample at an endpoint chosen from observed reversion. A trading system can use the work to improve empirical measurement and identify multiple relaxation regimes, but it should not assume that two-thirds of every peak impact is mechanically permanent or that the source's fitted coefficients are universal constants.
