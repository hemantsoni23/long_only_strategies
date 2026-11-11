# Macroeconomic releases and the interest rate term structure

Biao Lu and Liuren Wu, *Journal of Monetary Economics* 56 (2009), 872–884. DOI: 10.1016/j.jmoneco.2009.06.005. Source: [DynamicFactorModels_LuWu2009.PDF](../../Finance/DynamicFactorModels_LuWu2009.PDF), 13 PDF pages. Section and table numbers below refer to this source.

## Why this matters

This paper asks whether the information arriving in macroeconomic releases can account for movements across the interest-rate curve. Its useful innovation is to combine a dynamic factor filter that respects the actual dates of noisy economic announcements with a no-arbitrage term-structure model. Inflation and output indicators arrive at different times, have different measurement precision, and overlap in the economic information they contain. Treating their common component as a continuously evolving state gives a coherent way to connect these announcements to rates at many maturities.

The first empirical exercise extracts two states from macro releases alone and then fits LIBOR and swap rates using those states. The reported predictive-variation statistic is about 78–82% across the ten rate series. A second exercise filters the states jointly from macroeconomic and interest-rate observations and produces much higher fitted explanatory power. The distinction is essential: the second exercise uses yields to infer the very states used to explain yields. It cannot establish that releases alone forecast almost all rate variation.

For implementation, the central object is a release-calendar state-space model, followed by an affine bond-pricing model whose physical and risk-neutral persistence need not coincide. This distinction explains how inflation-related information can have a persistent effect across maturities while output-related information has a stronger effect at the short end. The results are an estimated historical association within the specified model, rather than an identified causal announcement experiment or a validated trading strategy.

## Data and the information set

The common estimation period is January 2, 1990 through May 26, 2004, covering 3,633 business days. The text and interest-rate section use January 2, whereas Table 1's notes print January 29; the exact initial-date alignment should be checked against the original data. The dynamic state advances daily with year fraction $\Delta=1/252$. Macro data come from MMS International and are used as originally released, dated by the actual release date. Individual histories begin earlier, between January 1960 and July 1989, but those start dates do not define the common estimation window.

There are seventeen release series. Seven measure inflation: CPI, core CPI, PPI, core PPI, the PCE deflator, core PCE deflator, and GDP deflator. Ten concern output and related activity: real GDP, industrial production, nonfarm payrolls, durable-goods orders, durable-goods orders excluding transportation, retail sales, capacity utilization, business inventories, consumer spending, and personal income. These are not seventeen daily observations. On a typical business day, only a small subset is released, and on many days there is no release.

All series are monthly releases except real GDP and the GDP deflator, whose reference period is quarterly. The authors include all three scheduled GDP readings for each quarter: preliminary, revised, and final. Consequently, GDP-related information can arrive every month even though it refers to a quarter. A replication must retain these separate vintages instead of replacing them with a single final quarterly observation. Repeated readings of the same underlying quarter also make independent measurement errors a substantive simplifying assumption.

Most variables enter as year-over-year percentage changes. Inflation is the percentage change in the current price index relative to twelve months earlier. Nonfarm payrolls enter as the cumulative twelve-month change in millions of jobs. Capacity utilization enters as a decimal level. Every series is then standardized to zero mean and unit standard deviation. Table 1 gives, for example, CPI mean 2.85 and standard deviation 1.09 percentage points, real-GDP growth 2.81 and 1.57, industrial production 1.90 and 3.00, and nonfarm payrolls 1.21 and 1.43 million. Capacity utilization has mean 0.81 and standard deviation 0.03.

The interest-rate data are daily Bloomberg eurodollar LIBOR rates at one, two, three, six, and twelve months, and swap par rates at two, three, five, seven, and ten years. LIBOR rates are simply compounded. The swap rates are par rates, rather than zero-coupon yields. Their measurement functions therefore differ from the affine continuously compounded spot-yield formula derived below. The period is the same as the macro common sample. Figure 1 shows substantial changes in both levels and curve shapes; one-month LIBOR falls from 8.37% at the beginning to approximately 1.1% at the end.

Actual release dates protect against one important kind of look-ahead: using a statistic before publication. They do not, by themselves, turn a full-sample parameter estimate into an out-of-sample forecast. The paper does not specify a separate training period, rolling re-estimation protocol, or held-out evaluation sample. Nor does it state a real-time rolling convention for estimating standardization constants. A reproduction of the reported historical fit should therefore be distinguished from an investable forecasting experiment.

## The macroeconomic state and sparse-release filter

Let $X_t$ be a two-dimensional state and let $M_t$ contain the standardized macro observations available on day $t$. The state equation is

$$
X_t=F X_{t-1}+\sqrt{Q}\,\epsilon_t,
\qquad Q=I_2\Delta,
\qquad \epsilon_t\sim N(0,I_2).
$$

The source calls the transition matrix $\Phi$. The state has a zero long-run mean. The innovation covariance is normalized to identity per unit time. This is not the same as setting the unconditional covariance of $X_t$ equal to identity: for a stable transition, its stationary covariance solves $P=FPF^\top+Q$.

The full observation equation is

$$
M_t=H X_t+e_t,
\qquad e_t\sim N(0,R_M).
$$

Here $H$ is a $17\times2$ loading matrix and $R_M$ is diagonal, with a distinct measurement-error variance for each series. The model treats measurement errors as mutually independent. It pools a common low-dimensional economic signal while allowing some individual statistics to be much noisier than others. In practice, on each date the algorithm selects only the rows of $H$, observations, and error covariance corresponding to releases that actually occur.

For clarity, write $x_t^-$ and $P_t^-$ for the predicted state mean and covariance, and $x_t^+$ and $P_t^+$ for the filtered quantities after observing that day's releases. The prediction is

$$
x_t^-=F x_{t-1}^+,
\qquad P_t^-=F P_{t-1}^+F^\top+Q.
$$

For the available observation rows, define the innovation $v_t=M_t-H_t x_t^-$ and covariance $S_t=H_tP_t^-H_t^\top+R_{M,t}$. The Kalman gain and update are

$$
K_t=P_t^-H_t^\top S_t^{-1},
\qquad x_t^+=x_t^-+K_t v_t,
\qquad P_t^+=P_t^--K_tS_tK_t^\top.
$$

If there is no release, the predicted state becomes the filtered state without a measurement update. If several releases occur together, the gain jointly weights their innovations using their loadings, uncertainty, and estimated measurement noise. A larger error variance generally reduces an observation's influence, conditional on the other components. This is the precise mechanism replacing an arbitrary assumption that all announcements are equally informative.

Parameters are estimated by maximum likelihood using Gaussian forecast errors. Up to constants, the contribution of an observed release vector of dimension $n_t$ is

$$
\ell_t=-\frac12\left(n_t\log(2\pi)+\log\det S_t+v_t^\top S_t^{-1}v_t\right).
$$

The dimension changes across dates. Missing releases must be omitted from the likelihood, rather than inserted as zero standardized surprises. Treating a missing observation as an observed zero would artificially pull the state toward its mean. The paper does not provide the optimizer, starting values, exact initial covariance, or every fitted measurement variance. Those are missing inputs to an exact numerical reproduction, even though the filtering equations are explicit.

With an isotropic state innovation covariance, orthogonal rotations of the state can preserve the observation model. The authors constrain the first factor's CPI loading and the second factor's real-GDP loading to be positive to help interpretation. These sign choices alone do not eliminate every rotational ambiguity. The parameterization used in estimation, including restrictions visible in the reported mean-reversion matrix, matters when comparing specific numerical loadings.

## What the release filter extracts

Table 2 provides the following loadings and predictive variations. PV is the reported fraction of the original series' variance accounted for through its prediction-error variance, $1-\operatorname{Var}(\text{prediction error})/\operatorname{Var}(\text{series})$.

| Standardized release | First loading | Second loading | PV |
|---|---:|---:|---:|
| CPI | 0.579 | -0.117 | 0.763 |
| Core CPI | 0.544 | -0.210 | 0.895 |
| PPI | 0.341 | -0.027 | 0.200 |
| Core PPI | 0.458 | -0.173 | 0.618 |
| PCE deflator | 0.520 | -0.195 | 0.845 |
| Core PCE deflator | 0.482 | -0.235 | 0.916 |
| GDP deflator | 0.485 | -0.237 | 0.915 |
| Real GDP | 0.059 | 0.387 | 0.751 |
| Industrial production | 0.236 | 0.390 | 0.664 |
| Nonfarm payrolls | 0.414 | 0.449 | 0.972 |
| Durable goods | 0.053 | 0.220 | 0.208 |
| Durable goods excluding transportation | 0.117 | 0.254 | 0.264 |
| Retail sales | -0.062 | 0.284 | 0.447 |
| Capacity utilization | 0.631 | 0.327 | 0.822 |
| Business inventories | 0.387 | 0.323 | 0.581 |
| Consumer spending | 0.484 | 0.111 | 0.353 |
| Personal income | 0.601 | 0.333 | 0.821 |

All seven inflation variables have significant positive loadings on the first factor. All ten output-related series have positive significant loadings on the second. This motivates calling them inflation-related and output-related factors, respectively. They are inferred latent states with economically interpretable loadings; the paper's claim of explaining rates without latent factors means without additional nonmacroeconomic latent factors, not that the two dynamic states are directly observed.

The PV values differ substantially. Payrolls reach 97.2%, core PCE 91.6%, and GDP deflator 91.5%, while PPI and durable goods are near 20%. Thus the model does not claim equally precise reconstruction of every macro statistic. Some of the apparent fit reflects the persistent year-over-year transformations being modeled. None of these entries is the fraction of intraday announcement-return variance explained by a surprise regression.

## Linking the states to the yield curve

The instantaneous short rate is affine:

$$
r(X)=a_r+b_r^\top X.
$$

For pricing, the source writes a continuous-time analogue of the state dynamics,

$$
dX_t=-\kappa X_t\,dt+dW_t,
\qquad \kappa=-\frac{1}{\Delta}\log F,
$$

with principal matrix logarithm. The affine market price of risk is $\gamma(X)=\gamma_0+\gamma_1X$. Under the corresponding risk-neutral dynamics, the state drift is $-\gamma_0-(\kappa+\gamma_1)X$. Physical persistence and pricing persistence can therefore be quite different.

A zero-coupon bond of maturity $\tau$ has price

$$
P(X,\tau)=\exp[-a(\tau)-b(\tau)^\top X],
\qquad y(X,\tau)=\frac{a(\tau)+b(\tau)^\top X}{\tau}.
$$

The coefficient functions solve the source's Equation 9:

$$
a'(\tau)=a_r-b(\tau)^\top\gamma_0-\frac12b(\tau)^\top b(\tau),
$$

$$
b'(\tau)=b_r-(\kappa+\gamma_1)^\top b(\tau),
\qquad a(0)=0,\quad b(0)=0.
$$

These equations specify a reproducible numerical pricing procedure: solve the two-dimensional linear equation for $b$ and integrate the scalar equation for $a$, then construct each instrument's quote from discount factors. A simply compounded rate can be reconstructed as $L(\tau)=[P(\tau)^{-1}-1]/\tau$. A standard single-curve par swap rate is $(1-P(T))/\sum_j\delta_jP(t_j)$ for fixed-leg accrual fractions $\delta_j$. These are implementation identities; the paper does not report all fixed-leg frequencies, day counts, holidays, or quote-conversion details needed to match the Bloomberg instruments exactly.

The daily state covariance $Q=I\Delta$ is also worth preserving accurately. For an exactly sampled continuous OU process with identity diffusion, the transition covariance would instead be $\int_0^\Delta e^{-\kappa s}e^{-\kappa^\top s}\,ds$. Setting the transition mean through the matrix logarithm does not make $I\Delta$ that exact covariance. The source's specification is naturally read as a daily discrete model with a continuous-time pricing analogue; silently substituting exact OU sampling changes the fitted model.

In the sequential exercise, the state estimates from macro releases are treated as observable and held to their first-stage filtered values. Interest rates have additive pricing errors. Because LIBOR and swap quotes are nonlinear in states, the authors use an extended Kalman treatment and Gaussian quasi-maximum likelihood in this stage. The macro states are not revised by the yield observations in this experiment. This one-way information restriction is what makes the sequential fit informative about the macro-only state representation.

## Parameters, fit, and the economic mechanism

Table 4 reports approximately

$$
a_r=0.045,\qquad b_r=(0.015,0.005)^\top,
\qquad
\kappa=\begin{pmatrix}0.252&0\\0.866&0.252\end{pmatrix},
$$

$$
\gamma_0=\begin{pmatrix}-0.308\\-1.336\end{pmatrix},
\qquad
\gamma_1=\begin{pmatrix}-0.252&0\\-0.030&0.412\end{pmatrix}.
$$

The short rate loads positively on both states. Reported absolute t-statistics for the two short-rate loadings are 168.4 and 102.7. In contrast, the two diagonal physical mean-reversion estimates have t-statistics 0.99 and 1.46; their precise values are much less securely estimated. The off-diagonal market-price coefficient has t-statistic 0.31. Rounded parameter tables are insufficient for machine-precision replication of every fitted rate.

Both physical eigenvalues are about 0.252 per year. The associated scalar decay half-life is about $\log(2)/0.252=2.75$ years, although off-diagonal coupling affects the full vector response. After risk adjustment, the first diagonal becomes approximately zero and the second approximately 0.664. This near cancellation in the inflation direction makes the pricing effect of inflation-related information persist across maturities. The output-related effect decays more rapidly under the pricing dynamics and contributes more strongly to changes in slope.

Table 3 reports PV values 0.797, 0.808, 0.814, 0.821, and 0.811 for one-, two-, three-, six-, and twelve-month LIBOR. The two-, three-, five-, seven-, and ten-year swap entries are 0.785, 0.779, 0.781, 0.784, and 0.783. Thus the range is 77.9–82.1%. These are model prediction-error variance ratios on rate series in the estimation sample. They should not be relabeled as held-out daily-change forecasting $R^2$, return predictability, or a proportion of causal monetary-policy shocks explained.

The authors translate the short-rate equation into a hypothetical CPI/GDP rule by assuming that just these two macro variables are measured without error and identify the two states exactly. With sample-mean inflation $\bar\pi$ and growth $\bar g$, Equation 11 is

$$
r_t=4.54\%+2.19(\pi_t-\bar\pi)+1.22(g_t-\bar g).
$$

Reported standard errors are 0.06, 0.40, and 0.30 in the equation's percentage-rate convention. This is a transformation of estimated state loadings under an explicit noiseless observation assumption. It is not the actual sparse-release Kalman update and is not an independent causal estimate of a Federal Reserve reaction function.

## Yield responses: what Table 5 does and does not measure

Table 5 imagines all seventeen standardized releases being observed simultaneously and the states being recovered without error by least squares:

$$
X=(H^\top H)^{-1}H^\top M.
$$

The reported response at maturity $\tau$ to a one-standard-deviation change in release $i$ is the corresponding component of

$$
\frac{b(\tau)^\top}{\tau}(H^\top H)^{-1}H^\top.
$$

At zero maturity, use $b_r^\top$ in place of $b(\tau)^\top/\tau$. Entries are percentage points. For CPI, the short-rate response is 0.24 percentage points, or 24 basis points, and the ten-year spot response is 0.19 points. Core CPI is 20 and 18 basis points. Real GDP is 12 and 1 basis point; industrial production is 21 and 7. Payrolls are 30 and 12, and capacity utilization is 37 and 20. Retail sales are 4 basis points at the short end but minus 3 at ten years. The pattern is predominantly inflation-driven level exposure and output-driven slope exposure, not a rule that every output variable raises every maturity.

These numbers must not be presented as the response to an actual one-standard-deviation announcement surprise on a particular date. In the operational filter, the change in the state is $K_tv_t$, and the change in a spot yield is $(b(\tau)^\top/\tau)K_tv_t$. That gain depends on the prior state covariance, observation noise, and co-releases. Table 5's hypothetical simultaneous, error-free inversion suppresses those ingredients. For a replication intended to study announcement sensitivity, both objects should be computed and labeled separately.

## Joint estimation and its limits

Section 4 combines available macro releases and interest rates into a joint observation system. Yield data now help extract the two dynamic states. The resulting state orientation changes, so the factor labels from the macro-only exercise no longer carry over automatically. Comparing response coefficients expressed in observed macroeconomic variables is more meaningful than comparing a raw first-factor coefficient across the two parameterizations.

Table 6's macro PV values range from 0.954 for durable-goods orders to 0.985 for core PCE. The joint interest-rate PV entries are 0.994, 0.998, 1.000, 0.995, and 0.983 for the five LIBOR maturities, then 0.976, 0.982, 0.994, 0.998, and 0.992 for swaps. The printed 1.000 is rounded and is not proof of exact prediction. The actual table range is 97.6–100.0% after rounding, which is more precise than repeating the abstract's approximate range.

Joint response estimates can also be much larger. CPI's short and ten-year responses become 1.23 and 0.57 percentage points, real GDP's 1.00 and 0.26, and payrolls' 1.91 and 0.66. These are responses within a jointly fitted representation, not an improvement in a fixed out-of-sample announcement strategy. Yield-informed state extraction, more flexible reconciliation of measurement errors, and a changed economic-state orientation all affect their interpretation.

## Reproduction boundaries and practical takeaways

A faithful reconstruction needs vintage release records, daily release masks, the exact seventeen transformations, and the ten historical market-rate series. Estimate the sparse macro filter first, save its filtered states, and maintain that restriction when fitting the sequential pricing exercise. Solve the affine pricing equations and map discount factors into the observed instruments. Reproduce Tables 2–5 before allowing joint state extraction and reproducing Table 6. Compare covariance normalization, state identification, and units explicitly rather than adjusting a model until only the headline PV matches.

The source leaves several choices insufficiently specified for exact numerical replication: initialization and optimizer settings; the complete measurement-error estimates; precise swap conventions; the standardization estimation window; and full-precision parameters. No transaction costs, portfolio construction, rebalancing rule, trading returns, or forecast-validation exercise is supplied. They cannot be inferred from the term-structure fit. A Gaussian two-factor single-curve model also omits independent liquidity and credit components in LIBOR and swaps, nonlinear policy behavior, and potentially correlated release errors.

The methodological takeaway is strongest where it is most concrete: respect publication timing, aggregate noisy releases with a state filter, and distinguish physical persistence from risk-neutral persistence when translating economic information into yield exposures. The empirical result is a high historical fit from macro-derived states, accompanied by a substantially higher joint fit. The paper supports that modeling architecture and the reported sample relationships. It does not establish that its high PV survives real-time parameter estimation or yields a profitable or causal forecasting rule.
