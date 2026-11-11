# Can Portfolio Rebalancing Explain the Dynamics of Equity Returns, Equity Flows, and Exchange Rates?

**Harald Hau and Hélène Rey. American Economic Review 94(2), May 2004, pp. 126–133, Papers and Proceedings. DOI: 10.1257/0002828041302389.**

**Primary source:** [ForexForecasting_HauRey_2004.pdf](../../Finance/ForexForecasting_HauRey_2004.pdf), the complete published article, with a JSTOR cover. Printed page numbers are used below. The authors' [technical supplement](https://haraldhau.com/aea_supplement.pdf), January 2004, was also inspected; it supplies the rotation-grid size and the additional impulse-response figures. The article studies compatibility with a portfolio-rebalancing mechanism, not an out-of-sample trading strategy.

## Why this matters

An investor whose foreign equity holdings outperform domestic holdings acquires a larger foreign-currency exposure even without trading. If that exposure is not fully hedged, reducing the resulting risk can require selling foreign assets and repatriating proceeds. Equity-market success can therefore be followed by capital outflows and depreciation of the successful market's currency. This reverses the simple intuition that high local equity returns must attract capital and strengthen the currency.

Hau and Rey turn this mechanism into restrictions on the joint behavior of equity returns, equity flows, and exchange rates. Their innovation is empirical identification through the signs of conditional correlations rather than a fixed recursive ordering of monthly shocks. Because financial prices and flows can react within a month, the assumption that one observed variable moves before all others is particularly difficult to defend.

The resulting evidence is supportive but deliberately theory-dependent. The authors select the decomposition most favorable to the proposed mechanism among decompositions consistent with the reduced-form covariance matrix. The right interpretation is that the data admit a plausible portfolio-rebalancing account and display the expected patterns under that identification. The exercise is not independent causal proof that rebalancing, rather than an omitted common shock, generated each movement.

## Economic mechanism and the three shocks

Two conditions are central. First, cross-border equity investors leave some foreign-exchange exposure unhedged. Second, arbitrageurs and counterparties do not absorb unlimited equity and currency demand at unchanged prices. Portfolio shifts can then affect both markets. These conditions do not require the market to be literally illiquid in the ordinary sense; finite risk-bearing capacity is enough for imperfectly elastic demand.

The article builds on an earlier equilibrium model by the authors, but does not reproduce its full preferences, endowments, and solution. Its own testable content consists of three hypotheses. Define the ordered vector

$$
y_t=(ER_t,FL_t,FX_t)'.
$$

The conventions are essential:

- $ER_t$ is the foreign equity-market return minus the U.S. equity-market return, with both measured in their **local currencies**. It is not a dollar-converted foreign excess return and not an excess return over a risk-free rate.
- $FL_t$ is net U.S. equity outflow into the foreign country, scaled by bilateral gross equity trading volume. A positive value is a flow toward the foreign market.
- $FX_t$ is the exchange-rate return with **dollar appreciation positive**. A stronger foreign currency therefore corresponds to negative $FX$.

**Equity-return shock, H1.** An increase in foreign relative equity value raises foreign exposure. Rebalancing produces foreign equity sales and repatriation toward the United States. Thus $ER$ and $FL$ should be negatively correlated conditional on a return shock, while $ER$ and $FX$ should be positively correlated.

**Exchange-rate shock, H2.** Foreign-currency appreciation itself increases the dollar value and currency exposure of foreign holdings. Investors respond by reducing the foreign allocation, putting downward pressure on foreign relative equity prices. With the paper's sign convention, a positive dollar-appreciation shock instead goes with positive foreign inflows and positive foreign relative equity returns. Consequently both $FL$–$FX$ and $ER$–$FX$ conditional correlations are positive.

**Equity-flow shock, H3.** A demand shift toward foreign equities raises foreign relative equity prices and strengthens the foreign currency. Thus conditional on a flow shock, $ER$–$FL$ correlation is positive and $FL$–$FX$ correlation is negative.

The complete sign map is

| Primitive shock | Correlation restriction 1 | Correlation restriction 2 |
|---|---|---|
| $s_1$: relative equity return | $\rho_{12\mid s_1}<0$ | $\rho_{13\mid s_1}>0$ |
| $s_2$: equity flow | $\rho_{12\mid s_2}>0$ | $\rho_{23\mid s_2}<0$ |
| $s_3$: exchange rate | $\rho_{13\mid s_3}>0$ | $\rho_{23\mid s_3}>0$ |

These are restrictions on shock-specific comovement, not necessarily on unconditional sample correlations. Mixing several shocks can offset or reverse the unconditional sign. Likewise, a conditional positive dollar response to foreign equity outperformance does not imply that every observed month of foreign outperformance must feature dollar appreciation.

## Data and construction

Section IV, pp. 131–132, uses monthly bilateral observations between the United States and **France, Germany, Japan, Switzerland, and the United Kingdom**, January 1990 through September 2003. The calendar span contains 165 months before losses from return construction and VAR lags. The paper does not enumerate the final effective regression row count or a missing-observation mask.

Equity flows come from the U.S. Treasury's Treasury International Capital system. For each partner, the data measure purchases and sales between U.S. and foreign residents in both foreign equity and U.S. equity. In a transparent implementation, let $NP_F$ denote U.S. residents' purchases minus sales of foreign equity, and $NP_U$ foreign residents' purchases minus sales of U.S. equity. Let $GV_F$ and $GV_U$ be the associated gross purchases-plus-sales totals. The article's normalized net outflow can then be organized as

$$
FL_t=\frac{NP_{F,t}-NP_{U,t}}{GV_{F,t}+GV_{U,t}}.
$$

This notation makes the source's verbal definition executable; the actual TIC line mappings and vintage must still be obtained. It is a transaction-flow measure, not a change in marked-to-market holdings. The gross-volume denominator accommodates the large secular growth in cross-border equity trading. It also means that a value of 0.05 represents 5% of combined gross bilateral equity transactions, not 5% of investor wealth, assets under management, or the foreign market's capitalization.

The reported average monthly gross bilateral volumes and standard deviations of normalized net flows are:

| Foreign country | Gross volume, billions of U.S. dollars per month | Standard deviation of $FL$ |
|---|---:|---:|
| France | 19.8 | 0.076 |
| Germany | 9.8 | 0.091 |
| Japan | 24.1 | 0.091 |
| Switzerland | 11.8 | 0.073 |
| United Kingdom | 95.8 | 0.040 |

The volume figures are in the article's footnote 4; the flow dispersions are in Section IV. These are useful unit checks for a reconstruction. A denominator using only foreign-equity transactions would generally fail those checks.

Equity returns are calculated from MSCI end-of-month local-currency index prices. Exchange-rate returns likewise use MSCI end-of-month dollar exchange rates. The article does not state a precise series identifier, dividend-treatment choice, or whether its percentage-return implementation uses simple or logarithmic differences. A replication should document those decisions and compare both plausible return conventions rather than silently calling a modern total-return series the original input.

France and Germany share the euro from 1999, so the final years of their exchange-rate data coincide. Their equity and flow data remain different. Treating the two currency series as independent corroborating exchange-rate realizations would exaggerate the breadth of evidence. More generally, the five bilateral systems share U.S. equity returns and common dollar shocks.

The TIC observations are residence-based cross-border transactions. Intermediary locations and the distinction between transaction flows and ultimate economic exposure are relevant measurement limitations. These are implications of the data structure, not additional country exclusions imposed by the authors.

## Reduced-form dynamics

Each country is modeled separately using a three-variable VAR with two lags. The source says standard criteria favored an AR(2), without naming the criterion or reporting the alternatives. Using a conventional coefficient sign convention, write

$$
y_t=c+A_1y_{t-1}+A_2y_{t-2}+\eta_t,\qquad
E[\eta_t\eta_t']=\Sigma.
$$

For a stable VAR, the moving-average representation is

$$
y_t=\phi+\sum_{h=0}^{\infty}B_h\eta_{t-h},\qquad B_0=I,
$$

with $B_1=A_1$ and $B_h=A_1B_{h-1}+A_2B_{h-2}$ for $h\ge2$. This recursion is an explicit reconstruction of the article's lag-polynomial notation. The supplement instead writes the autoregressive polynomial with plus signs; software must convert coefficient conventions consistently.

Estimate $\Sigma$ from residuals and obtain a lower-triangular Cholesky factor $P$ satisfying $PP'=\Sigma$. Cholesky is only a starting factorization, not the final recursive identification. For any orthogonal rotation $R$,

$$
\widetilde P=PR,\qquad C_h=B_hPR,\qquad
\varepsilon_t=R'P^{-1}\eta_t
$$

gives $E[\varepsilon_t\varepsilon_t']=I$ and preserves the reduced-form innovation covariance. The task is to choose the rotation using the six economic sign preferences.

Use three plane rotations in the $(1,2)$, $(1,3)$, and $(2,3)$ coordinate planes, in that order. For example,

$$
R_{12}(\theta)=
\begin{pmatrix}
\cos\theta&-\sin\theta&0\\
\sin\theta&\cos\theta&0\\
0&0&1
\end{pmatrix},\qquad
R=R_{12}(\theta_1)R_{13}(\theta_2)R_{23}(\theta_3).
$$

The other rotations use the same two-by-two block in their corresponding coordinates. Matrix multiplication order must be preserved: rotations generally do not commute. Column signs also require an orientation convention when plotting positive shocks, even though shock-specific correlations themselves are unchanged by reversing an entire column's sign.

## Conditional correlations and the identification objective

The article writes conditional correlations as normalized products of rows of the moving-average polynomial after selecting a primitive shock. Its notation suppresses the covariance operation over the lag sequence. An implementable stationary interpretation is to isolate the component of each variable driven by shock $j$:

$$
y^{(j)}_{a,t}=\sum_{h\ge0}C_{h,aj}\varepsilon_{j,t-h}.
$$

With serially independent, unit-variance primitive innovations, the contemporaneous correlation of these components is

$$
\rho_{ab\mid j}(R)=
\frac{\sum_{h\ge0}C_{h,aj}C_{h,bj}}
{\sqrt{\left(\sum_{h\ge0}C_{h,aj}^2\right)
\left(\sum_{h\ge0}C_{h,bj}^2\right)}}.
$$

This is a clarified mathematical reconstruction, not a separately specified finite-horizon formula in the source. The article and supplement do not state the MA truncation horizon used numerically. A reproduction must expose that choice and check convergence as the horizon increases. Using only the impact coefficient of one scalar shock would produce correlations of magnitude one whenever both loadings are nonzero, so it is not an adequate general replacement for the lag-polynomial covariance calculation.

For each of the six desired signs, define $d_k=+1$ for a positive prediction and $d_k=-1$ for a negative prediction. The linear objective is

$$
F(R)=-\sum_{k=1}^{6}d_k\rho_k(R),\qquad
R^*=\arg\min_R F(R).
$$

This is **not** a hinge penalty that is zero once a restriction is satisfied. A strongly correct-signed correlation contributes a larger negative value and can compensate for an unfavorable contribution elsewhere. Therefore the implementation should report each selected correlation as well as the total score; merely finding a low objective does not prove all restrictions hold.

The technical supplement specifies **90 grid points per angle** on $[-\pi/2,\pi/2]$, hence $90^3=729{,}000$ candidate triples. It also shows the full response matrices for all three shock types. The article itself supplies the economic restrictions and linear objective; the supplement resolves the otherwise missing grid resolution. [Technical supplement, appendix pp. 2–3 and figures 1–4](https://haraldhau.com/aea_supplement.pdf).

The practical sequence is to estimate a VAR, generate its MA coefficients, compute the six shock-specific correlations for each rotation, minimize their signed sum, orient the chosen shocks, and plot the corresponding responses. Flat or nearly tied minima should be retained for sensitivity analysis; the source does not report a tie-breaking rule or an identified set of near-optimal decompositions.

## Impulse responses and reported results

Section V reports **cumulative responses over ten months** to a one-standard-deviation primitive shock. With the normalization above, the cumulative response to shock $j$ through horizon $H$ is

$$
IRF^{cum}_{a,j}(H)=\sum_{h=0}^{H}C_{h,aj}.
$$

The source's figures label horizons from zero through ten. An implementation must state whether its stored ten-month horizon includes the impact observation; off-by-one differences can affect table comparisons. The confidence bands are two standard deviations, based on **250 simulations of the data process**. The article does not specify whether innovations are drawn parametrically or resampled, how starting values are handled, whether each simulated VAR is reidentified over the full rotation grid, or whether bands are pointwise or adjusted for joint coverage. They should not be described as simultaneous 95% confidence bands.

For a foreign relative-equity-return shock, Figures 1–3 show a positive cumulative relative-equity response, an outflow from the foreign country toward the United States, and dollar appreciation. The equity-flow adjustment takes several months, whereas the currency response is immediate. This timing is economically relevant: a currency market may respond to anticipated rebalancing before the cumulative measured transaction flow is complete.

The positive relative-equity response is persistent in most country systems. The United Kingdom is an exception in the strength of the persistence evidence. Likewise, the paper cannot establish a long-run dollar appreciation against sterling after the equity shock, although its initial response has the predicted sign. These qualifications prevent a uniform five-country claim of persistent and statistically clear effects at every horizon.

The article's numerical illustration is France. A roughly **4% foreign relative-equity return**, described as one standard deviation, is associated with an equity outflow from France toward the United States equal to approximately **5% of gross bilateral transaction volume**. At a monthly gross volume near \$20 billion, that is approximately **\$1 billion**. The associated dollar appreciation is approximately **2%**. The three numbers refer to an identified dynamic response and should not be interpreted as a separately estimated causal elasticity suitable for scaling arbitrary transactions.

For an equity-flow shock toward the foreign country, the source reports higher foreign relative equity returns and persistent dollar depreciation. It describes the depreciation as significant for all five country systems. For a dollar-appreciation shock, it reports U.S. outflows toward the foreign equity market and higher foreign relative equity returns, consistent with restoring currency exposure after the dollar value of foreign holdings falls. These findings are discussed on p. 132; the supplied article's main figures cover the equity-return shock, while the supplemental figures display the other shocks.

## Robustness and identification limits

The principal robustness exercise removes one of the six correlations from the objective, reoptimizes using the other five, and checks whether the omitted correlation still has the predicted sign. The source generally finds stable qualitative responses. Its footnote identifies an exception for Japan: the response of relative equity returns to an exchange-rate innovation changes sign in one omitted-restriction exercise. The printed footnote's correlation subscript does not align cleanly with its verbal description, so the precise omitted pair needs the original code or further clarification.

This procedure is more informative than simply displaying the restrictions used to select the rotation. It still is not an unrestricted test of the economic mechanism: five related restrictions remain in place, the same sample determines all rotations, and omitted common factors can shape the reduced form. Nor do six sign preferences minus three rotation angles automatically create a conventional chi-squared overidentification test. Inequality restrictions, nonlinear correlations, and grid selection require their own inferential treatment.

The source reports that equity-flow and relative-equity-return shocks account for **10–20% of exchange-rate variance**, rising to approximately **20% in each country** in a later subsample. Two limitations are material. First, that subsample is printed as 1997–2004 although the data section ends the sample in September 2003. Second, the article states that its variance decomposition does not depend on the identification procedure, but it does not supply the definition or horizon needed to reconcile that statement with a conventional structural decomposition.

For comparison, the usual forecast-error share for a subset of shocks $J$ is

$$
VD_{FX,J}(H)=
\frac{\sum_{h=0}^{H-1}\sum_{j\in J}C_{h,FX,j}^{2}}
{\sum_{h=0}^{H-1}\sum_{j=1}^{3}C_{h,FX,j}^{2}}.
$$

The denominator is invariant to orthogonal rotation, but the numerator generally is not. Thus the reported identification-independence claim cannot simply be transferred to this standard structural FEVD. This formula is an explanatory qualification, not evidence that the authors used this exact implementation. Their 10–20% figures should be retained as reported results with an unresolved decomposition definition.

## What is needed for an honest replication

A reproduction can recover the main experiment by obtaining the historical TIC and MSCI inputs, matching flow units, estimating each bilateral VAR(2), running the specified rotation search, and producing all cumulative response matrices. The strongest checks are the reported gross volumes and normalized-flow dispersions, consistent dollar-appreciation signs, and stability of the six selected correlations and leave-one-out results.

Exact numerical agreement additionally requires the original data vintage, return conventions, missing-data handling, VAR lag-selection criterion, residual-covariance normalization, MA truncation, shock orientation, simulation scheme, and variance-decomposition definition. The supplement resolves grid size but does not close all these gaps. Modern data downloads or alternative inference methods can provide valuable robustness exercises, provided they are identified as such.

The model is not a portfolio-construction recipe with a target allocation, leverage constraint, or trading-cost function. Its practical relevance is to the interaction of portfolio risk and exchange rates: realized changes in foreign asset values can create subsequent demand to rebalance currency exposure, and anticipated flows can affect prices before trades are fully observed. The evidence supports incorporating those interactions into international risk models while preserving the uncertainty introduced by theory-favorable identification and monthly aggregation.
