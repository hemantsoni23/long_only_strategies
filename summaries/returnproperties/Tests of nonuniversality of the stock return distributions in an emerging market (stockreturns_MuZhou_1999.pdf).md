# Tests of nonuniversality of the stock return distributions in an emerging market

Guo-Hua Mu and Wei-Xing Zhou. *Physical Review E* 82, 066103, published December 2, **2010**. DOI: 10.1103/PhysRevE.82.066103.

Source: [original published PDF](../../Finance/stockreturns_MuZhou_1999.pdf), eight pages. The basename says 1999, but the title page, receipt/revision dates, DOI, journal volume, and copyright establish 2010. Page references below use the article's numbered pages 066103-1 through 066103-8. All figures and Table I are in the local source; no separate appendix is included.

## Why this matters

An approximately inverse-cubic return tail is often treated as a common empirical regularity. Mu and Zhou ask a more discriminating question: after normalizing each stock to the same mean and variance, do tail exponents still vary systematically with turnover and capitalization? Their Chinese A-share sample provides evidence that they do, particularly at one- and five-minute horizons. Smaller capitalization and higher turnover are associated with heavier standardized tails.

The contribution is cross-sectional testing of a purported universal shape, using both grouped and individual-stock estimates and two different approaches to fitting tails. The paper does not propose a trading strategy. Its relevance is to risk modeling: a common volatility scale does not necessarily imply a common extreme-event distribution. Pooling all stocks under one tail exponent can conceal systematic heterogeneity even after standardization.

The longer-horizon conclusion is more tentative. Many associations weaken at fifteen or thirty minutes, but several negative-tail coefficients remain statistically significant. Failure to reject a slope in some specifications does not establish a universal distribution. The numerical results should therefore take priority over broad language suggesting that all longer-horizon tails become alike.

## Sample and return construction

Section II starts from a database of 1,232 A-share stocks traded on the Shanghai and Shenzhen exchanges from January 2004 through June 2006. Quotes disseminated to investors were recorded every six to eight seconds. These are public quote snapshots, not a complete sequence reconstructed from exchange order messages. The source explicitly distinguishes this information set from an ultrahigh-frequency order-flow database.

The maximum observed number of trading days per stock is 591. Stocks with fewer than 550 days are excluded, leaving 978 companies. Missing days can arise from suspensions, new listings, delistings, and other causes. The resulting universe is therefore a long-coverage subset of the database, not literally every A-share stock without qualification. Excluding short histories can affect the distribution of extreme observations and the cross-sectional relation with firm characteristics.

Returns are constructed at $\Delta=1,5,15,30$ minutes:

$$
r_i(t,\Delta)=\log S_i(t)-\log S_i(t-\Delta).
$$

Only within-day returns are used, deliberately eliminating overnight changes. This differs materially from studies that compress nontrading time but retain close-to-open returns. For each stock and each horizon separately, standardize using its sample mean and standard deviation:

$$
z_i(t,\Delta)=\frac{r_i(t,\Delta)-\bar r_i(\Delta)}{s_i(\Delta)}.
$$

The authors subsequently call these normalized quantities returns; this note uses $z$ when clarity requires distinguishing them from raw log returns. Each series has sample mean zero and variance one. Normalization does not change the asymptotic power exponent under a fixed positive affine scale, but it changes where a finite-sample numerical threshold lies. It also uses full-sample information, so it is a descriptive normalization rather than an implementable real-time volatility forecast.

The paper does not fully specify the snapshot-to-minute sampling rule, stale quotes, auction observations, lunch-break boundaries, overlapping versus nonoverlapping returns, corporate-action adjustment, bad-tick filters, or treatment of intraday missing data. A reproduction must document those choices. It should not import the overnight convention or sampling rules from an unrelated US study simply because the same tail estimators are used.

## Turnover and capitalization variables

For stock $i$, traded value within a minute is the sum of trade price times share volume:

$$
v_{i,t}=\sum_{j\in\text{minute }t}q_{i,j}p_{i,j}.
$$

Average over the available one-minute intervals to obtain $\bar v_i$. Turnover is measured as average traded value divided by capitalization, $\tau_i=\bar v_i/c_i$. This is a monetary-value turnover proxy, not the raw number of transactions and not automatically the same as shares traded divided by free float at each instant.

Section IV defines capitalization using **tradable shares**, multiplied by price at the beginning of the database records. During the sample, the paper says only about one-third of outstanding shares were tradable. Using total capitalization or a continuously updated float-cap series would change the explanatory variable. The source does not give a full protocol for later changes in tradable share counts or partial histories. The fixed beginning-of-record definition should be retained and its limitations recorded.

Because multiplying the time interval multiplies average traded value by a common factor under the authors' construction, the one-minute turnover variable is used at all four horizons. In a regression on its logarithm, changing common units shifts the intercept but does not change the slope. This does not mean minute-by-minute turnover is constant, nor that all stocks have the same intraday pattern.

Two separate grouping exercises sort the 978 stocks by turnover and by capitalization, respectively, then divide each ordering into 20 groups containing almost equal numbers of firms, approximately 48–49 each. At a fixed horizon, concatenate all standardized return observations from stocks in a group. The groups are not portfolios: returns are pooled as observations, not summed or averaged across stocks at each timestamp. The pooling implicitly gives more weight to firms with more available observations, even though group stock counts are similar.

For turnover groups, the group regressor is the average of stock turnover ratios. For size groups, it is average capitalization. Logarithms are applied after forming these group averages in the reported equations. A mean of logarithms or a ratio of separately averaged quantities is generally a different statistic. The two groupings contain different stocks, which is why the bivariate exercise later uses individual-company tail estimates.

## Whole-distribution Student-t or q-Gaussian fitting

The first estimation method fits a symmetric Student-t family, described as a q-Gaussian, to each group's normalized-return distribution. A consistent parameterization of the density intended by equation (5) is

$$
f(z;\alpha,L)=
\frac{\sqrt L\,\alpha^{\alpha/2}}{B(1/2,\alpha/2)}
\left(\alpha+Lz^2\right)^{-(\alpha+1)/2},
\qquad \alpha>0,\ L>0.
$$

Here $\alpha$ is the degrees of freedom and the survival-tail index, while $L$ is an inverse scale parameter. The density decays as $|z|^{-(\alpha+1)}$. The printed formula mixes an undefined symbol $n$ in its normalization with $\alpha$ in the kernel. The expression above sets the intended degrees-of-freedom symbol consistently and integrates to one; it is an algebraic clarification, not a claim to have recovered the authors' code.

For $\alpha>2$, this parameterization has variance $\alpha/[L(\alpha-2)]$. Enforcing unit model variance would require $L=\alpha/(\alpha-2)$. Although empirical returns are standardized, the paper does not clearly say whether the fit imposes that model restriction or estimates $L$ freely. This is a replication choice with consequences for the fitted shape. Likewise, it does not provide the fitting objective, density-bin scheme, numerical optimizer, weighting of tail versus center, starting values, or constraints.

The symmetric fit returns one exponent for both signs and is influenced heavily by the center, where most observations lie. Tick-size discreteness creates visible irregularity around zero at short horizons. A good whole-distribution fit therefore does not establish a correct extreme-tail exponent or sign symmetry. The authors explicitly introduce a second estimator because central observations can dominate the q-Gaussian fit.

## Tail-only estimation and an equation defect

The second approach follows the Clauset–Shalizi–Newman strategy: choose a lower tail cutoff, estimate a power-law exponent above it, calculate the Kolmogorov–Smirnov distance between the empirical and fitted tail, and select the cutoff minimizing that distance. Positive and negative tails are treated separately; negative returns must first be converted to positive magnitudes.

For a continuous Pareto survival tail above cutoff $u$,

$$
\Pr(X\ge x\mid X\ge u)=(x/u)^{-\alpha},\qquad x\ge u,
$$

the conditional density is $\alpha u^\alpha x^{-(\alpha+1)}$. Differentiating the log likelihood yields the continuous maximum-likelihood estimate

$$
\widehat\alpha(u)=\frac{N_u}{\sum_{j:X_j\ge u}\log(X_j/u)}.
$$

For each candidate cutoff, calculate

$$
D(u)=\sup_{x\ge u}\left|\widehat F_u(x)-\left[1-(x/u)^{-\widehat\alpha(u)}\right]\right|,
$$

and minimize $D(u)$ over the permitted candidates. This gives an explicit reproducible continuous implementation of the method described in the text.

**The source's equation (7) cannot be implemented literally as continuous Pareto MLE.** As printed, it multiplies $N$ by a sum of logarithms rather than dividing by that sum, and uses $r_{\min}-0.5$ inside the logarithm. A half-unit continuity correction is associated with approximations for integer-valued power laws; it is not automatically appropriate for standardized continuous returns, whose values are not observations on a common unit integer lattice. The original code is unavailable, so one cannot determine from the article whether this is only a typesetting error or which correction was used in the reported estimates. A careful reproduction should distinguish literal-formula diagnostics from the coherent continuous estimator above and request the original implementation before claiming exact numerical agreement.

The paper does not report chosen cutoffs, tail counts, all candidate restrictions, bootstrap goodness-of-fit probabilities, or comparisons against lognormal and stretched-exponential alternatives. Selecting a cutoff by KS minimization alone does not prove that the power law is the correct population model. It identifies the best fit under that procedure. Serial dependence, cross-stock dependence, and estimation error in the normalized series also affect uncertainty.

## Turnover regressions

For a grouped or individual estimate, fit the descriptive cross-sectional relation

$$
\widehat\alpha=A+B\log\tau+e.
$$

A negative $B$ means that higher turnover is associated with a smaller tail index, hence a heavier standardized tail. It is not a statement about the unconditional variance, because the observations have already been variance-normalized.

For the q-Gaussian estimates across the 20 turnover groups, the source reports:

| Horizon | Slope $B$ | Reported $p$ | $R^2$ |
|---|---:|---:|---:|
| 1 minute | −0.10 ± 0.03 | 0.001 | 0.45 |
| 5 minutes | −0.15 ± 0.04 | 0.003 | 0.39 |
| 15 minutes | −0.06 ± 0.05 | 0.280 | 0.06 |
| 30 minutes | 0.00 ± 0.07 | 0.972 | 0.00 |

These results support turnover-related heterogeneity at one and five minutes under the whole-distribution fit. The apparent decline in slope magnitude is not monotone between one and five minutes; it is a broad short-versus-long horizon pattern.

The tail-only grouped estimates provide a sign-specific check:

| Horizon | Positive slope; $p$; $R^2$ | Negative slope; $p$; $R^2$ |
|---|---|---|
| 1 minute | −0.15 ± 0.04; .001; .47 | −0.20 ± 0.02; printed .000; .87 |
| 5 minutes | −0.10 ± 0.04; .010; .31 | −0.17 ± 0.02; .001; .75 |
| 15 minutes | −0.04 ± 0.10; .700; .01 | −0.09 ± 0.04; .026; .25 |
| 30 minutes | 0.11 ± 0.12; .380; .04 | −0.10 ± 0.05; .050; .20 |

A printed $p=.000$ is a rounded small number, not an exact probability of zero. The negative tail retains evidence of a turnover association at fifteen minutes, and the thirty-minute result is borderline by the reported value. Thus the statement that no longer-horizon evidence exists would be inaccurate.

Individual-company tail estimates reduce the risk that pooling alone creates the relation. Their turnover slopes are −0.23 and −0.24 for positive and negative one-minute tails, with $R^2=.07$ and $.08$. At five minutes they are −0.06 and −0.13, with $R^2=.01$ and $.04$. At fifteen minutes they are −0.05 and −0.13, with reported $p=.046$ and rounded .000. At thirty minutes they are −0.02 ($p=.665$) and −0.09 ($p=.015$). Most stock-level explanatory power is low even when a coefficient is significant. Grouped $R^2$ values should not be substituted for these individual-stock values.

## Capitalization regressions

The parallel size specification is

$$
\widehat\alpha=A+B\log c+e.
$$

A positive slope means larger tradable capitalization is associated with lighter standardized tails. The grouped results from Figure 6 and Section IV are:

| Horizon | q-Gaussian slope | Positive tail-only slope | Negative tail-only slope |
|---|---:|---:|---:|
| 1 minute | 0.06 ± 0.02 | 0.15 ± 0.02 | 0.14 ± 0.02 |
| 5 minutes | 0.16 ± 0.03 | 0.11 ± 0.03 | 0.14 ± 0.02 |
| 15 minutes | 0.11 ± 0.04 | 0.08 ± 0.07 | 0.05 ± 0.03 |
| 30 minutes | −0.02 ± 0.05 | 0.02 ± 0.07 | 0.03 ± 0.03 |

At one minute, grouped positive- and negative-tail size regressions have $R^2=.80$ and $.76$, with rounded $p=.000$; the q-Gaussian result has $R^2=.45$ and $p=.001$. At five minutes, corresponding $R^2$ values are .49, .79, and .55. At fifteen minutes, q-Gaussian fitting reports $p=.010$, whereas positive and negative tail-only fits report .253 and .104. At thirty minutes, none of the grouped size slopes is significant by conventional thresholds in the reported tests.

Individual-stock size slopes are approximately 0.22 for both one-minute tails, 0.06/0.09 for five-minute positive/negative tails, 0.05/0.06 at fifteen minutes, and 0.01/0.01 at thirty minutes. The one-minute $R^2$ values are .10 and .12; they fall to .01/.04 at five minutes and .01/.01 at fifteen minutes. These statistics again show a systematic but incomplete explanation of cross-sectional tail variation.

The source has small reporting discrepancies between plotted error labels, prose, and Table I—for example, the negative one-minute size slope's uncertainty is shown as 0.02 in Figure 7 and 0.03 in the table/prose. Significance descriptions also occasionally overstate what the printed $p$ values support. The numerical tables and explicit reported probabilities are preferable to silently harmonizing those inconsistencies. No new corrected significance test is claimed here.

## Joint regressions and the dependence between regressors

Using the individual-stock tail estimates, Section V fits

$$
\widehat\alpha_i=A+B_\tau\log\tau_i+B_c\log c_i+e_i.
$$

The following reproduces the bivariate rows of Table I. Parentheses retain the paper's uncertainty digits: for example, −0.07(4) denotes the printed estimate with uncertainty 0.04. The caption describes these as error bars at the 5% significance level, but their relationship to the significance stars is not consistently clear. They should not be silently reinterpreted as a fully documented standard-error estimator. Stars are the source's labels: one for 10%, two for 5%, three for 1%.

| Horizon | Positive $B_\tau$ | Positive $B_c$ | Negative $B_\tau$ | Negative $B_c$ |
|---|---:|---:|---:|---:|
| 1 minute | −0.07(4)* | 0.18(3)*** | −0.06(3)* | 0.19(3)*** |
| 5 minutes | −0.02(3) | 0.05(2)** | −0.09(3)*** | 0.04(2)** |
| 15 minutes | −0.01(3) | 0.04(3)* | −0.14(3)*** | −0.01(3) |
| 30 minutes | −0.01(5) | 0.01(4) | −0.15(5)*** | −0.07(4)** |

At one minute, capitalization remains strongly associated with the tail index, while turnover loses much of its univariate significance. At fifteen and thirty minutes, the negative-tail joint regression has a sizeable turnover coefficient; the thirty-minute capitalization coefficient even reverses sign. These are not evidence for a simple universal long-horizon exponent, and they do not support an unqualified claim that the two signs behave identically.

The authors observe that average traded value and capitalization obey an approximate scaling relation

$$
\bar v_i\propto c_i^{0.47\pm0.02}.
$$

Since $\tau_i=\bar v_i/c_i$, the fitted relationship implies approximately $\log\tau_i=\text{constant}-0.53\log c_i$ plus residual variation. This algebra explains why the two explanatory variables are strongly related and why adding one can alter the other's coefficient. It also makes clear that turnover already contains capitalization in its denominator.

The paper describes correlated regressors as making the bivariate specification ill specified. Correlation alone does not invalidate OLS or establish misspecification; exact collinearity prevents separate identification, while high collinearity weakens precision and makes partial coefficients sensitive. Endogeneity, omitted variables, nonlinearities, and measurement error would require additional arguments. This distinction is an interpretive correction to the source's explanation, not a new empirical diagnosis from the unavailable raw data.

Neither the grouped nor individual regressions identify a causal effect of turnover or size. Firm liquidity, price discreteness, industry, information arrival, suspensions, and selection can be related to both characteristics and tails. Tail indices are themselves estimated dependent variables with unequal precision, but the paper does not provide an errors-in-variables or hierarchical treatment of that first-stage uncertainty. Nor does it describe a correction for the many horizons, signs, estimators, and regressions tested.

## What “nonuniversality” does and does not establish

The evidence against a single characteristic-independent short-horizon tail index is strongest at one and five minutes, where both estimation approaches and individual-stock checks broadly agree. All estimated individual-stock tail indices are reported above two, outside the non-Gaussian stable Lévy range. That is an empirical statement about estimates, not a proof of finite population variance. The mean fitted index increases with horizon, consistent with thinner standardized tails under aggregation.

At fifteen minutes the evidence depends on sign and estimator; at thirty minutes many univariate slopes are near zero, but some negative-tail effects remain. A nonsignificant relation with these two characteristics does not prove that all stocks have the same exponent, that other characteristics are irrelevant, or that their full distributions coincide. The paper's suggestion of possible universality at larger horizons is appropriately a conjecture, not a demonstrated equivalence result.

The comparison with mature markets is based on earlier studies, rather than a matched contemporaneous US/UK/France control panel re-estimated using the same data filters. Different universes, sampling clocks, price limits, tick regimes, and estimator choices could affect the comparison. This note therefore treats the contribution as documented heterogeneity in this Chinese sample, rather than proof of a permanent developed-versus-emerging-market divide.

## Reproduction design and remaining gaps

A reconstruction should first reproduce the 1,232-to-978 coverage filter and save each exclusion reason. Build within-day log returns at all four horizons, standardize each company independently, calculate beginning-of-record tradable capitalization and average one-minute value turnover, then create the two separate equal-count groupings. Save stock assignments and observation counts so that pooling can be checked.

Fit the Student-t family under an explicitly stated normalization constraint and objective. Independently estimate positive and negative Pareto tails with documented cutoff candidates, minimum tail counts, and the corrected continuous likelihood. Reproduce both grouped and individual regressions, retaining exact regressor definitions, signs, horizons, uncertainty conventions, and $R^2$. Finally, reproduce the joint regressions and the traded-value/capitalization scaling comparison. The purpose is to understand heterogeneity, not to maximize the number of significant coefficients.

Exact numerical reconstruction is limited by absent raw snapshots and cleaning rules, the q-Gaussian fitting objective, the defective printed tail-estimator formula, missing chosen cutoffs, unspecified uncertainty calculations, and incomplete treatment of intraday market mechanics. The paper provides no trading costs, execution assumptions, forecast validation period, or portfolio results because those are outside its design. Its substantive implication remains clear: volatility normalization can leave economically meaningful cross-sectional tail differences, and evidence that those differences weaken with horizon must be evaluated specification by specification.
