# The CDS-Bond Basis

Jennie Bai and Pierre Collin-Dufresne. September 2018 accepted manuscript, DOI: 10.1111/fima.12252. The supplied file explicitly precedes copyediting and final pagination. [Source PDF](../../Finance/bondCDSbasis_Bai_2018.pdf). All 43 pages were read, including both appendices, four tables, two figures, and references. Page numbers below refer to the PDF. Several equations and table cells in this version require qualifications; these are identified rather than silently replaced with presumed final-version values.

## Why this matters

A negative CDS–bond basis appears to offer a simple trade: buy a bond, buy default protection, and collect the difference between its credit spread and the CDS premium. During the financial crisis, those differences became large and persisted. Bai and Collin-Dufresne ask why arbitrage capital did not eliminate them, focusing on differences across bonds rather than the aggregate level of the basis.

Their contribution is to connect a trade’s funding and liquidation mechanics to bond-level proxies for collateral quality, trading liquidity, counterparty exposure, and funding sensitivity. The results support the view that a larger apparent spread opportunity can compensate for greater difficulty maintaining the position through adverse conditions. The striking exception is the bond-lending fee: a high fee could improve the value of owning a scarce bond, yet it is associated with a more negative basis during and after the crisis. The authors interpret it as a signal of shorting pressure that deters arbitrageurs from buying into continuing price declines.

The evidence is a set of contemporaneous cross-sectional regressions and sorted-bond portfolios. It does not measure realized profits from a financed strategy or establish that the regression residual is an exploitable opportunity. An apparent 243-basis-point or 560-basis-point spread gap is not a net return on invested capital. Haircuts, refinancing, protection sizing, execution, and mark-to-market losses determine whether the trade survives long enough to capture convergence.

## Basis definition and economically distinct trades

For reference entity $i$ and maturity $T$, the basis is

$$
b_i(T)=s_i^{CDS}(T)-s_i^{PECDS}(T),
$$

where PECDS is the par-equivalent CDS premium implied by a cash bond’s price. This is not simply the bond’s yield minus a Treasury yield. PECDS uses a survival-based valuation model and the dollar Libor swap curve to make the bond and CDS credit components more comparable.

With a positive basis, the stylized convergence trade shorts the bond and sells protection; costly or unavailable bond borrowing can prevent implementation. With a negative basis, it buys the bond and buys protection, requiring funding for the cash security and margin for the derivative. Deliverability, recovery terms, maturity, and coupon structure must match sufficiently closely for the package to hedge default. A fixed-rate bond and a CDS do not automatically constitute a perfect arbitrage, even before funding frictions.

The reference curve matters for the overall level. Swaps approximate funding conditions for intermediaries more closely than Treasury yields, which can contain liquidity, specialness, and tax effects. The authors therefore emphasize cross-sectional variation: one common curve error cannot straightforwardly explain enormous differences across issuers. This argument does not eliminate all measurement error. Bonds have different maturities and cash flows, so nonparallel curve errors, optionality, or valuation assumptions can still generate heterogeneous basis errors.

## Financing, hedge sizing, and a usable P&L interpretation

Let $B$ be the purchase price, $N$ bond face value, $h$ the repo haircut, $r$ Libor, $f$ the arbitrageur’s unsecured funding spread, and $r_{repo}$ the repo rate. The bond requires $hB$ of risk capital financed at $r+f$ and $(1-h)B$ financed in repo. CDS margin $M$ is also funded at $r+f$, assuming it earns no offsetting interest. Repo is short term and must repeatedly roll even when the intended trade lasts five years.

A full-face hedge buys CDS notional $N$. An alternative attempts to protect only the purchase price, using assumed recovery $R_0$:

$$
N_{CDS}=\frac{B-NR_0}{1-R_0}.
$$

For a discount bond this reduces the premium, but it leaves recovery risk. As an illustrative calculation independent of the paper’s empirical sample, $B=80$, $N=100$, and $R_0=0.40$ imply CDS notional 66.6667. If actual recovery is 0.20, bond recovery plus protection pays only $20+66.6667(0.8)=73.3333$, below the 80 purchase price. A hedge calibrated to expected recovery is not a guaranteed capital floor.

A spread-duration hedge instead selects $N_{CDS}D_{CDS}=D_B$, with $D_B$ the bond’s dollar spread sensitivity and $D_{CDS}$ CDS sensitivity per unit notional. This reduces small spread-move exposure but differs from a jump-to-default hedge. Recovery matching and duration matching cannot generally be imposed simultaneously with one CDS notional.

Equations (2)–(3), pages 9–10, illustrate bond and CDS mark changes, financing costs, and bid–ask effects. They should not be used as a complete backtest accounting equation without repair. They describe one day but omit an explicit year fraction on annual funding rates, do not explicitly add bond coupon carry or deduct running CDS premium, and equation (3) drops the benchmark-rate change appearing in the footnote’s bond-duration approximation. The footnote also expresses an ask-to-bid round trip using a change in spread width, although entry and exit half-spreads normally add.

A consistent first-order reconstruction, under matched spread sensitivities and a parallel benchmark-rate approximation, is

$$
\Delta\Pi\approx D_B(\Delta s_{CDS}-\Delta s_B)-D_B\Delta r+[C_B-s_{CDS}N_{CDS}-F]\Delta t-TC,
$$

where $C_B$ is the annual coupon/accrual contribution under the chosen accounting convention and

$$
F=B[h(r+f)+(1-h)r_{repo}]+M(r+f).
$$

This is an explicit reconstruction, not the paper’s reported equation or a claim to reproduce its data. A production implementation should use exact dirty-price cash flows, the actual CDS contract, and separate rate and spread sensitivities. For a literal entry-at-ask and exit-at-bid round trip, matched-dollar-duration execution cost is approximately half the sum of the bond and CDS full spread widths at entry and exit, multiplied by $D_B$. For an existing position marked consistently on one side, changes in width have a different role.

If the bond defaults at $\tau_B$, the stylized terminal receipt in equation (4) is

$$
RN+N_{CDS}(1-R)\mathbf1_{\{\tau_C>\tau_B\}},
$$

where $\tau_C$ is the protection seller’s default time. Despite the source’s P&L label, this is a receipt before subtracting purchase cost, financing, premiums, and other cash flows. The zero recovery on failed protection is a stylized exposure illustration. Actual collateral, netting, replacement, and bankruptcy recoveries complicate it. Counterparty risk depends on joint distress and closeout conditions, not solely on the protection seller’s standalone CDS spread.

These mechanics motivate the empirical signs. Bonds that become expensive to fund or costly to liquidate precisely when the basis diverges require more compensation from limited arbitrage capital. A basis that converges when funding costs rise is comparatively desirable. The paper does not solve an arbitrageur’s full dynamic capital-allocation problem or estimate its first-order conditions; its tests use these directional implications.

## Reconstructing PECDS and the appendix’s missing choices

Appendix A uses discount factors $Z(t)$ from swaps, survival probabilities $S(t)$, premium dates $t_j$, accrual fractions $\Delta_j$, and midpoint dates $\bar t_j=(t_{j-1}+t_j)/2$. Define the risky premium annuity and default leg per unit notional by

$$
A(S)=\sum_j Z(t_j)S(t_j)\Delta_j+\frac12\sum_j Z(\bar t_j)[S(t_{j-1})-S(t_j)]\Delta_j,
$$

$$
D(S)=(1-R)\sum_j Z(\bar t_j)[S(t_{j-1})-S(t_j)].
$$

Then the par CDS spread is $D(S)/A(S)$. The second annuity term accounts approximately for accrued premium at default, assumed halfway through each interval. Use actual contract day counts for a precise implementation; the source writes a common $dt$.

The authors first bootstrap $S_{CDS}$ using CDS maturities 1, 2, 3, 4, 5, 7, and 10 years and the corresponding swap curve. They then fit a bond-implied survival curve and reprice a five-year CDS on it. Equations (12)–(13) literally specify

$$
S_{bond}(t_j)=S_{CDS}(t_j)+\varepsilon,\qquad \widehat\varepsilon=\arg\min_\varepsilon[PV(S_{bond})-B_{market}]^2.
$$

This is a parallel additive shift of survival probabilities as printed, not a parallel hazard-rate shift. The PDF does not supply the bond PV formula, constraints on $\varepsilon$, how $S(0)=1$ is anchored, the recovery value, curve interpolation, coupon schedules, or callable-bond valuation details. Those are material missing inputs.

For example, a conventional recovery-of-face reconstruction for an option-free bond would use surviving coupons plus surviving principal and expected recovery payments. That supplies a possible $PV(S)$, but it is an additional convention. A literal unrestricted additive shift can make probabilities exceed one or fall below zero. Shifting time zero as well would violate $S(0)=1$; leaving it fixed changes the first default increment. A practitioner must impose valid decreasing survival probabilities and an initial anchor, or explicitly choose a different hazard-shift parameterization and label it a deviation. The source does not establish which was coded.

A useful independent numerical check of the CDS leg formulas is to use $Z(t)=e^{-0.03t}$, $S(t)=e^{-0.02t}$, quarterly payments over five years, and $R=0.40$. Both legs must match when the coupon is set to their ratio, which is near the continuous-premium benchmark $(1-R)\lambda=0.012$. A bond price generated under the same survival model and refitted consistently should produce zero basis. This tests units and mechanics; it cannot validate the empirical PECDS series without the omitted conventions and proprietary data.

## Data, filtering, and timing

The analysis joins Markit single-name CDS, Mergent bond characteristics, Enhanced TRACE transactions, CRSP equity returns, and a proprietary Markit corporate-bond lending dataset. The reported main period runs from July 2006 through December 2014. There are about 1.1 million daily observations, 4,415 CDS–bond pairs, and 679 CDS reference entities after matching and filtering, from an initial 1,842 CDS entities. Entity names are matched manually. The source alternates December 30 and December 31 as its endpoint, which must be resolved against the actual calendar in a replication.

The bond screen retains publicly traded U.S.-dollar corporate bonds of U.S. issuers, excluding private placements and Rule 144A securities, structured notes, mortgage- and asset-backed bonds, agency-backed and equity-linked issues, convertibles, and floating-rate coupons. Fixed and zero-coupon bonds remain. TRACE cleaning removes when-issued and locked-in trades, commission transactions, special-price or special-sale conditions, cancelled trades, and settlement exceeding two days; corrected and reversed records are adjusted. Exact transaction-to-daily-price aggregation is not fully specified.

Remaining maturity is recomputed each day and restricted to 3–7.5 years to align with liquid five-year CDS and the stated modified-restructuring deliverability window. About 67% of the sample is callable, so callables remain in the main analysis; a smaller sample without option features is described as a robustness exercise. The appendix’s simple survival-pricing description does not establish an option-adjusted procedure for those bonds. For ratings, use the available Moody’s or S&P rating, or their average when both exist.

CDS are dollar contracts with physical settlement and modified restructuring, MR. The manuscript acknowledges that the U.S. convention switched to no restructuring in April 2009 but retains MR throughout for consistency. It also acknowledges that actual bond deliverability into each bilateral CDS is difficult to verify. Those choices affect both market representativeness and comparability across crisis phases. CDS quoted on a standard \$10 million notional do not imply that all matched cash-bond transactions have that size.

Basis observations are winsorized at the 0.5th and 99.5th percentiles; 1/99 and 0.25/99.75 alternatives are said to give similar results. The precise cross-sectional versus pooled winsorization implementation is not stated. Weekly bond-level bases average available daily bases. The regression sample then retains negative bases only. This is conditioning on the dependent variable, so estimated relationships describe the negative-basis region rather than an unrestricted linear pricing law.

The four periods are July 2006–June 2007, July 2007–August 2008, September 2008–September 2009, and October 2009–December 2014. The labels “Before Crisis,” “Crisis I,” “Crisis II,” and “Post Crisis” follow the source, not an external crisis-dating rule. Sixty-week rolling beta estimates require at least 24 weekly observations before the test week. Footnote 26 says supporting data start in July 2001, resolving the need for a pre-2006 estimation history. It does not explain availability and coverage of every proprietary input that far back. Tables III–IV report 444 weeks; the main text says 466. The table count is more consistent with the stated interval, but exact sample dates remain a replication input.

## Seven explanatory variables and expected signs

The full weekly regression includes an intercept, rating, lending fee, illiquidity level, two liquidity betas, counterparty beta, and funding beta. Explanatory variables are said to be standardized across bonds each week. The collateral variables use weekly averages of daily observations; beta estimates use the prior rolling window.

Rating is coded so higher values mean better quality, with AAA at 21. The manuscript’s low-end labels “1 for CCC, 2 for CC−” are internally awkward relative to that direction; the full notch mapping should be obtained rather than inferred from that sentence alone. Higher quality should mean easier collateral financing and a less negative basis. Lending fee is the transaction-value-weighted average over open lending transactions. It was expected to have a positive coefficient because an owner can benefit from scarcity value, but high fees can also signal aggressive short demand.

Illiquidity level is the Bao–Pan–Wang price-reversal statistic

$$
L_{i,m}=-\operatorname{Cov}(\Delta\log P_{i,d},\Delta\log P_{i,d-1})
$$

estimated within a month and assigned to weeks in that month. Its expected coefficient is negative. Assigning the completed month’s estimate to early weeks is contemporaneous retrospective measurement, not necessarily an available-at-the-time signal. A trading implementation would need an explicitly lagged or expanding estimate.

Liquidity beta measures covariance of a bond’s illiquidity with the sample’s average bond illiquidity; liquidity-market beta measures covariance with CRSP’s value-weighted stock-market return. The prose describes regression-style betas but does not print their full normalization equations. The expected signs are negative and positive respectively: a bond that becomes illiquid when everyone else does is undesirable, while a bond whose trading costs rise in good stock-market states is comparatively safer to unwind in bad states.

The counterparty proxy is

$$
\beta_{i,CP}=\frac{\operatorname{Cov}(\Delta CDS_i,\Delta CDS_{dealer})}{\operatorname{Var}(\Delta CDS_{dealer})}.
$$

The dealer index is capitalization-weighted across Federal Reserve primary dealers, with membership updated over time: Lehman exits after bankruptcy, for example, and Nomura enters in July 2009. Appendix B gives an 18-name July 2009 list, while the text refers to 19 dealers in September 2008; these are different dates, not necessarily a discrepancy. The proxy measures CDS comovement, not an observed bilateral default correlation or actual counterparty portfolio. Its expected coefficient is negative.

Funding sensitivity is

$$
\beta_{i,FL}=\frac{\operatorname{Cov}(\Delta b_i,\Delta(r_{repo,3m}-r_{Tbill,3m}))}{\operatorname{Var}(\Delta(r_{repo,3m}-r_{Tbill,3m}))}.
$$

A higher beta is desirable because the negative basis tends to converge when funding becomes more expensive; its expected cross-sectional coefficient is positive. The repo–Treasury-bill spread is chosen to reduce the bank-credit contamination of Libor-based measures. An OIS–bill alternative has correlation 0.90 with it and reportedly preserves results. This beta is estimated from the basis itself, so persistence and generated-regressor error deserve attention when interpreting subsequent basis regressions.

## Empirical results, units, and discrepancies

Table I averages daily cross-sectional statistics through time. Its standard deviations are cross-sectional dispersion averaged across days, not time-series volatility of an individual basis or of the aggregate basis. All entries below are basis points:

| Group or statistic | Before crisis | Crisis I | Crisis II | Post crisis |
|---|---:|---:|---:|---:|
| Mean basis, all bonds | −10 | −118 | −324 | −137 |
| Mean basis, investment grade | −17 | −83 | −243 | −101 |
| Mean basis, high yield | 12 | −180 | −560 | −237 |
| Cross-sectional SD, all bonds | 59 | 192 | 369 | 152 |
| All-bond 10th percentile | −57 | −273 | −667 | −268 |
| All-bond 90th percentile | 45 | 14 | −55 | −32 |

Negative observations are 69.3%, 87.6%, 94.4%, and 93.9% in the four phases, and 92.7% overall. Dispersion remains substantial within rating groups. During Crisis II, AAA/AA mean basis is −111 bps and CCC is −1,113 bps. Some firms nevertheless sustain positive bases for more than 100 of the 271 Crisis-II trading days, including Newmont, Berkshire Hathaway, and firms rated as low as B. This challenges a single uniform haircut explanation, while not rejecting the broader margin-based pricing framework.

Each week the authors run cross-sectional regressions and report time averages of coefficients and adjusted $R^2$, with Newey–West adjusted t-statistics. The lag truncation, complete-case sample rules, and treatment of estimated-beta error are not documented. Table III’s all-variable Crisis-II specification reports rating 1.902, t=6.780; illiquidity −0.676, t=−3.156; counterparty beta −0.545, t=−5.216; and funding beta 0.794, t=3.706. The illiquidity coefficient is mistakenly enclosed in brackets in the table; the prose identifies it as the coefficient. The lending-fee coefficient is −0.004, t=−2.578, opposite the collateral-value prediction.

These are reported coefficient numbers, not confidently converted basis-point effects. Although Table I and Table IV Panel A state bps, Tables III and IV Panel B do not clearly specify the dependent-variable scaling, and some tiny coefficients sit beside much larger values despite the claimed standardization. The PDF alone does not justify declaring 1.902 to mean either 1.902 or 190.2 bps per cross-sectional standard deviation. Obtaining code or a clean final table is necessary for that economic-unit conversion.

The strongest story concerns selected crisis exposures, not universal sign agreement. Crisis-I all-variable counterparty and funding coefficients are −0.181 and 0.132, with t-statistics −2.563 and 2.336. But liquidity-market beta is −0.807, t=−1.921, opposite its predicted positive sign. In Crisis II, liquidity-risk beta is positive 0.101 and insignificant, t=0.391. The Crisis-II liquidity-market entry 0.517 has t=1.722 yet two stars; a usual two-sided 5% interpretation is not supported by that t-statistic. The before-crisis lending-fee coefficient rounds to zero with t=0.718, so the prose’s blanket claim of a significant negative fee relationship throughout all periods is too broad.

Counterparty coefficients turn positive outside the crisis: 0.059 before and 0.163 after, with t=4.363 and 8.313. The authors suggest correlations with rating and fee; non-crisis correlations are −0.31 and 0.21. That is a plausible interpretation, not proof that multicollinearity causes the sign reversal. Rating is the most consistently positive significant variable. The bond-level full-regression adjusted $R^2$ values are printed as approximately 0.356, 0.408, 0.366, and 0.442; the pre-crisis cell has a bracket formatting error. The post-crisis value exceeds Crisis II’s, so the conclusion’s statement that explanatory power decreases substantially after the crisis should not be repeated as a statement about these total $R^2$ values. Individual risk-variable significance changes more clearly than total fit.

## The 24 portfolios and what their fit establishes

Table IV first divides bond outstanding amounts into four bins using the full sample’s quartiles, then divides each size bin into six rating groups: AAA/AA, A, BBB, BB, B, and CCC or below. These are 24 portfolios of negative-basis bonds. The size breakpoints use information from the whole period and therefore define an explanatory sorting exercise rather than a point-in-time trading formation rule. The PDF does not completely specify portfolio weighting and aggregation of every risk characteristic; those details matter for reproducing the second-stage regression.

Mean bases by size and rating show broad patterns but not the strict monotonicity claimed in the prose. For small bonds, the six means are −126, −125, −201, −258, −318, and −534 bps. For large bonds they are −79, −98, −130, −238, −266, and −631. Larger issues generally have less negative bases among the better-rated groups, but CCC-and-below reverses sharply: its intermediate size bins are −487 and −436, followed by −631 for the largest bin. BBB means improve steadily with size, −201, −146, −132, and −130. These concrete exceptions prevent turning a broad tendency into a deterministic size ordering.

The portfolio-regression adjusted $R^2$ values are 0.799, 0.759, 0.774, and 0.839 across the four periods, supporting the headline “around 80%.” This is in-sample explanatory fit for only 24 sorted objects, not 80% of subsequent realized returns predicted out of sample. Averaging reduces idiosyncratic noise, and rating is both a sorting variable and an explanatory variable.

In Crisis II, portfolio coefficients are rating 1.268, t=10.039; fee −0.005, t=−3.224; liquidity-market beta 0.809, t=2.506; counterparty beta −0.800, t=−6.425; and funding beta 0.720, t=3.431. Illiquidity level and liquidity beta are negative, −0.261 and −0.421, but their t-statistics −1.119 and −1.430 do not establish conventional significance. After the crisis, illiquidity and liquidity beta become significantly positive, again limiting the uniform risk-compensation interpretation.

Table IV’s before-crisis rating coefficient is positive 0.111 while its t-statistic is printed −5.431. Since a conventional coefficient t-statistic has the same sign as its numerator, at least one sign is wrong. The note preserves the positive coefficient and identifies the conflict rather than assigning a corrected t-statistic. Table II’s caption also dates its combined crisis correlation sample to September 2008, whereas the main crisis division ends September 2009; the actual correlation-window code is unavailable.

## Reproduction priorities and limits of inference

A credible reproduction must first recover a dated security master, historical rating mapping, actual MR quotes, valid CDS deliverability rules, TRACE correction logic, bond-price aggregation, and a fully specified PECDS engine. Next it should verify that curve, recovery, and optionality conventions do not manufacture cross-sectional patterns. Then it can construct lagged exposures, state clearly which month’s liquidity estimate was available in each week, reproduce negative-basis selection and standardization, and document Newey–West settings and all coefficient units.

The proprietary lending data and underlying market series are not supplied with this PDF. The robustness statements describe alternative liquidity measures, windows, funding proxies, winsorization, and option-free subsets, but detailed tables for those exercises are not included. No new empirical backtest is claimed in this note. The scalar hedge and CDS-leg checks verify accounting and signs only.

The paper offers evidence consistent with limits to arbitrage, especially during the crisis, and an informative warning that a seemingly beneficial lending fee can carry adverse information. It does not identify a structural price of funding or counterparty risk, distinguish every channel causally, or establish an executable risk-free annuity. Its strongest use is to motivate joint analysis of a basis opportunity and the conditions under which capital must be committed, refinanced, collateralized, and eventually withdrawn.
