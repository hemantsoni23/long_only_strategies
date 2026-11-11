# The Short and Medium-Run Components of International Equity Return Volatilities

**Gregory Connor. Working paper, May 18, 2005.** Source: [original PDF](../../Finance/Connor_%20%20Short%20and%20Medium-Run%20Components%20of%20International%20Equity%20Return%20Volatilities_2005.pdf), 25 PDF pages. This note follows the working paper, including its appendix and tables. Several displayed formulas and parameter tables are internally inconsistent; the coherent model reconstructed below is distinguished from the paper's reported estimates.

## Why this matters and what is new

A conventional GARCH model can fit next-day variance reasonably while giving an implausible account of how volatility persists over months. Connor places a slowly changing variance benchmark inside a faster GARCH adjustment. The benchmark is a mixture of an exponentially weighted average of squared returns and a fixed unconditional variance. A temporary return shock can therefore affect both short-run volatility and the level toward which that volatility subsequently reverts.

The contribution is a parsimonious parameterization of this two-speed process, called benchmark-volatility GARCH, or BVGARCH, and an empirical decomposition of G7 volatility comovement into benchmark and short-run components. It is related to component GARCH rather than a wholly separate theory of return generation. Its practical attraction is that positivity is transparent in the structural representation even though the equivalent GARCH(2,2) can have negative coefficients. A generic optimizer working directly with the reduced coefficients may have difficulty finding or maintaining such admissible combinations.

The application is descriptive and estimated in sample. There is no reported trading strategy, rolling forecast contest, transaction-cost analysis, or confidence interval for the variance-component shares. Better agreement between fitted and empirical autocorrelations is evidence about the model's dynamics, not proof that it produces superior implementable covariance forecasts.

## A coherent specification and its timing

Let $\epsilon_t$ be the demeaned daily index return, $h_t=\operatorname{Var}(\epsilon_t\mid\mathcal F_{t-1})$, and $z_t=\epsilon_t/\sqrt{h_t}$, with conditional mean zero and conditional variance one. The paper writes the long-run variance as $\sigma_0$; this is a variance, despite notation that may suggest a standard deviation. Define

$$
a=e^{-1/\lambda},\qquad c=1-\alpha-\beta,\qquad d=(1-\delta)(1-a).
$$

The benchmark is

$$
b_t^*=a b_{t-1}^*+(1-a)\epsilon_{t-1}^2,
\qquad
b_t=\delta\sigma_0+(1-\delta)b_t^*.
$$

Equivalently,

$$
b_t=\delta(1-a)\sigma_0+a b_{t-1}+d\epsilon_{t-1}^2.
$$

The body equations (7)–(10), read with the positivity argument in the appendix, support the conditional-variance recursion

$$
h_t=b_{t-1}+\alpha(h_{t-1}-b_{t-1})+\beta(\epsilon_{t-1}^2-b_{t-1})
=c b_{t-1}+\alpha h_{t-1}+\beta\epsilon_{t-1}^2.
$$

Here $\alpha$ propagates short-run conditional variance, $\beta$ is the immediate squared-return response, $a$ controls the benchmark's memory, and $\delta$ anchors the benchmark to the unconditional level. The same shock enters $h_t$ immediately through $\beta$ and influences subsequent $h$ through the benchmark. The model uses $b_{t-1}$ in the variance equation, not the newly updated $b_t$. This indexing matters for both the reduced-form coefficients and forecasts.

The admissibility restrictions are $\alpha>0$, $\beta>0$, $\alpha+\beta<1$, $\lambda>0$, $0<\delta<1$, and $\sigma_0>0$. Positive starting values then give positive benchmarks and conditional variances recursively. The benchmark's half-life is $\lambda\log 2$ trading days, since $a^H=1/2$. The source's statement involving $\lambda\sqrt 2$ is not the half-life implied by its exponential decay formula.

The earlier equation (3) instead uses a contemporaneously indexed benchmark. Table 3 also reverses the benchmark mixture weights relative to the main text and prints a malformed updating rule. These are not innocuous changes if copied into code. The formulas above specify one internally consistent reconstruction; they do not establish which indexing and parameter labels were used in the author's original estimation program.

## Reduced GARCH form and why negative coefficients can be valid

Eliminating the benchmark from the structural equations gives, by direct substitution,

$$
h_t=\omega+\alpha_1h_{t-1}+\alpha_2h_{t-2}
+\beta_1\epsilon_{t-1}^2+\beta_2\epsilon_{t-2}^2,
$$

where

$$
\omega=c\delta(1-a)\sigma_0,\quad
\alpha_1=\alpha+a,\quad
\alpha_2=-\alpha a,\quad
\beta_1=\beta,\quad
\beta_2=cd-\beta a.
$$

The negative sign on $\alpha_2$ is essential. Equation (11) in the PDF repeats the first autoregressive coefficient in the position of the second; that does not follow from the structural model. This note gives the algebraic correction explicitly. Both $\alpha_2$ and $\beta_2$ can be negative without making $h_t$ negative because their values are tied together by the positive benchmark representation. Imposing nonnegativity on every reduced coefficient would exclude the intended model.

The sum of the four lag coefficients is

$$
\alpha_1+\alpha_2+\beta_1+\beta_2
=1-c\delta(1-a)<1.
$$

Consequently the stationary mean, when the requisite integrability conditions hold, is $E[h_t]=\sigma_0$. This is a useful implementation check: simulate a sufficiently long series, discard initialization, and compare the average conditional variance with the variance target. It is not a claim that every finite sample will be close or that the unconditional fourth moment necessarily exists.

For conditional mean forecasts of variance and the updated benchmark, the centered transition matrix is

$$
M=
\begin{pmatrix}
\alpha+\beta&c\\
d&a
\end{pmatrix}.
$$

Writing $x_t=(h_t-\sigma_0,b_t-\sigma_0)'$, the iterated conditional mean follows powers of $M$. Its first row sums to one; its second sums to $1-\delta(1-a)<1$. Because $c>0$ couples the first coordinate to the second, both row sums of $M^2$ are strictly less than one. Thus $\rho(M)<1$, and conditional means revert geometrically, potentially with two substantially different decay rates. This two-step argument repairs the source's overly strong one-step strict-contraction statement: equal positive coordinates need not contract strictly after a single application of $M$.

A further qualification concerns moments. Stability of the conditional mean and finite unconditional return variance do not by themselves make the variance process covariance stationary. To discuss autocovariances of $h_t$ or squared returns, one also needs finite fourth moments and a stronger second-moment condition for the random state transition. With standardized innovations, that random matrix is

$$
A(z)=
\begin{pmatrix}
\alpha+\beta z^2&c\\
dz^2&a
\end{pmatrix}.
$$

A standard sufficient condition is finite $E[z^4]$ and spectral radius below one for $E[A(z)\otimes A(z)]$. The article does not verify this condition at its fitted parameters. Student-$t$ degrees of freedom above four are necessary for finite innovation fourth moments but do not alone establish the full process condition.

## Estimation and an implementable filter

The application removes the sample return mean and variance-targets $\sigma_0$ using the sample variance. Innovations have a Student-$t$ distribution with an estimated degrees-of-freedom parameter. For an actual implementation the $t$ innovation must be standardized to unit variance; otherwise its scale is incorrectly folded into $h_t$.

With $\nu>2$, the standardized-$t$ contribution to the conditional log likelihood is

$$
\ell_t=
\log\Gamma\!\left(\frac{\nu+1}{2}\right)
-\log\Gamma\!\left(\frac{\nu}{2}\right)
-\frac12\log((\nu-2)\pi)
-\frac12\log h_t
-\frac{\nu+1}{2}\log\!\left(1+\frac{\epsilon_t^2}{(\nu-2)h_t}\right).
$$

After variance targeting, maximize $\sum_t\ell_t$ over $\alpha,\beta,\lambda,\delta,\nu$. A softmax-style parameterization can enforce positive $\alpha,\beta,c$ summing to one; a logistic transform can constrain $\delta$, and exponential transforms can enforce positive $\lambda$ and $\nu-2$. These are reconstruction choices, not a description of an optimizer supplied by the author. If finite-fourth-moment diagnostics are required, explicitly check $\nu>4$ and the random-matrix condition rather than assuming them.

For each observation, retain the old $b_{t-1}$ and $h_{t-1}$, compute $h_t$ using the old benchmark and the last observed squared return, and update $b_t$ with that same squared return. Evaluate the density of the new return using $h_t$. This avoids accidentally replacing $b_{t-1}$ by $b_t$ through an in-place update. Start values such as $h_0=b_0=b_0^*=\sigma_0$ are reasonable transparent choices, but initialization and burn-in are not specified sufficiently in the source to identify the original likelihood exactly.

The comparison model is a variance-targeted GARCH(1,1) with Student-$t$ innovations. The paper also discusses direct estimation of unrestricted GARCH(2,2). It does not provide enough likelihood values, convergence diagnostics, starting-point searches, or parameter constraints to establish a clean numerical optimization comparison. If two parameterizations span nested feasible models and optimization finds the global maximum, the unrestricted likelihood cannot be lower. An observed advantage of the restricted parameterization would therefore concern numerical optimization, admissibility, or different constraints, rather than overturning nesting.

## Data and descriptive dependence

Section 3 uses daily MSCI equity index returns for Canada, France, Germany, Italy, Japan, the United Kingdom, and the United States. The body gives December 1979 through March 2005 and 6,544 observations; the abstract describes the start as January 1980. The treatment of local versus common currencies, price versus total-return indices, holidays, missing observations, and international close-time differences is not specified clearly enough for an exact independent download. These choices matter especially for cross-country daily squared-return dependence.

Annualized standard deviations in Table 1 use $\sqrt{260}$: Canada 15.4%, France 19.5%, Germany 20.7%, Italy 21.9%, Japan 18.8%, UK 16.3%, and US 16.7%. The return correlation is 0.659 for Canada–US, 0.625 for France–Germany, and 0.114 for Japan–US. Squared-return correlations are respectively 0.566, 0.628, and 0.121; UK–Japan squared-return correlation is 0.494. A low contemporaneous Japan–US correlation is not by itself evidence of weak economic transmission because the close times differ.

Table 2 shows substantial first-order squared-return autocorrelation: 0.306 in Canada, 0.209 in France, 0.242 in Germany, 0.248 in Italy, 0.245 in Japan, 0.465 in the UK, and 0.131 in the US. At lag 50 these are 0.061, 0.072, 0.106, 0.048, 0.016, 0.072, and 0.014. At lag 100 they are 0.041, 0.031, 0.051, 0.025, 0.005, 0.019, and 0.005. Persistence is therefore heterogeneous, not a uniform property of every country at every lag.

The paper's statement that all blocks of autocorrelations are significant is too broad. For example, the US block statistics for lags 71–80 and 81–90 are 1.7 and 0.7, far below the approximately 18.3 upper 5% critical value of a chi-squared distribution with ten degrees of freedom. Such details matter when deciding whether a slow component is strongly identified in each individual market.

## Fitted dynamics and the limits of the parameter tables

The reported benchmark half-lives in Table 3 are 11.321 trading days for Canada, 37.677 for France, 39.733 for Germany, 27.508 for Italy, 55.393 for Japan, 25.564 for the UK, and 12.546 for the US. The benchmark can have longer economic influence than its mechanical half-life because it is embedded in the full two-state feedback system. Its decay parameter alone is not the complete persistence measure.

Reported BVGARCH Student-$t$ degrees of freedom range from 4.83 for Japan to 12.92 for the UK. The other estimates are Canada 5.84, France 8.10, Germany 8.51, Italy 7.13, and US 6.200. These values favor heavier conditional tails than Gaussian innovations, although the paper does not report parameter standard errors or a likelihood-ratio comparison against a Gaussian specification.

The numerical parameter tables cannot be treated as a reliable machine-readable specification of the fitted models. Table 3's Canadian $\beta=0.086$ and $\alpha=0.292$ sum to 0.378, while its displayed sum column is 0.872. France's 0.068 and 0.868 sum to 0.936, not the printed 0.969. The same problem occurs in the GARCH rows: the US entries 0.028 and 0.955 sum to 0.983, not 0.999. Table 6 then gives BVGARCH reduced-form $\beta_1$ values that do not match Table 3's $\beta$, although these must be identical under the derived transformation: Canada is 0.121 rather than 0.086 and the US 0.058 rather than 0.035.

Accordingly, the reported half-lives, degrees of freedom, and diagnostic results are transcribed as source claims, while the exact fitted state paths cannot be regenerated without corrected tables or code. It would be misleading to choose whichever conflicting coefficient seems plausible and call the resulting simulation a replication.

## Checking autocorrelations without copying damaged formulas

Let $y_t=\epsilon_t^2$ and $\eta_t=y_t-h_t$. Under the conditional variance model, $\eta_t$ is a martingale difference. The reduced GARCH representation implies

$$
y_t-\sigma_0=\phi_1(y_{t-1}-\sigma_0)+\phi_2(y_{t-2}-\sigma_0)
+\eta_t+\theta_1\eta_{t-1}+\theta_2\eta_{t-2},
$$

with $\phi_j=\alpha_j+\beta_j$ and $\theta_j=-\alpha_j$. For lags at least three, the autocovariance recurrence is $\gamma_k=\phi_1\gamma_{k-1}+\phi_2\gamma_{k-2}$; the source reverses the lag association in one displayed recurrence.

A numerically convenient reconstruction avoids relying on its questionable closed-form starting autocovariances. Compute $\psi_0=1$, $\psi_1=\phi_1+\theta_1$, $\psi_2=\phi_1\psi_1+\phi_2+\theta_2$, and subsequently $\psi_j=\phi_1\psi_{j-1}+\phi_2\psi_{j-2}$. When second moments of $y_t$ exist, its autocorrelation is

$$
\rho_k=\frac{\sum_{j=0}^{\infty}\psi_j\psi_{j+k}}{\sum_{j=0}^{\infty}\psi_j^2}.
$$

Truncate only after checking numerical convergence. This yields a directly testable curve for Figures 1–7, whose horizontal axes extend across multiple orders of lag. The BVGARCH curves generally follow empirical persistence more closely than the fitted GARCH curves, but Japan and the US retain visible discrepancies. No uncertainty bands are supplied.

Tables 4 and 5 concern squared standardized residuals, a more appropriate diagnostic than raw-return autocorrelation. Canada's first residual-square autocorrelation falls from 0.04097 under GARCH to 0.00999 under BVGARCH; the UK changes from 0.04937 to 0.039 and the US from 0.02244 to 0.01981. Canada's first ten-lag portmanteau statistic falls from 17.83 to 6.12, and the UK's from 18.79 to 12.12. Improvement is incomplete: Japan's lags 11–20 statistic remains 52.22, down from 60.96, and France's lags 61–70 statistic remains 21.38. This is evidence for a useful additional dynamic component, not a diagnosis that all conditional dependence has disappeared.

## Decomposing international volatility variation

For consistent timing define the medium-run component $m_{it}=b_{i,t-1}$ and short-run component $s_{it}=h_{it}-b_{i,t-1}$. Then

$$
\operatorname{Var}(h_i)=\operatorname{Var}(m_i)+\operatorname{Var}(s_i)+2\operatorname{Cov}(m_i,s_i),
$$

and for countries $i,j$,

$$
\operatorname{Cov}(h_i,h_j)=\operatorname{Cov}(m_i,m_j)+\operatorname{Cov}(s_i,s_j)
+\operatorname{Cov}(m_i,s_j)+\operatorname{Cov}(s_i,m_j).
$$

These identities decompose the time-series variation of **estimated conditional variances**. They do not divide the unconditional variance of the original return into independent risks. In particular, the short- and medium-run components are correlated. The source's equation (12) has a mismatched time index; the definition above makes the same-period identity explicit.

Table 8 divides each component by the corresponding total variance or covariance. Its diagonal shares are:

| Market | Medium-run | Short-run | Cross component |
|---|---:|---:|---:|
| Canada | 0.706 | 0.217 | 0.077 |
| France | 0.352 | 0.399 | 0.250 |
| Germany | 0.515 | 0.305 | 0.180 |
| Italy | 0.581 | 0.236 | 0.182 |
| Japan | 0.289 | 0.572 | 0.139 |
| UK | 0.360 | 0.345 | 0.296 |
| US | 0.428 | 0.340 | 0.232 |

Rounding explains totals slightly different from one. The substantial cross term prevents a simple conclusion that independent fast and slow effects each account for half. Canada's own variance dynamics are especially benchmark dominated, whereas Japan's short-run share is larger.

For Canada–US covariance the shares are 0.519, 0.222, and 0.260; for France–Germany they are 0.454, 0.320, and 0.226; for Japan–US, 0.344, 0.432, and 0.224. Both time scales contribute to international comovement. This is not a causal decomposition of transmission between countries: each country's filter is estimated separately and the common variation is measured afterward.

Table 7's heading, triangular display, and prose give conflicting descriptions of scaling and of whether entries represent covariances, correlations, or transformed dispersion. Those cells should not be assigned precise economic units without clarification. Table 8's explicitly normalized shares are more interpretable, although they inherit all uncertainty in the underlying variance filters.

## Replication boundary and practical use

A faithful reimplementation can reproduce the structural idea, positivity, reduced-form algebra, likelihood, and component accounting from the formulas in this note. Reproducing the published numerical results additionally requires the exact MSCI series, return currency and dividend convention, daily synchronization, corrected coefficient tables, initialization, likelihood scaling, optimizer settings, and clarification of the benchmark timing and mixture weight. The article supplies no uncertainty estimates for the reported decomposition and no out-of-sample tuning procedure.

The worthwhile empirical extension is a controlled forecast comparison with the benchmark filter and slow component fitted only on past observations. Forecast horizons should include both next-day and multiweek variance, since the innovation is precisely about their different dynamics. That is a proposed validation design rather than a result in this paper. The source supports the narrower conclusion that a positively parameterized, two-state volatility model offers a plausible account of slow persistence and materially changes how fitted international volatility variation is attributed across horizons.
