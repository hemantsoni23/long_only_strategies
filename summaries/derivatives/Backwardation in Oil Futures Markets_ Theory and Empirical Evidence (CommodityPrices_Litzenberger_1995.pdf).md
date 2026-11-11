# Backwardation in Oil Futures Markets: Theory and Empirical Evidence

**Robert H. Litzenberger and Nir Rabinowitz, 1995.** *Journal of Finance* 50(5), 1517–1545. [Source PDF](../../Finance/CommodityPrices_Litzenberger_1995.pdf). The 30-page file contains a JSTOR cover and the complete 29-page article, including six tables, three figures, the mathematical appendix, and references. All pages were read; equations, tables, figures, and appendix arguments were checked against rendered pages. Printed page 1517 is PDF page 2.

## Why this matters

Oil in the ground is an option to produce, not merely a physical commodity waiting to be sold at a predetermined date. Producing today destroys the right to avoid extraction when the future selling price is too low. Litzenberger and Rabinowitz show that this option value can make spot oil more valuable than discounted future delivery even when extraction costs grow at the interest rate. Their two-period equilibrium converts that argument into an exact identity: weak backwardation equals the value of a put struck at the future extraction cost of the current marginal producer.

The distinction between weak and strong backwardation is essential. Weak backwardation means $S_0>e^{-rT}F_{0,T}$; strong backwardation means $S_0>F_{0,T}$. The first compares present values, while the second compares undiscounted quoted prices. A positive option value is enough to generate a nonnegative weak gap under the model. Strong backwardation requires the option value to exceed the financing difference between futures and discounted futures. Neither condition alone is a statement about expected excess returns to a rolling futures strategy.

The contribution is to endogenize an option-related source of backwardation through extraction decisions. It complements storage-service or convenience-yield arguments and capacity constraints rather than empirically excluding them. The authors also establish production comparative statics and a multiperiod lower bound. Their empirical evidence links US extraction rates negatively to implied volatility and calendar-spread backwardation positively to option prices and implied volatility. These are reduced-form associations, not a structural estimation of marginal extraction costs or a backtest of tradable alpha.

The benchmark is Hotelling's certainty condition,

$$
S_t-x_t=(S_0-x_0)e^{rt},
$$

where $x_t$ is unit extraction cost. If costs grow at $r$, the discounted price is constant in the certainty benchmark. Slower cost growth can itself produce weak backwardation, while strong backwardation under certainty requires a sufficiently rapid decline in costs. The paper deliberately sets cost growth equal to the interest rate to isolate the value of retaining the extraction option.

## Two-period economy and producer choice

Total reserves are $Q=Q_0+Q_1$. Reserves $Q_0$ can be extracted at date 0 or date 1; $Q_1>0$ become available only at date 1. A continuum of price-taking producers owns equal reserve shares and has heterogeneous date-1 unit extraction costs $x$, uniformly distributed on $[0,\bar x]$. Date-0 costs are $e^{-r}x$. The positive $Q_1$ avoids a terminal zero-supply ambiguity when demand is low, and can be arbitrarily small.

Demand is linear at each date:

$$
D_0=a-bS_0,\qquad D_1=a+\varepsilon-bS_1,
\qquad a,b>0,\quad E[\varepsilon]=0.
$$

The maintained parameter restriction is $a/b>\bar x$. Demand has no temporal substitution in the displayed model. The authors say imperfect rather than zero substitution is the economically relevant restriction, but do not solve the more general system. Physical storage above ground is absent from the equilibrium; the ability to leave reserves unextracted provides the relevant intertemporal choice. Investment in new reserves, depletion-dependent costs, shutdown losses, capacity adjustment, and strategic producer behavior are omitted.

Let $C_x$ and $P_x$ be date-0 call and put values on date-1 oil, struck at $x$. The producer compares immediate extraction value $S_0-e^{-r}x$ with the value of waiting, $C_x$. It extracts if the former is greater, waits if it is smaller, and is indifferent at equality. For a marginal cost threshold $x^*$, current output is

$$
q_0=Q_0\frac{x^*}{\bar x},\qquad 0\le x^*\le\bar x.
$$

At an interior equilibrium,

$$
S_0-e^{-r}x^*=C_{x^*}.
$$

A reserve has terminal payoff $(S_1-x)^+$ because extraction at date 1 occurs only when it is profitable. This option interpretation differs from a mandatory-delivery forward: the reserve owner can decline to incur the extraction cost. The model assumes a continuum of traded options so that this value can be compared with market claims. The appendix's uniqueness and comparative-statics calculations additionally assume risk neutrality to specify option prices from the demand-shock distribution. That assumption is explicitly stated in footnote 18 and should not disappear when reconstructing the equilibrium.

Holding the future price distribution fixed, the difference between extracting and waiting has derivative $-e^{-r}-\partial C_x/\partial x\le0$. Hence lower-cost producers are at least as willing to extract. The source's main text calls the difference strictly decreasing; its appendix correctly states a weak inequality for the fixed-price-distribution problem. Strict monotonicity of the equilibrium root function is a different result because changing the threshold also changes current output and future price distributions.

## Backwardation identity and its interpretation

With deterministic interest rates, futures and forwards coincide for this purpose. Put-call parity is

$$
C_{x^*}=e^{-r}(F_{0,1}-x^*)+P_{x^*}.
$$

Substituting the marginal extraction condition cancels the discounted extraction cost:

$$
S_0-e^{-r}F_{0,1}=P_{x^*}.
$$

This is the central result. The producer must receive enough value from selling now to compensate for surrendering the downside protection associated with waiting. The theorem defines nonnegative backwardation magnitudes using positive parts:

$$
B_w=[S_0-e^{-r}F_{0,1}]^+=[P_{x^*}]^+,
$$

$$
B_s=[S_0-F_{0,1}]^+
=[P_{x^*}-(1-e^{-r})F_{0,1}]^+.
$$

The empirical tables instead use signed spreads and therefore include negative observations. A replication must not truncate those observed spreads merely because the theoretical definition contains a positive part.

The weak gap is strictly positive when the put has positive value, which requires an appropriately priced downside event below the strike. Under a degenerate demand shock with no put value, the certainty benchmark gives equality, $S_0=e^{-r}F_{0,1}$. Thus “always weakly backwardated” should retain this limiting equality qualification. Higher uncertainty does not mechanically produce strong backwardation at every parameter configuration; the put must be sufficiently valuable relative to the interest adjustment.

When extraction costs grow at rate $g$ rather than $r$, date-0 cost becomes $e^{-g}x^*$ and the identity is

$$
S_0-e^{-r}F_{0,1}
=P_{x^*}+(e^{-g}-e^{-r})x^*.
$$

The strong gap subtracts $(1-e^{-r})F_{0,1}$ from the same right side. Slow cost growth can reinforce the option effect; cost growth above the interest rate offsets it. Consequently an observed calendar spread cannot identify option value without information about extraction-cost dynamics.

The no-above-ground-storage corollary applies within this model: when discounted future proceeds are below spot, buying oil now solely to sell later is unattractive even before physical storage costs. It does not deny that actual refiners and transportation networks carry operational inventories or receive services from physical stocks. The authors explicitly view those services as complementary and discuss oil in pipelines, tankers, and refinery sites. They also recognize that some wells require minimum production to preserve recoverable reserves. Such a shutdown constraint can support current extraction in periods of contango, outside the frictionless stopping model.

## Constructing and solving the equilibrium

The appendix supplies more than a verbal option analogy. For a candidate threshold $x$, current price is $S_0(x)=(a-Q_0x/\bar x)/b$. Remaining date-1 supply includes the newly available reserves and the portion of initial reserves not yet extracted. For a terminal price $s$ between zero and $\bar x$, it is

$$
q_1(s;x)=\frac{Q_1}{\bar x}s+
\frac{Q_0}{\bar x}(s-x)^+.
$$

At $s\ge\bar x$, supply is capped at $Q-Q_0x/\bar x$. This produces the piecewise linear supply curve in Figure 3. The change in slope at $x$ matters: the future price is not a globally affine function of the demand shock.

Define two shock thresholds,

$$
k_1(x)=bx-a+Q_1\frac{x}{\bar x},
\qquad
k_2(x)=b\bar x-a+Q-Q_0\frac{x}{\bar x}.
$$

They correspond to terminal price reaching the candidate extraction threshold and the maximum extraction cost. The appendix decomposes the marginal producer's terminal payoff as

$$
(S_1-x)^+=\frac{\bar x}{b\bar x+Q}(\varepsilon-k_1)^+
+\frac{Q}{b(b\bar x+Q)}(\varepsilon-k_2)^+.
$$

Under risk neutrality, write $c(k)=e^{-r}E[(\varepsilon-k)^+]$. The call value is the same positive linear combination of $c(k_1)$ and $c(k_2)$. This decomposition makes numerical solution straightforward for a specified shock law, including a discrete distribution. No lognormal assumption is needed for this theoretical result; the Black model enters later when the authors convert observed option prices into implied volatilities.

The root function is

$$
H(x)=\frac{a-Q_0x/\bar x}{b}-e^{-r}x
-\frac{\bar x}{b\bar x+Q}c(k_1(x))
-\frac{Q}{b(b\bar x+Q)}c(k_2(x)).
$$

The appendix uses $-e^{-r}\le c'(k)\le0$ to establish that $H$ is strictly decreasing. Atoms in the shock distribution can be handled through monotonicity and one-sided derivatives. If $H(0)\le0$, the equilibrium has no current production; if $H(\bar x)\ge0$, all $Q_0$ is extracted; if $H(0)>0>H(\bar x)$, there is a unique interior threshold. Bisection is sufficient once expected positive parts can be evaluated. These endpoint conditions are the cleanest reproducible existence test.

The appendix also offers simple sufficient restrictions for interiority. There is a visible problem with its variance version: equation (39) prints $\operatorname{Var}(\varepsilon)<Q$, whereas the displayed final lower bound in equation (48) is proportional to $Q-\sqrt{E[\varepsilon^2]}$. With zero mean, positivity of that bound requires standard deviation below $Q$, equivalently variance below $Q^2$. The printed statement and proof therefore do not align without an unstated normalization. Some strict inequalities in the sufficiency proof also need care at boundary cases. A numerical implementation should test $H$ directly rather than rely on that printed sufficient condition.

This is an equilibrium model, not a single option-pricing formula applied to an exogenous oil price. Changing $x$ changes both today's supply and tomorrow's available reserves. Estimating a Black volatility and inserting it into a fixed-price call while holding all production unchanged would miss the feedback the appendix is designed to capture. The paper does not calibrate the distribution of extraction costs, $Q_0,Q_1$, demand elasticity, or the shock law to its empirical sample.

## Risk comparative statics and the multiperiod result

Theorem 2 compares demand shocks in convex order. If $\varepsilon_2$ equals $\varepsilon_1+\xi$ in distribution with $E[\xi\mid\varepsilon_1]=0$, each convex positive-part expectation increases weakly. Therefore $H(x)$ decreases weakly at every fixed threshold. Because $H$ is decreasing in $x$, its zero shifts left, so current output $Q_0x^*/\bar x$ cannot increase. The argument accounts for endogenous price changes and applies to boundary equilibria as well. It is more specific than saying that volatility and production must be negatively correlated in any observed sample.

Theorem 3 imposes an extra restriction for backwardation. The mean-preserving spread must occur inside the region where terminal price lies between the old marginal cost and $\bar x$, with shocks outside that region unchanged. In that region both relevant supply and demand pieces are linear. Holding the old production rule fixed, the spread preserves expected terminal price; allowing production to adjust leaves more oil for date 1, reducing its expected price, while lower current output raises current spot. Both weak and strong backwardation then increase weakly.

This support restriction is material. An arbitrary variance increase can move probability across the supply-curve kinks, so the simple expected-price argument no longer follows. The unrestricted production theorem and the restricted backwardation theorem should not be combined into a universal claim about any increase in measured implied volatility. Furthermore, a mean-preserving spread implies higher variance when variance exists, but higher variance alone does not establish a mean-preserving spread.

For $T$ periods, a reserve is an American option to extract at any date with strike schedule $x_t=e^{-r(T-t)}x_T$. Let $A_0$ be the option value for the date-0 marginal producer. Indifference gives $S_0-x_0^*=A_0$. For any $t\le T$, the American option is worth at least the European call exercisable at $t$ with strike $x_t^*$. Since $x_0^*=e^{-rt}x_t^*$, parity implies

$$
S_0-e^{-rt}F_{0,t}\ge P_{0,t}(x_t^*),
$$

and therefore

$$
[S_0-F_{0,t}]^+\ge
[P_{0,t}(x_t^*)-(1-e^{-rt})F_{0,t}]^+.
$$

The two-period equality becomes a lower bound because waiting retains more exercise opportunities. Deterministic interest rates are needed for the source's equivalence of forwards and futures; the paper explicitly notes the distinction under stochastic rates. The empirical section's sentence saying the American extraction option is “decreasing” in volatility conflicts with its surrounding argument and appears to be a sign error: the intended option-value effect is nondecreasing, yielding nonincreasing extraction.

## Data and observed backwardation

Table I uses daily NYMEX WTI futures observations from February 1984 through April 1992. The nearest contract proxies for spot, and contracts two through nine provide later prices. LIBOR rates of corresponding maturities supply the discount factors. The first nearby ranges from roughly one to thirty-one days to expiry; higher nearby contracts add calendar months. This is a nearby-contract construction, not a constant-maturity interpolation, and the spot proxy retains delivery timing and contract-specific basis effects.

For the second through ninth nearby contracts, mean weak backwardation in dollars per barrel is 0.29, 0.49, 0.64, 0.76, 0.87, 0.96, 1.04, and 1.11. Mean strong backwardation is 0.24, 0.43, 0.58, 0.70, 0.81, 0.90, 0.98, and 1.05. Weak-backwardation frequencies increase from 81.80% to 93.88%; strong-backwardation frequencies increase from 71.09% to 76.91%. These are frequencies of positive signed gaps, not risk-premium estimates.

The ninth-nearby weak spread has median 0.71, standard deviation 1.82, minimum −3.76, and maximum 10.80. Its strong counterpart has median 0.65, standard deviation 1.82, minimum −3.82, and maximum 10.70. Figure 1 shows the large Gulf War price and backwardation spike, but also earlier backwardated periods and episodes of negative spreads. Persistent backwardation motivates the theory; its occurrence alone does not identify the extraction-option mechanism.

Monthly production and reserve data come from the US Energy Information Administration. Daily futures and options prices come from DRI McGraw Hill. Production analysis is restricted to nonregulated US states, where producers can vary output with market conditions. The article does not enumerate the state list, reserve interpolation or revision rules, exact quote-time alignment, or a complete data-cleaning protocol. Those choices are necessary for an exact historical reproduction.

## Production-rate regressions

The dependent variable is the change in production as a fraction of reserves. The explanatory variable is the lagged change in the monthly average implied volatility from near-the-money futures calls on the second, third, or fourth nearby contract. Both production rate and volatility are expressed in annual percentage terms. The estimated equation is

$$
\Delta q_t=\alpha_\tau+\beta_\tau\Delta\bar\sigma_{\tau,t-1}+u_{\tau,t}.
$$

The use of lagged volatility prevents direct use of same-month option information in that equation, but does not establish causality or a forecasting strategy. Black's 1976 formula supplies the implied volatility. The fourth nearby is the longest examined because longer options were not actively traded in the sample.

Table II covers December 1986–December 1991, with 60 usable observations. For nearby contracts two, three, and four, volatility slopes are −0.002, −0.003, and −0.004; corresponding $t$ statistics are −1.190, −1.543, and −2.069, and reported $p$ values are 0.119, 0.064, and 0.021. These $p$ values are one-sided. The negative sign is uniform, but significance is not equally strong across maturities. Intercepts are approximately −0.024 to −0.025.

Excluding August 1990–February 1991 leaves 53 observations. Slopes become −0.007, −0.008, and −0.009 with $t$ statistics −2.351, −2.318, and −2.267 and one-sided $p$ values 0.011, 0.012, and 0.014. The prose says significance at 1%; the table does not support that literal threshold. The war exclusion increases absolute slope estimates because both US output and volatility rose during the war. This is an informative robustness check, but also demonstrates the sensitivity of a short time series to one historical episode.

Table III adds lagged changes in the monthly average first-nearby price. Full-sample volatility slopes are −0.002, −0.004, and −0.006, with one-sided $p$ values 0.069, 0.029, and 0.007. Price slopes are 0.010, 0.012, and 0.013, with $p$ values 0.080, 0.058, and 0.034. Thus the prose description of uniformly insignificant price coefficients is too broad under its own one-sided convention. Excluding the war gives volatility slopes −0.007, −0.007, and −0.008, with $p$ values 0.032, 0.034, and 0.037; price slopes are small and insignificant. The article does not provide a documented HAC specification or a structural instrument for volatility in these production equations.

## Option-price and volatility regressions for the curve

The marginal producer's extraction cost is unobservable, so the theoretical put cannot be directly priced from an observed strike. The authors substitute an at-the-money-futures put. They first infer Black volatility from the closest available strike, then reconstruct a hypothetical put with strike exactly equal to the futures price. For maturity $T$ and annual decimal volatility $\sigma$, that normalized Black price is

$$
P_{ATM}=e^{-rT}F\left[2\Phi\left(\frac{\sigma\sqrt T}{2}\right)-1\right].
$$

This formula is an implementation reconstruction from the method, not an additional model assumption about equilibrium demand shocks. It clarifies that the put-price regressor depends jointly on volatility, futures level, maturity, and rates. The option-implied volatility and put-price regressions are consequently related tests, not independent pieces of evidence.

The daily equation is $B_{\tau,t}=\alpha_\tau+\beta_\tau P_{ATM,\tau,t}+u_{\tau,t}$, using signed weak backwardation. Cochrane–Orcutt estimation corrects an AR(1) error process. Table IV labels the sample December 1986–April 1992, 1,222 observations, despite one sentence in the text ending it in December 1991. Excluding the Gulf War leaves 1,083 observations. The table's date and count should anchor a reproduction, with the prose inconsistency recorded.

| Regression and sample | Nearby 2 | Nearby 3 | Nearby 4 |
|---|---:|---:|---:|
| Put slope, full | 0.139 | 0.450 | 0.633 |
| Put slope $t$, full | 5.645 | 13.209 | 15.129 |
| Put slope, excluding war | 0.356 | 0.359 | 0.407 |
| Put slope $t$, excluding war | 5.965 | 4.975 | 4.433 |
| Volatility slope, full | 0.006 | 0.019 | 0.021 |
| Volatility slope $t$, full | 5.132 | 9.517 | 8.027 |
| Volatility slope, excluding war | 0.011 | 0.009 | 0.004 |
| Volatility slope $t$, excluding war | 5.952 | 3.766 | 1.703 |

Volatility regressors are annual percentage points, so their coefficients measure dollars of spread per one percentage-point change in volatility. Full-sample put-regression AR(1) estimates are 0.652, 0.733, and 0.780; excluding war they are 0.766, 0.799, and 0.805. Volatility-regression counterparts are 0.652, 0.743, and 0.810 in the full sample and 0.771, 0.863, and 0.870 after exclusion. These high values make serial-dependence assumptions consequential for inference.

The full-sample put-regression intercepts are 0.147, 0.018, and −0.049. The first has $t=4.339$, contradicting a literal reading of the text's statement that intercepts are insignificantly different from zero. In the war-excluded sample all three intercepts are insignificant. The fourth-nearby volatility slope after exclusion has one-sided $p=0.044$, corresponding to approximately 0.088 two-sided, so it is weaker evidence than the other entries.

An ATM put is generally more valuable than a put struck at a lower marginal extraction cost. A slope below one against the ATM proxy is therefore compatible with the model, but is not a direct test of the exact identity or lower bound. In particular, a pointwise lower bound on the correct-strike put does not imply a simple universal OLS restriction on intercept and slope when the bound's slack varies with the regressor. The paper's regression interpretation should be treated as qualitative consistency, not full structural identification.

Table VI adds contemporaneous spot proxy $S_t$. Full-sample volatility coefficients are 0.004, 0.011, and 0.014, with $t$ statistics 3.672, 7.251, and 7.235. Price coefficients are 0.038, 0.087, and 0.137, all strongly significant. War-excluded volatility slopes are 0.013, 0.012, and 0.009, with $t$ statistics 7.702, 5.913, and 2.037; price slopes are 0.096, 0.182, and 0.248. The corresponding error autocorrelations reach 0.949. The authors note a mechanical measurement-error concern because the spot proxy appears both inside the dependent spread and on the right side. Price control preserves the volatility association but does not eliminate joint determination or measurement error.

## Replication limits and investment use

A theoretical reproduction needs an explicit demand-shock distribution, risk-neutral valuation convention, demand parameters, cost distribution, reserves available at each date, and interest rate. The appendix gives a practical root problem and option decomposition, but the article does not provide a numerical calibration to WTI. A multiperiod implementation additionally needs a stochastic state process and an exercise algorithm; the paper proves a bound rather than estimating that full dynamic equilibrium.

An empirical reproduction needs the original option and futures panel, exact strikes and expiration dates, rate day-count conventions, nearby-roll dates, quote filters, treatment of American exercise features in applying Black's formula, state inclusion rules, reserve frequencies and revisions, and Cochrane–Orcutt implementation details. The paper provides enough to reconstruct the design and the displayed regressions, but not to guarantee exact coefficients from an arbitrary modern data vendor. Monthly production and reserve publication lags also matter for any attempted forecasting application.

The implied-volatility variable also mixes the market price of option risk with the physical uncertainty entering production decisions. The theoretical comparative static changes a zero-mean demand-shock distribution under a fixed valuation rule. Observed implied volatility can change because physical demand uncertainty changes, because the pricing of tail states changes, or because option supply and demand change. These alternatives are not separated by the regressions. An economic interpretation of the coefficient therefore requires more than its sign. For example, a one-percentage-point increase in annual implied volatility has a different meaning from a one-percent proportional increase in volatility, and neither is automatically a pure mean-preserving spread of demand.

No trading rule, holding period, portfolio leverage, turnover, slippage, transaction cost, financing return, or out-of-sample strategy evaluation is reported. The empirical exercise is explanatory and contemporaneous for backwardation, with a one-month lag in the production test. It cannot be converted into evidence that buying backwardated futures earns abnormal returns. The paper instead supplies an economic reason why a backwardated curve can coexist with rational extraction and valuable remaining reserves.

For research, its most useful discipline is to distinguish three objects: the reserve's exercise option, the observed futures-spot spread, and an investor's expected futures return. They are connected through equilibrium and pricing assumptions, but are not interchangeable. The exact option identity and multiperiod bound are stronger than the empirical identification; the data support the predicted signs over the studied sample while leaving extraction costs, alternative mechanisms, and deployable return forecasts unresolved.
