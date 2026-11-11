# Equilibrium Pricing and Optimal Hedging in Electricity Forward Markets

Hendrik Bessembinder and Michael L. Lemmon, *The Journal of Finance* 57(3), June 2002, pp. 1347–1382.

Source: [CommodityPrices_Bessembinder_2002.pdf](../../Finance/CommodityPrices_Bessembinder_2002.pdf).

## Why this matters

The paper explains why electricity forwards can trade below expected spot prices in ordinary conditions and above them when demand is high or sufficiently uncertain. Electricity cannot be economically stored, so the usual spot–forward cash-and-carry trade cannot determine the forward price. Instead, producers and retailers share risks through the forward market. Retail revenue risk creates pressure to sell forward; convex production costs and the possibility of price spikes create pressure to buy. The equilibrium premium is the price adjustment that clears these competing demands. Its exact expression is a difference of covariances; a Taylor approximation makes it decreasing in spot-price variance and increasing in the unstandardized third central moment, holding the other terms fixed.

The contribution is principally theoretical. The empirical study uses early PJM and California electricity markets and finds summer forwards substantially above fitted expected spot prices. That result is materially weaker when forwards are compared with subsequently realized spot prices. Mean load is positively associated with the fitted premium in both markets, but the predicted convex response to load variability is not statistically established. The paper does not present a tradable backtest, a calibrated estimate of investors’ required compensation, or an out-of-sample forecast system.

## Economic setting and institutional scope

The paper studies the newly deregulated wholesale markets of its period. It reports about 2.6 billion MWh of U.S. wholesale transactions in 1999, worth approximately \$85 billion. Electricity’s limited storability makes supply and consumption balance in real time: inventory cannot buffer an unexpected increase in demand or a production shortfall. Predictable intraday and seasonal price differences therefore need not create arbitrage. Daytime electricity can cost more than twice nighttime electricity; summer can systematically be more expensive than spring and fall.

The motivating PJM series is the average daily on-peak spot price from April 1997 through July 2000. The standard deviation of daily percentage price changes is 34%, compared with 5.7% for daily S&P 500 returns in October 1987. Figure 1 shows repeated, temporary summer spikes. The authors also cite the June 1998 Midwest episode in which electricity briefly rose from roughly \$30/MWh to above \$7,000/MWh. These observations motivate an explicitly nonlinear supply function and attention to the upper tail, rather than a diffusion calibrated solely to ordinary price variation.

Nonstorability blocks the familiar trade of buying spot electricity, holding it, and delivering it against a forward sale. It does not eliminate every arbitrage restriction among electricity claims, but it removes the cost-of-carry equation that would otherwise pin a forward to the current spot. Potential energy can be stored in fuel inventories or water behind dams; converting it into power requires finite production capacity. The paper treats this distinction as economically decisive.

Only producers and power retailers participate in the modeled forward market. A retailer purchases wholesale power and supplies final customers at a price fixed before demand is realized. Such a retail contract is a variable-quantity forward commitment: the customer controls the quantity purchased at the preset price. Seasonal retail prices can be predetermined; the restriction is that retail prices do not respond to contemporaneous wholesale shocks.

The authors motivate limited participation using the physical-delivery requirement and the thin futures and cash-settled markets of the time. A marketer purchasing physical electricity needs a customer or other destination to consume it. Outside speculators can avoid delivery by closing futures positions or use cash settlement, but the available mechanisms were limited. On October 2, 2000, NYMEX listed PJM contracts for October 2000 through November 2001; every maturity except November 2000 had zero open interest, and that contract had only four open contracts. The paper cites an estimate that cash-settled electricity trading was only about 5% of the physical-delivery market. These are historical arguments for the assumption, not evidence that limited participation must characterize electricity markets permanently.

With unconstrained risk-neutral outsiders, the forward would converge to expected delivery-date spot. With diversified risk-averse outsiders, compensation would instead depend on covariance with broader portfolio or market risk. If that covariance were negligible, the premium would again be small. The paper invokes Hirshleifer’s costly-entry model to argue that a finite number of outsiders might reduce the magnitude of a hedging-pressure premium without changing its sign when systematic financial-market risk is absent. It does not solve that extension. Its analogy to catastrophe-linked bonds is a conjecture about financial integration, not a tested prediction within the electricity sample.

## Model, timing, and exact spot equilibrium

There is one future production period. Forward positions are selected while future demand is uncertain. At the spot stage, demand is known, producers choose output competitively, and retailers acquire the electricity needed to serve customers. The no-uncertainty-at-the-spot-stage assumption approximates very short delivery horizons such as next-hour or next-day trading. There is no dynamic rebalancing, no stochastic information arriving during physical dispatch, and no endogenous investment or entry decision.

There are $N_P$ identical producers and $N_R$ retailers. Retailer $j$ faces exogenous random demand $Q_{Rj}$, and total system demand is

$$
Q^D=\sum_{j=1}^{N_R}Q_{Rj}.
$$

Every producer has total cost

$$
TC_i=F+\frac{a}{c}Q_{Pi}^{c},\qquad a>0,\quad c\geq2,
$$

where $F$ is fixed cost. Marginal cost is $aQ_{Pi}^{c-1}$. The parameter $c$ controls the curvature of supply: $c=2$ gives linear marginal cost, while $c>2$ gives convex marginal cost. The latter approximates the increasing use of inefficient peaking plants and the steep cost of meeting demand near capacity. There is no literal hard capacity bound, outage process, unit-commitment problem, or transmission constraint. Power is transmitted without cost, and the wholesale market is competitive.

Let $P_W$ be the delivery-period wholesale spot price, $P_F$ the previously agreed forward price, and $P_R$ the fixed retail price. All forward positions use a **sale convention**: $Q_i^F>0$ is a forward sale and $Q_i^F<0$ is a purchase. Producer physical output is $Q_{Pi}=Q_{Pi}^W+Q_{Pi}^F$, with $Q_{Pi}^W$ its net spot sale. Its profit is

$$
\pi_{Pi}=P_WQ_{Pi}^W+P_FQ_{Pi}^F-F-\frac{a}{c}Q_{Pi}^{c}.
$$

A retailer’s profit is

$$
\pi_{Rj}=P_RQ_{Rj}+P_FQ_{Rj}^F-P_W(Q_{Rj}+Q_{Rj}^F).
$$

The retailer buys the difference between realized customer load and its previously contracted forward purchases. A negative spot quantity is allowed in the algebra; there are no position or trading constraints.

Set $x=1/(c-1)$, so $0<x\leq1$. Price-taking producer optimization sets marginal cost equal to $P_W$, yielding

$$
Q_{Pi}^W=\left(\frac{P_W}{a}\right)^x-Q_{Pi}^F.
$$

Market clearing then gives the exact spot-price relation

$$
P_W=a\left(\frac{Q^D}{N_P}\right)^{c-1},\qquad
Q_{Pi}=\frac{Q^D}{N_P},\qquad
Q_{Pi}^W=\frac{Q^D}{N_P}-Q_{Pi}^F.
$$

Forward positions redistribute revenues and risks, but do not alter physical output in this competitive specification. This matters: the mechanism is risk sharing, rather than strategic forward commitments changing spot-market competition. With convex marginal cost, symmetric load variation can generate positively skewed prices because a high-load surprise raises marginal cost more than a comparable low-load surprise lowers it.

## Forward demand and the exact equilibrium premium

Define unhedged operating profits, denoted $\rho$ in the paper, by

$$
\rho_{Pi}=P_W\frac{Q^D}{N_P}-F-\frac{a}{c}\left(\frac{Q^D}{N_P}\right)^c,
\qquad
\rho_{Rj}=(P_R-P_W)Q_{Rj}.
$$

Each firm’s total profit is $\pi_i=\rho_i+(P_F-P_W)Q_i^F$. Firms maximize

$$
E[\pi_i]-\frac{A}{2}\operatorname{Var}(\pi_i),\qquad A>0.
$$

The common parameter $A$ measures the relevance of profit volatility to corporate value. The motivation is financial distress, taxes, financing frictions, managerial risk, and investment incentives. Those frictions are not modeled separately or estimated. Mean–variance preferences are imposed directly, so normally distributed profits are not needed to derive the optimum. Finite profit variances and the relevant covariances are needed.

Write $m=E[P_W]$ and $v=\operatorname{Var}(P_W)>0$. Since

$$
\operatorname{Var}(\pi_i)=\operatorname{Var}(\rho_i)+(Q_i^F)^2v-2Q_i^F\operatorname{Cov}(\rho_i,P_W),
$$

the first-order condition gives the exact position

$$
Q_i^{F*}=\frac{P_F-m}{Av}+\frac{\operatorname{Cov}(\rho_i,P_W)}{v}.
$$

The objective has second derivative $-Av$, so this is the unique unconstrained optimum when $A,v>0$. The first term is a speculative response to the premium; the second is the minimum-variance forward sale. A firm can optimally sell forward despite normally being a physical buyer, because its relevant exposure is the covariance of total operating profit with price, rather than its average purchase quantity alone.

For producers, substitution of the spot equilibrium gives

$$
\rho_{Pi}=\frac{1-1/c}{a^x}P_W^{x+1}-F,
\qquad
\operatorname{Cov}(\rho_{Pi},P_W)=\frac{1-1/c}{a^x}\operatorname{Cov}(P_W^{x+1},P_W).
$$

For retailers,

$$
\operatorname{Cov}(\rho_{Rj},P_W)
=P_R\operatorname{Cov}(Q_{Rj},P_W)-\operatorname{Cov}(P_WQ_{Rj},P_W).
$$

These terms represent producer revenue, producer production cost, retailer revenue, and retailer wholesale purchase cost risk. Producer wholesale revenue and retailer purchase costs cancel at industry level. What remains is random final-customer revenue less random production cost. Indeed, total unhedged industry profit is

$$
\Pi_0=P_RQ^D-N_PF-\frac{aN_P}{c}\left(\frac{Q^D}{N_P}\right)^c.
$$

Summing optimal forward positions and imposing zero net supply gives a particularly useful reconstruction of the central result:

$$
P_F-m=-\frac{A}{N_P+N_R}\operatorname{Cov}(\Pi_0,P_W).
$$

Thus a positive premium compensates sellers when the industry’s aggregate operating profit tends to fall in high-price states. A negative premium compensates forward buyers when aggregate profit rises with price and industry participants collectively want to sell that exposure.

Define $N=(N_R+N_P)/A$. Using $Q^D=N_PP_W^x/a^x$, the paper’s exact equation (12), also Appendix (A4), is

$$
P_F=m-\frac{N_P}{Nca^x}
\left[cP_R\operatorname{Cov}(P_W^x,P_W)-\operatorname{Cov}(P_W^{x+1},P_W)\right].
$$

The first covariance reflects retail revenue risk and lowers the forward price. The second reflects production-cost risk and raises it. Fixed cost $F$ disappears because it has no covariance with price. If the risk relevance parameter approaches zero, the premium approaches zero. Increasing aggregate risk-bearing capacity also reduces the premium holding the underlying operating exposure fixed. Altering producer numbers without holding the supply curve fixed changes the spot economy as well, so the latter comparative static should not be read as an unconditional claim about entry.

Footnote 15 allows different producer and retailer risk coefficients by replacing $N$ with $N_P/A_P+N_R/A_R$. The operating covariance numerator is unchanged under the same production and demand assumptions. Consequently, these differences change the premium’s magnitude but not its sign. The formula is a risk-bearing-capacity result, not an estimate of market-wide risk aversion.

## Variance, skewness, and the limits of the approximation

The paper expands the nonlinear price powers around $m$. For any constant $z$, the relevant second-order Taylor calculation is

$$
P_W^z\approx m^z+zm^{z-1}(P_W-m)
+\frac{z(z-1)}{2}m^{z-2}(P_W-m)^2.
$$

Taking covariance with $P_W$ gives

$$
\operatorname{Cov}(P_W^z,P_W)
\approx zm^{z-1}v+\frac{z(z-1)}{2}m^{z-2}\mu_3,
\qquad
\mu_3=E[(P_W-m)^3].
$$

Here $\mu_3$ is **unstandardized** skewness. It is not the dimensionless coefficient $\mu_3/v^{3/2}$. Substituting $z=x$ and $z=x+1$, and using $cx=x+1$, yields the paper’s equation (13):

$$
P_F\approx m+\alpha v+\gamma\mu_3,
$$

where

$$
\alpha=\frac{N_P(x+1)}{Nca^x}
\left(m^x-P_Rm^{x-1}\right),
$$

$$
\gamma=\frac{N_P(x+1)}{2Nca^x}
\left[xm^{x-1}-(x-1)P_Rm^{x-2}\right].
$$

For positive prices and $P_R>m$, the maintained profitable-retailing condition used by the authors, $\alpha<0$ and $\gamma>0$. If the price distribution has no skewness, retail revenue risk dominates this approximation and the forward lies below expected spot. Positive upper-tail skewness raises the premium because the industry needs protection against costly high-price states. The premium is positive when $\gamma\mu_3>-\alpha v$.

These are partial effects. Increasing demand uncertainty generally changes variance, skewness, and expected price together; it does not follow that more volatile demand must lower the premium. The paper’s four hypotheses distinguish the channels: the premium decreases with anticipated price variance, increases with anticipated price skewness, is initially decreasing and then increasing in demand variability, and increases with expected demand. The last two are illustrated by simulations rather than proved as unrestricted comparative-static theorems for every admissible demand distribution.

The exact covariance equation remains the preferred implementation formula. For $c=2$, $x=1$, the powers involved are linear and quadratic, making the variance–third-moment decomposition exact. For $c>2$, higher-order terms have been omitted. Rare price spikes are precisely where a local Taylor expansion can be least reliable. The paper supplies no bound on the approximation error and does not prove that its first three moments are sufficient statistics for arbitrary demand distributions.

## Simulation design and optimal hedge positions

The first simulation sets $E[Q^D]=100$, demand standard deviation between 1 and 40, and $N_R=N_P=20$. It varies $c$ from 2 to 5. The variable-cost scale is

$$
a=30\left(\frac{N_P}{100}\right)^{c-1},
$$

so spot price at demand 100 is \$30, independent of $c$. Retail price is $1.2E[P_W\mid c]$. For each parameter combination the authors generate 1,000 normal demand realizations, calculate spot prices from the exact supply relation, estimate the covariance terms, and calculate the exact equilibrium forward price. Figure 2 reports the premium as a percentage of expected spot.

With quadratic costs the price distribution is symmetric under normal demand, and the premium is negative and increasingly negative as demand variability rises. With convex marginal cost, the premium initially falls, reaches a minimum, then rises and can become positive. More convex costs produce an earlier reversal and a larger positive premium. Figure 3 fixes $c=4$, varies expected load from 75 to 125 and demand standard deviation from 1 to 40, and illustrates increasing premiums with mean demand, especially when demand variability is already high. The plotted premium ranges are illustrative: changing $A$ or the number of firms can change their scale arbitrarily.

There are replication ambiguities in the simulation description. The main text on p. 1360 specifies $A=0.8/c^2$, whereas the captions of Figures 2 and 3 specify $A=0.8/2^c$. They coincide at $c=2$ and $c=4$ but not generally. The text describes fixing $a$ at the demand-100 normalization, while Figure 3’s caption writes the normalization using $E[Q^D]$; whether $a$ is held fixed or recalibrated as mean demand varies needs resolution before reproducing that surface. Finally, an untruncated normal distribution admits negative demand, and the paper does not specify truncation or other treatment; this can matter at the largest relative standard deviations and for noninteger powers. No random seed or simulation code is supplied.

For producers, the exact optimal sale is

$$
Q_{Pi}^{F*}=\frac{\mathrm{PREM}}{Av}
+\frac{1-1/c}{a^x}\frac{\operatorname{Cov}(P_W^{x+1},P_W)}{v},
\qquad \mathrm{PREM}=P_F-m.
$$

Applying the second-order price-power approximation gives Appendix (A8):

$$
Q_{Pi}^{F*}\approx\frac{m^x}{a^x}+\frac{\mathrm{PREM}}{Av}
+\frac{xm^{x-1}}{2a^x}\frac{\mu_3}{v}.
$$

The main-text equation (14) replaces the first term by expected production $E[Q^D]/N_P$. Its economic reading is expected-output hedging, plus a premium response, plus a skewness adjustment. Producers sell more when forward compensation is positive; they also sell more to hedge the nonlinear revenue exposure associated with upward spot spikes. Figure 4 shows hedge ratios, forward sales divided by expected production, below one under low expected demand and modest demand risk and above one as these rise. Selling more than expected output is feasible here because output itself rises in the states with high wholesale prices.

**An approximation caveat in the source matters.** Appendix (A9) writes $m^x\simeq a^xE[Q^D]/N_P$ and describes it as following from a second-order expansion. The exact identity is instead

$$
\frac{E[Q^D]}{N_P}=\frac{E[P_W^x]}{a^x}.
$$

A second-order expectation gives

$$
E[P_W^x]\approx m^x+\frac{x(x-1)}{2}m^{x-2}v.
$$

For $0<x<1$ and nondegenerate positive prices, Jensen’s inequality also gives $E[P_W^x]<m^x$. Thus (A9) drops a curvature term; it is not a second-order identity as printed. This does not invalidate the exact covariance equilibrium or exact hedge demand. It means that equation (14), and the retailer simplification using the same substitution, should be treated as additional approximations. Retaining (A8) avoids that substitution, although its own covariance Taylor truncation still has higher-order error.

Retailers differ through local load dependence on system demand. The paper writes

$$
Q_{Rj}=\rho_j+\beta_j\frac{Q^D}{N_R}+\varepsilon_j,
$$

where $\rho_j$ is a regression intercept, distinct from the earlier notation for unhedged profit. The errors are assumed independent of total demand, stronger than the zero linear correlation delivered by OLS. Because price is nonlinear in total demand, OLS orthogonality alone does not remove covariance with price or price times the residual.

For this regression, the coefficient consistent with the displayed regressor is

$$
\beta_j=\frac{\operatorname{Cov}(Q_{Rj},Q^D/N_R)}{\operatorname{Var}(Q^D/N_R)}
=\frac{N_R\operatorname{Cov}(Q_{Rj},Q^D)}{\operatorname{Var}(Q^D)}.
$$

The definition printed immediately below equation (15) instead places $N_R$ in the denominator. That is inconsistent with its regression normalization, its subsequent formulas, and the interpretation that a retailer serving an average share of every system load has beta one. The regression-consistent definition is used here; the discrepancy is in the source, not an OCR choice.

Under the independence assumption, Appendix (A10) provides an exact retailer expression:

$$
Q_{Rj}^{F*}=-\rho_j+\frac{\mathrm{PREM}}{Av}
+\frac{\beta_jN_P}{N_Ra^xv}
\left[P_R\operatorname{Cov}(P_W^x,P_W)-\operatorname{Cov}(P_W^{x+1},P_W)\right].
$$

The main-text approximation is

$$
Q_{Rj}^{F*}\approx-E[Q_{Rj}]+\frac{\mathrm{PREM}}{Av}
+\beta_j^*\left[Z+Y\frac{\mu_3}{v}\right],
$$

with

$$
\beta_j^*=\frac{\beta_jN_P}{a^xN_R},\qquad
Z=P_Rxm^{x-1}-xm^x,
$$

$$
Y=\frac{P_Rx(x-1)}{2}m^{x-2}-\frac{x(x+1)}{2}m^{x-1}.
$$

Here $Y<0$, and $Z>0$ if $P_R>m$. The negative expected-load term is the ordinary purchase hedge. A positive premium reduces forward purchases. With positive demand beta, retail revenue risk also reduces purchases, while positive price skewness increases them by raising the importance of wholesale acquisition-cost risk. For beta zero, the retailer’s hedge differs from minus expected load only because of the premium; with the maintained independence, this conclusion can also be read directly from the exact formula.

Figures 5 and 6 illustrate $\beta=0$ and $\beta=2$, with $c=4$. The zero-beta retailer buys more than expected load when forwards are cheap and less when they are expensive. The high-beta retailer can reduce purchases dramatically or even sell forward when expected demand and demand risk are low. As the probability of price spikes increases, it buys increasingly large amounts forward. The displayed ranges reach roughly a positive 0.5 sale ratio at one extreme and a negative 2 purchase ratio at the other; these are simulation illustrations, not calibrated recommended limits.

The authors argue that costless sharing of retail customer loads would push betas toward one. Geographic contracting costs and regulation can prevent that diversification. With equal numbers of identical producers and fully representative retailers, market clearing makes the representative retailer’s equilibrium position the opposite of the producer’s. None of these hedge ratios includes default, liquidity, collateral, volumetric delivery limits, or position constraints.

## Data, estimation, and information timing

The empirical sample is PJM from April 1997 through July 2000 and CALPX from April 1998 through July 2000. These calendar spans comprise 40 and 28 months, respectively; the paper does not report exact daily observation counts. Daily load and spot-price data come from the PJM and California ISO websites. Daily spot price is average on-peak price; load is daily average load. The markets use centralized dispatch, with an independent system operator scheduling generation to meet demand from submitted supply schedules.

Figures 7 and 8 distinguish two major events. PJM’s July 1999 price spike coincides with the highest load and reverses quickly, broadly consistent with convex supply. CALPX prices rise sharply in summer 2000 and remain high through the sample end even though load is below corresponding periods in earlier summers. That episode requires a supply shift or market power, neither present in the model. The authors do not resolve the competing outage, emissions, and withholding explanations. They explicitly regard PJM as the cleaner setting for testing their competitive model.

To estimate the supply curve, the paper displays equation (17) as

$$
\ln(P_t)=a+(c-1)\ln(Q_t+d_t)+\varepsilon_t,
$$

where $d_t$ denotes calendar-month indicators intended to capture seasonal supply availability, including scheduled maintenance. June and July 2000 receive extra CALPX indicators. The empirical intercept $a$ here should not be mechanically equated with the cost scale in the theoretical cost function. There is also a specification ambiguity: the printed equation places $d_t$ inside the logarithm while describing estimation as a linear regression. The paper does not print the complete design matrix or estimated monthly coefficients. An implementation should not silently replace this with an additive-dummy regression and claim exact replication.

For PJM the estimated cost convexity is $c=4.80$, with reported $t=37.9$ and $R^2$ about 60%. For CALPX it is $c=5.81$, with $t=23.3$ and $R^2$ almost 70%. Both indicate a strongly convex estimated marginal-cost curve. The paper reports these statistics for $c$ but does not provide the complete regression output or the precise null underlying the quoted $t$ statistics.

As a fuel-cost check, the authors obtain nearby natural-gas futures prices for Southern California border delivery, available only from August 1998. Mean gas prices rise from \$2.30/MMBtu in August 1998 to \$3.88/MMBtu in July 2000. Replacing the dependent variable with the logarithm of the electricity-price/gas-price ratio gives $c=5.30$, $t=17.23$, and explanatory power near 60%. The summer-2000 indicators remain significantly positive, so gas prices alone do not account for the structural break. Subsequent reported CALPX results use the original specification, which covers four additional months and fits slightly better. The alternative results are described as qualitatively similar but are not tabulated.

Expected spot prices are estimated by a calendar-month bootstrap. For each month of the year, the authors draw 2,000 daily loads with replacement from all observations in that calendar month across all sample years. Each load is mapped through the fitted pricing curve, and the mean fitted price becomes the expected price for that calendar month. This assumes seasonality across months but stationarity across years. CALPX fitted expectations exclude the June/July 2000 special effects, treating them as unexpected developments outside the model. Sampling hourly instead of daily load reportedly gives similar expectations and unchanged qualitative premium inferences.

The method reduces realization noise by substituting a supply-model expectation for the observed spot outcome. It also makes the inference conditional on that model, the treatment of structural breaks, and the empirical load distribution. Both curve estimation and bootstrap use the available full sample. The exercise is therefore an in-sample estimate of seasonal expected prices, not a forecast formed only with data known at each forward trade date. No rolling or expanding-window estimation, separate training period, or holdout test is provided. The paper does not describe a log-to-level residual correction; without the exact fitted-value procedure, any such correction should be treated as an unresolved replication input.

## Numerical evidence

Table I reports equal-weighted actual daily on-peak price averages and the bootstrapped fitted expectations, in dollars per MWh. The large summer differences are central to the subsequent premium comparison.

| Month | PJM actual | PJM fitted | CALPX actual | CALPX fitted |
|---|---:|---:|---:|---:|
| January | 25.91 | 25.49 | 30.08 | 27.37 |
| February | 22.54 | 20.94 | 27.71 | 22.89 |
| March | 24.08 | 23.77 | 26.97 | 21.12 |
| April | 25.46 | 25.30 | 29.39 | 27.59 |
| May | 30.89 | 26.81 | 37.96 | 23.12 |
| June | 38.23 | 33.03 | 79.36 | 28.07 |
| July | 71.40 | 45.80 | 73.05 | 36.82 |
| August | 36.66 | 30.93 | 47.37 | 45.53 |
| September | 27.89 | 28.44 | 41.45 | 38.09 |
| October | 27.08 | 26.13 | 42.43 | 40.98 |
| November | 23.57 | 23.18 | 37.40 | 37.35 |
| December | 20.72 | 21.78 | 32.97 | 32.19 |

Table II computes monthly price variability and standardized skewness using deviations of daily prices from the estimated expected monthly price, then averages by season and across years. Winter is December–February, spring March–May, summer June–August, and fall September–November. Unlike $\mu_3$ in the theory, the reported skewness coefficient is normalized by the standard deviation cubed.

| Season | PJM expected price | PJM SD | PJM skewness | CALPX expected price | CALPX SD | CALPX skewness |
|---|---:|---:|---:|---:|---:|---:|
| Winter | 23.02 | 7.10 | 0.18 | 27.36 | 7.55 | 0.65 |
| Spring | 26.03 | 10.87 | 0.72 | 24.72 | 13.84 | 1.19 |
| Summer | 37.63 | 51.04 | 1.87 | 35.22 | 59.09 | 1.30 |
| Fall | 25.88 | 7.85 | 0.23 | 39.01 | 16.95 | 0.94 |

Summer has by far the highest price variability in both markets. Standardized skewness is positive in all cells and highest in summer, though CALPX spring is close. PJM expected price peaks in summer; CALPX fitted expected price is actually higher in fall. Because unstandardized skewness equals the standardized coefficient times the cube of volatility, the summer increase in both terms supports the possibility that the skewness contribution outweighs the negative variance contribution. These seasonal moments are descriptive; they do not directly estimate $\alpha$ or $\gamma$.

Forward data are daily observations of one-month-ahead delivery prices. The contracts deliver during weekday on-peak hours throughout the delivery month, rather than at one instant. PJM forward prices come from Bloomberg. California forward observations combine CALPX block forwards with earlier Palo Verde, Arizona, forwards, a related delivery location from which power often enters California. This introduces geographic basis error.

The splice date is inconsistent across the source: the body says CALPX block trading begins in August 1999 and uses Palo Verde through July 1999, whereas Figure 10 and Table III specify Palo Verde through June 1999 and CALPX from July 1999. Table III also describes CALPX closing prices as reported by Bloomberg, while the body emphasizes CALPX’s website. These differences should be resolved from raw data before replication. For PJM, Table III explicitly uses average forward prices during the month before delivery, which is the proper timing alignment for its comparison with delivery-month spot.

Figures 9 and 10 compare forwards both with fitted expectations and with realized delivery-month spot. Outside summer, biases tend to be modest. For CALPX July, forwards exceed fitted expectations by roughly \$40/MWh, over 100%, while June forwards fall below realized prices by a similar amount. The summer-2000 spike drives this discrepancy. Whether it represents a rare event that should have entered expectations or an unforeseeable structural break cannot be established from two or three summers.

Table III gives seasonal mean forward-minus-spot differences in dollars per MWh. Parentheses contain the source’s simple $t$ statistics. Each seasonal mean contains only 6–11 monthly observations.

| Season | PJM minus fitted | PJM minus realized | CALPX minus fitted | CALPX minus realized |
|---|---:|---:|---:|---:|
| Winter | 3.09 (6.24) | 2.78 (1.86) | −1.48 (−1.26) | −1.90 (−1.62) |
| Spring | −1.10 (−0.98) | −2.73 (−2.13) | −1.69 (−0.73) | −4.90 (−1.85) |
| Summer | 21.38 (2.25) | 8.62 (0.62) | 20.07 (1.84) | −12.84 (−1.02) |
| Fall | 0.24 (0.18) | −0.02 (0.01) | −5.44 (−2.01) | −6.82 (−2.87) |

The paper calls the two fitted summer premiums statistically significant, reporting $t=2.25$ and $1.84$. Those statistics should be retained rather than translated into an unqualified claim of conventional two-sided 5% significance, especially with few observations. Against realized spot, the PJM summer premium falls by more than half and is insignificant, while the CALPX summer difference becomes negative and insignificant. PJM winter has a positive fitted premium; CALPX fall has a negative one. Some temperate-season realized differences are negative as predicted. The small positive $t=0.01$ beside the negative PJM fall mean is reproduced from the table and appears to be a sign typo.

The authors also report, without a separate table, an apparent learning pattern: PJM summer 1997 forwards were below fitted expected spot, but summer forwards after the widely publicized June 1998 spikes were considerably above it. Non-summer relationships changed little. This is consistent with participants revising their tail-risk assessment, but it is not a separately identified learning model.

The final regression relates monthly fitted premium to load moments:

$$
\mathrm{PREM}_{it}=\alpha_0+\alpha_1\mathrm{MEAN}_{it}
+\alpha_2\mathrm{STD}_{it}+\alpha_3\mathrm{VAR}_{it}+\eta_{it},
\qquad \mathrm{VAR}_{it}=\mathrm{STD}_{it}^2.
$$

The expected signs are $\alpha_1>0$, $\alpha_2<0$, and $\alpha_3>0$. Table IV reports:

| Market | Mean-load coefficient | Load-SD coefficient | Load-variance coefficient |
|---|---:|---:|---:|
| PJM | 49.03 (3.46) | 39.31 (0.37) | −188.68 (−0.96) |
| CALPX | 37.81 (2.08) | 145.87 (0.51) | −582.41 (−0.59) |

Mean load has the predicted positive and statistically significant association in both markets. The two dispersion coefficients are insignificant and have signs opposite to the predicted decreasing-then-increasing pattern. The authors attribute limited precision partly to small samples and substantial multicollinearity. This supports the mean-demand implication, not a claim that all four hypotheses pass. Table IV omits the intercept, goodness of fit, complete estimation details, and an explicit load normalization sufficient to reproduce the coefficient magnitudes from raw MW data. Its coefficients should not be used directly as a trading rule without those inputs.

## Interpretation, implementation, and remaining limits

The durable insight is that hedging demand depends on how operating profit changes with the same states that move the hedge price. A retailer is exposed to both quantity and price; a producer’s output is also state dependent. Matching forwards one-for-one to expected physical volume ignores this interaction. A high correlation between local and system load makes the retailer particularly vulnerable when spot prices spike. For producers, high-price states also bring greater sales volumes, so the optimal hedge can exceed average output. These conclusions follow from the joint economics of price and quantity and do not require a standalone preference for skewness: mean–variance firms face nonlinear operating profits.

An implementation of the model would first specify a positive load distribution, the competitive supply curve, retail prices, producer and retailer counts, and risk coefficients. It would map each load scenario to price and unhedged operating profit, compute the exact covariance premium, then compute each firm’s exact forward position. The aggregate positions should sum to zero. For heterogeneous retailers, the joint local/system load distribution matters; a regression beta is sufficient only with the strong residual-independence assumption. Evaluating exact scenario profits avoids both the printed beta-normalization error and the extra expected-output approximation in Appendix (A9).

For empirical use, forecasts must be conditioned on information available when forwards are priced. Current capacity, planned maintenance, fuel costs, outages, weather forecasts, and demand growth can change the relation between load and price. The sample’s CALPX episode is an explicit example of such instability. A monthly delivery block also contains many different hourly states and shapes; the single-period theory does not solve the matching of daily average load to weekday on-peak block exposure. Geographic basis matters when substituting Palo Verde for CALPX, as do differences between firm-specific customer load and an ISO aggregate.

The paper offers no bid–ask spreads, commissions, market impact, financing charges, collateral requirements, credit adjustments, execution schedule, turnover, feasible notional capacity, or net returns. It does not report Sharpe ratios, drawdowns, or a strategy that survives a summer spike while selling the apparent forward premium. A forward above an estimated mean spot price is compensation conditional on a model of expected spot, not an arbitrage. For a producer or retailer, cash-flow variance reduction may be valuable even when the hedge has a negative expected standalone payoff. For an outside seller, the same premium must be assessed against tail loss, funding needs, and model error.

Several limitations are intrinsic to the equilibrium: identical producer technology; perfect competition; costless transmission; no hard generation capacity; fixed rather than real-time retail prices; no physical outages; no fuel-price state in the theoretical model; no market-power response; no outside investor; and an unconstrained, static mean–variance objective. A constant quadratic variance penalty does not reproduce state-dependent distress costs or the inability to meet collateral calls. Although financial distress motivates the objective, default itself never occurs in the model. The estimated production function is a reduced-form price–load relationship, not a separately identified engineering cost curve.

The empirical identification is also limited. The fitted premium jointly tests the equilibrium explanation and the estimated expectation model. Removing the California crisis effects from expected prices mechanically increases measured summer compensation relative to retaining those realizations in expectations. The realized-price comparison avoids that specific model benchmark but is extremely noisy. Bootstrap resampling increases simulation precision conditional on the available data; it does not create more independent summers or establish the correct frequency of rare events. The reported simple $t$ statistics do not provide a documented correction for estimated expectations, tail-driven sampling distributions, serial dependence, or the choice of exceptional-month indicators.

The bibliography locates the paper between several literatures. Anderson–Danthine, Rolfo, and Hirshleifer–Subrahmanyam supply the price–quantity hedging framework; this paper endogenizes both output and price and links the resulting covariances to price skewness. Smith–Stulz, Stulz, Bessembinder, and Froot–Scharfstein–Stein motivate corporate demand for risk reduction. Hirshleifer supplies the costly-speculator-entry argument. Pirrong–Jermakyan and Eydeland–Geman address electricity derivative pricing but do not supply this same endogenous industry hedging-pressure premium. Routledge–Seppi–Spatt study storage, conversion, and the spark spread, complementing rather than duplicating this risk-sharing mechanism. The market-power and transmission references explain important dimensions deliberately omitted here.

The paper therefore supplies a tractable structural account of the *sign* of power forward premia and a useful exact covariance hedge rule. The strongest reported empirical result is the positive relation between fitted premia and mean load, together with large fitted summer premia. Evidence for realized excess returns and for the predicted load-variance nonlinearity remains weak. Reproduction and application should preserve that distinction, use the exact equilibrium formulas where possible, and resolve the documented source ambiguities before treating the illustrated hedge ratios or coefficient magnitudes as operational inputs.
