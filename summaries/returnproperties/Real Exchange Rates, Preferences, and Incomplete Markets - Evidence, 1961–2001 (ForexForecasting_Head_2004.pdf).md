# Real Exchange Rates, Preferences, and Incomplete Markets: Evidence, 1961–2001

**Allen C. Head, Todd D. Mattina, and Gregor W. Smith. Canadian Journal of Economics 37(3), August 2004, pp. 782–801.**

**Source:** [ForexForecasting_Head_2004.pdf](../../Finance/ForexForecasting_Head_2004.pdf), complete article, five results tables, data appendix, and references; local PDF page 1 is a JSTOR cover. Printed page numbers are used below.

## Why this matters

A large class of international macroeconomic models implies that real exchange rates move with relative marginal utilities of consumption. This restriction can fail even when a model reproduces the persistence or volatility of each series separately. Head, Mattina, and Smith ask which preference specifications can make the cross-country restriction empirically credible before one commits to solving and calibrating a full general-equilibrium model.

Their contribution is a systematic nonlinear moment-condition comparison. They extend consumption-only utility to government spending, employment, money balances, and external habit, and examine two approaches to incomplete asset markets. The principal positive result is narrow: external habit produces plausible, precisely estimated composite parameters in a pooled panel and passes the reported overidentification test. Individual-country estimates are much weaker. Several competing specifications also pass a panel overidentification test, but only by choosing economically inadmissible preference parameters.

For implementation, the paper is a specification-testing exercise, not an exchange-rate trading strategy. It does not report out-of-sample currency forecasts, transaction costs, portfolio weights, or Sharpe ratios. Its useful output is a set of moment restrictions and a disciplined distinction between statistical fit and economic admissibility.

## The common restriction and notation

Let $i$ be a foreign country and $j$ the United States. The nominal exchange rate $e_{ijt}$ is units of country $i$ currency per unit of country $j$ currency. Let $p_{it}$ be the implicit private-consumption price deflator. Define

$$
q_{ijt}=\frac{e_{ijt}p_{jt}}{p_{it}}.
$$

An increase in $q$ is a real depreciation of country $i$ relative to the United States. The utility function depends on a vector $x_{it}$ containing consumption, and $U_c(x_{it})$ denotes marginal utility of private consumption. Under the paper's complete-market setup, the relative-price restriction is

$$
q_{ijt}=\frac{U_c(x_{jt})}{U_c(x_{it})}.
$$

Country-specific constant welfare weights can be absorbed in the level normalization; they disappear in growth rates. Goods-market frictions such as nontraded goods or local-currency pricing do not by themselves eliminate this complete-asset-market marginal-utility restriction. That is why changing only goods-market details may fail to solve the empirical disconnect.

The source uses $\Delta$ for a **gross growth operator**, not a difference: $\Delta x_t=x_t/x_{t-1}$. To avoid confusion, this note writes $G(x_t)=x_t/x_{t-1}$. The exact state-by-state condition becomes

$$
G(q_{ijt})=\frac{G(U_c(x_{jt}))}{G(U_c(x_{it}))}.
$$

An exact equality is clearly too strong for the historical observations. The authors weaken it to a conditional-forecast restriction and estimate unconditional moments formed with predetermined instruments. For a candidate preference vector $\vartheta$, write its implied right-hand side as $m_{it}(\vartheta)$ and define

$$
u_{it}(\vartheta)=G(q_{ijt})-m_{it}(\vartheta),\qquad
E[z_{it}u_{it}(\vartheta)]=0.
$$

Here $z_{it}$ is known before the realization being forecast. The criterion concerns predictability of the discrepancy, not equality of fitted and actual observations. Passing this weaker test is necessary for the complete-market formulation under the maintained measurement and preference assumptions; it does not prove the stronger state-by-state relation.

The paper also applies related restrictions to specified incomplete-market environments. These should be understood as maintained model-specific restrictions. Incomplete markets in general do not imply the complete-market equality of realized stochastic discount factors, and equality of bond Euler equations is not, without further conditions, an unrestricted equality of expected ratios. A replication of the reported estimates should implement the stated moments; an extension to another asset-market structure must derive its own moments.

## Estimation procedure

The estimator is iterated generalized method of moments. For a single country, construct

$$
\bar g_T(\vartheta)=\frac1T\sum_tz_{it}u_{it}(\vartheta),\qquad
\widehat\vartheta=\arg\min_\vartheta\bar g_T(\vartheta)'W_T\bar g_T(\vartheta).
$$

Update the weighting matrix using the covariance of the moment conditions and repeat to convergence. The paper says it uses iterated GMM but does not provide an optimizer, starting values, stopping tolerance, covariance kernel, bandwidth, or an explicit numerical update rule for parameter-dependent lagged-residual instruments. Those details must be documented in a reconstruction rather than presented as reported settings.

In the panel, parameters are common across country pairs, while instruments include a constant and each country's own lagged residual. The covariance weighting accounts for cross-country dependence associated with the common U.S. reference. The reported degrees of freedom imply fourteen moment conditions across seven foreign-country equations. The table's observation count is a count of country-quarter observations, not the number of dates.

Country-specific instruments vary with the utility model. Lagged residuals are intended to exploit the different persistence in exchange-rate and relative-consumption growth. The authors are concerned that weak persistence of relative consumption can make conventional instruments weak. They check a constant-only specification and alternative weighting matrices; the unfavorable consumption-only findings remain. These are useful sensitivity checks, but the article does not supply modern weak-identification-robust confidence sets.

A replication should first estimate unconstrained parameters to reproduce the tables and expose wrong signs. Imposing positive curvature from the outset changes the experiment. A second, explicitly constrained estimation can test the best economically admissible fit, but its estimates and boundary-test distribution would be additional results.

## Data construction and sample boundaries

The universe contains Canada, Denmark, Finland, France, Italy, Japan, New Zealand, Sweden, the United Kingdom, and the United States. Inclusion is driven by availability of disaggregated nondurable-and-services consumption. The principal balanced panel excludes Denmark and New Zealand, leaving seven foreign countries and the U.S. reference. Most table notes state 1981Q2–1999Q3; the habit table starts in 1981Q3 because of the additional lag. Individual-country estimation uses available longer histories, including Bretton Woods observations for relevant countries.

The data appendix, pp. 798–799, specifies the inputs:

- Real government expenditure, real private consumption, and the private-consumption deflator come from OECD Quarterly National Accounts. Most series follow fixed-weight national-accounting conventions, generally with bases compatible with 1992 prices.
- Private consumption is nondurables plus services, excluding durables. For the United States, nominal nondurables and services are summed and divided by the implicit final-consumption deflator, because disaggregated chain-weighted real components are not additive. The U.S. reference year is 1996.
- Nominal exchange rates come from IMF International Financial Statistics and are quarterly averages of local currency per U.S. dollar.
- Employment is an OECD Main Economic Indicators index, base 1995, generally measuring total employment rather than hours worked.
- Money is nominal broad money divided by the consumption deflator. Canada and Italy use M2; Denmark, Finland, France, New Zealand, Sweden, and the United States use M3; Japan and the United Kingdom use M4.
- Seasonal patterns are removed with the RATS `esmooth` command for Swedish consumption and government spending, Japanese consumption, employment data, and money data for Denmark, New Zealand, and Sweden. The complete options and settings are not specified.

The source provides heterogeneous availability windows in Table A1. For example, consumption begins in 1961Q1 for Canada, 1975Q1 for Finland, 1970Q1 for France, Italy, and Japan, 1980Q1 for Sweden, 1983Q1 for New Zealand, 1988Q1 for Denmark, 1955Q1 for the United Kingdom, and 1959Q1 for the United States. These are raw availability dates; effective model samples additionally require all relevant variables and lags.

There is a material reconciliation problem. Table A1 ends French and Swedish consumption in 1998Q4, Italian consumption in 1998Q3, and Japanese consumption in 1999Q1, earlier than the stated balanced-panel endpoint of 1999Q3. The article does not explain how the panel dates and availability table are reconciled. Table 5 also reports 504 observations while retaining the broader panel dates in its note. Exact reproduction therefore requires the original data vintage and actual row mask, not merely the published start and end labels. These conflicts should be recorded, not silently resolved by extrapolating missing consumption.

## Consumption and government spending

The baseline aggregator and utility are

$$
x_{it}=\left[\mu c_{it}^{\omega}+(1-\mu)g_{it}^{\omega}\right]^{1/\omega},\qquad
u(x)=\frac{x^{1-\alpha}}{1-\alpha},
$$

with logarithmic utility at $\alpha=1$. The economically standard curvature condition is $\alpha>0$. The CES limit $\omega\to0$ gives Cobb–Douglas aggregation $x=c^\mu g^{1-\mu}$. Differentiating utility with respect to consumption gives the relative-growth restriction in equation (8):

$$
m_{it}=\left[\frac{G(c_{it})}{G(c_{jt})}\right]^{1-\omega}
\left[\frac{G(x_{it})}{G(x_{jt})}\right]^{\alpha+\omega-1}.
$$

The unrestricted CES parameters are difficult to identify; the paper reports that $\omega$ is insignificant and does not tabulate this version. With Cobb–Douglas aggregation, equation (9) is

$$
m_{it}=r_{c,it}^{\,1-\mu(1-\alpha)}r_{g,it}^{-(1-\mu)(1-\alpha)},
\qquad r_{c,it}=\frac{G(c_{it})}{G(c_{jt})}.
$$

Define $r_g$ analogously. The nested consumption-only model, $\mu=1$, is simply $m_{it}=r_{c,it}^{\alpha}$. This sign is important: higher foreign relative consumption growth is supposed to accompany foreign real depreciation when curvature is positive.

For the Cobb–Douglas government specification, the panel estimates are $\widehat\alpha=-0.85$ with standard error 0.56 and $\widehat\mu=0.32$ with standard error 0.19. The $J$ statistic is 9.77 on twelve degrees of freedom, with reported $p=0.64$ (Table 1). Thus the moments are not rejected, but estimated utility curvature has the wrong sign. Seven of nine country estimates of curvature are negative; the positive estimates for Finland and Japan are imprecise. Five country cases reject at 5% according to the source's table and discussion.

The consumption-only panel estimate is $\widehat\alpha=-0.20$ (0.51), with $J=13.7$ on thirteen degrees of freedom and $p=0.39$ (Table 2). Italy is the conspicuous individual positive estimate: 2.05 (0.65), but its overidentification test has $p=0.04$. A plausible coefficient alone is therefore insufficient. Canada has a near-zero estimate, 0.01 (0.17); the United Kingdom has −0.39 (0.31).

The alternative additive aggregator is $x=c+\psi g$. Its logically implied moment uses $[G(c_i+\psi g_i)/G(c_j+\psi g_j)]^\alpha$. Equation (12) is printed with ambiguous growth notation around the sum; growth of the full aggregate is the interpretation consistent with equation (11) and marginal utility. Results are not tabulated: government spending does not acquire a significant role and curvature estimates are generally negative.

## Employment and money extensions

For employment, the source uses a power utility over a net-consumption measure. In the consumption-only special case, this is $d_{it}=c_{it}-\delta\ell_{it}^{\eta}$, so the estimated relative-growth term is

$$
m_{it}=\left[\frac{G(c_{it}-\delta\ell_{it}^{\eta})}
{G(c_{jt}-\delta\ell_{jt}^{\eta})}\right]^\alpha.
$$

The positivity of net consumption is required to evaluate the power function. Employment indexes are proxies for labor input, not measured leisure. This extension could introduce persistence through relative employment, but the source reports identification failures or wrong-signed $\delta$ and negative curvature. No numerical results table or full initialization protocol is supplied.

For money, replace government spending in the CES aggregator with real balances $m$. Marginal utility is

$$
u_c=\mu c^{\omega-1}
\left[\mu c^\omega+(1-\mu)m^\omega\right]^{(1-\alpha-\omega)/\omega}.
$$

The Cobb–Douglas estimating term becomes

$$
m_{it}(\vartheta)=r_{c,it}^{\,1-\mu(1-\alpha)}r_{m,it}^{-(1-\mu)(1-\alpha)}.
$$

The repeated use of $m$ for money and the prediction function can be avoided in code by calling the latter `predicted_q_growth`. The panel estimates are curvature −1.18 (0.51), consumption weight 0.87 (0.11), and $J=13.54$ on twelve degrees of freedom, $p=0.33$ (Table 3). The prose gives a more precise consumption weight of 0.867, implying a money weight of 0.133. A plausible money share does not rescue negative utility curvature.

Eight of nine country curvature estimates are negative; Japan's positive estimate is imprecise. Seven country tests reject at 5% according to the reported discussion. The individual money-model instruments are a constant, lagged relative consumption growth, lagged relative real-balance growth, and a lagged residual, except that Finland and Sweden omit lagged relative consumption. The government model analogously uses lagged government growth; Italy, Japan, and Sweden omit lagged consumption in that table.

## External habit: the central positive result

The habit model is not an additive surplus-consumption specification. Households evaluate consumption relative to an external benchmark:

$$
u(c_{it},s_{it})=\frac{1}{1-\alpha}\left(\frac{c_{it}}{s_{it}}\right)^{1-\alpha},
\qquad s_{it}=C_{it}^{\delta_0}C_{i,t-1}^{\delta_1}(\xi_i^t)^{\delta_2}.
$$

Here $C$ is aggregate consumption taken as exogenous by an individual household, $\xi_i\ge1$, and the $\delta$ parameters lie between zero and one. Because the benchmark is external, differentiating the household's utility holds $s$ fixed. Substituting aggregate consumption afterward gives

$$
U_{c,it}=C_{it}^{-\alpha+\delta_0(\alpha-1)}
C_{i,t-1}^{\delta_1(\alpha-1)}\xi_i^{t\delta_2(\alpha-1)}.
$$

Only composite parameters are identified:

$$
\phi=\alpha-\delta_0(\alpha-1),\qquad
\theta=\delta_1(\alpha-1),\qquad
\kappa_{ij}=(\xi_i/\xi_j)^{\delta_2(1-\alpha)}.
$$

The corresponding equation (22) is

$$
m_{it}=\kappa_{ij}r_{c,it}^{\phi}r_{c,i,t-1}^{-\theta}.
$$

The negative exponent on lagged relative consumption is essential. In logarithmic form the implied relation is a current relative-consumption-growth term minus a lagged term plus a constant. This explains how a model with positive structural curvature can produce an unfavorable coefficient in a consumption-only regression that omits the lagged benchmark effect. Taking logs here explains the mechanism; the reported estimator uses the nonlinear gross-growth moments, not an ordinary least-squares log regression.

Table 4 reports the panel estimates $\widehat\phi=1.84$ (0.44), $\widehat\theta=1.52$ (0.40), and $\widehat\kappa=1.00$ (0.01). The overidentification statistic is 6.36 on eleven degrees of freedom, with $p=0.85$. The source gives one economically plausible primitive configuration: $\alpha=3$, $\delta_0=0.58$, $\delta_1=0.76$. Indeed, $3-0.58(2)=1.84$ and $0.76(2)=1.52$. This is a consistent decomposition, not unique estimation of those three primitive preference parameters.

The point estimates imply an illustrative log response of approximately $1.84\times0.01=0.0184$ to a one-percentage-point contemporaneous relative-consumption-growth change holding the lag fixed, followed by an opposing lag coefficient of approximately −0.0152. These calculations describe the fitted restriction, not causal impulse responses from a solved dynamic economy. General-equilibrium feedback and the actual consumption process would change a full shock response.

The positive evidence depends on pooling. Individual estimates remain imprecise and frequently have implausible signs. Japan has $\widehat\phi=1.39$ (1.35) and $\widehat\theta=-1.76$ (1.39); the United Kingdom has −1.08 (0.55) and 0.89 (0.46). Country overidentification $p$ values include 0.01 for Canada and New Zealand, 0.02 for France, 0.04 for Finland and Italy, and 0.03 for the United Kingdom. Pooling changes both the parameter restriction and the time window, so the panel estimate should not be described as merely an average of the individual estimates.

## Two incomplete-market extensions

The first extension adds an endogenous discount factor to power utility:

$$
\beta(c_{it})=(1+c_{it})^{-\gamma},\qquad\gamma\ge0.
$$

Rising consumption raises impatience, helping anchor international wealth in models with limited asset trading. Households take the aggregate-consumption effect on discounting as external in the implementation described. The article's equation (25) adds a lagged growth term:

$$
m_{it}=r_{c,it}^{\alpha}
\left[\frac{G(1+c_{i,t-1})}{G(1+c_{j,t-1})}\right]^\gamma.
$$

The use of $1+c$ means consumption units and normalization matter, unlike a simple ratio of gross consumption growth. The data appendix does not fully specify a normalization that makes this term invariant to the national-accounting units. A faithful implementation needs the original series scale.

Panel estimates are $\widehat\alpha=1.53$ (0.374) and $\widehat\gamma=-2.05$ (0.350), with $J=8.63$ on twelve degrees of freedom and $p=0.73$ (Table 5). Adding dynamics restores positive curvature but produces the wrong sign for the discount-rate mechanism. The model's attractive statistical fit therefore cannot be accepted as evidence for its economic stabilization channel. Individual instruments are a constant, lagged residual, and lagged real-exchange-rate growth.

The second extension considers asset-market participation costs. In the underlying segmented-market argument, exchange rates depend on the marginal utilities of households active in asset markets, whose consumption is not directly observed. Higher inflation encourages broader participation. The paper tests a reduced-form inflation weighting of the consumption restriction:

$$
m_{it}=r_{c,it}^{\alpha}\left[1-\exp\{-\lambda(\pi_{it}+\pi_{jt})\}\right].
$$

The source reports positive estimates of $\lambda$ but generally negative curvature, with no results table. Its OECD sample does not contain the high-inflation environments most favorable to this participation mechanism.

There is also a literal-form qualification. Equation (27) multiplies a **gross** exchange-rate-growth prediction by a weight that tends to zero at zero inflation. Taken literally, it predicts gross growth near zero, rather than simply removing the relationship. The prose describes the latter interpretation. This is an unresolved normalization issue in the printed specification; a centered-growth alternative would be a modified model, not an exact transcription. Replication should preserve and flag the distinction rather than silently changing the equation.

## Replication sequence and limits of the conclusion

Build the vintage-consistent quarterly data first, preserving currencies, deflators, nonadditive U.S. consumption treatment, seasonal adjustments, and each specification's row mask. Compute gross growth rates; verify that positive $q$ growth means foreign depreciation. Fit each nonlinear moment system with its stated instrument exclusions and iterated weighting. Report parameter signs and standard errors alongside $J$ statistics, not only fit measures. Then reproduce the pooled and country-specific habit estimates, and show which primitive preference configurations are observationally equivalent.

The most important unresolved reproduction inputs are the panel-date inconsistency, original data vintage, exact seasonal-filter options, parameter-dependent instrument iteration, GMM covariance construction, numerical initialization, and scale of the endogenous-discount specification. Contemporary revised OECD data can support a robustness study, but should not be labeled an exact numerical reproduction of these tables.

The evidence favors a dynamic marginal-utility specification over static consumption-only utility in the pooled sample. It does not establish that external habit uniquely explains exchange rates, that international risk sharing is complete, or that the resulting model predicts tradable returns. The appropriate next step is a fully solved model that must also match consumption dynamics and other asset prices. This paper supplies a useful preliminary filter: a theory must satisfy both its statistical moment restrictions and its own economically meaningful parameter restrictions.
