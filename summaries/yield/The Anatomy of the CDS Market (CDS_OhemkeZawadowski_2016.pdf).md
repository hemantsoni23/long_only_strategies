# The Anatomy of the CDS Market

Martin Oehmke and Adam Zawadowski, *The Review of Financial Studies* 30(1), 2017, pp. 80–119; advance access August 18, 2016; accepted January 17, 2016. DOI 10.1093/rfs/hhw068. [Source PDF](../../Finance/CDS_OhemkeZawadowski_2016.pdf). The filename uses the advance-access year and a misspelling of Oehmke; the supplied article is the 2017 journal version. All 40 PDF pages, including Appendices A and B and references, were read. The five figures, seven tables, sample-construction rules and likelihood equations were inspected visually. Printed page numbers equal PDF page numbers plus 79.

## Why this matters

CDS activity is often discussed as either insurance or speculation. This paper asks a more useful market-design question: why do investors trade a firm's credit risk through a derivative when they can trade its bonds? Its answer is that CDSs offer a comparatively standardized venue when the issuer's bonds are split across small issues with different terms. Credit-risk trading can migrate toward that venue, while basis traders connect the derivative and cash markets.

The contribution is reference-entity-level evidence linking CDS positions and trading to bond supply, analyst disagreement, bond fragmentation, contractual heterogeneity and relative pricing. It combines unusually broad DTCC position data with bond-level trading and security characteristics. It is an empirical market-structure study, not a newly solved equilibrium model or a returns backtest. The theory guiding the basis-trade predictions comes from the authors' separate 2015 paper.

Three findings organize the results. Outstanding bonds and disagreement are positively associated with net CDS positions, consistent with both hedging and speculation. Fragmented or contractually heterogeneous bonds are associated with more CDS activity and less bond trading, consistent with a standardization advantage. Finally, the relation between CDS positions and the negative CDS–bond basis is stronger when funding is easier; a stronger estimated relation is associated with a smaller negative basis and lower bond price impact. The authors explicitly describe the analysis as largely descriptive because they lack natural experiments establishing causal effects.

## What the quantity data measure

For a reference entity, gross notional is the total contractual amount of protection bought, equivalently sold. It counts chains of intermediated and offsetting trades. Net notional first offsets each counterparty's protection purchases and sales, then sums the positive net protection purchases. If $n_k$ is counterparty $k$'s signed net purchase,

$$
N=\sum_k\max(n_k,0)=\frac12\sum_k|n_k|,
\qquad\sum_kn_k=0.
$$

This is not gross notional divided by two or a net balance across the entire market, which would be zero. Figure 1 illustrates the distinction with \$10 million trades. Initially X sells protection to Y, so both gross and net equal \$10 million. Y then sells \$10 million to Z: gross becomes \$20 million, net remains \$10 million. Finally Z sells \$10 million to X: gross is \$30 million but all three parties have zero net positions, so net is zero.

Net notional is a useful measure of the stock of credit exposure transferred after within-counterparty offsets. It is not a direct measure of cash at risk after recovery and collateral, a count of distinct end-investor bets, or a measure of the counterparty network's gross settlement and replacement exposures. A high net-to-bond ratio also does not itself identify prohibited or destabilizing trading; investors can hedge counterparty exposure and anticipated future borrowing as well as currently outstanding bonds.

DTCC's weekly single-name position data start October 31, 2008. The top 1,000 reference entities are selected by **gross**, not net, notional. That distinction is central to the econometrics. The data capture nearly the entire standard CDS market, with the source citing DTCC's roughly 95% global coverage estimate, but the authors' matched U.S. corporate sample is much narrower.

Weekly trading data begin July 16, 2010; the monthly trading sample begins August 2010. The measure includes market-risk activity: new trades, qualifying terminations and assignments that transfer credit risk. It excludes clearing of existing bilateral contracts, compression and backloading that do not create the relevant risk transfer. Trading volume is a flow and should not be confused with the stock of net notional; a closing transaction can count as trading without increasing net positions.

## Sample construction and security matching

The position sample covers October 2008 through December 2012, and the trading sample August 2010 through December 2012. Those are 51 and 29 calendar months respectively. The text calls the first span 52 months, but the dates and the later tables' 51 dates support 51; this note preserves the discrepancy rather than inventing an extra observation month.

Eligible firms are public U.S. parent companies in Compustat with at least one SEC-registered outstanding bond, an S&P rating, at least two analysts for the disagreement measure, and evidence of an existing CDS market. A market exists once the firm either appears among DTCC's top 1,000 entities or has five-year Markit CDS quotes from at least three dealers. Once established, CDS-market existence is assumed to persist through the remaining sample. This rule distinguishes a CDS-traded but censored entity from a company assumed to have no CDS market.

Sources are Compustat for balance sheets, ratings and industry; Mergent FISD for bonds and contractual terms; TRACE Enhanced for transactions including uncapped large trade sizes; CRSP for stock prices and historical issuer identifiers; IBES for forecasts; Markit for CDS quotes; and DTCC for positions and risk-transfer volume. Parent/issuer matching is partly manual. CDSs written on a subsidiary are not reassigned to its parent. Multiple ambiguous DTCC matches are dropped, and firms exit upon bankruptcy or a CDS settlement auction.

The bond measure used as the main hedging proxy includes direct parent issues and obligations inherited from acquired firms that have been fully dissolved. Separate subsidiary debt is kept distinct because the parent generally is not liable without a guarantee. Consolidated Compustat debt therefore cannot simply replace legally matched parent bonds. Historical CRSP CUSIPs, FISD parent identifiers, manual corporate checks and six-digit issuer CUSIPs are used to reconcile these relationships.

Appendix A excludes original maturities shorter than 366 days, issue and redemption months, retail notes, denominations below \$1,000, pass-through notes, foreign-currency bonds, zero or missing offering amounts and effectively recalled bonds. Partial recalls reduce the outstanding amount. Bond turnover is winsorized at the 99th percentile at issue level. Firms without assets or industry codes and nonoperating establishments are excluded. Suspect matches are removed when FISD outstanding bonds exceed Compustat total debt by more than 50% of assets. Conglomerates are manually assigned to their dominant industry; Fannie Mae, Freddie Mac and the U.S. Postal Service are excluded.

Each month, unbounded variables are winsorized at the 1st and 99th percentiles; the smaller basis sample uses the 2nd and 98th percentiles. These are cross-sectional monthly transformations, not rolling forecasting rules. The source does not release the matching crosswalk or specify every weekly-to-monthly position aggregation decision within this PDF.

The resulting universe has 496 firms, 302 appearing in DTCC at least once, and 22,229 firm-months in the baseline censored regression. Table 1 reports 13,411 observed net/gross position observations, whereas the accompanying prose says 13,441. The table is the source for the count used here. A basis is available for 123 firms, 97 of which appear in DTCC; complete regression controls reduce the corresponding observation counts further.

## Descriptive magnitudes and constructed regressors

Amounts in the tables are billions of dollars unless stated otherwise. For observed DTCC positions, mean net notional is 1.035 and median .817, while mean gross is 13.13 and median 9.914. Netting therefore changes the scale dramatically. Median net CDS divided by directly issued bonds is 26.1%, and the 90th percentile is 113.8%. Including subsidiary bonds in the denominator lowers those values to 18.2% and 85.9%. These are distributions of firm ratios, not the ratio of aggregate totals.

Mean monthly CDS turnover, volume divided by net CDS, is 50.6%, with median 43.7%. Bond turnover, volume divided by outstanding bonds, averages 7.16%, with median 4.62%. The denominators differ economically, so their ratio is not a pure liquidity measure. Figure 3 shows comparable aggregate monthly CDS and bond trading for the DTCC firms, while Figure 2 shows aggregate single-name net positions declining by about 35% to roughly \$1 trillion at end-2012. The paper cautions that declining aggregate positions need not mean less customer relevance: gross interdealer positions declined while customer purchases and sales to dealers increased.

Insurable interest is proxied primarily by direct bonds outstanding $B_{it}$. Other debt is consolidated short- plus long-term debt minus parent and subsidiary bonds. Accounts payable is set to zero for financial firms because its accounting content can include deposits. A separate dummy identifies named credit-enhancement providers, such as monoline insurers, for whom other investors may seek a hedge of counterparty risk.

Disagreement is the standard deviation of analysts' two-year earnings-per-share forecasts divided by the contemporaneous CRSP share price, provided the price exceeds \$1. Lower prices are treated as missing. This is a proxy for potential differences in valuation, not observed speculative CDS positions. A declining equity price can raise the ratio mechanically, and a common measure of analyst disagreement need not equal disagreement among the actual derivative counterparties.

For issuer $i$ with issue sizes $b_{ij}$, the issue-concentration index is

$$
H_i=\sum_j\left(\frac{b_{ij}}{B_i}\right)^2,
\qquad B_i=\sum_jb_{ij}.
$$

A single issue gives $H=1$; five equal-sized issues give $H=.2$. Regress $\log H$ on $\log B$, then take minus the residual as bond fragmentation $F$. This removes the fitted mechanical relation between size and concentration while preserving variation in how a given debt amount is split. The source does not state the exact pooling/window convention of this auxiliary regression. Its reported standard deviation is .406. A high-fragmentation dummy indicates an above-median value.

Contractual heterogeneity is one if an issuer's outstanding bonds differ in at least one of six binary features: callable, puttable, convertible, fixed coupon, covenants or credit enhancement. It is zero when all bonds agree along all six dimensions. This is a coarse diversity indicator, not a measure of the economic distance between covenant packages or maturities. Its mean is .671. The text's explicit zero/one rule on printed p. 93 clarifies the less precise Table 1 wording.

## Censored position regression and identification assumptions

The latent position model is $y^*_{it}=X_{it}'\beta+\varepsilon_{it}$, with conditional Gaussian error standard deviation

$$
\sigma_{it}=a+\gamma B_{it}>0.
$$

The regressor vector contains the economic proxies, credit-rating categories, time dummies and either first-digit SIC industry dummies or firm effects. Rating controls are AA and above, A, BBB, B, and CCC and below, with BB omitted. Positions are modeled in dollar levels rather than divided by assets. This lets outstanding bonds enter as a hedging proxy instead of imposing asset-proportionality on speculative or arbitrage demand.

Let $c_t$ be the modeled net-notional censoring cutoff, $d_{it}=1$ for an observed DTCC position, $m_{it}=X_{it}'\beta$, and $z_{it}=(y_{it}-m_{it})/\sigma_{it}$. Appendix B's log likelihood is

$$
\ell=\sum_{i,t}\left\{
 d_{it}[\log\phi(z_{it})-\log\sigma_{it}]
 +(1-d_{it})\log\Phi\left(\frac{c_t-m_{it}}{\sigma_{it}}\right)
\right\}.
$$

Observed positions contribute a normal density, and missing-but-traded entities contribute the probability of being below the threshold. They are not set to zero in the estimation. Figure 4 plots censored firms at zero only for illustration; its horizontal axis is $\log(\mathrm{bonds})$, despite Appendix B referring to $\log(\mathrm{assets})$.

The crucial approximation is converting a **gross-notional** selection rule into a **net-notional** cutoff. The authors use the month's mean empirical gross/net relation among observed entities and assume it also applies to excluded entities. This is not an exact observed selection threshold for net positions: two firms with different offsetting/intermediation structures can have the same gross but different net notional. The paper reports that allowing cutoff uncertainty does not materially change estimates but omits that adjustment for simplicity. A faithful replication needs the precise gross-to-net mapping, the weekly/monthly cutoff series and the treatment of any observed net positions that fall below the imputed cutoff.

Maximize jointly over $\beta,a,\gamma$, imposing positive standard deviations for every observation. A numerically stable implementation uses log-normal-CDF calculations for censored tails and a firm-clustered sandwich covariance, with scores summed within firms. The source specifies heteroscedasticity and firm clustering, but not positivity enforcement, optimization tolerances, initial values, finite-sample covariance factors or fixed-effect treatment beyond the sample restrictions. The Gaussian latent distribution permits negative values; the model is a statistical approximation for positive positions, not a structural nonnegative demand equation.

Firm-fixed-effect specifications include only firms observed in DTCC at least once, so that a firm effect can be identified. That reduces the sample from 496 to 302 firms and changes both the variation used and the population. Fragmentation and contractual heterogeneity are nearly constant within firms, so their main specifications use industry rather than firm fixed effects. They cannot claim to absorb every stable issuer characteristic correlated with bond design.

## Position results: hedging, disagreement and standardization

Table 2 column 1 estimates a coefficient of .0777 on outstanding bonds, with $t=7.30$, and 4.672 on disagreement, with $t=4.74$. In the paper's coefficient-based interpretation, an extra dollar of direct bonds corresponds to 7.77 cents more net CDS. Moving bonds from the 25th percentile, \$0.8 billion, to the 75th, \$4.15 billion, gives approximately \$260 million using the printed rounded inputs, or 31.9% of median net CDS. The prose rounds the amount to \$261 million.

A one-standard-deviation disagreement change gives $4.672\times.0313=.146234$ billion, about 18% of median net CDS. These magnitudes are changes in the fitted latent location. They are not estimates of the fraction of observed CDS trades that were motivated by hedging or speculation. The same contract can have a hedger on one side and a speculator on the other.

With firm fixed effects, the bond coefficient falls to .0138 and is statistically insignificant ($t=1.36$); disagreement falls to .928 but remains significant at 5% ($t=2.31$). The authors attribute some weakening to little within-firm variation and the short panel. The result supports a strong cross-sectional relation more clearly than a precise within-firm response of CDS positions to incremental debt issuance.

In column 4, subsidiary bonds are small and insignificant; other borrowing has a negative coefficient −.00535 ($t=-2.06$); credit-enhancement providers have an additional 2.215 billion ($t=4.63$). Accounts payable has coefficient .0163 ($t=2.52$), or 1.63 cents per dollar. Printed p. 97 describes 2.02 cents, inconsistent with the visually checked table. The table figure is reported here without asserting what unrounded or earlier estimate might explain the prose.

Fragmentation enters with coefficient .272 ($t=3.41$), implying .110432 billion for a .406 standard-deviation change. The above-median fragmentation dummy also happens to have coefficient .272 ($t=4.27$): \$272 million, or about 33% of median positions. Those identical coefficients belong to differently scaled regressors and should not be treated as the same experiment. Predetermined fragmentation, measured when CDS trading starts or January 2002 if later, remains positive at .165 ($t=2.29$), using 431 firms and 19,606 observations. This reduces one reverse-causality concern but does not randomize financing structure.

Contractual heterogeneity alone is associated with .291 billion more net CDS ($t=3.97$), about 36% of the median. When included jointly with fragmentation, coefficients are .235 ($t=3.04$) and .181 ($t=2.16$). Thus the two measures capture overlapping but not identical aspects of the cash market.

## Joint trading-volume model and cross-market comparison

The volume regressions use firms with net positions reported in DTCC and cover 288 firms and 8,041 observations in the baseline. The firm-effect version has 287 firms and 8,029 observations after excluding a firm with no bond transactions. Zero monthly volume occurs in fewer than 1% of CDS observations and fewer than 5% of bond observations. The authors use a joint Tobit model, allowing the CDS and bond latent-volume errors to correlate.

For markets $k\in\{C,B\}$, the intended representation is

$$
V^*_{kit}=X_{it}'\beta_k+\sigma_{kit}u_{kit},\qquad
V_{kit}=\max(0,V^*_{kit}),\qquad
\operatorname{Corr}(u_{Cit},u_{Bit})=\rho.
$$

Each $\sigma_k$ has its own constant-plus-bonds form. Appendix B prints the single-equation normal-density/zero-mass likelihood, while the text describes joint correlated estimation. To reconstruct the joint likelihood, two positive observations contribute a bivariate normal density divided by $\sigma_C\sigma_B$. If CDS volume is zero and bond volume positive, the contribution is the bond marginal density times the conditional normal probability that latent CDS volume is below zero. Writing $z_B=(V_B-m_B)/\sigma_B$ and $a_C=-m_C/\sigma_C$, that contribution is

$$
\frac{\phi(z_B)}{\sigma_B}
\Phi\left(\frac{a_C-\rho z_B}{\sqrt{1-\rho^2}}\right).
$$

The reverse case swaps the markets, and two zeros contribute $\Phi_2(a_C,a_B;\rho)$. This completion of the described model is derived here; the local appendix does not print all four joint cases. The correlation parameter and estimated heteroscedasticity coefficients are not tabulated.

Table 3's baseline coefficients on bonds are .0283 for CDS volume ($t=8.94$) and .0862 for bond volume ($t=29.72$). Both are positive and significant, but equality is rejected. The disagreement coefficients are 4.594 ($t=3.29$) for CDS and .427 ($t=1.14$) for bonds, with cross-market equality rejected at $p=.005$. Multiplying by .0313 gives approximately \$144 million extra CDS volume, 43.1% of the .334 billion median, versus an insignificant \$13.4 million in bond volume. Firm-effect estimates preserve this contrast: disagreement coefficients are 3.352 and .208, with equality $p=.007$.

The coefficient-based calculations follow the paper but are not exact marginal effects on observed Tobit means. For one equation,

$$
E[V\mid X]=m\Phi(m/\sigma)+\sigma\phi(m/\sigma).
$$

With fixed $\sigma$, a continuous regressor's mean effect is $\beta\Phi(m/\sigma)$. When that regressor also changes $\sigma$, an additional $\partial\sigma/\partial x$ times $\phi(m/\sigma)$ enters. The latter applies to bonds under the specified variance model. A dummy's mean effect requires evaluating the entire expression at both values. Since zeros are uncommon, latent-coefficient magnitudes may approximate some observed effects, but the paper does not report the observation-level quantities needed to verify that approximation.

Continuous fragmentation coefficients are .0825 for CDS volume ($t=2.05$) and −.0377 for bond volume ($t=-3.88$), with equality rejected at $p=.004$. Above-median fragmentation corresponds to .0899 billion more CDS volume and .0201 billion less bond volume, approximately +27% and −22% relative to their reported medians. Contractual heterogeneity gives .0843 billion and −.0173 billion respectively, with equality $p=.002$. These signs support venue substitution; they do not establish that every dollar disappearing from bond trading mechanically becomes a dollar of CDS trading.

## Bond trading costs as evidence for the mechanism

The cost measure follows matched same-size transactions occurring no more than 15 minutes and ten trades apart. Only institutional-size trades of at least \$1 million face value are included. Half-roundtrip customer/dealer spreads are doubled to obtain a full implied roundtrip cost. This is an inferred transaction-cost measure, not a quoted bid–ask spread observed continuously.

Table 4 regresses roundtrip cost by OLS and turnover by Tobit, with rating, time and industry controls and firm-clustered inference. Fragmentation's cost coefficient is .0426 in percentage-point units ($t=3.90$); the turnover coefficient is −.0199 ($t=-3.98$). A .406-standard-deviation change gives .017296 percentage points, or 1.73 basis points, more roundtrip cost. Relative to the median .280% cost, that is 6.18%, matching the paper's 6.2%. The turnover calculation is a .008079 change, about 17.5% of the .0462 median.

Contractual heterogeneity separately gives .0246 percentage points more roundtrip cost and −.0101 turnover, around 8.8% and −21.9% relative to the respective medians. When both heterogeneity and fragmentation enter, heterogeneity loses significance in both equations; fragmentation remains significant. These are consistent with a liquidity mechanism but do not eliminate omitted issuer characteristics or endogenous trading demand. The paper itself emphasizes that turnover mixes ease of trading with the demand to trade, which is why direct liquidity measures are outcomes here rather than the main explanatory variables in the earlier position regressions.

## Basis construction and arbitrage hypotheses

Define the CDS–bond basis as CDS spread minus the bond spread over the risk-free rate. A negative basis means the bond offers more spread than the cost of buying credit protection. The corresponding trade buys the bond and buys CDS protection; the positive-basis trade shorts the bond and sells protection. The approximate no-arbitrage comparison assumes sufficiently matched risks and cash flows. Financing costs, collateral, counterparty exposure, contract terms, bond shorting and delivery options prevent a raw spread difference from being a guaranteed realizable profit.

The authors use fixed-coupon bonds without embedded options and remaining maturities of one to 30 years. They match or interpolate CDS spreads to maturity, use OIS as the risk-free benchmark, and use actual size-weighted customer purchase prices for the negative trade and sale prices for the positive trade, from bond transactions exceeding \$1 million face value. The CDS leg uses the Markit midpoint because executable bid and ask prices are unavailable. The resulting basis is more execution-aware than a mid-bond-price calculation, but it still excludes an observed CDS bid–ask cost and a complete funding/margin budget.

For each day, choose the most negative eligible bond basis and, separately, the most positive. Define $B^-_{it}$ and $B^+_{it}$ as monthly averages of their positive magnitudes, setting the corresponding daily opportunity to zero where none exists. Thus larger $B^-$ means a **more negative** raw basis. Monthly percentage-point units matter: 1.496 corresponds to 149.6 basis points. Table 1's 3,012 basis observations are more numerous than Table 5's 2,730 complete baseline regression observations.

The position regression adds $B^-$ and $B^+$ to the controls. Theory predicts a positive coefficient on $B^-$ because a larger cheap-bond opportunity attracts basis positions. Interactions should be negative when funding is difficult, bond trading is costly, or disagreement draws investors into directional bets. These are equilibrium joint-pattern predictions; position and basis are determined together, so the regression is not an exogenous demand experiment.

Table 5's baseline $B^-$ coefficient is .0888 ($t=2.61$). A 1.496-point increase implies .132845 billion more net CDS, around 16% of the median. With firm effects it remains positive at .0290 ($t=2.86$), on 97 firms and 2,422 observations. Positive-basis coefficients are insignificant throughout, compatible with shorting frictions and the relative scarcity of positive-basis observations. The absence of significance is not proof that no positive-basis trades occur.

The negative-basis/TED interaction is −.104 ($t=-3.87$) when entered individually, and −.0840 ($t=-3.73$) in the full-interaction specification. The roundtrip-cost interaction is −.123 ($t=-2.48$) and −.0729 ($t=-2.12$), respectively. Fragmentation's interaction is negative but insignificant alone, −.104 ($t=-1.34$), becoming significant jointly, −.158 ($t=-2.08$). Disagreement's interaction is −1.029 ($t=-2.90$) alone but −.721 ($t=-1.29$) jointly. Consequently, the paper's four directional hypotheses find support across specifications, but not all four interactions are significant in the most inclusive regression.

The use of the most extreme bond per issuer is economically motivated by opportunity selection. It can also link the measured basis to the number of eligible issues mechanically. Comparing an average-basis construction is therefore useful; the main text reports such robustness in Online Appendix Table 13 but does not include that table in this local PDF.

## Generated measure of basis-trade strength

The next analysis allows the negative- and positive-basis slopes in the position regression to vary by month, with the other control coefficients held common across months. Denote the estimated negative-basis slope by $\widehat a_t$. It measures how sensitively net CDS positions covary with negative-basis opportunities in that month's cross section. It is not an observed arbitrageur balance sheet, the fraction of CDS activity due to basis traders, or an investment return.

Figure 5 shows the slope near zero during late 2008 and early 2009, larger after funding conditions improve, and less precisely estimated later. Its mean is .265 and standard deviation .198. The authors also report that allowing bonds and disagreement coefficients to vary over time produces similar results, without supplying that full estimated series here.

Second-stage regressions explain the negative basis and bond price impact using $\widehat a_t$, controls, and crisis interactions. Because $\widehat a_t$ is common to all firms in a month, unrestricted time fixed effects would absorb its main effect; these second-stage tables do not include them. The crisis indicator covers October 2008 through December 2009; the postcrisis period is January 2010 through December 2012.

Inference uses 1,000 bootstrap samples, first resampling dates and then firms within each date, rerunning both estimation stages in each draw and taking coefficient standard deviations. Reusing only a fixed first-stage slope series in the bootstrap would omit generated-regressor uncertainty. The stated resampling scheme is not a serial block bootstrap and does not automatically preserve within-firm histories across sampled dates. The authors report a Monte Carlo exercise supporting conservative inference under generated data resembling their sample, but do not provide its parameterization or numerical output here.

Measurement error can attenuate a slope under classical assumptions; with jointly estimated contemporaneous variables and potentially common shocks, downward bias is not a universal theorem. The note therefore treats the source's conservative-inference assertion as a reported simulation conclusion, not a guarantee for every alternative data-generating process.

## Basis compression and price impact

Table 6 uses only firm-months with at least one negative-basis bond, yielding 2,112 observations, 120 firms and 51 dates. The controlled industry-effect specification estimates a coefficient −2.624 on basis-trade strength ($t=-4.91$); the firm-effect version gives −2.210 ($t=-5.09$). Multiplying −2.624 by .198 gives −.519552 percentage points, or approximately 52 basis points, matching the reported one-standard-deviation magnitude.

The crisis-split specification with industry controls gives a postcrisis main coefficient −.291 ($t=-2.74$) and an additional crisis interaction −7.128 ($t=-4.40$). The crisis slope is their sum, −7.419, rather than the interaction alone. After TED controls, the corresponding coefficients are −.279 and −5.676. These associations remain negative, but the common time-series nature of the strength measure leaves omitted market-wide developments and simultaneity as identification concerns. The study does not independently estimate how much an exogenous expansion of arbitrage capital would lower a firm's borrowing cost.

For price impact, form a bond issue's daily midprice from the average of value-weighted bid and ask transaction prices; if unavailable, use value-weighted interdealer prices. On trading day $d$, calculate the absolute percentage price change from the previous trading day $d-1$ to the next $d+1$, divide by day-$d$ volume in billions of dollars, and average across eligible issue-days within the firm-month:

$$
\mathrm{AMI}_{it}=\operatorname{average}_{j,d\in(i,t)}
\frac{100\left|P_{j,d+1}/P_{j,d-1}-1\right|}
{\mathrm{Volume}_{j,d}\;\text{in billions}}.
$$

Only days with at least \$1 million volume are used. This is a two-trading-day price-change window divided by the central day's volume, not the usual same-day equity-return formula. It is a liquidity proxy, not a directly identified response to an exogenous signed supply shock. The source obtains 15,639 firm-months, using an average 26.3 eligible issue-days each; Table 7 includes 469 firms.

The industry-controlled coefficient on strength is −2.954 ($t=-3.60$), and the firm-effect coefficient is −2.677 ($t=-3.95$). The .198-standard-deviation change implies a .584892 reduction in the Amihud statistic, or 28.9% of its 2.023 median. That is a reduction in the reported proxy's scale, not a 28.9-basis-point spread change.

The relationship is concentrated in the crisis. With industry controls and crisis interactions, the main coefficient is .0753 and insignificant; the crisis interaction is −12.67 ($t=-4.11$). With TED controls it falls to −3.390 ($t=-1.87$), significant only at 10%; with both TED and firm effects it is −2.870 ($t=-1.52$), insignificant. The source acknowledges the last result. Its broader prose also says fragmentation increases price impact significantly in all specifications, but Table 7's firm-effect fragmentation coefficients are insignificant, including −.194, .131 and .108. The table supports the cross-sectional liquidity relation more strongly than a uniform within-firm one.

These qualifications do not erase the overall pattern: conditions consistent with more active basis trading coincide with a smaller negative basis and less bond price impact. They do delimit the evidence for a causal shock-absorption mechanism, especially outside the crisis.

## Reproduction priorities and source coverage limits

A faithful reconstruction starts with legal-entity matching and monthly eligibility, not with a regression package. Build parent and subsidiary obligations separately, define the observation/selection indicator from DTCC, retain censored CDS-traded entities, construct the gross-to-net cutoff approximation, reproduce the monthly winsorization, then fit the position and joint-volume models with their specified heteroscedasticity and controls. Bond fragmentation needs a documented auxiliary-regression convention; disagreement needs the two-year forecast horizon and the \$1 price floor; contractual diversity needs the explicit one-if-any-difference rule.

The liquidity and basis calculations require TRACE Enhanced trade direction, size and timing, plus security terms and maturity-matched CDS/OIS curves. Dollar amounts, percentage-point costs, basis points and decimal turnover must remain distinct. The second-stage bootstrap must repeat the monthly slope estimation and preserve the stated conditional negative-basis sample. An implementation should separately report latent coefficients and observed-mean Tobit effects instead of assuming they coincide.

Missing inputs include proprietary source records, the hand-matching crosswalk, exact weekly-to-monthly aggregation, original gross/net cutoffs, auxiliary-regression pooling details, optimized variance parameters and joint error correlation, detailed basis interpolation/pricing conventions, optimizers, seeds and Monte Carlo settings. The source's repeated references to separate Online Appendix Tables 8–13 describe additional hedging, disagreement, volume, liquidity and average-basis checks. That supplement is not part of the supplied 40-page PDF and was not found in the local filename search; those robustness claims are reported from the main text, not independently read tables.

The paper has no held-out strategy evaluation, rolling out-of-sample window, realized basis-trade P&L, fully costed arbitrage simulation or investor-level identification of motives. Its durable contribution is a set of carefully measured conditional market-structure facts: standardized derivatives attract credit trading where cash instruments are fragmented, and links between the venues appear economically important. Its regressions provide targets for structural modeling and future identification, rather than a causal estimate of the total social benefit or cost of CDS trading.
