# Closing auctions: Nasdaq versus NYSE

**Narasimhan Jegadeesh and Yanbin Wu.** *Journal of Financial Economics* 143 (2022), 1120–1139. DOI: 10.1016/j.jfineco.2021.12.003. [Source PDF](../../Finance/ClosingAuctions_Jegadeesh_2022.pdf). Page references below use the PDF's 20-page sequence; printed journal pages are 1119 higher.

## Why this matters

A closing-auction cost estimate depends critically on when the benchmark price is observed. Measuring only the difference between the auction price and the immediately preceding continuous-market price misses the response to the earlier public imbalance announcement. Jegadeesh and Wu measure the response from that announcement through the auction, then trace its reversal for five trading days. On that definition, Nasdaq has larger price impact than NYSE, and much of the initial movement subsequently reverses. For execution research, this is a warning against equating a small final auction-to-midquote difference with a small total cost of the closing order flow.

The paper also presents an economically interesting institutional comparison. NYSE gives floor participants information and order-handling advantages. Those advantages may discourage ordinary outside liquidity providers, but the floor participants can nonetheless add enough liquidity to improve total depth. The model makes that tradeoff explicit. The March–May 2020 floor shutdown provides supporting evidence, although the pandemic episode does not isolate each privilege or establish its welfare consequences.

The practical results are sizable: gross five-day returns from buying the strongest sell imbalances and shorting the strongest buy imbalances are 40.49 basis points on Nasdaq and 18.58 basis points on NYSE in Table 7. These are paper portfolio results, not executable net alpha estimates. Order timing, normalization by full-day volume, borrow, auction allocation, and the effect of the strategy's own orders remain material implementation gaps.

## Contribution and institutional setting

The paper contributes a risk-sharing model with differently informed liquidity providers, a common empirical framework for the two exchanges, evidence relating auction activity to ETF and fund flows, and estimates of both immediate impact and subsequent reversal. Its claim is not simply that auctions contain uninformed trading. It asks how the composition and information of the supplying side of an auction affect the price required to absorb that trading.

Nasdaq's auction is primarily an electronic interaction among outside traders. NYSE combines outside orders with designated market makers and floor brokers. In the period studied, floor participants can see more disaggregated information about orders, including prices, sizes, and entering or clearing firms. Repeated dealings may help identify the motives behind particular orders. NYSE's parity and priority rules also give floor participants allocation advantages. Floor brokers can use discretionary orders, or D-orders, to react late; the paper describes entry or modification until 3:59:50 p.m., whereas the public sees D-orders in the imbalance information beginning at 3:55 p.m. Nasdaq emphasizes time priority, with restrictions on altering certain late on-close orders. These are the historical rules underlying the sample, not a statement about current exchange rules.

The first imbalance release is not at a constant time throughout the data. Appendix A and the Figure 2 caption give the following schedule:

| Exchange | Dates | First public imbalance release |
|---|---|---|
| Nasdaq | March 1, 2010–October 28, 2018 | 3:50 p.m. |
| Nasdaq | October 29, 2018–April 14, 2019 | 3:55 p.m. |
| Nasdaq | April 15, 2019 onward | 3:50 p.m. |
| NYSE | March 1, 2010–March 31, 2019 | 3:45 p.m. |
| NYSE | April 1, 2019 onward | 3:50 p.m. |

The main discussion on PDF p. 10 reverses some initial exchange times and uses inconsistent transition dates. A replication should follow the explicit appendix and figure schedule, while independently verifying the exchange messages in the underlying data. This matters because a five-minute error changes both the impact benchmark and the amount of subsequent price discovery included in the return.

## Model, demands, and what the propositions establish

The model on PDF pp. 3–5 has one risky asset with terminal value $v$ and a risk-free asset whose rate is zero. The prior for $v$ is normal with mean $\mu$ and precision $\omega$. There are $N$ informed investors with a common signal $s$, distributed conditionally as $N(v,1/\psi)$. Their posterior mean and variance are

$$
v_0=\gamma\mu+(1-\gamma)s,\qquad
\gamma=\frac{\omega}{\omega+\psi},\qquad
\sigma_v^2=\frac{1}{\omega+\psi}.
$$

Investor $i$ begins with cash $c_i$ and an asset endowment $e_i$. The endowments have mean zero and variance $\sigma_e^2$. With common absolute risk aversion $\rho$, the demands used in the paper are

$$
q_i^{\mathrm{inf}}=\frac{v_0-p}{\rho\sigma_v^2}-e_i
=\lambda_{\mathrm{inf}}(v_0-p)-e_i,
\qquad
\lambda_{\mathrm{inf}}=\frac{\omega+\psi}{\rho}.
$$

The displayed utility in the PDF has a sign problem: it prints $-e^{\rho W}$, whereas the stated demand corresponds to the standard increasing CARA utility $-e^{-\rho W}$. This note uses the demand actually employed in the model, and identifies the implied utility correction rather than attributing the corrected expression to the printed source. There are no binding inventory, financing, or short-sale constraints in these linear demands.

Noise traders submit an aggregate market-on-close imbalance $OI$, assumed mean zero and independent of fundamental information. Outside liquidity providers have only the prior, so one provider's demand is

$$
q^{\mathrm{LP}}=\lambda_{\mathrm{LP}}(\mu-p),\qquad
\lambda_{\mathrm{LP}}=\frac{\omega}{\rho}.
$$

NYSE floor traders receive an additional signal $\delta$ of precision $\psi_\delta$. Their posterior mean is

$$
p^*=\gamma_\delta\mu+(1-\gamma_\delta)\delta,\qquad
\gamma_\delta=\frac{\omega}{\omega+\psi_\delta},
$$

and their demand is $\lambda_{\mathrm{FT}}(p^*-p)$, where $\lambda_{\mathrm{FT}}=(\omega+\psi_\delta)/\rho$. The signal construction is intended to give floor traders information that does not add to the informed investors' own signal. Another printed expression labels the nonzero posterior variance as $\operatorname{Var}(p^*\mid\delta)$; because $p^*$ is a function of $\delta$, that conditional variance is zero. The variance consistent with the demand is $\operatorname{Var}(v\mid\delta)=1/(\omega+\psi_\delta)$.

Let $K_N$ and $K_Y$ be the numbers of outside providers on Nasdaq and NYSE and let $N_F$ be the number of NYSE floor traders. Aggregate demand slopes, written here as $\Lambda$ to keep them distinct from individual slopes, are

$$
\Lambda_N=N\lambda_{\mathrm{inf}}+K_N\lambda_{\mathrm{LP}},
$$

$$
\Lambda_Y=N\lambda_{\mathrm{inf}}+K_Y\lambda_{\mathrm{LP}}
+N_F\lambda_{\mathrm{FT}}.
$$

Market clearing sets the sum of informed demand, outside-provider demand, floor demand when applicable, and $OI$ to zero. Consequently,

$$
p_N-\mu=
\frac{N\lambda_{\mathrm{inf}}(v_0-\mu)-\sum_i e_i+OI}{\Lambda_N},
$$

$$
p_Y-\mu=
\frac{N\lambda_{\mathrm{inf}}(v_0-\mu)-\sum_i e_i
+N_F\lambda_{\mathrm{FT}}(p^*-\mu)+OI}{\Lambda_Y}.
$$

These equations expose an important notational error in the source. The demand slope $\Lambda$ has the economic role of depth, measured in shares per unit price; $1/\Lambda$ is price impact per share. The PDF calls $1/\lambda$ depth and asserts an inverse-slope ordering inconsistent with its own $\lambda_{\mathrm{FT}}>\lambda_{\mathrm{LP}}$. The economically meaningful comparison is that better information raises the willingness to absorb a given price discrepancy. Calling the reciprocal depth would reverse that interpretation.

The appendix proof conditions on the noise imbalance. Under the independence and zero-conditional-mean assumptions,

$$
E[p_j-\mu\mid OI]=\frac{OI}{\Lambda_j},\qquad
E[v-p_j\mid OI]=-\frac{OI}{\Lambda_j}.
$$

The second identity is a reversal result under an explicitly uninformed imbalance. It is not a general theorem that all observed auction imbalance is temporary. A component of imbalance correlated with $v$, different signal distributions across venues, or endogenous participation would change the result.

Outside providers incur a fixed operating cost $\kappa$, and the entry argument equates their certainty-equivalent profit to that cost. Floor advantages reduce outside-provider opportunity, so the paper argues that $K_Y<K_N$. It does not give a completely solved entry equilibrium with empirically calibrated $\kappa$. NYSE's total depth is nevertheless larger precisely when

$$
N_F\lambda_{\mathrm{FT}}>(K_N-K_Y)\lambda_{\mathrm{LP}}.
$$

Removing floor traders without instant replacement by outside providers can therefore lower depth sharply. This is a conditional comparative static, not a claim that privileged entry always improves liquidity. Nor does it price the distributional cost of privileging one class of participants.

## Sample and construction of trading proxies

The main sample runs from March 2010 through December 2020. It includes NYSE- and Nasdaq-listed common stocks with CRSP share codes 10 or 11, excluding stocks whose previous close is below \$5. The authors identify auction prints in TAQ using the relevant auction trade flags. TAQ intraday returns in the most extreme 0.1% of the distribution are excluded to reduce errors; the corresponding exclusion is not imposed on CRSP daily or opening-price returns used later. A reproduction must distinguish those filters rather than apply a single winsorization rule everywhere.

Closing auctions account for approximately 3% of dollar trading volume in 2010, around 10% in 2019, and 7% in 2020. The 2020 drop in share reflects the increase in total trading volume. Figure 1 smooths its series using 90-day moving averages. Table 1's stock-day mean auction fraction is 8.16%, with a 5.11% median; mean auction dollar volume is \$3,493,226 and median volume is \$320,728. These are different estimands from the aggregate annual time series.

To proxy for liquidity-motivated auction demand, the authors use domestic physical, unlevered equity ETFs in Morningstar, including active and inactive funds, and quarterly holdings information. Matching uses ticker and CUSIP information. There are 713 unique ETFs over the sample. The annual coverage expands from 199 ETFs with \$350.9 billion in 2010 to 580 with \$2,638.8 billion in 2020, representing approximately 80% of the relevant CRSP ETF assets.

For stock $i$, the ETF auction-arbitrage proxy aggregates ETF closing-auction volume translated into the value of that ETF's underlying stock position:

$$
B_{i,t}=\sum_j N_{j,t}S_{i,j,t},\qquad
ETF\_arb_{i,t}=\frac{B_{i,t}}{DollarVolume_{i,t}},
$$

where $N_{j,t}$ is ETF $j$'s number of shares traded at its close and $S_{i,j,t}$ is the dollar value of stock $i$ held per ETF share, constructed from the latest quarterly holdings and current prices. Here $DollarVolume_{i,t}$ is the stock's full-day dollar volume. Table 1 reports the dollar numerator, while Eq. (14) defines the normalized regression variable. A separate $ETF\_cr$ proxy uses ETF creation and redemption activity. Fund-flow proxies use the analogous stock allocation of index mutual fund and active mutual fund flows.

These variables are noisy indicators rather than identified trades. ETF auction trades need not be arbitrage; underlying basket trades need not occur in the auction; and creations and redemptions can be intermediated differently. Mean $ETF\_arb$ is \$147,036, with median \$12,427. Its mean ratio to stock auction volume is 14.25%, but the median ratio is only 2.93%. The mean creation/redemption proxy is \$1,135,126; mean index-fund and active-fund flow proxies are \$193,983 and \$696,524.

Table 2 regresses closing-auction volume divided by daily volume on these proxies. All variables are standardized within each day by subtracting the cross-sectional mean and dividing by its standard deviation. The models include firm and date effects, with standard errors clustered by stock and day. The univariate ETF-arbitrage coefficient is 0.171, $t=29.46$; the creation/redemption coefficient is 0.208, $t=47.58$. In the joint regression they are 0.080, $t=13.21$, and 0.160, $t=28.78$. The index-fund coefficient becomes 0.001, $t=0.07$, and the active-fund coefficient is −0.003, $t=-1.68$. Thus the joint result is strongest for the ETF proxies, not equally strong for all passive-flow measures.

The earnings indicator identifies announcements after the day's close. Its joint coefficient is −0.071, $t=-23.25$, and the joint model has 7,245,959 observations and adjusted $R^2=0.248$. Auction participation declines as a fraction of daily trading before those announcements, consistent with greater relative informed trading intraday. It does not imply that auction volume declines in dollars: daily volume approximately doubles while auction dollar volume rises about 35% relative to the preceding five days. The distinction between a ratio and its numerator is central to this interpretation.

## Imbalance dynamics and price impact

The main imbalance measure uses the first public auction message:

$$
OI_{i,t}=\frac{C^{\mathrm{buy}}_{i,t}-C^{\mathrm{sell}}_{i,t}}
{\text{total shares traded during day }t}.
$$

The denominator is full-day realized volume. That is reasonable for a descriptive regression but is not observable at the first imbalance release. A trading implementation would need a forecast or a lagged denominator; the paper does not provide or test one. Normalizing instead by total on-close buy plus sell orders produces qualitatively similar results according to the text.

NYSE has a higher mean absolute imbalance, 2.27% of daily volume versus Nasdaq's 1.48%, and a much higher median absolute imbalance, 1.30% versus 0.02%. Signed means are near zero. Nasdaq imbalance falls by more than 80% within a minute of its first announcement. NYSE imbalance changes little until D-orders become visible at 3:55 p.m., then drops sharply. These paths should not be read as direct counts of offsetting shares: price changes affect which orders participate, and the paper's new-order-volume analysis supplies separate evidence about entry.

NYSE's additional late orders grow over time. Relative to orders at the first dissemination, new on-close orders at the close are approximately 17% in the early sample and 44% in the later sample; at 3:55 p.m. the corresponding amounts are approximately 4% and 18%. Figure 4's D-order series reaches roughly 50% in 2019 and is around 40% in 2020 outside the shutdown. Its denominator is auction volume at the first dissemination, not final auction volume, so it cannot be substituted for the introductory statement about D-orders' fraction of final closing volume.

The main price-impact regression is

$$
R^{\mathrm{announce}\to\mathrm{close}}_{i,t}
=a+b\,OI_{i,t}+c\,1_{\{Nasdaq\}}OI_{i,t}
+\Gamma'X^{\mathrm{signed}}_{i,t}+f_i+g_t+u_{i,t}.
$$

The controls are signed by the direction of imbalance. They include the previous day's absolute return divided by dollar volume, current-day quoted spread averaged equally across transactions, lagged log market capitalization, and inverse previous closing price. Firm and day effects are included, and inference clusters by stock and day. The current-day spread is a descriptive liquidity control rather than an ex ante input fixed at the first announcement.

Table 4's pooled imbalance coefficient is 2.555, $t=30.66$. Without liquidity controls the NYSE coefficient is 2.080, while the Nasdaq increment is 0.887, giving Nasdaq 2.967. With controls the corresponding coefficients are 1.670 and 0.979, giving Nasdaq 2.649: approximately 59% more impact than NYSE. Those coefficients are reported in the source's regression scaling; the relative comparison does not require guessing an additional percent-to-basis-point convention.

The venue difference becomes larger in the later subsample. With controls, 2010–2015 coefficients imply 2.383 for NYSE and 2.865 for Nasdaq, whereas 2016–2020 imply 1.084 and 2.542. Thus NYSE's estimated impact drops substantially while Nasdaq's falls less. This is consistent with rising floor participation, but exchange listing, stock characteristics, changing rules, and time trends are not randomly assigned.

The NYSE floor closes from March 23 through May 25, 2020. Table 5 uses April 2019–December 2020 and adds venue-specific shutdown interactions. Without controls, NYSE impact changes from 1.508 to $1.508+4.447=5.955$; Nasdaq changes from $1.508+1.171=2.679$ to $3.473$. The NYSE shutdown interaction has $t=11.25$ and the Nasdaq interaction $t=1.83$. With controls, the implied shutdown slopes are 5.608 and 3.335. The relative deterioration is striking.

Two limitations are essential. First, the shutdown coincides with extraordinary volatility and potentially different pandemic exposures across listings; the difference-in-differences interpretation needs the counterfactual relative venue effect to be stable after controls. Second, shutting the physical floor removes a bundle of participation mechanisms. It does not separately identify the information advantage, allocation rule, relationship capital, or D-order timing. The Table 5 caption also describes a common 3:50 p.m. dissemination regime over a period that begins before Nasdaq's April 15, 2019 change.

## Reversal estimates and portfolios

The paper first estimates auction impact from the imbalance regression without liquidity controls, then regresses future cumulative returns on that predicted impact. Each venue is estimated separately. Firm and date effects and two-way clustering are retained. Overnight ends at the next opening price; the longer horizons end at subsequent closes.

| Horizon | Nasdaq reversal slope | NYSE reversal slope |
|---|---:|---:|
| Overnight | −0.430 | −0.212 |
| One trading day | −0.641 | −0.389 |
| Two trading days | −0.744 | −0.454 |
| Three trading days | −0.756 | −0.512 |
| Four trading days | −0.818 | −0.627 |
| Five trading days | −0.848 | −0.615 |

These Table 6 estimates indicate about 85% reversal on Nasdaq and 62% on NYSE over five days. The five-day $t$-statistics are −31.24 and −16.84. The authors report no significant incremental reversal through day ten in an untabulated test. The results are not 100% reversal, unlike the literal fully uninformed-imbalance model. Nor does an average regression slope mean that every imbalance yields a profitable contrarian trade.

Table 7 sorts stocks daily within venue into imbalance deciles. A same-direction announcement-to-auction portfolio buys the largest buy imbalances and shorts the largest sell imbalances. Its reported gross return is 30.34 basis points on Nasdaq, $t=40.02$, and 24.79 on NYSE, $t=48.69$. The paper acknowledges that prices react rapidly to the public release, making this apparent profit difficult to capture. There is also an internal Table 7 inconsistency: the NYSE extreme-leg entries, −11.12 and 13.12 basis points, differ by 24.24, not the printed 24.79. The reported long-short entry should not be silently reconstructed as if the table were arithmetically consistent.

The contrarian strategy enters at the auction, buying the largest sell-imbalance decile and shorting the largest buy-imbalance decile. Its gross returns are:

| Holding period | Nasdaq | NYSE |
|---|---:|---:|
| Overnight | 15.08 bp, $t=28.89$ | 5.79 bp, $t=16.69$ |
| One day | 28.42 bp, $t=23.63$ | 12.27 bp, $t=13.76$ |
| Five days | 40.49 bp, $t=16.86$ | 18.58 bp, $t=10.14$ |

The text elsewhere gives 5.09 basis points for NYSE overnight; the table gives 5.79. Panel B also has a portfolio-label/sign inconsistency relative to its legs. The economic orientation reported here is the stated contrarian strategy; the discrepancies should be resolved from code before reproduction.

The authors use Newey–West standard errors with 12 lags for portfolio returns. A SPY market-model adjustment, taking the risk-free rate as zero, leaves five-day equal-weight alpha of 40.48 basis points on Nasdaq and 18.46 on NYSE. Value-weight alpha is smaller: 26.92 and 11.39 basis points, with $t$-statistics 7.47 and 4.41. The reduction under value weighting indicates that the simple equal-weight headline should not be taken as the return on an institutional dollar-weighted execution opportunity.

Table 8 gives the scale of the extreme portfolios' underlying imbalances. Nasdaq's sell and buy extremes average −5.44% and 5.31% of daily shares, or approximately 24,735 and 24,317 shares per stock, worth about \$1.11 million. NYSE's corresponding values are −6.10% and 6.25%, approximately 77,801 and 76,032 shares, worth \$3.76 million and \$3.69 million. These are observed imbalances, not demonstrated capacity that an added contrarian strategy can fill without moving the auction.

The paper cites auction fees of \$0.00085–\$0.0027 per share, less than one basis point at a \$30 stock price. That comparison does not establish net profitability. It omits the full liquidation cost, short borrow fees and locate availability, allocation risk, financing, overlapping holding-period capital, and endogenous impact from supplying the imbalance. Entry after observing the first message also requires an order type and submission time allowed by the relevant historical venue rules. The complete future daily volume used to rank normalized imbalance is another timing issue. A credible implementation needs those pieces before converting the paper portfolios into a net strategy.

## Interpretation and limits

The paper provides evidence that auctions can be cheap relative to many forms of continuous-market trading while still generating predictable temporary price pressure. Its comparison with published regular-session spreads and impact estimates is contextual, not a matched experiment with identical stock-days, order sizes, and trading motives. The market-on-close benchmark may be the correct objective for a fund tracking a closing-price index even when it differs from the best estimate of fundamental value.

The apparent conflict with studies finding small NYSE-to-Nasdaq differences, or very little auction price discovery, is partly about the measurement window. Public auction messages can move continuous quotes before 4 p.m. This paper includes that adjustment. A study beginning at the final midpoint measures the remaining auction displacement. Both quantities are useful, but neither can substitute for the other in implementation shortfall accounting.

The suggested reforms—more flexibility for late Nasdaq order changes and incentives for qualified market makers—follow from the model's risk-bearing mechanism. They are proposals, not policy experiments evaluated in this paper. Allowing later revisions could reduce liquidity suppliers' exposure to adverse information, while affecting manipulation risk, order certainty, and queue incentives. The supplied evidence does not quantify the net effect of those competing mechanisms.

A reproduction should preserve the exact historical dissemination schedule; construct venue-consistent auction flags; separate daily-return cleaning from TAQ intraday cleaning; align quarterly holdings without future information; keep full-day and ex ante imbalance normalizations distinct; and resolve the utility, depth, and Table 7 inconsistencies from the authors' implementation. The main empirical conclusions survive those reporting cautions as conclusions of the reported tables: NYSE has lower full announcement-to-close impact in normal periods, loses that advantage during the floor closure, and both venues exhibit substantial multi-day reversal. Their use as causal institutional claims or tradable net returns requires stronger assumptions than the descriptive estimates alone provide.

## Source map

The supplied PDF contains the complete 20-page article, including its model proof and historical timing appendix. Institutional details and model: PDF pp. 2–5, Eqs. (1)–(13). Sample and flow proxies: pp. 6–9, Tables 1–2. Imbalance paths and impact: pp. 10–14, Figs. 2–4 and Tables 3–5. Reversals and portfolios: pp. 15–18, Tables 6–8. Discussion and Appendix A–B: pp. 18–20. The primary results above are from this article; comparisons to other work are the authors' contextual comparisons rather than independent validations supplied by this note.
