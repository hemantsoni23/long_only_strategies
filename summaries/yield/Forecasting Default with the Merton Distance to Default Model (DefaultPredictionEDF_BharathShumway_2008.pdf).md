# Forecasting Default with the Merton Distance to Default Model

Sreedhar T. Bharath and Tyler Shumway. *The Review of Financial Studies* 21(3), 2008, pp. 1339–1369. DOI: 10.1093/rfs/hhn044; advance publication May 19, 2008. Source: [DefaultPredictionEDF_BharathShumway_2008.pdf](../../Finance/DefaultPredictionEDF_BharathShumway_2008.pdf). All 31 pages, including all tables and references, were read. Printed page $p$ is PDF page $p-1338$.

## Why this matters

A sophisticated structural model may owe its predictive success to a useful nonlinear transformation of ordinary inputs rather than to its internal calibration. Bharath and Shumway test this distinction directly. Their simple approximation to Merton distance to default predicts corporate defaults at least as well as an iterative Merton implementation in the principal comparisons. Adding profitability and other predictors improves performance further. The structural theory is useful as feature engineering; the implied probability is not a sufficient summary of default information.

The result is especially relevant when a credit or equity research process treats distance to default as a self-contained risk estimate. It argues for retaining the nonlinear leverage–volatility–return interaction while validating the expensive inversion and the final probability mapping separately. Ranking firms, calibrating absolute failure probabilities, and pricing credit-sensitive instruments are different tasks. The paper supplies evidence on each, with much stronger evidence on ranking than on calibration or pricing.

It does not test the exact proprietary Moody's KMV product. Nor does it show that a single naive score is optimal, that structural models are universally useless, or that an estimated physical default probability can be substituted directly into a credit-pricing model.

## The three hypotheses

The first hypothesis is sufficiency: if the Merton model and its implementation are correct, its implied probability should contain all relevant information for forecasting default. Additional predictors should not improve a correctly specified conditional forecast.

The second is that the model's nonlinear distance-to-default form adds value beyond a linear combination of its constituent inputs. The naive score is designed to isolate this hypothesis by retaining the form while simplifying asset value, asset volatility, and expected-return calculations.

The third is that the nonlinear Merton solution itself contributes information. This is tested by comparing the iterative score with the naive score, with reduced-form hazard models, and with alternative calculations that replace individual steps. The findings reject sufficiency, support the nonlinear transformation, and find little incremental value from the iterative inversion once a strong competing specification is included.

These are empirical comparisons within the selected models. Statistical significance of a nonlinear score after linear inputs enter does not establish that its exact functional form is uniquely correct; other nonlinear approximations might work as well or better.

## Structural model and exact default formula

Firm asset value follows geometric Brownian motion,

$$
dV_t=\mu V_tdt+\sigma_VV_tdW_t.
$$

Debt is represented by one zero-coupon obligation with face value $F$ due at horizon $T$. Equity is a call on assets:

$$
E=V\Phi(d_1)-Fe^{-rT}\Phi(d_2),
\qquad
d_1=\frac{\log(V/F)+(r+\sigma_V^2/2)T}{\sigma_V\sqrt T},
\qquad d_2=d_1-\sigma_V\sqrt T.
$$

Ito's lemma and option delta imply

$$
\sigma_E=\frac{V}{E}\Phi(d_1)\sigma_V.
$$

Equity value and equity volatility are observed or estimated; asset value and volatility are inferred. The physical distance to default and probability are

$$
DD=\frac{\log(V/F)+(\mu-\sigma_V^2/2)T}{\sigma_V\sqrt T},
\qquad \pi_M=\Phi(-DD).
$$

The risk-free rate enters the equity-pricing inversion; the physical asset drift enters the default forecast. Confusing them changes the estimand. The SDE drift $\mu$ is the instantaneous expected proportional return, while the expected log-growth rate is $\mu-\sigma_V^2/2$. The source describes estimation using implied daily log asset returns but does not spell out every annualization and drift-conversion step. A replication must document whether a half-variance adjustment is made rather than subtracting it twice.

Default here occurs when assets are below the debt barrier at the horizon. The model does not contain first-passage default before maturity, multiple debt seniorities and maturities, strategic bankruptcy, stochastic volatility, jumps, taxes, or an explicit liquidity channel. The debt-barrier proxy used empirically is an accommodation to actual balance sheets rather than a derivation from the one-bond model.

## Iterative implementation

For each monthly observation, equity volatility is estimated from the preceding year of daily returns. The initial asset-volatility guess is $\sigma_V^{(0)}=\sigma_E E/(E+F)$. With this fixed volatility, solve the equity-pricing equation for daily asset values over the previous year. Recalculate asset log returns, asset volatility, and the mean-return estimate from that implied series. Repeat until successive asset-volatility estimates differ by less than $10^{-3}$. The converged values enter the one-year DD formula.

This is not simply a one-date simultaneous solution of the pricing and delta-volatility equations. The historical iteration allows leverage and inferred equity-option sensitivity to vary through the preceding year. It conditions on a whole return path. The comparison therefore needs a naive construction that also includes historical returns, rather than using only today's leverage.

The article provides the convergence threshold but not a complete specification of daily debt interpolation, statement-release lags, numerical root brackets, maximum iterations, or nonconvergence handling. Those details can change the implied asset-return history and therefore the final score. The procedure also produces a plug-in probability without a directly reported standard error; calibration and parameter uncertainty are not summarized by the existence of a converged nonlinear solution.

## Naive construction and what it preserves

The approximation treats market debt value as face value, $D_N=F$, and assigns debt volatility

$$
\sigma_{D,N}=0.05+0.25\sigma_E.
$$

Five percentage points represent interest-rate variability, and the quarter-equity-volatility term represents default-related debt risk. These constants were chosen heuristically, not estimated or optimized on the sample. The resulting asset-volatility proxy is

$$
\sigma_{V,N}=\frac{E}{E+F}\sigma_E+\frac{F}{E+F}(0.05+0.25\sigma_E).
$$

This is a weighted sum of volatilities, not the general standard deviation of an equity-plus-debt portfolio under arbitrary correlation. It acts as an approximation consistent with strongly related debt/equity risk, and is deliberately simple rather than structurally exact.

Set $V_N=E+F$ and $\mu_N=R_{i,t-1}$, the stock's cumulative return over the previous year. Then

$$
DD_N=\frac{\log[(E+F)/F]+(R_{i,t-1}-\sigma_{V,N}^2/2)T}{\sigma_{V,N}\sqrt T},
\qquad \pi_N=\Phi(-DD_N).
$$

All rate and volatility inputs must be decimals in these formulas: 0.05 is five percentage points per year, not 0.05 percent. The annual stock return is a proxy for asset drift, not an unbiased estimator justified by Merton. It is used to match the historical information content available to the iterative method. The comparison's point is whether a rough but informed transformation performs competitively, not whether the heuristic is a literal asset-pricing identity.

The normal CDF is strictly monotone, so sorting by $\pi_N$ is equivalent to sorting by $-DD_N$. Good rank performance therefore does not validate the CDF as a probability calibration. In a hazard regression the nonlinear transformation can affect functional fit, but in a decile ranking its scale and calibration are irrelevant apart from numerical ties.

## Data and preprocessing

The main sample is the intersection of the COMPUSTAT Industrial quarterly file and CRSP daily NYSE, AMEX, and Nasdaq equity data, 1980–2003. The article excludes SIC codes 6021, 6022, 6029, 6035, and 6036. These are specified banking/thrift codes; describing the rule as an exclusion of every possible financial firm would be broader than the listed implementation.

Default events come from Edward Altman's database through 2000 and Moody's published list for 2001–2003. There are 15,018 firms, 1,449 defaults, and 1,016,552 firm-months with complete data. The quarterly ranking sample contains 350,662 firm-quarters. The paper does not reproduce the full event-file taxonomy and censoring code, so “default” should not be silently replaced by all financial delistings or by bankruptcy filings alone.

Month-end market equity $E$ is price times shares outstanding, in millions of dollars. The barrier is debt in current liabilities plus half long-term debt, using the source's COMPUSTAT items 45 and 51. Additional predictors include the prior year's cumulative stock return minus the CRSP value-weighted NYSE/AMEX index return and net income divided by total assets. The latter's table scale is percent, as indicated by its summary magnitudes; coefficient replication requires consistent scaling.

The main text says the risk-free input is the one-year Treasury constant-maturity yield, while Table 1 describes a three-month bill rate. This is a source inconsistency, not a reason to choose whichever series happens to improve the results. Both variants can be reported if the original code is unavailable. A separately labeled sensitivity should also distinguish discrete quoted yields from continuously compounded rates used in the option formula.

All variables except default probabilities are winsorized at the first and ninety-ninth percentiles. The article does not clearly specify a training-only threshold policy. A prospective implementation must estimate preprocessing constants from past data and apply appropriate statement-publication lags; those steps should be documented as safeguards beyond the article's incomplete timing description.

Table 1 reports mean $\pi_M=10.95\%$ and mean $\pi_N=8.95\%$, but medians of 0.01% and approximately zero. The distributions have heavy upper tails. Their correlation is 0.8642; asset-volatility proxies correlate 0.8748. The mean inferred asset drift is 3.25% with standard deviation 57.17%, highlighting substantial mean-estimation noise. These score means are not validated annual empirical default frequencies.

## Cox hazard model and inference

The reduced-form model is

$$
\lambda_i(t)=\lambda_0(t)\exp[x_i(t)'\beta],
$$

with time-varying covariates and a common unspecified baseline hazard. Cox partial likelihood estimates $\beta$ by comparing the failing firm's covariates with the risk set at each failure time. In the no-ties case its log objective is

$$
\sum_{j\in\text{events}}\left[x_{i_j}(t_j)'\beta-\log\sum_{k\in\mathcal R(t_j)}e^{x_k(t_j)'\beta}\right].
$$

This equation is an explanatory restatement of the estimation principle, not a claim that the paper discloses its tie-handling convention. A hazard rate is an intensity, not a bounded probability; a cumulative event probability additionally requires integration of the baseline and future covariate path. The model accommodates censoring, but inference still depends on its censoring and proportional-hazards assumptions. The article does not supply extensive proportionality diagnostics or a full clustered-standard-error recipe.

Univariate coefficients on $\pi_M$ and $\pi_N$ are 3.635 (SE 0.068) and 4.011 (SE 0.067), respectively. In a joint model they remain significant at 1.697 and 2.472, showing that each contains information beyond the other under that specification.

The decisive expanded Model 6 includes both probabilities, $\log E$, $\log F$, $1/\sigma_E$, prior excess return, and net income/assets. The Merton coefficient falls to 0.230 (SE 0.164), while the naive coefficient is 1.366 (SE 0.178). Profitability is strongly negative, with coefficient −0.044 (SE 0.002) on the paper's scale. The naive score remains useful after its constituent variables enter linearly; the iterative score does not.

Model 7 removes the insignificant Merton score and retains the naive score with coefficient 1.526 (SE 0.138). The source reports VIFs no larger than 4.27 and a condition number of 4.38, arguing against severe numerical collinearity. High correlation still matters economically: conditional insignificance is a statement about marginal information in this specification, not a claim that the omitted score has no standalone predictive value.

## Out-of-sample discrimination

At each quarter's start, firms are sorted by their forecast score into deciles, and defaults during that quarter are counted. The headline measure is the share of all defaults captured in the highest-risk decile. It is recall at a 10% selection fraction, not the probability that a selected firm defaults. The model's one-year DD is used for a next-quarter ranking test; good performance here does not directly establish one-year probability calibration.

Over 1980–2003, the highest decile captures 64.9% of defaults for Merton and 65.8% for the naive score. The highest quintiles capture 80.0% and 80.1%. Market-equity, past-excess-return, and profitability sorts capture 35.7%, 44.4%, and 46.8% in their highest-risk deciles. The nonlinear credit composites substantially beat any one ingredient, while the difference between the two composite methods is small and is not accompanied by a formal paired significance test.

The authors give a useful calibration distinction: $1,449\times0.649/(350,662\times0.1)\approx2.7\%$ is the observed next-quarter default rate in the highest Merton decile. That is very different from saying the model correctly forecasts a 64.9% default probability for those firms.

For 1991–2003, hazard models are reestimated each quarter on all previous data. The paper's example forecasts 1995 Q2 using a model trained through 1995 Q1. The evaluation contains 226,604 firm-quarters and 847 defaults.

| Score/model | Defaults in highest-risk decile | Defaults in lowest-risk half |
|---|---:|---:|
| Merton DD | 69.4% | 6.0% |
| Naive DD | 70.0% | 5.7% |
| Linear inputs, Model 4 | 68.8% | 8.5% |
| Inputs plus naive DD, Model 5 | 70.4% | 8.2% |
| Expanded Model 6 | 75.6% | 6.0% |
| Expanded Model 7, without Merton | 75.8% | 6.0% |

Profitability and the expanded specification matter more than the iterative inversion. No single model dominates every metric: the naive score has fewer defaults in the lower-risk half than the expanded models, despite lower top-decile capture. The table therefore supports a decision-dependent comparison rather than a universal ranking of forecast quality.

## Alternative calculations

Replacing the iterative asset-drift estimate with the risk-free rate lowers top-decile capture to 60.0%. Simultaneously solving the two one-date Merton equations, also using the risk-free drift as described in Table 5, captures 65.1%, close to the baseline 64.9%. These are different interventions: changing drift in the iterative history need not be equivalent to changing both inversion and drift together.

OptionMetrics 30-day at-the-money call implied volatility is available for a smaller 1996–2003 sample. The option-based score captures 84.1% of defaults in its highest-risk decile, versus 80.7% for Merton and 83.0% for naive DD on the same matched sample. Only 88 defaults and 36,274 firm-quarters support this comparison. Option coverage selects different firms; the 84.1% figure cannot be compared directly with 64.9% in the full sample. The apparent gain over naive DD is also only about one default in eighty-eight, based on rounded percentages.

An 80-firm August 2000 comparison with published Moody's KMV data yields rank correlations 0.788 for Merton and 0.786 for naive probabilities. Asset volatility rank correlations are 0.574 and 0.853, respectively. This small, selected large-issuer cross-section shows that both capture substantial information in the commercial scores, but cannot validate equivalence with the proprietary product. KMV uses its own structural extensions, accounting adjustments, and empirical DD-to-default mapping.

## CDS comparison and risk-neutral probabilities

The CDS sample has 3,833 firm-months, December 1998–July 2003. The paper assumes a constant annual conditional default probability, annual premium payments, default halfway through a year, half-year accrued premium at default, a flat continuously compounded discount rate, and 75% loss given default. Equating expected premium and protection legs extracts $\pi_{CDS}$.

Under exactly these simplifying assumptions, the common survival-discount sum cancels. Writing $s$ for annual spread in decimals, $L=0.75$, and $a=e^{-r/2}$, direct algebra from equations (15)–(16) gives

$$
\pi_{CDS}=\frac{sa}{L+sa-s/2}.
$$

This closed form is derived here; the paper describes solving a nonlinear equation. It depends on a flat hazard and discount rate and does not extend unchanged to an actual quarterly schedule, a term structure of credit spreads, or stochastic recovery. It is a risk-neutral probability under the pricing assumptions, whereas $\pi_M$ and $\pi_N$ aim to be physical probabilities.

For this comparison the two model scores are capped between 0.20% and 20%. Mean CDS spread is 165.89 basis points; mean implied CDS probability is 2.13%. The CDS probability correlates 0.3762 with Merton and 0.5199 with naive DD. In regressions with time dummies, log-CDS-spread $R^2$ is 0.26 with log Merton probability and 0.38 with log naive probability. Including both leaves the Merton log coefficient insignificant at −0.0194 (SE 0.0105), while naive remains 0.2931 (SE 0.0118).

The mean CDS-to-Merton probability ratio is 5.09 and its median 3.73; for naive DD they are 5.54 and 4.14. These do not isolate a clean default-risk premium because model misspecification, horizon mapping, recovery, score caps, and liquidity can influence the ratios. The paper argues that ratios below one contradict a correctly calibrated positive-premium model. That conclusion requires a positive default-risk-price assumption; risk-neutral probability exceeding physical probability is not a universal no-arbitrage ordering for every issuer and state.

There is also a printed table/text discrepancy: the discussion says the lower quartile of both ratios is below one, but Table 6 reports the naive ratio's 25th percentile as 1.62, versus 0.80 for Merton. Both minima are below one, but the claim about both quartiles is not supported by the table. Similarly, a regression slope below one is not by itself a theorem-level violation of risk-neutral versus physical probability ordering when intercepts, measurement error, and conditioning differ.

## Bond-spread evidence

The 1980–1997 Lehman/Warga sample excludes matrix-priced bonds, embedded options, sinking funds, floating coupons, unusual coupon frequencies, inflation indexing, bonds outside the Lehman indexes, maturities below one year, and AAA-rated issues. The remaining 61,776 bond-months are based on dealer quotes, not guaranteed executable transactions. Spread is yield to maturity minus the nearest-maturity Treasury index yield, rather than a fitted zero-curve option-adjusted spread. The mean is 108.09 basis points; mean maturity is 10.32 years.

Regressions include equity volatility, maturity, log issue size, risk-free yield, coupon, rating, year, and industry dummies, with additional accounting controls in some specifications. Conditional on ratings, the score coefficients are economically small. A coefficient of 0.50 basis points per probability percentage point means a move in naive default probability from 0% to 5% changes fitted spread by only 2.5 basis points. The corresponding Merton-only coefficient is 0.08; when both scores enter, Merton falls to 0.007 and is insignificant in the basic specification. Extended controls can restore some significance, so the result is weak incremental pricing information rather than literal zero correlation everywhere.

Adding bond spreads to a hazard model leaves only 571 firms and 58 defaults. Spreads and naive DD remain significant; Merton does not. The severe sample reduction limits generalization and makes lost significance in other variables difficult to distinguish from loss of power. Spread may contain information beyond equity inputs, but it is not a pure physical default signal because it also reflects recovery, liquidity, and risk compensation.

## Replication and use in a research process

The first replication layer should reconstruct the state inversion and naive formula on identical observations, with clear treatment of missing/zero debt, annualization, historical statements, and the risk-free-series discrepancy. The second should recreate quarterly ranks and event counts before comparing probabilities: rank results are robust to monotone recalibration but vulnerable to stale inputs and selection. The third should fit expanding Cox models with documented risk sets, censoring, ties, and matured labels, then assess both discrimination and calibration on genuinely unseen periods.

Useful modern metrics would include time-dependent rank discrimination, calibration by forecast bucket and calendar period, log loss, and decision-specific false-negative costs. Those are proposed extensions; the paper mainly reports capture rates, hazard coefficients, and spread regressions. It supplies no trading strategy, loan-loss portfolio optimization, transaction costs, recovery allocation, or capital-budget objective, so its tables should not be converted into investment PnL or regulatory capital savings without additional modeling.

The practical result is a strong baseline: a cheap structural transformation plus accounting information can be more useful than a costly structural inversion used alone. Retaining theory's nonlinear scaling while testing calibration, incremental information, and implementation error separately is the paper's most durable research contribution.

## Source map

Bharath and Shumway (2008), “Forecasting Default with the Merton Distance to Default Model.” Structural and naive formulas: equations (1)–(13), pp. 1343–1348. Hazard and CDS models: pp. 1348–1351. Data and summary statistics: pp. 1351–1354, Tables 1–2. Hazard and ranking evidence: pp. 1354–1360, Tables 3–5. CDS results: pp. 1361–1363, Table 6. Bond results: pp. 1363–1367, Table 7. References: pp. 1368–1369. No separate mathematical appendix is included in the supplied article.
