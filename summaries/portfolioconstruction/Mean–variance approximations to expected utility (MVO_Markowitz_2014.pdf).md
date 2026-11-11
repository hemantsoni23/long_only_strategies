# Mean–variance approximations to expected utility

Harry Markowitz, European Journal of Operational Research 234 (2014), pp. 346–355, available online September 7, 2012. DOI 10.1016/j.ejor.2012.08.023. Source: [MVO_Markowitz_2014.pdf](../../Finance/MVO_Markowitz_2014.pdf), ten pages. This is a methodological review of approximation studies, including the author's geometric-mean and risk-measure comparisons; it is not one new unified portfolio experiment.

## Why this matters and the central argument

Normal returns and quadratic utility are sufficient settings for exact mean–variance representations, but they are not necessary conditions for a useful approximation in portfolio choice. Markowitz argues that the relevant practical question is whether an appropriately selected mean–variance efficient portfolio nearly maximizes the investor's expected utility. The article reviews evidence that two-moment approximations often do so for diversified portfolios and moderate utility curvature, while identifying failures involving very high risk aversion, bankruptcy, leverage, and extreme distributions.

This is a claim about approximation quality on a specified set of distributions and preferences. It is not a theorem that every concave utility can be represented exactly by mean and variance, nor a universal error bound for every return distribution. The distinction between an exact representation and a useful approximation is the essential contribution of the review. The paper's empirical comparisons are evidence supporting the latter under the conditions studied.

## Core mathematics: what is approximated

Let $R$ be a simple portfolio return in decimal units, $E=E[R]$, and $V=\operatorname{Var}(R)$. For a utility function $U$, the zero-centered and mean-centered second-order expansions are

$
Q_0(R)=U(0)+U'(0)R+\tfrac12U''(0)R^2,
$

$
Q_E(R)=U(E)+U'(E)(R-E)+\tfrac12U''(E)(R-E)^2.
$

The mean-centered approximation gives $E[U(R)]\approx U(E)+U''(E)V/2$. The linear term disappears on taking expectations. For log utility $U(R)=\log(1+R)$, equations (5)–(6) are

$
f_0(E,V)=E-\tfrac12(E^2+V),\qquad
f_E(E,V)=\log(1+E)-\frac{V}{2(1+E)^2}.
$

Both use two moments but are different functions. The second is generally much more accurate in the reviewed evidence. A pointwise approximation need not be exact to give a close expected value: deviations above and below the mean may partly cancel. Conversely, a good fit in a central interval does not by itself control the utility contribution from rare extreme losses. For log utility the domain $R>-1$ is indispensable.

The review gives a simple scale illustration. For a 30% loss, log utility is approximately $-.36$ and the zero-centered quadratic $-.35$. For a 40% gain, they are .34 and .32. The fit deteriorates farther away. These numerical comparisons concern total portfolio return and utility values, not percentage return errors. The article emphasizes that returns must be entered as fractions: 6% is .06, not 6. With beginning wealth of \$1 million, a 6% gain gives \$1.06 million, not \$7 million. Its critique of Loistl's pessimistic approximation results turns on this return/wealth scaling issue.

For any portfolio weights $w$, the identities

$
E_p=w^\top\mu,\qquad V_p=w^\top\Sigma w
$

hold whenever the relevant finite moments exist, regardless of normality, symmetry, or moderate fat tails. These identities alone do not prove that expected utility depends only on those moments. They make two-moment calculations straightforward; approximation of preferences remains a separate question.

## Explicit, approximate, and implicit optimization

The paper distinguishes three procedures. Explicit expected-utility optimization specifies a utility function and the joint return distribution and optimizes its expectation directly. Mean–variance approximate optimization specifies a utility but maximizes an approximation such as $f_E$ over an efficient frontier. Implicit optimization asks the investor to select a suitable portfolio from that frontier without eliciting a complete numerical utility function.

Markowitz argues that computational speed is no longer the main practical reason to avoid direct utility optimization. More persistent difficulties are estimating a complete joint distribution, eliciting individual utility, and explaining the decision problem. A factor or scenario model can supply covariance inputs, but an explicit expected-utility calculation generally demands more distributional structure. Reducing inputs does not make their estimation error disappear; it changes the modeling burden.

Implicit choice is useful only if the investor's selection is sufficiently careful and the relevant frontier adequately approximates the choices its utility would favor. The review does not specify a universal questionnaire or rule translating a vague risk tolerance into an optimal frontier point. Nor does high correlation between approximation and utility prove that every maximizer is close in welfare: small ranking errors near the optimum can matter, motivating optimization-premium and certainty-equivalent comparisons discussed later.

## Return utility, wealth utility, and risk-aversion scale

With current wealth $W_t$ fixed, next wealth is $W_{t+1}=W_t(1+R)$. Log utility changes by an additive constant when moving between utility of next wealth and utility of one plus return. Power utility changes by a positive multiplicative constant when the appropriate sign is used for increasing concave preferences. These transformations preserve rankings. Portfolio proportions under those forms can therefore be independent of beginning wealth in the stated one-period problem.

For exponential wealth utility $U(W)=-\exp(-aW)$, substituting $W_t(1+R)$ produces a return-utility curvature coefficient $b=aW_t$. The preferred return distribution can change as beginning wealth changes even if the wealth-utility function is constant. A mean–variance approximation can be recalculated at each decision date; it does not require the return-utility function to be fixed forever.

This scale distinction matters when interpreting the highly risk-averse examples. A coefficient such as $b=10$ belongs to a particular return/wealth normalization and cannot be interpreted independently of units. Utility values can be rescaled by positive affine transformations without changing choices, but rescaling the argument changes preferences unless parameters change consistently.

## Levy–Markowitz: distributions, fitting rule, and results

The reviewed 1979 study fits a quadratic through utilities at $E-k\sigma$, $E$, and $E+k\sigma$, trying $k=.01,.1,.6,1,2$. The value .01 generally performs best and is essentially the mean-centered local quadratic. For an empirical return series, exact average utility is $T^{-1}\sum_t U(R_t)$, compared with the two-moment approximation across a collection of assets or portfolios.

The first collection is 149 mutual funds with complete annual-return records over 1958–1967, drawn from Wiesenberger. Each fund's history is treated as a return distribution. For log utility, the Pearson correlation across distributions between average utility and its approximation is .997. For the listed positive-power utilities with exponents .1 through .9, correlations are .998–.999. These are approximation correlations, not correlations between predicted and future returns.

The stock collection consists of 97 randomly chosen US stocks with annual returns over 1948–1968 according to the review's prose. Its table heading broadly labels the historical comparison 1958–1967; the differing date descriptions should be checked against the original study rather than silently homogenized. For annual individual-stock log utility the correlation falls to .880. For monthly returns on those stocks it rises to .995, consistent with a narrower one-period return range.

Nineteen portfolios of five or six stocks are formed by randomly dividing the 97 stocks without replacement. The log-utility correlation for their annual distributions is .998. This supports the importance of even modest diversification in that dataset. It is not a universal theorem that five stocks suffice, nor an examination of concentrated portfolios in every crisis or market.

The difficult cases are highly curved exponential utility functions. For $U=-\exp[-b(1+R)]$, Table 2 reports mutual-fund correlations of .855 at $b=5$ and .447 at $b=10$. At $b=10$, corresponding annual individual-stock, monthly individual-stock, and small-portfolio correlations are .659, .899, and .768. Thus the same two-moment approximation can perform poorly when utility concentrates value on a narrow low-return region.

The review illustrates the mechanism using $E=.10$ and $\sigma=.15$. A rescaled exponential utility $-1000\exp[-10(1+R)]$ turns sharply near the mean and flattens toward its upper bound for gains. A quadratic cannot fit both regions well. Its value-of-a-blank-check discussion shows that such preferences favor a certain 10% gain over a 50–50 choice between breaking even and an arbitrarily enormous gain. Reported survey medians for the comparable certainty value are 401% of the investor's portfolio or 143% of total wealth, much higher than this example. The survey is external evidence reviewed here, not a new preference-estimation sample supplied with the article.

## Simaan: why a risk-free asset changes the approximation problem

Simaan's reviewed experiment assumes a one-factor return model $1+r_i=a_i+b_iF+u_i$, with a skewed Pearson Type III factor and jointly normal residuals that need not be independent. The portfolio constraint is only that weights sum to one. Ten randomly selected securities' monthly returns motivate the numerical illustration. The review does not supply the actual coefficients, factor parameters, or stock histories, so exact replication requires the original paper.

The welfare metric is an optimization premium: the extra return that must be added to the approximately optimal portfolio to make it as desirable as the explicitly optimized portfolio. This is more decision-relevant than a general correlation over many inferior portfolios. At $b=10$, the premium is .00323 per month without a risk-free asset and .00010 with one, approximately 32.3 and one basis points. At $b=100$ the figures are .05719 and .00001, or 571.9 and .1 basis points monthly. These are compensation amounts in that model, not trading alphas.

The mechanism is that an extremely risk-averse investor can choose a sufficiently safe total portfolio when the risk-free asset is available. Without it, the feasible set may force exposure to return ranges where the approximation is poor. The result is not uniformly monotone across every reported coefficient: at $b=2$ the premium is .00023 without and .00050 with the risk-free asset. Markowitz's practical emphasis concerns the high-curvature cases.

The review also reports difficulties when small exponential curvature parameters and unrestricted borrowing generate very large opposing long and short positions. Those outcomes are not taken as realistic unconstrained portfolio recommendations. Availability of a risk-free asset must be considered together with feasible leverage and bankruptcy constraints.

## Hlawitschka: option portfolios and higher Taylor orders

The reviewed option experiment uses monthly returns over ten years for eleven equally weighted portfolios, each containing twenty randomly chosen stocks. Calls are modeled as 5% out of the money when bought and priced with Black–Scholes. Call portfolios include 10% Treasury bills so simultaneous option expiry at zero does not wipe out all wealth. The cash allocation is material for log utility and should not be omitted from a reconstruction.

For stock portfolios, Spearman rank correlations between exact utility and quadratic approximation are one in six of seven cases and .9909 in the remaining exponential case. These are ranks of eleven portfolios, not Pearson correlations across thousands of observations. For call portfolios, the quadratic rank correlations include .9727 for log utility, .9545 for square-root utility, and .8364 for the most curved exponential case listed.

Higher order does not guarantee better finite truncation. For the call portfolios in Table 5, log utility's third-order rank correlation is $-.8636$, compared with .9727 at second order. Five of seven third-order correlations are negative. The sign is visible in the PDF and can be lost in extraction. Table 6 likewise shows log-utility correlations for individual-call-plus-cash distributions of .8764 at second order, $-.7527$ at third, .7304 at fourth, $-.7054$ at fifth, and .7469 at sixth.

These findings illustrate that convergence of an infinite Taylor series says little about the quality of a particular low-order truncation over a wide distribution. They do not prove that higher moments are always harmful. The distributions, expansion points, utility functions, and portfolio cash protection determine performance. Exact option maturity, volatility inputs, and construction details must be obtained from the original study; this review is not a self-contained options database.

## Ederington: resampled annual distributions

Ederington uses quarterly returns for 130 mutual funds over 1970–1979, forty quarters per fund. For each fund, 10,000 synthetic annual returns are generated by selecting four quarterly observations and compounding:

$
1+R_i=\prod_{j=1}^{4}(1+r_{ij}).
$

This is described as a semi-ex-ante, bootstrap-like exercise rather than a prospective forecast. The sampling assumes quarterly outcomes can be treated as serially independent draws for this purpose. It can create combinations more extreme than the observed annual paths but cannot introduce entirely new tail events absent from the quarterly empirical support. The review does not report random seeds or enough sampling-code detail for identical draws.

Three approximations are compared: the mean-centered quadratic; a fourth-order expression using actual third and fourth central moments; and a fourth-order near-normal expression that replaces those moments by their Gaussian relationships. With variance defined as $V$, those relationships are $M_3=0$ and $M_4=3V^2$. The printed text on p. 352 says $M_4=3V$, a dimensional error relative to its definition of variance. The squared-variance form is the correct Gaussian identity and is also consistent with the later fourth-order log formula.

For $\log(1+R)$, the correlations of exact utility with near-normal, quadratic, and actual-four-moment approximations are .9969, .9993, and .9995. Fourteen of twenty-two utilities have quadratic correlations above .99. More difficult preferences deteriorate: for $-\exp[-6(1+R)]$ the three correlations are .9469, .8526, and .9369; for $-(1+R)^{-5}$ they are .4721, .2324, and .4819. The near-normal two-moment formula can thus compete with actual higher-moment input in these experiments. That is an empirical approximation comparison, not evidence that the return distribution is actually Gaussian.

## Geometric-mean formulas and their domains

For positive gross returns, the geometric mean is $G=\exp(E[\log(1+R)])-1$. The review compares six approximations using mean and variance:

$
g_{Q0}=\exp[E-(V+E^2)/2]-1,
$

$
g_{QE}=\exp\left[\log(1+E)-\frac{V}{2(1+E)^2}\right]-1,
$

$
g_{EDD}=\exp\left[\log(1+E)-\frac{V}{2(1+E)^2}-\frac{3V^2}{4(1+E)^4}\right]-1,
$

$
g_{LMT}=E-V/2,\qquad
1+g_{NLN}=\frac{1+E}{\sqrt{1+V/(1+E)^2}}.
$

The final two-point approximation is reconstructed as

$
1+g_{HL}=\sqrt{(1+E)^2-V}.
$

For two equally likely returns $E-\sigma$ and $E+\sigma$, multiplying gross returns gives $(1+E)^2-\sigma^2=(1+E)^2-V$. The source's equation (18f) prints a plus/minus standard-deviation term instead, which is not the required product. The corrected form above is explicitly an algebraic repair. It requires positive admissible gross outcomes and a nonnegative radicand; it is not meaningful for an arbitrary mean–variance pair with bankruptcy exposure.

The near-lognormal formula is exact if gross return is lognormal. In general it is an approximation. The cited comparisons use commonly allocated asset classes and real equity returns for sixteen countries over 1900–2000, obtained through Morningstar EnCorr. The review reports that $g_{Q0}$ performs worst, then removes the simple limit and Ederington approximations from the preferred set. Among the remaining three, results vary by dataset, with $g_{NLN}\geq g_{QE}\geq g_{HL}$ under their relevant domain. No universal best formula for every distribution is claimed.

## Alternative risk measures: what the experiment measures

The final comparison fits the log arithmetic–geometric gap

$
\Delta L=\log(1+E)-\log(1+G)
$

as $\beta f(RM)$ with zero intercept, across return series in each database. The zero-intercept rationale is that the gap is zero for a constant return. Variance, mean absolute deviation, semivariance, VaR and CVaR transformations are compared. This tests approximation of one log-growth quantity; it does not test whether VaR or CVaR is useful for every solvency or tail-risk mandate.

Raw VaR treats observed returns as an equally likely empirical support at approximately a 5% tail level. Interpolated VaR smooths between the relevant ordered returns in the asset-class data. For the 101-observation country histories, the fifth-worst return gives the paper's empirical tail cutoff. CVaR averages returns at or below the raw-VaR threshold. Precise sign conventions and the transformation applied to each risk measure must be kept consistent with the fitted gap.

In percentage units, the asset-class root-mean-squared errors are .05 for variance divided by $(1+E)^2$, .10 for unadjusted variance, .11 for semivariance, .51 for raw MAD, .65 for raw VaR, and .48 for CVaR. For the sixteen-country series they are .18, .17, .35, .70, .68, and .55 respectively. Squared and rescaled tail measures improve some results but do not overtake variance in those tables. These are in-sample cross-series approximation residuals with a fitted slope, not out-of-sample portfolio returns.

The text interprets twice an RMS error as a rough confidence interval, for example ten basis points around an asset-class estimate using adjusted variance. Without a distributional and sampling argument, twice a fitted residual RMS is not automatically a calibrated 95% prediction interval. The table's precision should not be promoted into a universal statistical guarantee.

## Reimplementation scope, limitations, and use

A reconstruction can implement the quadratic formulas, calculate exact utility under a stated empirical distribution, and compare ranks, correlations, certainty equivalents, or optimization premiums. Reproducing each published experiment exactly requires its original securities, return histories, utility parameters, portfolio constraints, and simulation details; this review does not print them all. The different metrics answer different questions and should not be merged into one apparent accuracy statistic.

Bankruptcy is an explicit boundary. The review notes unfavorable examples involving extreme binary returns, unrestricted borrowing, or insufficient constraints keeping wealth positive. High approximation correlations in historical diversified portfolios cannot rule out missing rare tail states, and finite means and variances do not ensure every utility expectation exists. Nor does selecting a mean–variance frontier solve the estimation of future means and covariances.

The defensible practical conclusion is to validate a two-moment approximation on the actual portfolio return range, utility curvature, cash allocation, and feasible constraints. Exact Gaussian or quadratic assumptions are not necessary for such validation. Equally, convenience is not a substitute for checking utility-domain violations or economically important approximation error. The review's evidence supports mean–variance as a useful approximation in many settings while providing concrete reasons to test rather than presume its adequacy.
