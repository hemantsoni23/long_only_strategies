# The Excess Co-movement of Commodity Prices

Robert S. Pindyck and Julio J. Rotemberg, NBER Working Paper 2671, July 1988. [Source PDF](../../Finance/futures/Futures_PyndickRotenberg_1988.pdf). This is the supplied 1988 working-paper version, not a silently substituted later publication. It contains 33 PDF pages: two front pages, text pp. 1–18, Appendix A, Appendix B, references, footnotes, and seven tables. Printed p. 1 is PDF p. 3. The historical source filename misspells both authors' surnames; the bibliography above follows the document.

## Why this matters

Commodity diversification can fail even when the commodities have different uses, production regions, and physical supply chains. The question is whether correlated price changes are simply the response to common economic conditions or whether substantial common variation remains after those conditions and market forecasts are accounted for. This paper tests that question without requiring observed inventory stocks.

Its methodological contribution has two parts. First, a competitive storage model motivates a cross-equation restriction: after conditioning on the common drivers of prices, unrelated commodities should have uncorrelated residual innovations. Second, a multiple-indicator, multiple-cause latent-variable model allows market participants to know more about future inflation and production than the econometrician observes. The test therefore goes beyond regressing commodity prices on a few contemporaneous macroeconomic series.

The reported residual correlation is statistically strong, survives several variations, and explains a meaningful fraction of some commodities' in-sample price variation. It does not establish that correlated trading caused the movements. The null bundles commodity unrelatedness, the chosen macroeconomic state variables, restrictions on market forecasts, functional form, and distributional assumptions. Rejection can reveal a missing common fundamental as well as a departure from the authors' competitive benchmark. This distinction is central when using the paper to justify factor models or portfolio stress scenarios.

## Data universe and construction

The universe is seven U.S. cash-price series: wheat, cotton, copper, gold, crude oil, lumber, and cocoa. The authors choose commodities with different uses and growing or production conditions, arguing that they are neither close substitutes nor complements, are not jointly produced, and do not use one another as major inputs. That economic selection is the identifying premise; it is not an estimated system of cross-price elasticities.

The source data cover January 1960–December 1985. Most regressions use April 1960–November 1985, a span of 308 calendar months before any specification-dependent missing-data treatment. The paper emphasizes nominal U.S. average monthly cash prices and computes changes in their logarithms. These are not futures excess returns, collateralized investment returns, or tradable end-of-month quotations. Monthly averaging, heterogeneous grades, and differences in delivery timing can smooth or distort the timing of common shocks.

Appendix B, printed p. 21, gives the following source map.

| Commodity | Price definition and source |
|---|---|
| Cocoa | BLS spot cocoa-bean prices in New York through January 1985; from February 1985, average daily cash price quoted in Chicago for Accra delivery |
| Copper | Producers' electrolytic wirebar copper prices delivered to U.S. destinations, American Metal Market via *Commodity Yearbook*; monthly averages of daily wholesale delivered cash prices |
| Cotton | U.S. 1-1/16-inch strict low middling spot cotton at designated markets, USDA Agricultural Marketing Service via *Commodity Yearbook* |
| Crude oil | Average wholesale crude-petroleum price collected by the Independent Petroleum Association of America, from annual editions of *Platts Oil Price Handbook and Oilmanac* |
| Gold | Handy and Harman cash price, averaged from daily spot observations |
| Lumber | BLS aggregate price index for lumber and primary lumber products |
| Wheat | Number 1 hard winter wheat at Kansas City, USDA Agricultural Marketing Service via *Commodity Yearbook* |

The cocoa splice and lumber's status as an aggregate index are material replication details. The source does not supply the numerical raw series, a splice adjustment, or machine-readable vintage identifiers. It reports limited experiments replacing gold with platinum without a substantial change in conclusions, but does not reproduce those alternative estimates.

The observable macroeconomic vector includes industrial production, CPI, an equally weighted index of the dollar values of the British pound, German mark, and Japanese yen, and the nominal three-month Treasury-bill rate. The additional forecasting variables are M1 and the S&P Common Stock Index. Price-like and quantity-index variables enter through log changes; the interest rate enters in level form, as footnote 4 explicitly states. The exchange-rate quote convention means that an increase represents foreign-currency appreciation against the dollar. The paper does not fully document macro-data vendors, seasonal-adjustment vintages, annualization or rate units, and later revisions. Those gaps prevent a claim of exact replication from the PDF alone.

## Raw correlation and its likelihood test

For $p=7$ commodities, let $R$ be the sample correlation matrix of log price changes and $N$ the number of usable observations. Under an independent multivariate Gaussian sampling model, the likelihood-ratio statistic for a diagonal population covariance is

$$
T=-N\log|R|\ \overset{a}{\sim}\ \chi^2_{p(p-1)/2}=\chi^2_{21}.
$$

The source obtains this from the Gaussian likelihood proportional to $|\Sigma|^{-N/2}\exp[-N\operatorname{tr}(\Sigma^{-1}\widehat\Sigma)/2]$. Under the unrestricted model the covariance estimate is the sample covariance; under a diagonal restriction its diagonal entries are the sample variances. The determinant ratio becomes $|R|$. This is a joint test of all 21 pairwise restrictions, not 21 independent pairwise t tests.

Table 1 gives a monthly statistic of 114.6. Ten of 21 off-diagonal correlations exceed 0.1. Representative monthly correlations are 0.253 for wheat–cotton, 0.322 copper–gold, 0.245 gold–oil, and 0.122 lumber–cocoa. Not every pair moves together: wheat–gold is −0.020 and oil–lumber is −0.085.

Tables 2 and 3 use nonoverlapping quarterly and annual log changes. Their statistics are 53.5 and 56.3, respectively, both reported significant at 1%. The numerical decline relative to the monthly statistic does not imply smaller correlations; there are far fewer nonoverlapping observations. The growth in selected correlations is substantial.

| Pair | Monthly | Quarterly | Annual |
|---|---:|---:|---:|
| Wheat–cotton | 0.253 | 0.300 | 0.504 |
| Wheat–gold | −0.020 | 0.136 | 0.606 |
| Copper–gold | 0.322 | 0.391 | 0.521 |
| Gold–oil | 0.245 | 0.419 | 0.548 |
| Lumber–cocoa | 0.122 | 0.302 | 0.582 |
| Oil–lumber | −0.085 | −0.096 | −0.176 |

The prose says that 19 of 21 annual correlations exceed 0.2. Counting the printed Table 3 gives 18: copper–lumber is 0.099, oil–lumber −0.176, and oil–cocoa −0.030. This is a derived correction to the count; it does not change the reported joint test or the broad increase in dependence.

The authors also use all overlapping quarterly and annual changes. Their statistics are 194.9 and 517.7, but overlap invalidates the independent-observation chi-square reference distribution. They simulate 15,000 draws under a null of independent, identically distributed monthly price changes uncorrelated across commodities. The largest simulated statistics are 121.3 and 504.1. No simulated draw exceeds the respective observed statistic. This is finite Monte Carlo evidence under the stated null, not a probability literally equal to zero and not a test robust to arbitrary serial dependence or volatility clustering. The source does not specify a seed or enough simulation implementation details to regenerate its exact maxima.

## Competitive storage model and the role of expectations

Let $p_{i,t}=\log P_{i,t}$ and let net supply be

$$
Q_{i,t}=a_{i,t}+b_i p_{i,t}.
$$

The intercept $a_{i,t}$ collects commodity-specific conditions and common macroeconomic drivers. “Unrelated” commodities have negligible direct cross-price effects and do not share the commodity-specific shocks contained in these intercepts. Inventory obeys

$$
I_{i,t}=I_{i,t-1}+Q_{i,t}.
$$

Risk-neutral inventory holders satisfy the one-period expected-return condition

$$
r_t=\frac{E_t[P_{i,t+1}]-C_{i,t}-P_{i,t}}{P_{i,t}},
$$

where $C_{i,t}$ is holding cost less the capitalized marginal convenience benefit. More inventory reduces the marginal convenience benefit. The authors model its log as $c_{i,t}=n_{i,t}+\gamma_i I_{i,t}$, with $n$ driven by current and past macro variables. Logging $C$ requires positive net carrying cost in the region of the approximation; if convenience benefits exceed holding cost, this particular log representation requires modification.

Appendix A linearizes the return condition and solves a second-order inventory difference equation with a nonexplosive branch. Price consequently depends on lagged inventories and discounted expectations of future $a$ and $n$. The inferential idea is that common macroeconomic forecasts should account for common price innovations, while the remaining commodity-specific terms should be cross-sectionally independent.

The Appendix should not be copied literally as production code. Its stated expansion point, constants, and later inventory coefficients are not fully consistent. A transparent derived local expansion starts from $R_{t+1}=P_{t+1}/P_t-C_t/P_t$. Let $A>H>0$ be the reference gross price ratio and carrying-cost ratio. For $u=p_{t+1}-p_t$ and $v=c_t-p_t$,

$$
\log R_{t+1}\approx\log(A-H)
+\frac{A}{A-H}(u-\log A)-\frac{H}{A-H}(v-\log H).
$$

Writing $\delta=A/(A-H)$ and collecting constants gives $\log R_{t+1}\approx K+\delta p_{t+1}-p_t+(1-\delta)c_t$. Approximating the expected log return by the required simple return is itself a local approximation, with a variance/Jensen qualification. The source's preceding display labels one reference ratio using growth in $C$ and prints a constant that does not follow from this Taylor expansion. These details should be separated from the reduced-form hypothesis rather than treated as exact identities.

For completeness, if one adopts the resulting local Euler relation $r_t\approx K+\delta E_t p_{t+1}-p_t+(1-\delta)(n_t+\gamma I_t)$, substitution of the inventory identity yields

$$
E_t I_{t+1}-A_I I_t+\delta^{-1}I_{t-1}=g_t,
$$

$$
A_I=\frac{1+\delta-b(1-\delta)\gamma}{\delta},\qquad
g_t=E_ta_{t+1}-\frac{a_t}{\delta}-\frac{b(1-\delta)n_t}{\delta}-\frac{bK}{\delta}+\frac{br_t}{\delta}.
$$

The printed Eq. (A3) would need a rescaling of $n$ and $\gamma$ to match these coefficients; the text explicitly absorbs the discount-rate term but does not fully document such a rescaling. Under $b,\gamma>0$ and $\delta>1$, the homogeneous polynomial has roots $k<1<\lambda$. With $d=1/\lambda$, eliminating the explosive branch gives

$$
I_t=kI_{t-1}-d\sum_{j=0}^{\infty}d^jE_t[g_{t+j}],
$$

provided the conditional sum converges and the corresponding terminal term vanishes. This is the stable-root mechanism behind the Appendix's forward sum. It is a reconstruction of the local system, not an assertion that the article estimates these structural parameters. Inventory nonnegativity, stockouts, nonlinear convenience yields, and global existence are not built into the linear statistical specification.

The empirical reduction is much stronger than the storage accounting identity alone. Assume that forecasts of future macro variables are linear functions of observable current and lagged variables, and assume that the remaining commodity-specific price component follows a random walk. First differences then satisfy

$$
\Delta p_{i,t}=\sum_{k=0}^{K}\alpha_{i,k}'\Delta x_{t-k}
+\sum_{k=0}^{K}\beta_{i,k}'\Delta z_{t-k}+\varepsilon_{i,t},
$$

with the interest-rate convention implemented separately. Under the maintained null, $E[\varepsilon_{i,t}\varepsilon_{j,t}]=0$ for $i\ne j$. The source also estimates a version with $\rho_i\Delta p_{i,t-1}$ to allow more own-series dynamics. The random-walk residual and finite lag truncation are assumptions used to reach the testable regression, not consequences of rational storage by themselves.

## Observable-macro regressions and their magnitude

The baseline OLS equations include current and one-month-lagged values of all six macro or forecasting variables. A second version includes current values and six lags. The objective is explanatory and contemporaneous: current macro movements enter the same month's commodity-price equation. There is no training/validation split, rolling forecast window, or claimed executable strategy.

Table 4's monthly $R^2$ values, more precisely displayed in Table 6, are 0.056 wheat, 0.053 cotton, 0.090 copper, 0.244 gold, 0.211 oil, 0.177 lumber, and 0.069 cocoa. Several variables matter jointly even when individual coefficients are noisy. For example, current inflation has a wheat coefficient of 0.273 with t statistic 3.1 and an oil coefficient of 0.333 with t statistic 4.1. Current exchange-rate movement has a gold coefficient 0.325 with t statistic 5.5, while the oil coefficient is −0.146 with t statistic −2.4. These are regression sensitivities in the table's data scaling, not annual investment returns.

The Durbin–Watson statistics are 1.34, 1.20, 1.48, 1.40, 1.51, 1.10, and 1.87 in the same commodity order. Residual dynamics therefore matter. Simply treating all residual observations as independent would not be a neutral choice.

Table 5 reports likelihood-ratio tests that exclude both current and lagged observations of one variable from all seven equations. The one-lag versions have 14 restrictions; the six-lag versions have 49.

| Excluded group | One lag, 14 df | Six lags, 49 df |
|---|---:|---:|
| Inflation | 73.22 | 127.29 |
| Industrial production | 29.48 | 71.56 |
| Treasury-bill rate | 29.32 | 93.24 |
| Exchange rates | 62.06 | 166.41 |
| M1 | 36.29 | 81.93 |
| Stock-market changes | 20.44 | 101.05 |

All are marked significant at 1% except the one-lag stock group, which has no significance mark, and six-lag industrial production, marked at 5%. Thus the source's broad prose statement that every variable is significant needs the stock-group qualification.

The diagonal-residual tests at the bottom of Table 5 are 89.36 and 99.44. Both reject at 1%. Later prose compares the latent-variable result with an OLS statistic of 88.6 rather than 89.36; the source provides no reconciliation. The table values are retained here and the discrepancy is explicit. Adding six lags does not automatically reduce the rejection statistic: the authors note that fitting unimportant regressors can reduce residual variances without commensurately reducing covariance.

With a lagged dependent variable and current plus one-lag macro controls, the system likelihood comparison gives 71.2 for the 21 diagonal restrictions, still strongly rejecting. The simple determinant shortcut is not used indiscriminately here because the equations have different lagged dependent regressors. This distinction matters in recreating the test.

To assess economic magnitude, Table 6 adds the contemporaneous price changes of the other six commodities to each equation. These are in-sample association measures, not feasible advance predictors. The following entries show macro-only and augmented fits.

| Commodity | Monthly $R^2$ | Quarterly $R^2$ | Annual $R^2$ |
|---|---:|---:|---:|
| Wheat | 0.056 → 0.135 | 0.136 → 0.237 | 0.577 → 0.889 |
| Cotton | 0.053 → 0.154 | 0.278 → 0.367 | 0.401 → 0.887 |
| Copper | 0.090 → 0.181 | 0.179 → 0.233 | 0.701 → 0.906 |
| Gold | 0.244 → 0.333 | 0.373 → 0.398 | 0.908 → 0.960 |
| Oil | 0.211 → 0.261 | 0.402 → 0.482 | 0.944 → 0.974 |
| Lumber | 0.177 → 0.187 | 0.279 → 0.298 | 0.753 → 0.818 |
| Cocoa | 0.069 → 0.085 | 0.159 → 0.209 | 0.872 → 0.890 |

For annual cotton, the increment is 0.486, nearly half the total sample variance. Wheat's annual increment is 0.312. With only roughly two dozen annual observations and many contemporaneous regressors, large raw $R^2$ values must not be interpreted as validated predictive accuracy. The paper does not report adjusted fits, holdout performance, or a penalized model comparison.

## Latent forecasts and identification

Observable regressions can leave common residuals because market participants have additional information about future macroeconomic conditions. The authors introduce two latent variables: the time-$t$ forecast of inflation over $t$ to $t+1$, and the corresponding forecast of industrial-production growth. Let $J_t$ collect those forecasts; let $X_t$ collect the observable direct controls and their lags; and let $Z_t$ contain current and lagged M1 and stock changes. A compact representation is

$$
J_t=A X_t+B Z_t+v_t,\qquad
\Delta p_t=C X_t+GJ_t+\varepsilon_t,\qquad
y_{t+1}=J_t+w_{t+1}.
$$

The last equation anchors the latent variables in realized future macroeconomic changes. Rational forecast errors $w$ are orthogonal to time-$t$ information. The model assumes normal disturbances, unrestricted covariance within $v$ and within $w$, and cross-block orthogonality among $v$, $w$, and commodity-specific $\varepsilon$ at all leads and lags. The diagonal restriction is imposed only on the contemporaneous covariance of the seven-dimensional $\varepsilon$ vector and then tested by freeing its 21 off-diagonal elements.

Two strong restrictions make this model testable. Money and stock prices affect commodity prices only through the specified forecasts, not through an additional direct liquidity, discount-rate, or portfolio channel. Also, the latent forecast vector is assumed rich enough to span the unobserved information relevant for forecasts of all future macro states entering commodity prices. Two one-period forecasts do not automatically span the entire term structure of private information; the paper explicitly calls the relevant full-rank condition strong.

Conditionally on observable causes, a useful implementation check is the model-implied covariance block

$$
\operatorname{Var}\begin{pmatrix}\Delta p_t\\y_{t+1}\end{pmatrix}
=
\begin{pmatrix}
G\Omega G'+\Sigma_\varepsilon&G\Omega\\
\Omega G'&\Omega+\Psi
\end{pmatrix},
$$

where $\Omega=\operatorname{Var}(v)$ and $\Psi=\operatorname{Var}(w)$. The exclusion restrictions also govern covariance with $Z$. The authors estimate the system by Gaussian maximum likelihood in LISREL using the correlation matrix of commodity changes, controls, instruments, and future macro outcomes. Positive covariance matrices and the unit loadings in the realization equations are part of identifying a reproducible fit.

Replacing $J_t$ with realized $y_{t+1}$ and running instrumental variables is not sufficient for the residual-correlation test. The resulting residual contains the shared forecast error term $-Gw_{t+1}$, whose cross-commodity covariance can be nonzero even under the economic null. This is the central reason for modeling forecasts and realizations jointly rather than interpreting IV residual correlations directly.

## Latent-model estimates and robustness

Table 7 reports generally positive expected-inflation loadings: 1.334 wheat (t=1.8), 1.483 cotton (1.9), 2.037 copper (2.1), 1.876 gold (2.1), 2.247 oil (2.3), −1.648 lumber (−1.2), and 0.563 cocoa (0.9). Expected production growth has its clearest reported loading for lumber, 2.290 with t=2.4; the other loadings are not individually strong at conventional two-sided levels. The commodity-equation fits are 0.08, 0.13, 0.26, 0.39, 0.31, 0.39, and 0.09. The two forecast equations have $R^2$ values 0.65 and 0.35. These results show useful modeled common forecast information without making every loading statistically precise.

The less restricted model, allowing commodity residual covariance but retaining the forecast structure and exclusions, has a likelihood-ratio statistic of 35.5 against a fully unconstrained alternative, with 25 degrees of freedom. It is not rejected at 5%. This is a specification check with limited power, not proof that the exclusions are true. Imposing the additional 21 diagonal restrictions raises the statistic by 49.7, significant at 1%. Thus modeled forecast information reduces but does not eliminate residual co-movement.

A model with expected inflation alone gives 48.2 for the diagonal test; expected production alone gives 57.0. The slightly smaller first statistic does not make the inflation-only model generally superior: its secondary restrictions yield 51.8 on 27 degrees of freedom and reject at 1%. The comparison concerns two different restrictions, which should not be conflated. With lagged dependent variables, the corresponding diagonal statistics are 49.7 for two factors, 46.3 for inflation alone, and 40.3 for production alone. Attempts to add more lags to the latent specification fail to converge. The source reports that failure rather than a completed large-lag robustness result.

Additional observable-regression checks yield diagonal-test statistics of 77.1 after excluding October 1973–December 1974, 75.4 when extending through October 1986, and 83.0 when ending in November 1984. The main sample stops before a major 1986 change in U.S. cotton-market intervention. Adding U.S. heating degree days, cooling degree days, temperature, and precipitation gives 87.7. All remain strong rejections under the reported reference tests. These checks weaken a simple oil-shock-window explanation without exhausting common global fundamentals.

## Interpretation and replication limits

The paper considers missing macro variables, slow transmission of macro news, high-frequency idiosyncratic noise, common speculator liquidity, and bubbles or market psychology. Longer-horizon correlation is compatible with several of these mechanisms. Monthly measurement noise can wash out at longer horizons; omitted slow-moving fundamentals can become more important; shared wealth constraints can transmit larger accumulated losses. None of those explanations is separately identified by the diagonal-covariance rejection.

To reproduce the study, one must reconstruct the historical cash series and macro transformations, align the sample and aggregation endpoints, estimate the OLS and dynamic systems with common observation sets, recreate the constrained and unconstrained covariance likelihoods, and then fit the anchored latent model with its exclusions. The source lacks original code, starting values, convergence tolerances, raw correlation input to LISREL, covariance estimates, exact Monte Carlo generator settings, and sufficient detail on data vintages. Modern bootstrap or heteroskedasticity-robust extensions would be additional work, not reported source results.

The finding is therefore best used as evidence that a small observable macro model can materially understate cross-commodity dependence. It motivates checking common residual factors in diversification and stress analysis. It does not supply an investment rule, estimated trading costs, portfolio leverage, rebalancing schedule, expected alpha, or a causal estimate of speculative financialization. Those quantities cannot be inferred from contemporaneous cash-price $R^2$ or from the rejection of a joint storage-and-information specification.
