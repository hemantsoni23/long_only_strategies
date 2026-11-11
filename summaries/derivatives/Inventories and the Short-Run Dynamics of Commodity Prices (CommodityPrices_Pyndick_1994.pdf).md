# Inventories and the Short-Run Dynamics of Commodity Prices

Robert S. Pindyck, *RAND Journal of Economics* 25(1), Spring 1994, pp. 141–159. [Source PDF](../../Finance/CommodityPrices_Pyndick_1994.pdf). The original filename's spelling is preserved. PDF page 2 is printed page 141; the supplied 20-page file includes its cover and the complete appendix and references.

## Why this matters

Inventory models often infer production smoothing from the observation that production varies less than sales. That inference is not identified by the variance comparison alone. Firms can also hold stocks to organize deliveries, maintain continuity of operations, and avoid costly stockouts. These services make the last units of inventory particularly valuable even when reducing stocks would save financing and physical storage costs. Pindyck connects this distinction to observable commodity futures prices: the spot–forward relation provides a monetary measure of the marginal benefit of having physical inventory.

The substantive contribution is an empirical structural model combining a convex marginal convenience-yield function with production and inventory Euler equations. Futures prices identify the scale of inventory services, while physical production and inventory quantities permit estimation of marginal production and adjustment costs in absolute units. A second specification substitutes the futures-implied convenience yield directly into the Euler equation, removing the inventory-service functional form and measured stocks from that part of the model. This is a valuable specification check because inventory measurement and the assumed service curve need not be accurate for production costs to be estimated.

The evidence concerns monthly US copper, softwood lumber, and heating oil in the 1970s and 1980s. It supports increasing marginal production costs for heating oil, but does not establish a robust positive adjustment-cost mechanism: the positive reduced-system lumber estimate occurs in a system whose restrictions are rejected. For all three commodities, the value of inventory becomes steeply convex as the inventory-to-sales ratio falls. Thus inventory can moderate price movements when stocks are ample, yet become very expensive to draw down in periods of scarcity. The paper does not estimate a trading strategy or an out-of-sample price predictor. Its application is to interpreting physical scarcity and designing commodity valuation or operational models whose inventory services remain economically plausible near low stocks.

## Objects, timing, and the carry measurement

Let $P_t$ be the end-of-month commodity spot price, $y_t$ production during month $t$, $Q_t$ sales during that month, and $N_t$ end-of-month inventory. The accounting identity is

$$
N_t=N_{t-1}+y_t-Q_t.
$$

The distinction between a flow and a stock is material. The explanatory ratio in the inventory-service curve is $N_t/Q_{t+1}$, current end-of-period stocks relative to next-period sales. Production and inventories are measured in physical units, not nominal expenditure divided by a price index. Copper quantities are short tons; lumber quantities are millions of board feet; heating-oil quantities are millions of barrels. Price units in the figures are cents per pound for copper, dollars per thousand board feet for lumber, and cents per gallon for heating oil. Production-cost coefficient units must be interpreted with those conversions rather than compared directly across commodities.

The model represents marketing or operating costs by $\Phi(N_t,E_tQ_{t+1},P_t)$. It assumes $\Phi_N<0$, $\Phi_{NN}>0$, and increasing costs with anticipated sales and price. Low inventory increases the cost of arranging production and deliveries or avoiding a stockout. Marginal inventory services are $-\Phi_N$. With direct storage cost $a$ per physical unit per period, the net marginal convenience yield is

$$
\psi_t=-\Phi_N-a.
$$

Here $\psi$ is a monetary amount per unit of commodity for the holding period. It is not automatically a percentage yield or an annualized rate. A percentage convenience yield would divide by an appropriate price, with an explicit time convention. Negative net convenience yield can occur when gross service benefits are smaller than direct storage costs.

For a delivery horizon $\tau$, let $f_{t,\tau}$ be the forward price, $r_{\tau,t}$ the nominal holding-period interest rate, and $\psi_{t,\tau}$ the present value of the net services over that interval. The carry relation, equation (1a), is

$$
(1+r_{\tau,t})\psi_{t,\tau}
=(1+r_{\tau,t})P_t-f_{t,\tau}.
$$

Writing $R_{\tau,t}=1/(1+r_{\tau,t})$ gives $\psi_{t,\tau}=P_t-R_{\tau,t}f_{t,\tau}$. The capitalized service value is $(1+r_{\tau,t})\psi_{t,\tau}$. This distinction prevents mixing the service flow with its terminal value. It is a carry-based measure maintained by the model, not a direct observation of each firm's avoided delivery costs. A risk premium in expected future spot prices does not enter this contemporaneous carry identity; therefore the futures basis alone does not identify that risk premium.

The empirical exercise substitutes a futures price $F$ for the forward price $f$. The appendix, printed page 158, explicitly examines the resulting bias rather than assuming that futures and forwards are exactly equal under stochastic rates. Its covariance expression is

$$
F_{T,t}-f_{T,t}
=-\int_t^T F_{T,w}\operatorname{cov}
\left(\frac{dF_{T,w}}{F_{T,w}},\frac{dB_{T,w}}{B_{T,w}}\right)dw,
$$

where $B_{T,w}$ is the price of a bond paying one dollar at $T$. Approximating bond-price changes by duration times yield changes and replacing the futures price in the integral by its average produces the one-month estimate $\bar r\,\widehat{\operatorname{cov}}(\Delta r/r,\Delta F/F)$. Using the three-month Treasury-bill yield and nearest active futures contract, reported percentage biases are 0.0030% for copper, −0.0032% for lumber, and 0.0077% for heating oil. The last is less than one hundredth of a cent for the one-month contract. This is an empirical short-horizon approximation for these data, not a general equality theorem.

## Nonlinear inventory services and descriptive evidence

Equation (2) specifies

$$
\psi_t=\beta P_t\left(\frac{N_t}{Q_{t+1}}\right)^{-\phi}-a,
\qquad \beta>0,\quad\phi>0.
$$

The estimated implementation includes monthly shifts in $a$. Holding price and expected sales fixed, the gross service value declines with stocks and is convex in stocks. Its level diverges as stocks approach zero. The model therefore operates with positive inventories and does not generate the literal stockout regime central to some competitive-storage models. Pindyck argues that low physical stocks, liquid spot and futures markets, and costly potential stockouts can make this a reasonable approximation, while acknowledging that the service function is imposed rather than derived from a fully specified scheduling technology.

The conditional expectation in structural estimation must be treated carefully. The paper's descriptive curve uses realized $Q_{t+1}$, while the decision problem depends on information at $t$. In the estimating equations, future realizations replace conditional expectations and create forecast errors. In particular, $E_t[(N_t/Q_{t+1})^{-\phi}]$ is generally different from $(N_t/E_tQ_{t+1})^{-\phi}$. A reproduction should state which object it computes rather than silently moving the expectation inside this nonlinear function.

Table 1, printed page 147, reports detrended production-to-sales variance ratios of 0.701 for copper, 0.976 for lumber, and 0.380 for heating oil. After removing monthly seasonality and time trends, the ratios are 0.680, 1.011, and 0.744. Thus the apparently strong smoothing in heating oil is partly seasonal. Production–sales correlations are 0.728, 0.964, and 0.198 before deseasonalizing, and 0.698, 0.962, and 0.399 afterward. Lumber production tracks sales closely; heating-oil stocks accommodate much more of the seasonal difference.

The table also normalizes production-to-inventory variance ratios by squared mean quantities. Those ratios are 0.191, 3.187, and 0.263 for copper, lumber, and heating oil; their deseasonalized counterparts are 0.149, 9.035, and 0.391. These are descriptive variance statistics, not estimates of a causal smoothing effect. Demand shocks, cost shocks, and operating constraints can produce similar variance patterns.

Figures 1–3 plot spot prices and monthly net convenience yields. In December 1987, copper's reported yield was about ten cents per pound per month, roughly 8% of its price. The discussion notes a subsequent 1988 value around forty cents, nearly 30% of price, outside the formal copper estimation endpoint. Lumber and heating oil also reached service values around 8–10% of price. These are monthly monetary-service ratios, not annualized investment returns. The willingness to maintain substantial inventories despite such expensive foregone services motivates the operating-cost interpretation.

Figures 4–6 plot service value against the inventory-to-next-month-sales ratio and show a sharp increase at low stocks. Table 2 fits the nonlinear curve separately, with monthly dummies and an AR(1) correction. The estimates are:

| Commodity | $\beta$ (SE) | $\phi$ (SE) | AR coefficient | $R^2$ | DW |
|---|---:|---:|---:|---:|---:|
| Copper | 0.0120 (0.0021) | 0.9050 (0.1088) | 0.75 | 0.922 | 1.72 |
| Lumber | 0.0934 (0.0073) | 0.3029 (0.1540) | 0.50 | 0.814 | 1.62 |
| Heating oil | 0.1107 (0.0223) | 0.8110 (0.2788) | 0.54 | 0.609 | 2.21 |

The joint seasonal-dummy $F$ statistics are 2.79, 2.75, and 3.66, all marked significant at 5%. The linear-in-inventory special case corresponds to $\phi=-1$, not $\phi=1$ or zero, and is rejected. These preliminary estimates are not the later joint-system estimates: the latter impose production and inventory optimality at the same time.

## The cost model and reconstructable Euler equations

Define seasonal marginal production cost $c_t=c_0+\sum_{j=1}^{11}c_jD_{jt}$ and seasonal storage cost $a_t=a_0+\sum_{j=1}^{11}a_jD_{jt}$. The per-period cost in equation (3) is

$$
C_t=(c_t+\gamma'w_t+\eta_t)y_t
+\frac12by_t^2+\frac12\beta_1(\Delta y_t)^2
+\Phi(N_t,E_tQ_{t+1},P_t)+(a_t+\nu_t)N_t.
$$

Here $b$ controls the slope of marginal production cost, $\beta_1$ the quadratic adjustment cost, $w_t$ measured input-cost variables, and $\eta_t,\nu_t$ unobserved production and storage/marketing shocks. The inventory coefficient $\beta$ and adjustment coefficient $\beta_1$ are distinct. Producers take prices as given and choose production and sales to maximize

$$
E_t\sum_{\tau=0}^{\infty}R_{\tau,t}
\big(P_{t+\tau}Q_{t+\tau}-C_{t+\tau}\big),
$$

subject to the stock-flow identity and nonnegative inventories. The assumed divergence of inventory services as stocks vanish makes the solution interior in the maintained model. Nominal prices and costs are discounted with nominal factors.

It is useful to collect direct marginal production cost as $m_t=c_t+\gamma'w_t+by_t+\eta_t$. The sales/output first-order condition, equation (6), becomes

$$
P_t=m_t+\beta_1\big(\Delta y_t-R_{1,t}E_t\Delta y_{t+1}\big).
$$

Producing one extra unit now increases current adjustment costs, but changes the next period's adjustment cost in the opposite direction. The inventory first-order condition compares producing now with drawing stocks down and replacing them later. In compact notation, equations (7) and (8) imply

$$
\psi_t=E_t\left[m_t-R_{1,t}m_{t+1}
+\beta_1\big(\Delta y_t-2R_{1,t}\Delta y_{t+1}
+R_{2,t}\Delta y_{t+2}\big)\right],
$$

with the corresponding storage-cost shock included in the measured-service relation. The coefficient two on the one-period-ahead change follows from perturbing both current and subsequent production changes. It is not the single-period adjustment term from equation (6).

For implementation, the independent carry/service equation is

$$
R_{1,t}F_{1,t}-P_t
=a_t-\beta P_tE_t\left[\left(\frac{N_t}{Q_{t+1}}\right)^{-\phi}\right]+\nu_t.
$$

The full system estimates equations (6), (7), and (8) with common parameters. Alternatively substitute $P_t-R_{1,t}F_{1,t}$ for the marginal convenience yield in the inventory equation. This gives equation (7a), together with equation (6), and eliminates $N_t$, $\beta$, $\phi$, and $a_t$ from that system. The reduced system still relies on the futures-implied service measure and the production cost structure. It does not establish that inventory services are irrelevant; it absorbs their observed marginal value into an Euler restriction.

## Data construction and estimation

The formal data section, printed page 152, specifies November 1972–December 1987 for copper and lumber, and November 1978–June 1988 for heating oil. An earlier descriptive discussion starts the first two series in October 1972. Leads and lags reduce the estimation bounds by two months at each end; the paper does not supply a row-level dataset that resolves every descriptive-versus-estimation boundary. A reproduction should follow the formal sample statement and document any initial month used solely to construct a lag.

Copper production is US refined output from ore or recycled scrap; inventories are refined copper at refineries and COMEX warehouses. Stocks in process, at mines and smelters, or unrefined copper at refineries are excluded. Sources are *Metal Statistics* of American Metal Market. Lumber data come from the National Forest Products Association's *Fingertip Facts and Figures*, covering softwood lumber. Heating-oil data are monthly distillate/no. 2 fuel-oil production and end-month stocks from the Department of Energy's *Monthly Energy Review*. Sales are reconstructed as $Q_t=y_t-(N_t-N_{t-1})$. Comparisons with direct sales series are mostly identical, with occasional differences up to 1%.

Input costs are average hourly nonagricultural earnings and the producer-price index for intermediate materials, supplies, and components. Heating oil additionally uses the crude-petroleum PPI. Discount factors use the end-month nominal Treasury-bill rate. The author explicitly ignores systematic risk in production-cost discounting: while the carry equation warrants a risk-free rate, production cost components could have different risk premia. An industry average cost of capital would not automatically solve that problem.

Spot prices are not ordinary monthly-average cash quotations. Cash prices can include relationship-specific discounts, and expiring futures may be thinly traded or absent in a given calendar month. Instead the paper extrapolates the log spread between the nearest and next-nearest active futures contracts:

$$
P_t=F_{1,t}\left(\frac{F_{1,t}}{F_{2,t}}\right)^{n_{01}/n_{12}},
$$

where $n_{01}$ is days from the observation to the nearest expiration and $n_{12}$ days between the two expirations. A 30-day futures equivalent is then $P_t(F_{1,t}/P_t)^{30/n_{01}}$. This assumes a locally linear log term structure; seasonal curvature can create errors. Comparisons with available actual spot-contract prices give root-mean-square percentage errors of 1.21% for copper and 3.99% for lumber, mean percentage errors −0.12% and 0.39%, and correlations 0.998 and 0.983. There is no equivalent heating-oil validation. Re-estimation using actual spot-contract prices when available reportedly gives similar results.

Estimation replaces future conditional expectations by realized values and uses GMM instruments orthogonal to the resulting composite errors. Forecast errors are orthogonal to time-$t$ information under rational expectations, but unobserved cost shocks need not be. Therefore lagged endogenous quantities are not automatically valid. The selected instruments are seasonal dummies and current and once-lagged M1, industrial production, housing starts, PPI inflation, S&P 500 growth, labor-hours growth, the three-month Treasury-bill rate, and the trade-weighted dollar against other G-10 currencies. Copper and lumber also use crude-oil price instruments. The stated totals are 30 instruments for copper and lumber and 28 for heating oil.

The residuals initially exhibit AR(1) dependence. Equations (6), (7), and (7a) are quasi-differenced and re-estimated, with separate AR coefficients for the two production-related restrictions. The reported standard errors are asymptotic and heteroskedasticity consistent. The paper does not provide the complete weighting-matrix algorithm, starting values, numerical tolerances, revised data vintages, or a calendar-to-dummy mapping. Those are missing replication inputs, not parameters that can be inferred from the regression tables. One should preserve the effective sample induced by two leads, lags, and quasi-differencing rather than compare GMM objectives computed on different rows.

## Structural estimates, restrictions, and limits

Tables 3–4 provide the central production estimates. Parentheses below are standard errors.

| System and parameter | Copper | Lumber | Heating oil |
|---|---:|---:|---:|
| Full system $b$ | −0.0000021 (0.0000028) | −0.0038 (0.0027) | 0.1551 (0.0343) |
| Full system $\beta_1$ | −0.0000011 (0.0000012) | −0.0004 (0.00093) | −0.0689 (0.0124) |
| Reduced system $b$ | 0.0000018 (0.0000024) | −0.0057 (0.0023) | 0.2357 (0.0621) |
| Reduced system $\beta_1$ | −0.00000052 (0.00000083) | 0.0019 (0.00069) | −0.1048 (0.0208) |

Negative adjustment estimates do not represent economically meaningful negative adjustment costs in a convex-cost technology. They show that the maintained positive-cost interpretation is not supported by those estimates. The reduced lumber estimate is positive, but lumber's overall model restrictions are rejected; it is therefore inappropriate to describe the exercise as establishing a robust adjustment-cost mechanism. Similarly, the reduced lumber marginal-cost slope is significantly negative, whereas heating oil's positive slope appears in both systems.

For heating oil, the full-system estimate implies that the increasing-marginal-cost component accounts for about 15% of price on average. Temporary output increases add approximately three to six cents to marginal cost. This provides a production-smoothing rationale when stocks are normal or high. The fitted service curve shows why that conclusion does not extend unchanged into scarcity: drawing down the last inventories sacrifices increasingly valuable operating services.

The full-system inventory-service parameters are copper $\beta=0.0133$ (0.0011), $\phi=0.7551$ (0.0710); lumber 0.2378 (0.0407), 3.092 (0.5230); and heating oil 0.0854 (0.0096), 1.420 (0.1555). Their seasonal base costs $a_0$ are 0.3795 (0.0588), 7.510 (0.9113), and 0.8913 (0.4526), in the commodity's price units per month. Eleven additional monthly coefficients shift these bases; Table 3 gives them explicitly. The substantial differences from the separate nonlinear regressions, particularly lumber's $\phi$, show the effect of joint restrictions and should not be concealed by presenting one set as interchangeable with the other.

The full-system $J$ statistics are 77.43, 93.38, and 60.38 with 59, 59, and 52 degrees of freedom. Only lumber is marked rejected at 5%. The reduced-system values are 43.32, 65.26, and 34.99 with 43, 43, and 38 degrees of freedom; again lumber rejects. Nonrejection for copper and heating oil is a failure to reject the joint moment restrictions, not proof that every cost assumption or instrument is correct. The fitted AR coefficients are very persistent: full-system pairs are (0.9443, 0.9895), (0.9886, 0.9550), and (0.9962, 0.8962); reduced pairs are (0.9694, 0.9757), (1.000, 0.9878), and (0.9899, 0.8444). Near-unit persistence warrants caution about finite-sample precision and the quasi-differenced specification.

Reported robustness exercises substitute next-period price in the service curve, use quarterly observations, add cubic production costs, and introduce a risk-premium parameter into production discount factors. Results remain broadly similar; cubic terms are insignificant, and the risk-premium additions are insignificant or quantitatively unimportant. Detailed alternative tables are not supplied, so these checks cannot be reproduced numerically from the article alone.

The most important remaining limitation is structural. Symmetric quadratic adjustment costs omit irreversibilities such as closing a mine, refinery, or smelter and later restarting it. Such sunk costs can preserve production through large price movements without resembling a smooth quadratic penalty. Monthly first-order conditions may also be too restrictive for actual operational decisions. The evidence favors sharply nonlinear inventory services and a limited heating-oil smoothing role; it does not identify a universally valid commodity supply technology, a stockout probability, or an executable futures premium.
