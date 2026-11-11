# A Practical Guide to Volatility Forecasting through Calm and Storm

**Authors:** Christian Brownlees, Rob Engle, and Bryan Kelly. **Version:** the 21-page working paper stored under the 2010 filename; the supplied title page does not print a manuscript date. **Source:** [Volatility_BrownleesEngleKelly_2010.pdf](../../Finance/Volatility_BrownleesEngleKelly_2010.pdf). Page references below are PDF pages, which match printed pagination. The separately referenced online appendix is not bundled with this source; its unreported details cannot be reconstructed from these pages.

## Why this matters and what is new

The paper asks how to operate a volatility forecast, rather than simply which ARCH acronym wins a comparison. It jointly varies model, estimation history, frequency of parameter updating, forecast horizon, innovation likelihood, asset class, and market regime. Its central empirical recommendation is modest: asymmetric GARCH, especially the threshold specification, estimated using a long history and refreshed at least weekly, is a competitive daily-return benchmark. More elaborate models or heavier-tailed likelihoods do not systematically improve variance forecasts in these tests.

The second contribution separates two different meanings of failure during 2008. A model can forecast tomorrow's variance reasonably after observing today's shock while failing to anticipate a persistent sequence of shocks several weeks earlier. The evidence supports the first capability and documents deterioration in the second. This does not imply that the crisis itself was predicted, that asset losses were small, or that positions sized from one-day variance could be liquidated safely. The relevant operational lesson is that the horizon of risk measurement must match the horizon over which exposure can be changed.

The authors evaluate conditional variance, not expected returns, tail quantiles, market liquidity, or the distribution of liquidation costs. Their comparisons exclude stochastic-volatility models and models driven by high-frequency realized measures as forecasting inputs. Realized variance enters as an evaluation proxy. Thus the results establish a useful benchmark within a deliberately limited model class, not global optimality among all available volatility methods.

## Information sets, targets, and the five models

Let $r_t$ be the daily continuously compounded total return and $\mathcal F_t$ information through day $t$. The paper suppresses the conditional mean:

$$
r_{t+1}=\sqrt{h_{t+1}}\epsilon_{t+1},\qquad
E(\epsilon_{t+1})=0,\qquad E(\epsilon_{t+1}^2)=1.
$$

Innovations are independent and identically distributed under each maintained model. The $i$-step target is $\operatorname{Var}(r_{t+i}\mid\mathcal F_t)$, written $h_{t+i\mid t}$ for a forecast. It is the variance on the future day at horizon $i$, rather than the variance of the cumulative return over all $i$ days. Forecast horizons are 1, 5, 10, 15, and 22 trading days. On every forecast origin the researcher produces a new path at those horizons, so forecast paths overlap.

The baseline GARCH(1,1) recursion is

$$
h_{t+1}=\omega+\alpha r_t^2+\beta h_t.
$$

The source imposes $\alpha+\beta<1$ for mean reversion. Standard nonnegative-variance implementation also requires admissible intercept and response parameters. The article does not list its optimizer's full constraints, initial variance, or treatment of failed fits. For fixed parameters, the unconditional variance is $\bar h=\omega/(1-\alpha-\beta)$ and the exact iterated forecast is

$$
h_{t+i\mid t}=\bar h+(\alpha+\beta)^{i-1}(h_{t+1}-\bar h).
$$

This last equation is an explanatory derivation from the reported model, not an additional empirical result. It makes the horizon interpretation unambiguous and supplies a direct implementation check.

The threshold model, called TARCH here, is the GJR-type variance specification

$$
h_{t+1}=\omega+\bigl(\alpha+\gamma\mathbf 1\{r_t<c\}\bigr)r_t^2+\beta h_t.
$$

A positive $\gamma$ increases the response to sufficiently negative returns. The source introduces threshold $c$ but does not explicitly report its fitted or fixed value. Using the conventional $c=0$ is a reasonable replication specification only if labeled as a choice requiring confirmation. Under that choice and a symmetric standardized innovation distribution, the expected variance persistence is $\alpha+\beta+\gamma/2$, not $\alpha+\beta+\gamma$. Its long-run variance and multi-step forecasts then follow the GARCH formula with that persistence. An asymmetric innovation law or nonzero threshold changes the relevant truncated second moment, so mechanically using one-half would be incorrect.

EGARCH evolves log variance:

$$
\log h_{t+1}=\omega+\alpha\bigl(|\epsilon_t|-E|\epsilon_t|\bigr)
+\gamma\epsilon_t+\beta\log h_t.
$$

Here leverage corresponds to $\gamma<0$. Conditional variance is positive automatically, but $\exp(E_t\log h_{t+i})$ is generally not $E_t h_{t+i}$. A multi-step implementation must integrate the nonlinear transformation or simulate the innovations and average variances. The paper does not provide the numerical integration or simulation settings used for this task. For Gaussian innovations $E|\epsilon|=\sqrt{2/\pi}$; the corresponding standardized Student distribution has a different absolute first moment.

The printed NGARCH equation on page 7 is

$$
h_{t+1}=\omega+\alpha(r_t+\gamma)^2+\beta h_t.
$$

The negative shift $\gamma$ amplifies the squared response to a negative return of given magnitude. This is the formula actually printed in this manuscript. It is not silently replaced here by a different common nonlinear-GARCH specification with a shift proportional to $\sqrt{h_t}$. In the printed form, $\gamma$ has return units and changing returns from decimals to percentages requires transforming it. Replication should confirm whether the omitted implementation uses this literal recursion or another parameterization.

Finally, APARCH is

$$
h_{t+1}^{\delta/2}=\omega+\alpha(|r_t|-\gamma r_t)^\delta+\beta h_t^{\delta/2}.
$$

The power $\delta$ is estimated rather than fixed at two; the asymmetric absolute-return term allows different shock effects by sign. Taking power $2/\delta$ converts the state to variance. As with EGARCH, nonlinear aggregation matters for forecasts: a forecast of the power state transformed afterward need not equal a variance forecast. Parameter restrictions must keep the power base and variance well defined. The paper's main PDF does not supply the complete set of numerical bounds or the model-by-model multi-step forecasting routine.

## Estimation and the real-time experiment

For each forecast origin $t$, estimate each candidate using information ending at or before $t$. The baseline is an expanding history beginning in 1990, Gaussian likelihood, and weekly parameter re-estimation. The updated state still assimilates each new return between parameter fits. A weekly fitting schedule does not mean that yesterday's realized shock is ignored until the next fitting date. The exact weekday and holiday adjustment convention are not reported.

For a zero-mean Gaussian model, the relevant negative log likelihood, omitting constants, is

$$
\frac12\sum_{s\in\mathcal W_t}\left(\log h_s(\theta)+\frac{r_s^2}{h_s(\theta)}\right),
$$

where $\mathcal W_t$ is the estimation window and $\theta$ denotes the model's parameters. The competing likelihood uses standardized Student innovations, which must have unit variance if $h_s$ is to retain its interpretation. Degrees of freedom, optimization starts, convergence tolerances, boundary handling, and numerical safeguards are not reported in the supplied paper.

The design perturbs three estimation choices: expanding history versus four-year and eight-year rolling histories; daily versus weekly versus monthly parameter updates; and Gaussian versus Student likelihood. These dimensions should be changed while keeping forecast origins, return units, and evaluation samples aligned. The article reports selected summaries of a larger comparison relegated to its external appendix. It is therefore inappropriate to infer a fully specified factorial design, exact significance-test implementation, or every pairwise outcome from the main tables alone.

The advantage of the expanding window is lower estimation noise. Its disadvantage under drift is that old observations can pull parameters away from current dynamics. Frequent re-estimation partially adapts the parameters while retaining the precision supplied by the long history. The empirical claim is that this compromise worked better on average in the examined samples; it is not a theorem that old data always help after a structural break.

## Data, preprocessing, and the evaluation proxy

The primary daily series is the S&P 500, split- and dividend-adjusted, from Datastream for 1990–2008. Forecast evaluation spans 2001–2008. The crisis subsample is September–December 2008. Exact first and last trading dates, day counts, and handling of market holidays are not tabulated in the source.

The wider comparison uses ten US-dollar exchange rates, nine US sector portfolios, and international equity ETFs. Table 1 starts currencies on January 5, 1999; sector SPDRs on December 23, 1998; and international iShares series on March 19, 1996. The currency list is Australian dollar, British pound, Canadian dollar, euro, Indian rupee, Hong Kong dollar, Japanese yen, South Korean won, Swiss franc, and Thai baht. The sectors are consumer discretionary, consumer staples, energy, financials, healthcare, industrials, materials, technology, and utilities.

The text says there are 18 international indices, but Table 1 names 17 entries: Singapore, Netherlands, Japan, Australia, Belgium, Canada, Germany, Hong Kong, Italy, Switzerland, Sweden, Spain, Mexico, UK, World, Emerging Markets, and BRIC. The main source does not resolve the missing eighteenth identifier or explain how differing actual product inception dates were handled in the claimed balanced panel. Exact tickers, any backfilled index histories, and currency quotation direction are necessary replication inputs. They should not be invented from present-day product lists.

For the S&P comparison, the high-frequency proxy comes from SPDR ETF midquotes in NYSE TAQ. The authors filter using cited Brownlees–Gallo and realized-kernel data-handling procedures, but do not reproduce those rules. They sample every $d_t$th midquote, choosing $d_t$ so the average duration is five minutes. This is tick-time sampling with a daily adjusted tick increment, rather than a fixed calendar-time five-minute grid. If sampled log midquotes are $p_{t,1},\ldots,p_{t,I_t}$, the proxy is

$$
RV_t=\sum_{i=2}^{I_t}(p_{t,i}-p_{t,i-1})^2.
$$

The overnight return is omitted. The paper calls this realized volatility, although the sum is in variance units. Square roots and annualization are applied for the volatility figure; loss comparisons require forecast and proxy in the same variance units. An exact annualization constant is not stated in the main text.

Two limitations follow directly from this construction. The forecast uses an index total return while the proxy uses ETF intraday midquotes, so they are not literally identical measurement objects. In addition, excluding overnight variation makes the raw proxy an imperfect match for full-day return variance. These issues matter because the robustness argument below requires an appropriate conditionally unbiased proxy. The article does not report a full-day scaling adjustment or an overnight component in its proxy formula.

## Robust losses, normalization, and uncertainty

The two principal variance losses are mean squared error and quasi-likelihood loss. A convenient zero-minimum normalization of the latter is

$$
L_{QL}(v,h)=\frac vh-\log\left(\frac vh\right)-1,
\qquad L_{MSE}(v,h)=(v-h)^2.
$$

There is a source inconsistency worth preserving explicitly: page 8 prints the QL expression without the final $-1$, but Table 2 reports realized-variance losses as small as 0.234. Since $x-\log x\geq1$ for $x>0$, such table values cannot be generated by the formula exactly as printed. Subtracting one is the natural explanation, but the main PDF does not confirm its code's normalization. This constant has no effect on pairwise loss differences or rankings. It does affect ratios of average loss levels, so verbal claims that loss doubled or quadrupled depend on the convention. All numbers below reproduce the source tables without adjustment.

Why prefer QL when comparing calm and turbulent regimes? Suppose the measured proxy is $v=h_0\eta$, where $h_0$ is the true target and the multiplicative measurement error has conditional mean one. Conditional on the relevant information and true target, MSE's extra expected noise term is $h_0^2\operatorname{Var}(\eta)$, while the QL excess is $-E\log\eta$, independent of $h_0$ if the error distribution is stable. For small mean-zero deviations of $\eta$ from one, a second-order expansion gives $-E\log\eta\approx\operatorname{Var}(\eta)/2$. The latter is an approximation, not an identity.

This explains why MSE can rise sharply just because variance is high. It does not make all realized QL losses identically distributed. The paper's iid description is appropriate in a correctly specified one-step scale model with iid standardized shocks; overlapping multi-step errors and realized-proxy dependence require more care. Statistical uncertainty in average loss differences must account for the dependence created by overlapping horizons. The supplied source labels some improvements significant, but does not provide enough detail to reproduce the testing procedure, covariance estimates, bandwidths, or multiple-comparison adjustment.

A related distinction is between robust rankings in expectation and rankings in one finite sample. Conditional unbiasedness and suitable integrability support the former. A less noisy proxy increases power and can change observed rankings. Comparing absolute loss levels across squared returns and realized variance does not itself establish that one forecast is better: the proxies have different irreducible noise and potentially different targets.

## Numerical forecasting results

Table 2's baseline one-day QL losses are:

| Model | Squared-return proxy | Realized-variance proxy |
|---|---:|---:|
| GARCH | 1.460 | 0.273 |
| TARCH | 1.415 | 0.243 |
| EGARCH | 1.420 | 0.234 |
| APARCH | 1.417 | 0.249 |
| NGARCH | 1.422 | 0.244 |

Thus TARCH wins the first proxy, EGARCH the second. The authors report that these two models do not significantly outperform one another. More generally, asymmetry helps most at one day and one week; the difference from symmetric GARCH becomes insignificant at one month. For TARCH, squared-return losses across 1, 5, 10, 15, and 22 days are 1.415, 1.442, 1.478, 1.547, and 1.624. The realized-variance counterparts are 0.243, 0.289, 0.328, 0.368, and 0.415. EGARCH's one-month realized-proxy loss is 0.413, almost identical to GARCH's 0.414 and TARCH's 0.415. Extra flexibility in APARCH does not translate into a dominant score.

The recommendation for Gaussian likelihood is an average operational conclusion, not a statement that Student fitting never helps. Table 2 marks Student improvements for several asymmetric models under squared-return loss, and marks individual benefits of different windows or update frequencies. However, the authors find no systematic large gains from replacing the baseline across the wider comparison. A replicator should preserve those exceptions rather than interpreting the concluding recommendation as a uniform inequality.

Table 3 shows TARCH crisis losses of 1.461, 1.560, 1.985, 2.311, and 2.875 using squared returns. With realized variance they are 0.304, 0.353, 0.590, 0.672, and 1.380. One-day performance deteriorates moderately; the one-month deterioration is much larger. These are out-of-sample figures, distinct from the long-history exercise below.

Table 4's cross-asset squared-return losses give a similar horizon pattern. Currency one-day loss is 1.976 for the full sample and 1.925 during the crisis, while one-month loss rises from 2.138 to 3.244. Sector one-day loss moves from 2.236 to 2.217 and one-month loss from 2.412 to 3.870. International-equity one-day loss moves from 2.253 to 2.153, while one-month loss rises from 2.464 to 4.250. These averages combine time and assets within each class, rather than reporting confidence bands for a typical instrument.

The authors find asymmetric models useful for domestic and international equities. Symmetric GARCH remains a good full-sample currency descriptor, but asymmetry improves crisis-period currency forecasts. Their economic interpretation is dollar flight-to-quality: directional exchange-rate moves and increasing variance become linked during distress. That interpretation depends on the quotation direction and is not evidence that the same asymmetry sign holds for both a rate and its reciprocal.

## The separate long-history crisis experiment

Section 4 is not another genuinely real-time forecast exercise. It fits a model over January 1926–December 2008 and computes in-sample multi-horizon forecast losses, including the period whose extremity is being assessed. Table 5 reports whole-sample losses 1.5, 1.6, 1.7, 1.7, and 1.8. For January 2003–August 2008 they are 1.4, 1.5, 1.5, 1.5, and 1.5; for September–December 2008 they are 1.4, 1.6, 2.1, 2.8, and 4.1. The text sometimes describes the calm period as 2003–2007, while the table labels it through August 2008; the table's explicit dates should be retained.

There is also a likelihood inconsistency: the historical-exercise prose says Gaussian TARCH, but Table 5's caption says Student innovations. The subsequent simulation clearly uses Student innovations. Without the external implementation, the historical row cannot be assigned a unique likelihood with certainty.

The empirical exceedance procedure forms rolling four-month averages of daily horizon-specific losses throughout the long history. It compares pre-September-2008 averages with the average for the final four-month crisis interval. The historical exceedance probabilities in Table 6 are 54.5%, 38.2%, 12.3%, 3.6%, and 1.3% as the horizon rises from one to 22 days. These are probabilities of an average loss at least as large as the crisis average, not probabilities of the crisis return path or of a particular drawdown.

The Monte Carlo counterpart simulates 80 years from TARCH using full-sample fitted parameters and Student shocks. It then estimates the correctly specified model on each simulated history, generates in-sample forecasts, and averages losses over the last four months. Repeating 5,000 times produces exceedance probabilities 53.8%, 35.4%, 11.4%, 3.9%, and 2.0%. Re-estimation introduces parameter sampling variation. The source does not provide the fitted coefficients, Student degrees of freedom, initialization, burn-in, exact trading-day conversion of 80 years, or seed needed for exact numerical reconstruction.

At one month, a 2% Monte Carlo proportion from 5,000 independent replications has a binomial standard error of about 0.20 percentage point; this is a calculation from the reported design, not a reported confidence interval. Historical windows overlap heavily and cannot be treated as independent Bernoulli draws. The 1.3% and 2.0% exceedance estimates support the narrow statement that this loss statistic is not beyond a 1% upper-tail threshold under these retrospective benchmarks. They would not support nonrejection at every conventional level: both are below 5%. Nor do they establish a pre-crisis 99% predictive interval for realized portfolio loss.

## Reimplementation boundary and practical use

The supplied paper is sufficient to build the core experiment: daily-return ARCH forecasts, aligned horizons, expanding and rolling fits, update-frequency alternatives, two likelihood families, proxy-based loss comparisons, and a separate retrospective crisis simulation. Exact table replication still requires the external appendix or code for model parameterization, threshold choice, constraints, optimizer behavior, nonlinear multi-step integration, exact assets and dates, TAQ filters, loss normalization, and significance tests. These gaps are consequential implementation inputs, not reasons to invent defaults and label them author choices.

The most portable finding is that predictable changes in tomorrow's variance can be captured even during severe distress when the latest shocks are incorporated quickly. The strongest limitation is that this responsiveness supplies little advance warning for a position that cannot be adjusted for weeks. A researcher using the result should evaluate the entire horizon-dependent forecast distribution and the feasible exposure-adjustment policy. Choosing a good one-day variance model is one component of that problem; it is not a substitute for modeling the risk that volatility itself will change over the holding period.
