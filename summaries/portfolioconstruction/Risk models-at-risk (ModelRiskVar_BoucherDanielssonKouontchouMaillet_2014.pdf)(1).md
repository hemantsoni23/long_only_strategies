# Risk models-at-risk

Christophe M. Boucher, Jón Daníelsson, Patrick S. Kouontchou, and Bertrand B. Maillet (2014), *Journal of Banking & Finance* 44, 72–92. DOI: 10.1016/j.jbankfin.2014.03.019. [Local source PDF](../../Finance/ModelRiskVar_BoucherDanielssonKouontchouMaillet_2014.pdf).

The local file is the 21-page published article, including Appendices A–C, references, and supplementary tables and figures embedded in those appendices. Page references below count PDF pages; printed journal page numbers are 71 higher. The complete file was read, with the main formulas and empirical tables checked visually. Several printed conventions are inconsistent. Where this note supplies a coherent implementation, the repair is a derivation for this note, not an official erratum.

## Why this matters

A value-at-risk forecast can fail because its parameters are estimated noisily, because the distributional model is wrong, or because both problems occur together. Reporting a precise quantile while ignoring these sources of error creates a false sense of accuracy. Boucher and coauthors propose turning the historical failure of a risk model into an additional capital allowance: find the smallest conservative change to a model's forecasts that would make their historical exceptions acceptable under specified backtests.

The useful contribution is therefore a second layer of risk management around an existing forecasting model. It does not require replacing every baseline with a single preferred model, and it distinguishes exception frequency, clustering, and magnitude. A model may produce approximately the right number of violations while placing those violations together in time or understating their severity. These deficiencies can require different adjustments.

The evidence also shows why this adjustment should be treated as a calibrated historical allowance rather than a known correction for the true quantile. Different models, test criteria, estimation windows, and market histories produce different buffers. Passing a backtest on the observations used to select the buffer is an in-sample constraint, not proof that future model error is bounded. This distinction is central to using the paper constructively.

## Quantile conventions and the object being estimated

Use a consistent negative-return convention. Let $r_t$ be the one-period portfolio return, $\alpha$ the high confidence level, and $p=1-\alpha$ the lower-tail probability. Given information available before observing $r_t$, the ideal return threshold is

$$
v_t=F_t^{-1}(p).
$$

For a typical risky asset, $v_t<0$. Its positive loss VaR is $-v_t$. A fitted model produces $\widehat v_t=\widehat F_t^{-1}(p)$, and the realized exception indicator is

$$
I_t=\mathbf 1\{r_t<\widehat v_t\}.
$$

These definitions resolve two problems in the source's notation. Its prose calls VaR a negative return, but its hit definition uses $r_t<-\mathrm{EVaR}_t$. It also labels $\alpha$ as a high confidence level while writing the null number of hits as binomial with probability $\alpha$. With the negative-return convention above, the event is $r_t<\widehat v_t$ and the hit probability is $p$, not $\alpha$. A positive-loss convention would also work, provided the sign and probability are changed together.

The theoretical decomposition is

$$
v_t=\widehat v_t+e_t.
$$

Here $e_t$ is the realized difference between the ideal and estimated quantiles. Although the article repeatedly calls this quantity a bias, it is not necessarily a statistical expectation such as $\mathbb E[\widehat v_t]-v_t$. A simulation can measure it because the data-generating distribution is known. A historical market sample cannot reveal it directly. The operational procedure replaces knowledge of $e_t$ with a backtest-based adjustment.

The opening classification and Appendix A identify five sources of risk-model error. Parameter estimation introduces uncertainty within a chosen family. Specification error arises when that family cannot represent the relevant return law. Granularity restricts the probability resolution of an empirical distribution, roughly to multiples of $1/n$ for $n$ equally weighted observations. Measurement error includes the construction of portfolio profit and loss and the treatment of costs or fees. Liquidity can distort measured returns through smoothing, stale observations, and eventual price jumps. The numerical work emphasizes the first two; it does not separately estimate all five components.

The article contrasts a direct quantile correction with probability shifting. One can evaluate the true distribution at an estimated quantile, or the estimated distribution at a true quantile, to express the discrepancy as a changed tail level. However, every genuine CDF value remains between zero and one. The source's discussion of a required probability exceeding 100% is best understood as failure to reach the target quantile within the estimated distribution or search range, particularly for an empirical distribution with finite support. It is not a valid probability greater than one, nor a theorem that probability-level adjustments are always impossible.

## Controlled experiments: estimation and specification

The main simulation on PDF pages 4–6 compares a normal GARCH(1,1) forecasting model with a two-state Markov-switching GARCH model using Student innovations. The latter is intended to combine persistent volatility regimes and heavy tails. The return equation is $r_t=\mu_{s_t}+\sigma_{s_t}z_t$, where $s_t$ is a two-state Markov chain and the Student degrees of freedom are 5.56. The published variance recursion contains $\beta_{s_t}^{\,2}$ multiplying the lagged variance; this square should be retained in a literal transcription rather than silently replaced by the more familiar unsquared GARCH coefficient.

In the source's state-index notation, the recursion is

$$
\sigma_{s_t}^{\,2}=\omega_{s_t}
+a_{s_t}\varepsilon_{t-1}^{\,2}
+\beta_{s_t}^{\,2}\sigma_{s_{t-1}}^{\,2},
\qquad \varepsilon_t=r_t-\mu_{s_t}.
$$

Time is implicit in the state-indexed volatility. The normal-GARCH comparison removes the switching and changes the innovation law. Specifying the innovation scale is necessary before interpreting the displayed variance recursion as a conditional second moment.

The reported parameters are $\mu_1=\mu_2=0$, $\omega_1=3.1699\times10^{-6}$, $\omega_2=2.509\times10^{-5}$, $a_1=0.0733081$, $a_2=0.0064734$, $\beta_1=0.90801$, and $\beta_2=0.10453$. The state persistence probabilities are $P(s_t=1\mid s_{t-1}=1)=0.99654$ and $P(s_t=2\mid s_{t-1}=2)=0.99328$. Calling this a second-order model in the text should not be read as specifying a Markov chain with two lags; the displayed transition structure is a first-order chain with two states.

There are unresolved replication details. The body refers to DJIA calibration from January 1, 1990, whereas the table captions start on January 1, 1900; both end on September 20, 2011. The text describes 360,000 simulated daily observations used with 1,000-observation windows, while the captions describe 360,000 series of 1,000 daily returns. Initialization, burn-in, random seed, treatment of the path dependence in switching GARCH, and variance standardization of the Student innovations are not fully specified. These choices materially affect a literal reproduction.

Table 1 reports annualized daily quantiles at confidence levels 95%, 99%, and 99.5%. An annualized daily threshold is not the quantile of an annual holding-period return. In the matched normal-GARCH experiment, mean estimated and ideal thresholds agree at −36.16%, −59.70%, and −70.99%. Mean error is reported as zero, but individual errors are large: at 99%, the minimum is −32.66 percentage points and the maximum is +32.02.

When specification error alone is imposed, the estimated thresholds are −30.78%, −43.83%, and −48.61%, against the same ideal thresholds. The corresponding mean corrections are −5.38, −15.87, and −22.38 percentage points. When estimation and specification error are combined, mean estimated thresholds are −28.97%, −41.28%, and −45.78%, requiring mean corrections of −7.19, −18.42, and −25.20 points. At 99.5%, the correction ranges from −47.84 to +15.03 points.

These are conditional results for the chosen simulation and parameterization. They establish neither a universal percentage haircut nor a monotone relationship between risk confidence and model error for every distribution. The article's prose says mean combined errors equal specification errors, but the displayed means do not agree exactly; the table values above preserve that distinction. The practically robust finding is that an approximately unbiased estimator under its own family may still have substantial sample dispersion, while misspecification shifts its center and can become especially costly deep in the tail.

## Operational adjustment: make the objective explicit

Let a historical calibration window contain $m$ forecasts and their subsequently realized returns. Apply a nonnegative additive buffer $b$ to the negative-return thresholds:

$$
\widetilde v_t(b)=\widehat v_t-b,\qquad
I_t(b)=\mathbf 1\{r_t<\widetilde v_t(b)\}.
$$

Given a selected test statistic $T_j(b)$ and critical value $c_j$, the intended least-conservative accepted correction can be expressed as

$$
b_j^*=\inf\{b\geq0:T_j(b)\leq c_j\}.
$$

For simultaneous acceptance, replace the single inequality with all required test inequalities. The corrected positive loss VaR is $-\widehat v_t+b_j^*$. Alternatively write $q=-b\leq0$ and choose the largest acceptable $q$. This notation states exactly what “minimum adjustment” means.

The source's Equation (8) uses a supremum over accepted negative-return VaRs, which agrees with the least-conservative interpretation. Equation (14), however, writes an argmin over corrections added to negative VaR. Its search description also moves from a very conservative starting value toward larger thresholds until a first accepted point appears. Depending on the starting point and acceptance set, that first point need not be the least-conservative accepted boundary. The minimization direction must therefore be fixed before implementation. The definition above is a derived operational clarification, not a claim that the published code used precisely this convention.

A practical search should enumerate candidate buffers, record the entire accepted set, and select its smallest nonnegative element. For frequency and independence tests, exception patterns change when $b$ crosses a historical gap $\widehat v_t-r_t$. These gaps provide natural event points for a fine search, with care about strict versus weak inequalities. Magnitude tests can vary within those intervals and need a numerical search as well.

Acceptance is not generally monotone in conservatism. Too few exceptions can fail a two-sided unconditional-coverage test, and changes in the clustering pattern need not be monotone as individual exceptions disappear. Consequently, blind bisection on “passes versus fails” is not justified. An empty acceptance set is a possible outcome and should be returned explicitly rather than concealed by an arbitrarily large buffer. The paper says it did not encounter an empty set in its application and that zero adjustments occurred in fewer than about 5% of its stated 27,842 forecasts. Neither observation is a mathematical existence result.

There are three distinct confidence choices: the VaR confidence $\alpha$, the backtest significance level $\eta$, and the historical quantile or maximum selected from the distribution of required buffers. Conflating them obscures the economic meaning of a reserve. Increasing the VaR confidence moves farther into the return tail; decreasing the rejection significance level changes how difficult it is to reject the model; choosing a higher buffer quantile protects against a larger fraction of historically observed adjustment requirements.

## The backtests and a reproducible likelihood

For unconditional coverage, let $K=\sum_{t=1}^{m}I_t$ and $\widehat p=K/m$. Under independent, correctly calibrated hits, $K\sim\operatorname{Binomial}(m,p)$. The usual likelihood-ratio statistic is

$$
\mathrm{LR}_{\mathrm{uc}}
=2\left[
K\log\frac{\widehat p}{p}
+(m-K)\log\frac{1-\widehat p}{1-p}
\right],
$$

with $0\log0=0$ at boundaries. The reference asymptotic distribution is chi-squared with one degree of freedom. At 99.5% VaR and a 250-observation window, only 1.25 exceptions are expected under the null; asymptotic calibration and statistical power are therefore important limitations. The paper additionally considers resampling adjustments to critical values.

For independence, let $N_{ij}$ count observed transitions from $I_{t-1}=i$ to $I_t=j$. Fit $p_{01}=N_{01}/(N_{00}+N_{01})$ and $p_{11}=N_{11}/(N_{10}+N_{11})$. The Markov alternative likelihood is

$$
L_1=(1-p_{01})^{N_{00}}p_{01}^{N_{01}}
(1-p_{11})^{N_{10}}p_{11}^{N_{11}}.
$$

Under the independence null, impose a common transition probability $\bar p=(N_{01}+N_{11})/\sum_{i,j}N_{ij}$ and compute the likelihood $L_0$ at that restriction. Then $\mathrm{LR}_{\mathrm{ind}}=2(\log L_1-\log L_0)$ has the usual asymptotic chi-squared reference with one degree of freedom. Zero transition counts require limiting likelihood calculations; undefined empirical transition ratios should not be inserted without a convention.

The printed alternative likelihood in Appendix B uses $N_{10}$ where the exponent on $p_{01}$ should be $N_{01}$. The expression above follows directly from the transition counts. A conditional-coverage test can combine frequency and independence statistics with a two-degree-of-freedom reference, although the article reports adjustments by the separate criteria.

Magnitude evaluation requires a predictive distribution, not merely a reported quantile. Define the probability integral transform $u_t=\widehat F_t(r_t)$ and $z_t=\Phi^{-1}(u_t)$. Under a continuous, correctly specified conditional distribution, the $z_t$ should behave as independent standard normals. To focus on the lower tail, retain observations below $a=\Phi^{-1}(p)$ and otherwise record a censoring indicator.

A buffer search also needs to specify how changing the quantile changes that full distribution. Merely replacing $\widehat v_t$ by $\widehat v_t-b$ while holding the PITs and censoring threshold fixed would leave the magnitude statistic unchanged. One self-contained reconstruction is a location shift:

$$
\widehat F_t^{(b)}(x)=\widehat F_t(x+b),\qquad
u_t(b)=\widehat F_t(r_t+b),\qquad
z_t(b)=\Phi^{-1}(u_t(b)).
$$

This distribution has $p$-quantile $\widehat v_t-b$, so censoring $z_t(b)$ at the fixed threshold $a$ agrees with the corrected hit definition. Evaluate the likelihood below using these buffer-dependent $z_t(b)$ values for every candidate $b$. This location shift is an additional implementation assumption derived for this note, not a uniquely specified rule from the source. It changes the entire predictive distribution, including its center. Other ways of extending a quantile adjustment to a full CDF can generate different magnitude buffers; without that convention the magnitude-adjustment path remains underdetermined.

A coherent censored-normal log likelihood is

$$
\ell(\mu,\sigma)=
\sum_{z_t\geq a}\log\left[1-\Phi\left(\frac{a-\mu}{\sigma}\right)\right]
+\sum_{z_t<a}\left[
-\log\sigma+\log\phi\left(\frac{z_t-\mu}{\sigma}\right)
\right].
$$

Compare the maximized likelihood with $\ell(0,1)$ using a two-parameter likelihood ratio. The uncensored latent normal has mean zero and variance one under the null; the censored variable itself does not generally have those moments.

The published likelihood on PDF page 19 also subtracts $\log\Phi((a-\mu)/\sigma)$ for every tail observation. That term converts a normal density into a density conditional on falling in the tail, but the formula retains the non-tail censoring probability without supplying the missing tail probability. It therefore mixes truncated and censored likelihood constructions. The expression above is a derived consistent censored version. It is not sufficient to reproduce the published numerical magnitude adjustments exactly, because the paper does not disclose whether its implementation used the printed hybrid, a proper censored likelihood, or another convention.

For a historical quantile estimator, the necessary predictive CDF and treatment of atoms also require specification. The source notes limitations of a parametric magnitude test for historical simulation but still provides magnitude-related table entries for the model set. A replication must state how empirical PITs are interpolated or randomized and how zero or unit CDF values are handled before applying $\Phi^{-1}$.

Appendix B constructs resampling critical values from statistics evaluated on consecutive subsamples of length $b$. If $K_{b,t}$ is the statistic on the block starting at $t$, the empirical distribution is

$$
G_b(x)=\frac{1}{m-b+1}\sum_{t=1}^{m-b+1}
\mathbf 1\{K_{b,t}\leq x\},
$$

and the critical value is its $(1-\eta)$ quantile. The operational block length is not fully specified in the article. “Bootstrap” or starred results should not be assumed automatically more conservative or less conservative: Table 3 contains both directions, particularly for magnitude tests. The discussion also cautions that resampling does not eliminate model misspecification.

## Historical experiment: models, timing, and reported adjustments

The main application uses daily DJIA data from Bloomberg. Most captions give January 1, 1900 through September 20, 2011. The body also mentions an endpoint of March 2, 2011 and a count of 29,002 observations, followed by a larger reported forecast count; a separate footnote gives 27,842 forecasts. These quantities do not define a single unambiguous evaluation calendar. A faithful reconstruction must obtain the original data calendar or explicitly choose and disclose a substitute.

The standard estimation window is four years, represented by 1,040 daily returns. Forecasts are re-estimated as this window moves. A 250-observation out-of-sample window is used to evaluate forecast errors, giving a calibration-to-estimation sample ratio of approximately 0.24. “Out of sample” here first describes returns outside the baseline model's estimation sample. If those same returns are then used to choose a buffer, they are the buffer's calibration sample. A prospective evaluation requires applying the buffer only to later returns.

The nine baseline methods are historical simulation, Gaussian parametric VaR, Student parametric VaR, Cornish–Fisher VaR, RiskMetrics EWMA with decay factor 0.94, Gaussian GARCH(1,1), CAViaR, generalized extreme-value estimation, and generalized Pareto estimation. The paper identifies these model families, but does not provide every numerical specification needed for an identical rerun. Examples include the EVT threshold or block-size selection, the exact CAViaR specification and optimizer, and handling of failed estimates. These are not cosmetic choices because an extreme or unstable estimate changes both the exception process and the required correction.

Table 3 on PDF page 10 summarizes daily 95% VaR and its adjustments at a 5% test significance level. The table below reproduces its model rows with the source's percent labels. Here $q_1$, $q_2$, and $q_3$ denote frequency, independence, and magnitude corrections; a star denotes the corresponding resampling variant.

| Model | Mean VaR | $q_1$ | $q_1^*$ | $q_2$ | $q_2^*$ | $q_3$ | $q_3^*$ |
|---|---:|---:|---:|---:|---:|---:|---:|
| Historical | −1.60 | −2.61 | −2.03 | −4.85 | −3.24 | −3.10 | −5.90 |
| Gaussian | −1.68 | −2.66 | −1.86 | −4.62 | −2.76 | −2.76 | −5.49 |
| Student | −1.89 | −2.49 | −1.86 | −4.25 | −2.85 | −3.11 | −6.30 |
| Cornish–Fisher | −1.26 | −8.29 | −7.48 | −8.40 | −8.86 | −8.40 | −8.86 |
| RiskMetrics | −1.59 | −0.98 | −0.65 | −2.03 | −1.02 | −1.02 | −2.89 |
| GARCH | −1.61 | −1.13 | −0.96 | −2.57 | −1.15 | −1.20 | −2.46 |
| CAViaR | −1.66 | −1.87 | −1.55 | −2.59 | −2.22 | −2.08 | −2.56 |
| GEV | −1.84 | −2.42 | −1.99 | −4.47 | −2.99 | −2.80 | −6.97 |
| GPD | −2.11 | −2.35 | −1.67 | −4.43 | −2.63 | −2.71 | −6.51 |

The relative ranking depends on the criterion. RiskMetrics has the smallest unstarred frequency and independence adjustments in this table, whereas GARCH's resampled magnitude adjustment is smaller than RiskMetrics'. Cornish–Fisher performs poorly by these correction magnitudes despite its relatively small mean reported VaR. The table does not support ranking models by their mean threshold alone.

Units require care. The paper discusses corrections as proportions in places, whereas its additive equations and percent-labeled tables suggest return-scale changes. Appendix C.5 reports a largest historical frequency adjustment of 42.02 for historical simulation; dividing that number by $\sqrt{260}$ gives approximately 2.61, the corresponding daily figure in Table 3. This is consistent with an annualization relationship, not a statement that 2.61 means 2.61% of the baseline VaR. The article's various capital-ratio tables do not reconcile cleanly through a single ratio of the displayed mean threshold and adjustment. Accordingly, the entries above retain their printed labels and should not be fed into capital code as fractional multipliers without resolving the unit convention.

Figures 4 and 5 on PDF page 9 distinguish local time-varying corrections from the running historical maximum of correction magnitudes. The latter is monotone by construction: an extreme episode permanently increases the stored worst requirement. Such a running maximum can be implemented with information available at the time; using the final whole-sample maximum at the beginning of a backtest would instead introduce future information.

The horizon exercise randomly changes the starting date and asks how much of the full-sample maximum correction would have been discovered after different elapsed histories. The paper uses 30,000 starts and reports the minimum across starts at each horizon. Its discussion says about ten years can reveal roughly 80% of the maximum, while full discovery can require approximately 18 years for GEV and 46 years for CAViaR. Those figures describe this historical path and sampling construction, not a general sample-complexity bound. The appendix extends the comparison to ten-year, 2,600-observation estimation windows and a sample ending October 7, 2013. These are additional experiments with a different endpoint; they should not be merged silently with the four-year main specification.

Figure 7 compares empirical distributions of required corrections for historical and GARCH forecasts and annotates severe episodes. It makes the buffer's economic interpretation clear: selecting less than the historical maximum deliberately leaves some historical failures unprotected. No threshold in this chart certifies coverage of an unseen crisis, and the chart does not measure the opportunity cost of holding the associated capital.

## Cross-asset portfolios and stress comparisons

Table 4 uses daily asset-class indices from December 31, 1986 through November 28, 2011, with DataStream and Bloomberg as sources. Equity is a 95% MSCI Europe and 5% MSCI World combination. Real estate is represented by a European real-estate investment-services index, commodities by the CRB spot index, and bonds by a splice: Merrill Lynch US Treasury/Agencies Master AAA before January 1, 1998 and JPM EMU Global Aggregate Bond AAA thereafter. The splice changes the economic market represented by the bond series and should be preserved and examined in a replication. The liquidity index is not identified sufficiently for an exact rebuild.

The defensive allocation is 10% bonds and 90% liquidity. The balanced allocation has 30% equity, 10% real estate, 10% commodities, 40% bonds, and 10% liquidity. The aggressive allocation has 70% equity, 15% real estate, and 15% commodities. The baseline here is 95% GARCH VaR with a four-year window and 5% backtest significance. Portfolio rebalancing details, currency treatment, and transaction costs are not fully documented. Since the objective is risk calibration rather than trading profitability, no net strategy return should be inferred.

For the unstarred magnitude criterion, annualized corrections in Panel A are −44.80% for equity, −63.83% for real estate, −13.76% for commodities, and −18.44% for bonds. They are −1.04%, −15.79%, and −35.05% for the defensive, balanced, and aggressive portfolios. The corresponding reported capital ratios in Panel B are 2.56, 3.03, 2.41, 3.66, 3.00, 2.52, and 2.58. Across all criteria in that panel, the ratios range from 1.01 to 3.66; it would be inaccurate to characterize every historical correction as a factor between three and five.

Panel C compares these results with selected stress shocks: −30% equity, −40% real estate, −30% commodities, and −20% bonds, all on the source's annualized presentation. Under the magnitude column, stress-based ratios are 4.81, 4.99, 3.83, and 4.04 for the four assets, and 2.20, 5.10, and 6.10 for the three portfolios. Stress reserves are often larger, but not uniformly: the defensive portfolio's stress ratio 2.20 is below its historical magnitude-based ratio 3.00. These are alternative calibration constructions, not evidence that one has a universally correct failure probability.

The exercise is useful for exposing differences between a rule tied to observed model failures and a rule tied to a selected shock scenario. It does not establish the uniquely appropriate regulatory multiplier. Its ratios depend on the underlying VaR method, the chosen test, the scenario shocks, the sample history, and the incomplete operational definitions noted above.

## Appendix evidence and its limits

Appendix C.1 supplies an unconditional Gaussian-versus-Student example based on 100,000 simulated series of 250 daily returns. At 95%, 99%, and 99.5%, Gaussian thresholds are −29.49%, −41.88%, and −46.41%, while Student-$t_5$ ideal thresholds are −36.22%, −60.75%, and −72.87%. Pure specification corrections are therefore −6.73, −18.87, and −26.46 percentage points. This is a distinct unconditional illustration of tail misspecification; it should not be confused with the main conditional switching-GARCH calibration.

Tables C.2–C.4 are labeled Brownian, Lévy, and Hawkes experiments. They describe 250,000 simulated returns with common first moments, including mean 0.12% and standard deviation 1.02%, and give additional jump-process parameters. However, extensive numerical blocks are identical across all three tables, including rows labeled as specification and combined errors. The stochastic descriptions also blur jump sizes and jump intensities. Without code or clarification, these printed panels cannot be treated as three independently reproduced demonstrations of process-specific differences. Their repeated entries are reported here as a source limitation, not repaired by inventing replacement results.

Table C.5 associates the largest corrections with particular dates. For example, its unstarred frequency column gives 133.65 for Cornish–Fisher on May 13, 1915, 15.85 for RiskMetrics on March 28, 1938, and 18.24 for GARCH on March 24, 1938. Historical simulation's largest value, 42.02, occurs on February 9, 2009. These are adjustment magnitudes in the appendix's presentation, not asset returns realized on those dates.

Table C.6 contains conspicuous values that do not reconcile readily with the main text or neighboring columns. RiskMetrics' displayed ratios include 20.77, 57.18, 41.47, 36.84, and 101.69, and CAViaR also has unusually large entries. The note does not silently change decimal locations or use these entries as clean estimates of economically required capital. An exact numerical replication needs either the authors' code and original tables or an explicit reconciliation of those anomalies.

## Implementation plan and conclusions warranted by the evidence

A defensible reproduction starts by separating the baseline forecast layer from the buffer layer. For each date, estimate a chosen model on the preceding 1,040 observations, store its forecast distribution and 95% lower-tail threshold, then observe the next return. Once 250 genuinely prior forecast errors are available, search for the least buffer passing the chosen frequency, independence, or magnitude criterion. For magnitude, recalculate the PITs for each candidate using an explicit distribution-adjustment rule, such as the location-shift reconstruction above. Freeze that buffer before evaluating the following return. Record test failures, undefined likelihoods, missing model estimates, and empty acceptance sets rather than omitting them.

Implement each criterion separately first. Use event points from historical forecast gaps for hit-based tests and a suitably resolved numerical search for magnitude tests. Verify the likelihoods against hand-constructed hit sequences. Compare asymptotic and explicitly specified block-resampling critical values. Report the local buffer, its past running maximum, and a chosen historical quantile as distinct outputs. If all tests must pass simultaneously, compute the actual intersection of acceptance sets; taking the largest of separate minimum buffers is not automatically sufficient when acceptance is nonmonotone.

The replication specification must fix the return definition, currency, data calendar, baseline model equations, optimization settings, volatility initialization, EVT thresholds, predictive-CDF construction, annualization convention, buffer search grid, subsampling block length, and timing. It should provide an untouched future evaluation period for the buffer selection rule. The source does not supply all these inputs, so the paper supports implementation of the framework more strongly than exact recovery of every reported number.

The paper's evidence favors treating model validation as an ongoing source of measurable capital uncertainty. A small reported VaR is not necessarily a good risk model, different backtests reveal different defects, and a long history may be needed to encounter the episodes that determine a historical worst-case adjustment. Its empirical comparisons are informative diagnostics rather than proof that a calibrated buffer equals the unknown true quantile error. There is no transaction-cost-adjusted trading strategy, causal estimate of bank safety, or universal capital multiplier established by these experiments.
