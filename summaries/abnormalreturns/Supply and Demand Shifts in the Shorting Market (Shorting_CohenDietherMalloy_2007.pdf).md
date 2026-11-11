# Supply and Demand Shifts in the Shorting Market

Lauren Cohen, Karl B. Diether, and Christopher J. Malloy. *The Journal of Finance* 62(5), October 2007, pp. 2061–2096.

**Source:** [Shorting_CohenDietherMalloy_2007.pdf](../../Finance/Shorting_CohenDietherMalloy_2007.pdf). The supplied PDF contains a JSTOR cover followed by the complete article. References below use the article's section and table numbers; PDF page numbers include that cover. This note distinguishes the paper's observed lending transactions, its identification argument, and its approximate implementation-cost calculation.

## Why this matters

A rise in short interest need not mean that investors have become more pessimistic. It can also mean that lending supply has expanded, allowing previously constrained demand to be executed. The paper's contribution is to observe both the price and quantity of stock loans and use their joint movements to distinguish these mechanisms. An increase in loan quantity accompanied by a higher borrowing fee identifies an outward demand movement under the paper's supply-and-demand assumptions. More quantity accompanied by a lower fee points instead to an outward supply movement.

The empirical question is whether these different movements predict different subsequent stock returns. In this institution's small-stock lending sample, outward demand shifts predict substantial negative abnormal returns. Most other shifts do not produce similarly robust regression results. This supports the interpretation that some demand for borrowing reflects adverse information, whereas the amount on loan alone combines informative demand with changes in borrowing availability.

The distinction is useful for signal design, but it is not sufficient to establish an easily tradable anomaly. The equal-weighted results are much stronger than the value-weighted results, the demand-out portfolio is small, and the paper's cost estimates consume most of the spread. A faithful reconstruction must therefore preserve the lender-specific nature of the data, the timing of fee and quantity observations, and the difference between statistical predictability and implementable net returns.

## The identification argument

Let $f$ denote the annual stock-loan fee and $q$ the lender's shares on loan divided by the stock's shares outstanding. The fee is the relevant money-market collateral rate less the rebate paid to the borrower. A lower rebate therefore means more expensive borrowing, holding the collateral rate fixed. The paper observes changes between consecutive formation dates and defines four mutually exclusive indicators:

| Indicator | Change in fee | Change in loan quantity | Identified movement |
|---|---:|---:|---|
| DOUT | Positive | Positive | Outward demand |
| DIN | Negative | Negative | Inward demand |
| SOUT | Negative | Positive | Outward supply |
| SIN | Positive | Negative | Inward supply |

The economic assumptions are upward-sloping loan supply and downward-sloping loan demand, with economically comparable observations at the two dates. These are directional restrictions, not an estimated system of supply and demand elasticities. Both curves may move. The observed quadrant identifies at least one necessary direction of movement; it does not prove that only the named curve moved.

An illustrative linear system makes that qualification precise. Suppose, purely to illustrate the sign argument, that $q^D=a-bf$ and $q^S=c+df$, where $b,d>0$. Between equilibria,

$$
\Delta a=\Delta q+b\Delta f,
\qquad
\Delta c=\Delta q-d\Delta f.
$$

When both observed changes are positive, $\Delta a>0$ regardless of their relative sizes, but $\Delta c$ may have either sign. These equations are an explanatory example, not a structural model fitted by the authors. The empirical paper uses the sign indicators, without estimating $b$, $d$, or the magnitudes of latent shifts.

Observations with both fee and quantity unchanged can remain in the regression with all four indicators equal to zero. Observations where only one variable changes have an ambiguous quadrant classification and are excluded from the classified-shift construction. The raw lending data must also distinguish a true zero loan balance from an absent or unavailable loan-price observation. The paper examines new borrowing separately; a replication should not silently manufacture a fee for a stock that had no preceding loan.

This identification concerns the market represented by one lender. A shift in borrowers' choice of lender, or a lender-specific change in inventory, can affect its observed quantities. The authors address this with market-share measures and aggregate short-interest data, but the baseline is not a consolidated market-wide loan book.

## Data and sample construction

The principal source is confidential daily, contract-level stock-lending data from a large institutional investor, September 1999 through August 2003. The return tests cover October 1999 through September 2003. Contract records include the number of shares, rebate, collateral, prevailing market rate, lending income, and broker information. Multiple contracts for a stock can carry different fees. The baseline fee is the fee on the largest contract, measured by shares; quantity is the sum of shares across its contracts. Alternative mean and share-weighted fee definitions reportedly produce similar conclusions.

The authors join these records to CRSP stock returns, shares outstanding, and volume; Compustat book equity; I/B/E/S analyst coverage and earnings information; CDA/Spectrum institutional holdings; and exchange short-interest data. Institutional ownership is institutional shares held divided by shares outstanding, lagged one quarter: the monthly return regression uses $IO_{i,t-3}$. The paper reports robustness using aggregate short interest beyond the lender's own positions.

The principal universe consists of NYSE, AMEX, and Nasdaq stocks below the lagged NYSE median market capitalization and with lagged prices of at least \$5. The lender's presence is concentrated in smaller companies. The price restriction is also connected to collateral conventions: loans generally require collateral of 102% of market value, marked to market, and the institution applies a minimum \$5 valuation to low-priced shares. These conventions can distort the economic meaning of a quoted borrowing cost for very low-priced stocks.

The distinction between the broad stock universe and the active lending sample is essential. Table II reports approximately 2,098 small stocks per month in the relevant universe, but only about 172, or 8.2%, have loans at both required observation dates. Roughly 125 of those observations fall into the four shift categories. The average monthly counts are about 22 DOUT, 34 DIN, 38 SIN, and 31 SOUT; the median DOUT count is only 14. These are not diversified portfolios of hundreds of independent demand shocks.

The lender represents about 26% of aggregate short interest in its small-stock positions, compared with about 2% for large stocks. In 13.6% of the relevant observations it accounts for at least two-thirds of the stock's total short interest; in 7.5% it accounts for all of it. Its mean small-stock fee is 3.94% annually, compared with 0.39% for large stocks. The fraction of shares outstanding on loan is about 0.85% versus 0.14%, and the corresponding average numbers of contracts are 11.79 and 4.64. The overall average fee is about 2.6% annually. These statistics explain why a single institution may be informative about some hard-to-borrow small stocks while being much less representative of the broad large-cap market.

Table II also documents economically visible changes within the classifications. For DOUT observations, the average fee rises from 3.30% to 3.72% annually and the quantity on loan rises from 0.78% to 1.10% of shares outstanding. For DIN, fees decline from 2.57% to 2.16% and quantity from 1.09% to 0.80%. SIN fees rise from 2.88% to 3.28% as quantity falls from 0.98% to 0.65%. SOUT fees fall from 3.11% to 2.55% as quantity rises from 0.79% to 1.09%. Fee changes are changes in an annual rate, whereas the return outcomes below are generally monthly percentages.

## Timing and the baseline return regression

For the monthly strategy, compare lending conditions on successive month-end trading dates. The resulting signal, known at the end of month $t-1$ within the confidential lender data, predicts returns during month $t$. Weekly and daily versions apply the analogous shorter observation intervals. The median loan lasts approximately three weeks, providing one reason to examine horizons shorter than a quarter.

The main dependent variable is a stock's return less the contemporaneous return on its matching size and book-to-market portfolio. There are 25 benchmark portfolios from a five-by-five sort, with equal-weighted benchmark returns. The stock's characteristics used for assignment precede the outcome return. The generic regression is

$$
AR_{i,t}=\alpha_t+\beta_D DOUT_{i,t-1}
+\beta_I DIN_{i,t-1}+\beta_S SIN_{i,t-1}
+\beta_O SOUT_{i,t-1}+\gamma'X_{i,t-1}+\varepsilon_{i,t}.
$$

Here $\alpha_t$ is a calendar-month fixed effect. Controls include the preceding month's stock return, the compounded return over months $t-12$ through $t-2$, institutional ownership, and recent turnover. Turnover is based on average daily exchange-adjusted trading volume over the preceding six months. The separation of the latest month's return from the earlier eleven months is important: it controls short-term reversal and longer-term momentum separately.

The main estimates pool stock-month observations and cluster standard errors by calendar month. This allows contemporaneous cross-stock dependence in residual returns. The sample contains only 48 return months, so the apparent cross-sectional abundance should not be mistaken for thousands of independent time observations. The authors also consider Fama–MacBeth regressions, but emphasize pooled regressions because some months have very few observations in individual shift categories.

Extensions add fee levels, indicators for expensive borrowing, loan quantities, continuous changes in fees and quantities, and interactions. A replication must keep the set of included observations consistent when comparing specifications: changing the set of stocks with valid fees can otherwise masquerade as an incremental explanatory contribution.

## What the main estimates actually show

Table III, column 2, estimates a DOUT coefficient of **−2.983 percentage points per month**, with an absolute $t$-statistic of 3.96. The corresponding DIN, SIN, and SOUT coefficients are +0.299, −0.063, and −0.820 percentage points, with absolute $t$-statistics of 0.59, 0.08, and 1.23. The robust result is the negative DOUT coefficient, not a symmetric four-quadrant return pattern.

There is a source inconsistency worth preserving rather than concealing: nearby prose gives different numerical descriptions for some of the other shift coefficients. The figures above are taken directly from the displayed Table III specification. They should not be combined with coefficients from prose as if they came from a single regression.

The DOUT-only version gives −3.144 percentage points, with $|t|=3.20$. Adding borrowing-fee information reduces the estimate but leaves it economically substantial. In column 7, DOUT is −2.364, with $|t|=3.27$. The indicator for an annual fee above 5% is −1.596, with $|t|=1.63$, compared with approximately −2.025 and $|t|=2.09$ when the shift variables are absent. Loan quantity in levels does not provide comparable explanatory power.

Continuous changes also illustrate why the joint-sign construction matters. In column 8, the coefficients on the fee change and quantity change are −0.920 and −0.907, with absolute $t$-statistics of 1.95 and 2.45. When the shift indicators are added in column 9, DOUT is −2.485 with $|t|=3.19$, while the quantity-change coefficient falls to −0.343 with $|t|=0.77$. The fee-change coefficient remains negative, −0.912, but has $|t|=1.76$. Thus, simply using a change in short quantity loses information about the market movement that produced it.

Several alternatives reported in the text support the direction of the finding. Using raw shares on loan rather than scaling by shares outstanding gives approximately −2.23% with $|t|=2.52$. Expanding to all stocks gives about −1.53% with $|t|=2.69$. Those checks are useful evidence of robustness, but the paper does not provide the same complete tables for every alternative.

At a weekly horizon, a DOUT event predicts about −0.56% in the following week, with $|t|=2.24$. Coefficients across the first four separate weekly lags total approximately −1.68%. In monthly distributed-lag results, the first two lags are significant and all six reported coefficients are negative. These lag coefficients describe a regression pattern; summing them is not automatically equivalent to the realized return of a continuously rebalanced six-month strategy. Daily estimates are weaker.

## Magnitude, borrowing costs, and the interpretation of interactions

Table IV asks whether particularly large joint changes predict larger losses. An interaction for observations where both the fee increase and quantity increase exceed their respective 90th percentiles is −4.480 percentage points, with $|t|=2.32$. In that specification the ordinary DOUT coefficient is −2.458. The conditional DOUT contrast for the extreme group is therefore approximately −6.938 percentage points, before considering other included terms. The interaction is an incremental effect, not the entire predicted return.

The individual extreme-change indicators are not similarly decisive. An extreme outward-supply combination has an interaction of +2.633 with $|t|=1.32$, which is not strong evidence of a positive return effect. The evidence is concentrated in joint adverse-demand movements.

When DOUT is interacted with a fee above 3% annually, the interaction is −4.144 with $|t|=2.69$, alongside a base DOUT coefficient of −0.769. The DOUT contrast within the expensive-borrowing group is consequently about −4.913 percentage points. A prediction relative to a completely different baseline stock would additionally include the fee-level indicator and other controls. By comparison, the corresponding expensive-borrowing interaction for SIN is −1.691 with $|t|=0.93$. High borrowing costs alone do not identify the same return pattern as an outward demand movement at high costs.

These interactions fit an informed-demand explanation, but neither the classification nor the regression reveals the content of traders' private information. The result remains a conditional return association in a selected lending sample.

## Portfolio construction and the importance of weighting

At each month-end, the authors form portfolios from the observed shift classifications and hold them during the next month. Table V reports equal-weighted and value-weighted results, excess returns, and characteristic-adjusted returns. In addition to the 25 size/book-to-market benchmarks, the paper uses 75 portfolios formed from three size groups, five book-to-market groups, and five momentum groups. The relevant lagged-price restriction applies to the benchmark construction as well.

The equal-weighted monthly excess returns are approximately +1.65% for DIN, −1.82% for DOUT, +0.84% for SIN, and −1.12% for SOUT. The DIN-minus-DOUT spread is **3.48% monthly**, with $t=2.34. The SIN-minus-SOUT spread is 1.96%, with $t=1.55.

Characteristic adjustment leaves a substantial equal-weighted demand spread. With 25 benchmarks, DOUT is −2.34% with $t=-2.52$, DIN is +0.84%, and the spread is 3.18% with $t=2.17$. With 75 benchmarks, DOUT is −2.11% with $t=-2.15$, DIN is +0.76%, and the spread is 2.87% with $t=2.21$. A four-factor DOUT alpha reported in the text is approximately −2.41% with $t=-2.48$.

Value weighting materially changes the conclusion about the long–short strategy. The excess-return DIN-minus-DOUT spread falls to 1.06% with $t=0.65$. The 25- and 75-benchmark-adjusted spreads are 0.93% and 0.61%, with $t=0.56$ and $t=0.41$. Value-weighted DOUT abnormal returns themselves are about −1.05% and −0.88%, neither statistically compelling. Some value-weighted SOUT portfolio returns are significantly negative, but that observation does not recreate a robust four-quadrant pattern in the pooled regressions.

A replication should therefore report both weighting schemes and the monthly number of constituents, rather than presenting the strongest equal-weighted spread as a broad-capacity strategy. The paper also discusses stronger value-weighted results at a two-month horizon without supplying all the same numerical detail. That statement cannot substitute for a fully specified independent two-month backtest.

## Checks on lender coverage and alternative explanations

Table VI adds 48 industry indicators and obtains a DOUT coefficient of −3.030% with $|t|=4.05$. The result is therefore not simply a between-industry comparison during the technology downturn.

The authors next examine the lender's share of total short interest. The interaction with a continuous market-share measure is negative but imprecise. An indicator that the lender supplies more than two-thirds of total short interest produces an interaction of −8.361 with $|t|=2.38$ in the displayed table. The base DOUT coefficient in that specification is −2.741, implying an especially large conditional contrast in a small and selected high-coverage group. The adjacent discussion gives a different $t$-statistic; the table value is used here. This is suggestive evidence that more representative lender observations are more informative, not a stable estimate of a scalable −11% monthly strategy.

A separate construction substitutes aggregate market short interest for the institution's own loan quantity. Short-interest reporting dates and settlement timing matter: the measure corresponds to the fifteenth of the month, or the preceding trading day, and the paper accounts for the three-day settlement interval when selecting the lender's fee observation. The associated return window runs from the close on the sixteenth to the next month's sixteenth. This test, covering November 1999 through September 2003, produces a DOUT coefficient of about −1.262% with $|t|=2.06$. A public-data implementation would still have to respect the actual release delay of exchange short-interest information; the measurement date is not automatically the public availability date.

Lowering the price cutoff to \$1 expands the universe to about 3,760 stocks and the average DOUT portfolio to 38 stocks. The text reports a coefficient near −2.23% with $|t|=2.85$. Newly initiated borrowing is studied separately: 205 events involving expensive loans and substantial lender ownership yield a negative but statistically insignificant estimate near −1.95%. The baseline finding should not be generalized to all transitions from no borrowing to positive borrowing.

Table VII investigates information-related explanations. Residual analyst coverage is constructed from a monthly cross-sectional regression of $\log(1+\text{analyst count})$ on log size. Its interaction with DOUT is only +0.052 with $t=0.24$. This shows little measured variation in the DOUT effect with that coverage proxy; it does **not** establish that the effect is significantly stronger among low-coverage stocks. The dividend-month interaction is positive but imprecise, consistent with the possibility that some dividend-related borrowing has tax rather than information motives. Insignificance is not proof that the conditional effect is exactly zero. Restrictions excluding earnings announcements or forecast revisions reportedly leave the central result intact.

## Trading costs and limits to arbitrage

The paper explicitly attempts to reconcile a large gross spread with limited exploitation. The DIN-minus-DOUT strategy turns over about 90% of its long side and 87% of its short side each month. Estimated trading costs are taken from institutional trading evidence in Keim and Madhavan, using small-stock and order-size categories; these are not contemporaneous realized transaction records for the proposed strategy.

For the long leg, the illustrative monthly round-trip turnover calculation is

$$
2(0.90)\left[0.72(0.88\%)+0.28(0.63\%)\right]
\approx1.46\%.
$$

The corresponding short-leg estimate is about 1.44%, giving roughly 2.90% per month in combined trading costs. The source market and execution conditions behind these estimates differ from the strategy's 1999–2003 sample. They are useful scale estimates, not an executed cost-inclusive backtest.

The authors first annualize the gross monthly 3.48% spread, producing approximately 50.8%, subtract the 3.72% annual borrowing fee, and convert the result back to a monthly figure near 3.27%. Subtracting 2.90% monthly transaction costs then leaves about 0.37% monthly, or 4.5% annually. This is the paper's approximate arithmetic. It mixes annual compounding, a representative annual fee, and monthly turnover costs; it should not be read as a precise realized net return.

For perspective, a different simple approximation that subtracts $3.72\%/12$ directly from the monthly gross spread leaves about $3.48\%-0.31\%-2.90\%=0.27\%$ per month. This is an explanatory sensitivity calculation, **not** a replacement performance estimate. Correct net performance requires the actual time path of borrow fees, holdings, trading, collateral, and financing. Both approximations show that small implementation differences can absorb much of the remaining return.

The reported monthly Sharpe ratio of 0.338 is before transaction costs. The paper compares it with market and HML ratios calculated over 1990–2003, rather than over the strategy's identical 1999–2003 window. This is not a matched-sample performance comparison. Capital requirements for a two-leg portfolio, margin, search for lendable shares, and loan recall risk further prevent interpreting the long–short spread as a fully financed investor return.

Table VIII uses size, idiosyncratic volatility, and turnover as proxies for arbitrage difficulty. Idiosyncratic risk is the standard deviation of residuals from a trailing one-year daily regression on contemporaneous and lagged CRSP value-weighted market returns. The smallest-stock interaction is −3.903 with $|t|=2.38$. The high-idiosyncratic-risk interaction is negative but insignificant, and the high-turnover interaction is essentially zero. These tests do not observe loan recalls directly and cannot rule out rare short-side tail losses merely because a proxy interaction is insignificant.

## A reproducible implementation and its remaining gaps

A reconstruction should begin with a point-in-time contract panel, not an exchange short-interest series alone. Aggregate contracts into the largest-contract fee and total lender quantity, join contemporaneous shares outstanding, and document corporate-action adjustments. Apply the lagged size and price filters, then compare consecutive month-end observations only where both endpoints support a valid classification. Keep an explicit category for unchanged observations and an explicit exclusion reason for one-variable-only changes or missing prices.

Next, construct the lagged return, institutional ownership, and six-month turnover controls; assign characteristic benchmarks without using future data; and fit the stated calendar-effect regressions with month-clustered inference. Reproduce Table III before adding interactions. Report coefficients in monthly percentage points, and keep annual borrowing-fee units separate. Build the month-end equal- and value-weighted portfolios from the same eligible observations, saving membership, weights, turnover, and counts for every month. Only then layer in actual fees, trading-cost assumptions, and alternative holding periods.

The supplied article does not release the confidential contract panel or executable code. It does not provide every data-cleaning decision needed for an exact reproduction, including complete treatment of missing loan quotes, contract amendments, intraday observations, corporate actions, and all implementation details of the alternative horizons. The lender's identity and universe coverage also limit external reproducibility. These gaps should be recorded as missing inputs, rather than filled with undocumented convenient assumptions.

The durable research lesson is that a quantity signal can combine economically different forces. Observing the price of borrowing helps separate them, and the separation is informative about returns in this sample. The practical lesson is more conditional: the strongest effect lies in a small, expensive-to-trade part of the market, and the evidence for broad value-weighted or net-of-cost profitability is much weaker than the headline equal-weighted spread.
