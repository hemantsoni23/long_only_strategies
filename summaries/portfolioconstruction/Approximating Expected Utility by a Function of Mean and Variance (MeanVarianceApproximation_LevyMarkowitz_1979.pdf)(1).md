# Approximating Expected Utility by a Function of Mean and Variance

H. Levy and H. M. Markowitz, *The American Economic Review* 69(3), June 1979, 308–317.

Source: [MeanVarianceApproximation_LevyMarkowitz_1979.pdf](../../Finance/MeanVarianceApproximation_LevyMarkowitz_1979.pdf). The PDF consists of a JSTOR cover followed by the ten printed article pages. It is a scanned document; the equations, tables, footnotes, and references were inspected visually. References below use printed pages.

## Why this matters

A mean–variance description need not be an exact expected-utility representation to be useful for choosing a portfolio. Levy and Markowitz ask whether a well-chosen mean–variance-efficient portfolio can have expected utility close to the best available, even when utility is not quadratic and returns are not assumed normal. They construct a family of approximations using only the portfolio mean and variance, test it on historical return distributions, and explain why the approximation can work in ordinary diversified portfolios yet deteriorate for more speculative payoffs or sharply curved utility.

The paper's contribution is constructive. It gives an explicit approximation that can be computed without knowing higher moments, an error analysis that is meaningful across candidate portfolios, and empirical comparisons with directly calculated expected utility. It also distinguishes a quadratic function used as a local numerical approximation from a globally quadratic preference function. The latter distinction answers a common objection: fitting a new quadratic around each candidate distribution does not force an investor to retain one quadratic utility of wealth forever.

The reported empirical results concern historical-distribution approximation, not forecasting or a tradable anomaly. The authors do not recommend treating unadjusted historical observations as correct future probabilities. A reproducing researcher should first reproduce the utility comparisons on the historical samples; any rolling estimation, portfolio optimization, or prospective allocation test is an additional experiment.

## Utility and the approximation family

Let $R$ be a one-period net return, expressed as a fraction, with mean $E$, variance $V$, and standard deviation $\sigma=\sqrt V$. Let $U(R)$ be utility of that return. For the logarithmic and power examples, the economically relevant domain is $R>-1$. In this note, $E$ without brackets denotes the mean return, while $\mathbb E[\cdot]$ denotes expectation, avoiding the source's overloaded notation.

A Taylor approximation about zero gives

$$
\mathbb E[U(R)]\approx U(0)+U'(0)E+
\frac12U''(0)(E^2+V).
$$

A Taylor approximation about the candidate portfolio's own mean gives

$$
f_0(E,V;U)=U(E)+\frac12U''(E)V.
$$

The latter typically performed better in the motivating earlier tests discussed on p. 309. The distinction is material: recentering changes both the utility level and local curvature used for each candidate portfolio. It is not equivalent to selecting a single quadratic function and applying it everywhere.

For $k>0$, the authors fit a quadratic through three utility evaluations at $E-k\sigma$, $E$, and $E+k\sigma$. Write

$$
Q_k(R)=a_k+b_k(R-E)+c_k(R-E)^2.
$$

The interpolating coefficients are

$$
a_k=U(E),
$$

$$
b_k=\frac{U(E+k\sigma)-U(E-k\sigma)}{2k\sigma},
$$

$$
c_k=\frac{U(E+k\sigma)+U(E-k\sigma)-2U(E)}{2k^2\sigma^2}.
$$

Because $\mathbb E[R-E]=0$ and $\mathbb E[(R-E)^2]=V$, the expected quadratic is

$$
f_k(E,V;U)=\mathbb E[Q_k(R)]
=U(E)+\frac{U(E+k\sigma)+U(E-k\sigma)-2U(E)}{2k^2}.
$$

These are equations (11)–(16), p. 310. The factor $\sigma^2$ disappears from the final denominator because it cancels against the variance multiplying $c_k$. Losing that cancellation changes the approximation substantially.

At $k=1$, this becomes the average of two utility evaluations:

$$
f_1=\frac{U(E+\sigma)+U(E-\sigma)}{2}.
$$

For logarithmic utility this is

$$
f_1=\frac{\log(1+E+\sigma)+\log(1+E-\sigma)}2.
$$

As $k\to0$, the centered second difference converges to $U''(E)V$, so $f_k\to f_0$. A deterministic portfolio with $\sigma=0$ should be handled directly as $f_k=U(E)$; it does not require dividing by the interpolation coefficients' vanishing denominators.

The evaluation points must lie inside the utility domain. For the return utilities used here, the authors require $E-k\sigma>-1$ for all portfolios under consideration. A historical portfolio may never have lost everything while its mean-minus-multiple-of-standard-deviation falls below $-1$. The approximation is then undefined for log utility even though the observed utility average is finite. This is a domain failure that should be reported, rather than repaired by clipping the input without disclosure.

## Why the approximation selects an efficient portfolio

Dependence on only two moments is not by itself enough to guarantee that maximizing an approximation selects a mean–variance-efficient portfolio. The approximation must also prefer greater mean and lower variance over the relevant domain.

The sufficient utility conditions used on p. 310 are $U'>0$, $U''<0$, and $U'''\ge0$. For fixed mean,

$$
\frac{\partial f_k}{\partial\sigma}
=\frac{U'(E+k\sigma)-U'(E-k\sigma)}{2k}<0.
$$

Concavity makes marginal utility lower at the higher evaluation point. For fixed variance,

$$
\frac{\partial f_k}{\partial E}
=U'(E)+\frac{U'(E+k\sigma)+U'(E-k\sigma)-2U'(E)}{2k^2}>0.
$$

The third-derivative condition makes $U'$ convex, so the centered difference is nonnegative. Consequently, a portfolio dominated in mean and variance cannot maximize $f_k$. This is the formal connection between the approximation and the efficient set. It does not claim that every point on the frontier is equally desirable, or that the investor's optimal point can be inferred without a utility preference.

The utilities tested include logarithmic utility, power utility $(1+R)^a$ with $0<a<1$, and negative exponential utility $-\exp[-b(1+R)]$ with $b>0$. They satisfy these derivative conditions on the appropriate return domain. The utility parameters control curvature; they are not estimated from the data or optimized to improve investment returns.

## Error analysis: what should be small

Define pointwise approximation error and its expectation by

$$
d_k(R;E,V,U)=U(R)-Q_k(R),\qquad
D_k=\mathbb E[d_k(R)]=\mathbb E[U(R)]-f_k.
$$

The average error is determined jointly by the error function and where a portfolio's return probability lies. A poor fit in a remote region need not dominate expected utility if little probability lies there. Conversely, apparently good fit near the mean can be misleading when a substantial tail probability reaches a region of rapidly changing utility.

Table 1, p. 311, illustrates this for logarithmic utility, $E=0.10$, and $\sigma=0.15$. For the mean-centered Taylor approximation $k=0$, the pointwise errors at returns $-0.30$ and $+0.60$ are approximately $-0.02233$ and $+0.02345$. They are much smaller around the mean. Of the mutual-fund distributions with means near 10%, the observed annual outcomes lie between a 30% loss and a 60% gain; 64 funds have mean returns between 8% and 12% and fall inside that range.

The paper also considers a worst-case discrete calculation over returns from $-0.30$ to $+0.60$ in increments of 0.05 while fixing the mean at 0.10. It reports a distribution placing probability $3/8$ at $-0.30$ and $5/8$ at $+0.35$, giving average error about $-0.00649$. These printed weights are inconsistent with the stated constraint: they produce mean 0.10625 and exact logarithmic-utility error about $-0.006245$. Holding those two support points and enforcing mean 0.10 requires probabilities $5/13$ and $8/13$, which give error about $-0.006491$. The latter is a direct recalculation, not an official erratum.

The numerical exercise as described fixes the mean and support, not the variance as an additional constraint. Therefore it should not be presented as a sharp worst-case bound over distributions with both the stated mean and the illustrative $\sigma=0.15$. Its purpose is to show how return concentration and cancellation affect expected approximation error.

Absolute utility errors are not economically interpretable without normalization. Multiplying utility by a positive constant multiplies both exact and approximate expected utilities and their errors, while leaving preferences unchanged. The authors therefore relate error variation to variation in the approximate expected utilities across the candidate distributions.

Let $\sigma_D$ be the cross-candidate standard deviation of expected errors and $\sigma_f$ that of $f_k$. Put $\gamma=\sigma_D/\sigma_f$. For $0\le\gamma<1$, the correlation satisfies

$$
\operatorname{Corr}(\mathbb E[U],f_k)\ge\sqrt{1-\gamma^2}.
$$

To reproduce the argument in the footnote to equation (20), let $r=\operatorname{Corr}(f_k,D_k)$. Since exact expected utility is $f_k+D_k$,

$$
\operatorname{Corr}(f_k,f_k+D_k)
=\frac{1+\gamma r}{\sqrt{1+\gamma^2+2\gamma r}}.
$$

Minimizing over feasible $r\in[-1,1]$ gives the minimum at $r=-\gamma$, yielding the bound. If $f_k$ varies ten times as much as the error, $\gamma=0.1$ and the lower bound is $\sqrt{0.99}\approx0.995$. This is a bound on cross-sectional agreement across candidate distributions. It is not a confidence interval, a time-series return correlation, or an out-of-sample performance statistic.

High correlation also does not logically guarantee identical maximizers: small ranking errors near the top can matter. The authors accordingly examine whether approximation-based selection finds the exact-utility winner in their finite candidate sets. Their evidence on that question is reported below, separately from the correlation bound.

## Historical experiments and reported results

The principal sample comprises 149 investment companies with annual returns available throughout 1958–1967 in annual editions of A. Wiesenberger and Company's *Investment Companies*. Each fund supplies one historical distribution, and each utility specification supplies one comparison across the 149 distributions. This is a complete-history selection rule. The article does not give the fund identifiers, a machine-readable return panel, or all underlying accounting conventions needed to reconstruct the raw data exactly.

For each distribution, compute the empirical mean and variance, the empirical average of $U(R)$, and $f_k(E,V;U)$. Table 2 uses $k=0.01,0.1,0.6,1.0,2.0$. The paper does not calculate $k=0$ correlations directly, but infers that continuity makes them close to the $k=0.01$ results. A replication should report $k=0$ separately if it computes that limit analytically; it should not label the printed $0.01$ column as exactly zero.

Selected correlations from Table 2 are:

| Utility | $k=0.01$ | $k=0.1$ | $k=0.6$ | $k=1$ | $k=2$ |
|---|---:|---:|---:|---:|---:|
| $\log(1+R)$ | 0.997 | 0.997 | 0.997 | 0.995 | 0.983 |
| $(1+R)^{0.1}$ | 0.998 | 0.998 | 0.998 | 0.997 | 0.988 |
| $(1+R)^{0.5}$ | 0.999 | 0.999 | 0.999 | 0.999 | 0.998 |
| $(1+R)^{0.9}$ | 0.999 | 0.999 | 0.999 | 0.999 | 0.999 |
| $-\exp[-(1+R)]$ | 0.997 | 0.997 | 0.997 | 0.996 | 0.995 |
| $-\exp[-3(1+R)]$ | 0.949 | 0.949 | 0.941 | 0.924 | 0.817 |
| $-\exp[-5(1+R)]$ | 0.855 | 0.855 | 0.852 | 0.837 | 0.738 |
| $-\exp[-10(1+R)]$ | 0.447 | 0.449 | 0.503 | 0.522 | 0.458 |

The remaining power exponents are 0.3 and 0.7, and the remaining exponential parameters are 0.1 and 0.5; these have correlations at or near 0.999 for small $k$. The important exception is high exponential curvature, not a uniformly excellent fit across all utilities. For $b=10$, increasing $k$ first improves correlation, but the overall approximation remains poor. The authors note that an unreported $b=20$ experiment is an even stronger exception; they do not provide a table of its numerical results.

The introductory $k=1$ examples additionally report regressions of actual expected utility on approximated expected utility. For log utility, actual equals $0.002+0.996$ times estimated, with correlation 0.995. For square-root utility, actual equals $-0.013+1.006$ times estimated, with correlation 0.999. In both examples the fund maximizing the approximation also maximizes directly computed historical expected utility. These intercepts and slopes are in the stated utility normalization, not percentage returns or alphas.

The second data source consists of 97 U.S. common stocks over 1948–1968. The authors began with 100 stocks randomly selected from CRSP subject to complete return availability over the period; mechanical problems reduced the usable sample to 97. They explicitly acknowledge that requiring complete histories may create selection bias. The stock sample is used in three ways: annual individual-stock distributions, monthly individual-stock distributions, and annual distributions of 19 small portfolios.

The small portfolios partition the 97 stocks by drawing without replacement: 17 portfolios contain five stocks each and the last two contain six each. Thus stocks are not repeatedly reused across the 19 portfolios within a draw. The source reports that repeating the random assignment produced negligible changes, except for the $b=10$ exponential case, where a median result is given. It does not specify the number of repetitions, random seed, full portfolio memberships, precise constituent weighting convention, or rebalancing mechanics. Those details cannot be recovered from the table alone.

Table 3 reports $k=0.01$ correlations:

| Utility | Annual individual stocks | Monthly individual stocks | Annual portfolios of five or six stocks |
|---|---:|---:|---:|
| $\log(1+R)$ | 0.880 | 0.995 | 0.998 |
| $(1+R)^{0.1}$ | 0.895 | 0.996 | 0.998 |
| $(1+R)^{0.3}$ | 0.932 | 0.998 | 0.999 |
| $(1+R)^{0.5}$ | 0.968 | 0.999 | 0.999 |
| $(1+R)^{0.7}$ | 0.991 | 0.999 | 0.999 |
| $(1+R)^{0.9}$ | 0.999 | 0.999 | 0.999 |
| $-\exp[-0.1(1+R)]$ | 0.999 | 0.999 | 0.999 |
| $-\exp[-0.5(1+R)]$ | 0.961 | 0.999 | 0.999 |
| $-\exp[-(1+R)]$ | 0.850 | 0.997 | 0.998 |
| $-\exp[-3(1+R)]$ | 0.850 | 0.976 | 0.958 |
| $-\exp[-5(1+R)]$ | 0.863 | 0.961 | 0.919 |
| $-\exp[-10(1+R)]$ | 0.659 | 0.899 | 0.768 |

The log-utility comparison is especially informative: correlation rises from 0.880 for annual individual-stock returns to 0.998 for annual small-portfolio returns. Monthly individual-stock returns also yield 0.995. Lower dispersion and some diversification improve approximation in this sample. These results do not establish a universal minimum number of holdings, and the dependence structure of the historical stocks matters. Five or six stocks are the experiment's construction, not a prescription for every market.

The authors report that in every Table 2 or Table 3 case with correlation greater than 0.9, the candidate maximizing $f_{0.01}$ also maximizes exact empirical expected utility. Candidate counts are 149, 97, or 19 depending on the experiment. This statement concerns winners among those finite sets; the paper does not optimize over every possible portfolio of the underlying securities. It also does not state that 0.9 is a generally sufficient threshold. No standard errors, confidence intervals, or formal sampling tests accompany these correlations or selection coincidences.

## Local risk aversion and the quadratic objection

Section IV distinguishes three constructions. One fits a quadratic utility of wealth once and retains it as wealth changes. Another refits a quadratic at current wealth at each decision date, equivalently fitting around zero net return. The third fits a quadratic around the mean of each candidate distribution, potentially also using its variance. The proposed $f_k$ belongs to the third class.

This matters because increasing absolute risk aversion of a fixed concave quadratic does not automatically describe an approximation whose coefficients change with the distribution being assessed. The authors formalize the distinction using a small-risk premium. Consider distributions with common mean $E_0$ and $\sigma_i\to0$. Define the approximation-based premium by

$$
f(E_0-\pi_i,0)=f(E_0,\sigma_i).
$$

Suppose the approximation is the expectation of a quadratic centered at the candidate mean, with $a=U(E)$ and $c(E,\sigma)\to U''(E)/2$ as $\sigma\to0$. The $f_k$ family satisfies these conditions for fixed finite $k$, including the $k=0$ limit. Then

$$
\lim_{i\to\infty}\frac{\pi_i}{\sigma_i^2}
=-\frac12\frac{U''(E_0)}{U'(E_0)}.
$$

This agrees with the underlying utility's small-risk premium in return units. To reproduce pp. 315–316, first note that the right side of the defining certainty-equivalent equation converges to $U(E_0)$, so $\pi_i\to0$ under increasing continuous utility. Expand $U(E_0-\pi_i)$ about $E_0$, divide the resulting equality by $\sigma_i^2$, and use the limit of $c$. The denominator contains $U'(E_0)$ plus a term vanishing with $\pi_i$; the limit follows.

Units require care when converting to a utility of wealth $V(W)$. If $U(R)=V((1+R)W_{t-1})$, then $U''/U'=W_{t-1}V''/V'$. The premium expressed in return units and the premium expressed in wealth units differ by scale. This chain-rule relation is needed when interpreting the printed discussion of Pratt's coefficient; the core result above is stated wholly in the paper's return variable and is unambiguous.

The local theorem does not prove that all $k$ perform equally well for substantial risks. The empirical table shows otherwise. It establishes correct limiting local curvature while leaving large-risk approximation quality to the error analysis and data. Likewise, counterexamples to exact mean–variance ordering remain valid. The authors' claim is that useful approximation can survive failure of exact global representation.

## Reproduction specification and practical limits

A faithful reproduction should keep the candidate distributions and the cross-sectional comparison separate. For each fund, stock, or constructed portfolio, form the historical distribution of returns and calculate exact empirical utility and its moment-based approximation. Then calculate correlations across candidates for each fixed utility and $k$. Do not correlate each candidate's time series of returns with its utility or pool all fund-year observations into one distribution; either operation answers a different question.

The natural internally consistent implementation uses equally weighted observed dates and central moments computed from that empirical probability distribution, with variance divisor $T$. The article does not explicitly state its variance divisor. If the source implementation used an unbiased sample-variance divisor instead, results would differ, especially with only ten annual fund observations. A reconstruction should state the convention and, if exact matching is the goal, assess the alternative rather than silently claim the original denominator is known.

For small $k$, direct subtraction in the centered second difference may lose numerical precision. The analytic $f_0$ expression is a useful check, and stable utility evaluation or higher precision can assess whether a discrepancy comes from the model or floating-point cancellation. These are implementation checks derived from the formula, not numerical procedures documented by the authors.

The missing raw identifiers, data conventions, portfolio weights, and randomization details prevent an exact reconstruction of every printed coefficient from the article alone. Its mathematical procedure is nevertheless explicit. A modern extension can use a documented panel, retain disappearing securities, specify return treatment and portfolio weights, and evaluate ranking losses as well as correlations. Such an extension should be labeled new work; the original results are neither corrected for those design choices nor validated prospectively.

The actionable conclusion is conditional. For the historical diversified distributions and many utility functions studied, a simple two-moment approximation preserves expected-utility ordering exceptionally well. For strong curvature or substantial probability in extreme outcomes, it can fail visibly. Inspecting the utility approximation error over the relevant return range, relative to variation across candidate opportunities, is more informative than asserting either that mean–variance is always exact or that its lack of exactness makes it useless.
