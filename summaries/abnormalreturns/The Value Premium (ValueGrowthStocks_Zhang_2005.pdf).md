# The Value Premium

Lu Zhang. *Journal of Finance* 60(1), February 2005, 67–103. Source: [ValueGrowthStocks_Zhang_2005.pdf](../../Finance/ValueGrowthStocks_Zhang_2005.pdf), 38 PDF pages including the JSTOR cover, proofs, numerical appendix, and references. Printed page 67 is PDF page 2. This note describes the published calibration and simulation model, distinguishing its equilibrium claims, numerical approximations, and empirical comparisons.

## Why this matters

A common intuition says that growth options are leveraged claims on favorable future conditions and should be riskier than assets already installed. If so, growth stocks should earn more than value stocks. Zhang shows why that conclusion can reverse when firms can expand capital relatively easily but cannot cheaply dispose of unproductive capital in downturns. Value firms then carry an economically burdensome stock of assets precisely when bad aggregate states are expensive to bear.

Two ingredients work together: asymmetric capital adjustment costs and a countercyclical price of aggregate risk. Value firms' exposure rises disproportionately in bad times, and those are the states when the pricing kernel places a high value on protection. A moderate unconditional market-beta difference can therefore coexist with a substantial average value premium. The model produces investment, profitability, valuation, and return patterns from firms' optimization rather than assigning a “value factor” directly to stock returns.

The claim is one of rational feasibility and quantitative plausibility. The discount factor is specified externally, and the model does not solve households' consumption problem. It is an industry equilibrium with endogenous product prices and firm decisions, not a complete general-equilibrium explanation of the aggregate equity premium. Its calibrated success does not establish that this mechanism is the unique or empirically dominant source of value returns.

## Economic environment and timing

There is a continuum of competitive firms producing one homogeneous industry product. Firm $j$ enters month $t$ with installed capital $k_{jt}$ and observes aggregate log productivity $x_t$, idiosyncratic log productivity $z_{jt}$, and the product price. Production has decreasing returns to capital:

$$
y_{jt}=\exp(x_t+z_{jt})k_{jt}^{\alpha},\qquad 0<\alpha<1.
$$

The shocks follow stationary AR(1) laws:

$$
x_{t+1}=(1-\rho_x)\bar x+\rho_xx_t+\sigma_x\varepsilon^x_{t+1},
\qquad
z_{j,t+1}=\rho_z z_{jt}+\sigma_z\varepsilon^z_{j,t+1}.
$$

Innovations are standard normal, independent across firms for idiosyncratic shocks and independent of the aggregate innovation. Aggregate uncertainty is needed for a nonzero risk premium; idiosyncratic uncertainty creates cross-sectional heterogeneity. The model does not exogenously classify some firms as permanent value firms and others as growth firms. Their productivity, capital, and valuation states evolve.

Industry output is the sum or integral of firm outputs. Inverse demand is

$$
P_t=Y_t^{-\eta},\qquad 0<\eta<1,
$$

where $1/\eta$ is demand elasticity. Write $p_t=\log P_t$. Operating profit is

$$
\pi(k,z;x,p)=\exp(x+z+p)k^{\alpha}-f,
$$

with a nonnegative fixed operating cost $f$. Firms take the current and anticipated product-price process as given when choosing investment, but market clearing determines that process from all firms' output. This feedback is important: changes in the cross-sectional distribution affect future prices, which affect individual cash flows and risk.

After observing the current states, choose investment $i_t$, possibly negative, with next month's capital

$$
k_{t+1}=i_t+(1-\delta)k_t.
$$

Adjustment costs are deducted from current profit:

$$
h(i,k)=\frac{\theta(i)}2\left(\frac{i}{k}\right)^2 k,
\qquad
\theta(i)=\begin{cases}\theta^+,&i\geq0,\\\theta^-,&i<0,\end{cases}
\qquad \theta^->\theta^+>0.
$$

The factor one-half matters for the first-order condition. This is costly reversibility, not a hard irreversibility constraint: disinvestment is allowed but expensive. The quadratic cost is zero at zero investment and has a continuous first derivative there, even though its curvature changes. A numerical implementation must compare both sides of zero investment; imposing $i\geq0$ would solve a different model.

Dividends are $d_t=\pi_t-i_t-h(i_t,k_t)$. The article imposes no separate financing constraint or nonnegative-dividend restriction in this Bellman equation. An implementation that prohibits equity injections or adds a bankruptcy rule changes the feasible set and mechanism. Capital bounds appear in the numerical procedure, with the upper bound chosen to be nonbinding.

## The discount factor and what is imposed

The stochastic discount factor is

$$
\log M_{t+1}=\log\beta+\gamma_t(x_t-x_{t+1}),
\qquad \gamma_t=\gamma_0+\gamma_1(x_t-\bar x),
$$

with $\beta>0$, $\gamma_0>0$, and $\gamma_1<0$. Aggregate productivity improvements lower the SDF when $\gamma_t$ is positive, so payoffs in good states are discounted more strongly. The sensitivity is higher in low-productivity states. The large numerical values of $\gamma_0$ and $\gamma_1$ are not directly coefficients of household relative risk aversion; the author does not derive preferences producing them.

For implementation define

$$
\mu_{m,t}=\gamma_t(1-\rho_x)(x_t-\bar x),
\qquad s_{m,t}^2=\gamma_t^2\sigma_x^2.
$$

Conditional lognormality gives the gross real risk-free return and maximal conditional Sharpe ratio:

$$
R_{f,t}=\frac{1}{E_t[M_{t+1}]}
=\beta^{-1}\exp[-\mu_{m,t}-s_{m,t}^2/2],
\qquad
S_t=\frac{\operatorname{sd}_t(M_{t+1})}{E_t[M_{t+1}]}
=\sqrt{\exp(s_{m,t}^2)-1}.
$$

These simplify equations (20)–(23). The author calibrates the SDF to aggregate return moments before studying cross-sectional returns. This imposes plausible time variation in aggregate discount rates; it does not explain that time variation from first principles. Under a continuous Gaussian state process, $\gamma_t$ is not globally guaranteed positive, so its intended economic sign must also be checked over the numerical state support.

## Firm valuation and the exact pricing identity

The value function is cum-dividend:

$$
v(k,z;x,p)=\max_{i,k'}\left\{\pi(k,z;x,p)-i-h(i,k)
+E[M(x,x')v(k',z';x',p')]\right\},
\qquad k'=i+(1-\delta)k.
$$

The expectation integrates over the aggregate and idiosyncratic transitions and the perceived future price law. It is not a simple expected-profit maximization with a constant discount rate. Current optimal investment changes both next period's productive capital and its exposure to future aggregate states.

Write $v^e_t=v_t-d_t$ for ex-dividend value. The gross equity return is

$$
R_{j,t+1}=\frac{v_{j,t+1}}{v_{jt}-d_{jt}}
=\frac{v^e_{j,t+1}+d_{j,t+1}}{v^e_{jt}}.
$$

Using the cum-dividend numerator and ex-dividend denominator avoids double-counting the payout. At the optimum, the Bellman equation implies $v_t-d_t=E_t[M_{t+1}v_{t+1}]$, and hence $E_t[M_{t+1}R_{t+1}]=1$. Proposition 1 decomposes expected return as

$$
E_t[R_{j,t+1}]=R_{f,t}+b_{jt}\lambda_{m,t},
\qquad
b_{jt}=-\frac{\operatorname{Cov}_t(R_{j,t+1},M_{t+1})}
{\operatorname{Var}_t(M_{t+1})},
\qquad
\lambda_{m,t}=\frac{\operatorname{Var}_t(M_{t+1})}{E_t[M_{t+1}]}.
$$

This $b_{jt}$ is an exposure to the negative SDF, not automatically the empirical market beta displayed in portfolio tables. The decomposition follows algebraically from the Euler equation. Confusing it with an unconditional CAPM restriction would remove the state-dependence central to the argument.

Within either investment regime, the first-order condition can be written $1+\theta(i)i/k=q$, where $q=E[M_{t+1}v_k(k',z';x',p')]$ is the discounted marginal value of installed capital. Thus larger adjustment coefficients damp the response of investment to marginal value. Optimality, market clearing, and a firm-distribution transition consistent with the capital policy jointly define the recursive competitive equilibrium. In a simulation, the distribution must evolve with the optimal policy and idiosyncratic shocks; simply keeping the initial cross section fixed would remove the equilibrium channel.

Appendix A obtains the Euler/beta identity directly and cites contraction and industry-equilibrium results for value-function regularity and uniqueness. Its theorem invokes compact state spaces and additional technology/demand conditions, while the initial shock specification is Gaussian. The operational numerical model discretizes those states. The short proof should not be interpreted as a fully verified global existence result for every unbounded continuous-state extension or every added financing/entry rule. The implemented cross section contains a fixed number of simulated firms; entry/exit policies are not developed as part of the numerical experiment.

## Benchmark monthly calibration

| Parameter | Value | Role |
|---|---:|---|
| $\alpha$ | 0.30 | Capital exponent |
| $\delta$ | 0.01 | Monthly depreciation |
| $\rho_x$ | $0.95^{1/3}\approx0.983$ | Aggregate persistence |
| $\sigma_x$ | $0.007/3\approx0.00233$ | Monthly aggregate innovation scale as used in the paper |
| $\eta$ | 0.50 | Inverse demand elasticity |
| $\beta$ | 0.994 | SDF discount parameter |
| $\gamma_0,\gamma_1$ | 50, −1,000 | Level and cyclicality of SDF sensitivity |
| $\theta^+$ | 15 | Expansion adjustment curvature |
| $\theta^-/\theta^+$ | 10 | Contraction/expansion asymmetry |
| $\rho_z,\sigma_z$ | 0.97, 0.10 | Idiosyncratic persistence and innovation scale |
| $f$ | 0.0365 | Fixed production cost |
| $\bar x$ | −5.70 | Scale normalization giving long-run capital near one |

Table I separates three calibration groups. Technology and aggregate-shock parameters are borrowed from prior studies. SDF parameters match the average Sharpe ratio and the mean and volatility of the real risk-free rate. The remaining five parameters—adjustment speed, asymmetry, idiosyncratic persistence and volatility, and fixed cost—have more calibration discretion and receive sensitivity analysis.

The model's annual Sharpe ratio is 0.41 versus a comparison value 0.43. Mean real interest is 2.2% versus 1.8%, and its annual volatility is 2.9% versus 3.0%. Mean value-weighted industry return is 13% versus 12–14%, and volatility 27% versus 23–28%. Average individual-return dispersion is 28.6% versus 25–32%. Industry book-to-market averages 0.54 versus 0.67 and has volatility 0.24 versus 0.23. Annual investment and disinvestment rates are 0.135 and 0.014 versus comparison values 0.15 and 0.02. These reference moments come from different cited studies and samples, not one jointly estimated dataset.

Two frequency conventions deserve explicit attention. The source calls monthly depreciation 1% equivalent to annual 12%, an arithmetic annualization rather than compounded depreciation. More materially, it maps a quarterly aggregate innovation standard deviation of 0.007 into monthly $0.007/3$. For a monthly AR(1), exact three-step innovation variance is $\sigma_x^2(1+\rho_x^2+\rho_x^4)$, so that conversion is not the exact AR variance mapping. Reproduce the table's monthly parameter for the published experiment; use the exact mapping only as a separately labeled alternative calibration.

## Numerical solution: the implementable core

The full cross-sectional distribution is a high-dimensional state because it determines industry output and prices. Appendix B uses approximate aggregation: guess a low-dimensional price law, solve the firm's problem under that perceived law, simulate many firms, update the law from simulated data, and repeat until beliefs and realized prices agree closely. This is a numerical approximation to equilibrium, not an analytical elimination of the distribution.

The perceived law is

$$
p_{t+1}=\delta_1+\delta_2p_t+\delta_3(x_t-\bar x)+\delta_4\sigma_k.
$$

The source identifies $\sigma_k$ as a cross-sectional dispersion term for firm characteristics. Its exact calculation and transition as an input to the four-state value-function problem are not specified as completely as the price and productivity grids. A reproduction needs to resolve this from the original program. The author describes current price as the one principal distributional aggregate while also adding this dispersion predictor; it would be misleading to say that price alone exactly closes the aggregate state.

Initialize the price law with $\delta_2=1$ and the other coefficients zero. Simulate 5,000 firms for 12,000 monthly periods, discarding the first 2,000 to estimate the perceived-law coefficients from the stationary region. Firms initially have the same capital, with independently drawn idiosyncratic productivity. Update the price law, re-solve the policies, and continue until parameters converge and forecast errors are small; if fit is poor, enrich the aggregate state or functional form. The article does not state exact convergence tolerances or damping parameters.

For the benchmark the fitted law is

$$
p_{t+1}=0.0486+0.9821p_t-0.1173(x_t-\bar x)+0.0040\sigma_k+e_{t+1},
$$

with $R^2=0.9994$ and forecast-error standard deviation 0.0012. Figure B.1 reports that excess demand in 10,000 retained simulated months is less than 0.2% of actual output in magnitude. These are numerical diagnostics, not statistical validation on external data. Replacing price with aggregate capital in the forecasting equation gives only about 75% $R^2$, showing why the aggregate summary matters.

Solve the firm problem by value-function iteration on a grid of 50 capital points, 11 aggregate-productivity points, 15 idiosyncratic-productivity points, and five evenly spaced log-price points. Use Rouwenhorst discretization for the persistent productivity processes. Capital points are nonuniform, with the recursive increment

$$
k_i=k_{i-1}+c_{k1}\exp[c_{k2}(i-2)],
$$

chosen to concentrate points near the lower bound, where value curvature is greater. The capital and price endpoints are selected so simulated states remain inside them; numerical values are not supplied. Value functions, policy functions, and expected returns use piecewise linear interpolation off grid.

For a forecast price $\widehat p'$ and discrete price point $p_\ell$, the reported transition weight is proportional to $1/|p_\ell-\widehat p'|$, normalized over all five grid points. A numerically valid implementation must handle exact equality by assigning unit mass to the matching grid point, rather than dividing by zero. This special case is an implementation clarification, not an additional economic assumption. Expectations then reduce to weighted sums over discrete states.

The Bellman maximization uses a discrete global search over 20,000 equally spaced candidate capital values between the bounds, ensuring both investment and disinvestment regions are considered. Evaluate expected returns separately as $E_t[v_{t+1}]/(v_t-d_t)$; do not insert the SDF into the numerator when calculating a physical expected return. The SDF belongs in valuation, while the ordinary conditional expectation belongs in the expected payoff.

Appendix B prints the initial idiosyncratic standard deviation as $\sigma_z/\sqrt{1-\rho_z}$, whereas the stationary AR(1) standard deviation implied by equation (2) is $\sigma_z/\sqrt{1-\rho_z^2}$. This is a source inconsistency. The 2,000-month burn-in should make initial-distribution effects negligible in a stable implementation, but it is still worth recording. Random seeds, exact bounds, interpolation edge handling, and stopping tolerances are not supplied; the original programs were available on request rather than reproduced in the article.

## Simulation design and main quantitative result

After solving the benchmark, generate 100 artificial panels, each with 5,000 firms and 900 months. Compute statistics separately for each panel and average the statistics across simulations. Book equity is capital $k$, and market equity is **ex-dividend** value $v^e$. Sort on $k/v^e$ to construct ten book-to-market portfolios and a Fama–French-style two-by-three HML portfolio. The paper refers to the standard Fama–French construction rather than restating every timing and breakpoint convention. A literal reproduction must use that referenced construction, not a monthly high-minus-low decile substituted for HML.

The empirical comparison for the book-to-market portfolios covers July 1927–December 2001 using the Davis–Fama–French series from Kenneth French's library. Table III uses simple returns and annualized means and volatilities. HML means are in percent, while most other mean/volatility entries are decimals—a mixed-unit table that needs careful transcription.

| Case | Annual HML mean | HML market beta | Annual HML volatility |
|---|---:|---:|---:|
| Historical data | 4.68% | 0.14 | 12% |
| Benchmark: asymmetry and countercyclical SDF sensitivity | 4.87% | 0.43 | 12% |
| Model 1: symmetric costs, constant SDF sensitivity | 2.19% | 0.09 | 4% |
| Model 2: asymmetric costs, constant SDF sensitivity | 2.54% | 0.11 | 4% |

The benchmark reproduces the HML mean and volatility reasonably well, but its HML market beta is materially larger than the empirical 0.14. The lowest book-to-market decile earns about 9% annually in the benchmark and the highest about 15%; the corresponding data are about 11% and 17%. Matching one spread therefore does not imply exact replication of every exposure and return moment.

Model 1 sets $\theta^-/\theta^+=1$ and $\gamma_1=0$, while Model 2 restores the ratio to ten but retains $\gamma_1=0$. Other benchmark parameters are held fixed. These counterfactuals isolate a large effect of state-dependent discounting in conjunction with the asymmetry, but are not complete recalibrations to restore all aggregate moments after the change. They should be interpreted as structural comparative statics under the author's maintained calibration.

Table IV varies Model 1's idiosyncratic volatility to 0.08 or 0.12, expansion adjustment coefficient to 5 or 25, fixed cost to 0.0345 or 0.0385, and idiosyncratic persistence to 0.95 or 0.98. The HML means range from 1.57% to 2.63%. Combining high volatility, slow adjustment, high fixed cost, and high persistence produces 3.13%, still below the historical 4.68%. This establishes robustness over the explored parameter alternatives. It does **not** mathematically prove that no conceivable parameter vector without the two main ingredients can match the premium, despite stronger wording in the paper.

## The mechanism and its testable predictions

Low idiosyncratic productivity lowers market value relative to installed capital, creating a high book-to-market firm. These value firms are less profitable and would like to shrink, especially in an aggregate downturn. The expensive contraction technology limits their ability to reallocate resources and smooth distributions to shareholders. Growth firms are more productive and typically expand; they face the lower adjustment coefficient. Risk differences are therefore endogenous consequences of policy flexibility.

The SDF amplifies this asymmetry in two ways. It changes the continuation value in the investment decision, making low-productivity firms more eager to dispose of capital in bad times. It also prices a given covariance exposure more heavily in those same states. Averaging a product of state-dependent exposure and state-dependent price of risk is not the same as multiplying unconditional averages. That covariance between quantity and price of risk is essential to the value-premium account.

“Bad times” in the simulation mean aggregate productivity below its unconditional mean by more than one unconditional standard deviation $\sigma_x/\sqrt{1-\rho_x^2}$; good times are the symmetric upper region. They are not defined using ex post market crashes. Figure 3 predicts more disinvestment and higher adjustment expenditure for value firms in bad times, but more investment and adjustment expenditure for growth firms in good times. The definitions matter when taking the hypothesis to data.

Profitability is return on book equity, $(\Delta k_t+d_t)/k_{t-1}$, aggregated by summing numerators and denominators across the portfolio. In an eleven-year event window around formation, growth firms are persistently more profitable than value firms before and after formation, with gradual mean reversion. This matches the direction of prior empirical evidence, but the plotted curves are generated by the model.

Table V regresses subsequent HML on the log book-to-market difference between value and growth, the growth-minus-value earnings-growth spread, aggregate productivity relative to its mean, and median industry book-to-market. Results are averaged over 100 panels. The annual value-spread regression has adjusted $R^2=8.84%$ and slope $t=3.77$; the earnings-growth spread gives 6.42% and $t=2.95$. Their joint adjusted $R^2$ is 11.04%. The annual relation with aggregate productivity is negative, with $t=-2.79$ and adjusted $R^2=9.45%$. Monthly predictability is much weaker. Reported regression inference adjusts for heteroskedasticity and autocorrelation up to twelve lags.

Table VI studies industry returns, using 100 simulations of 840 months for those exercises. Beginning-period industry book-to-market positively predicts subsequent industry returns, with adjusted $R^2=1.65%$ monthly and 17.62% annually. The value spread predicts with 2.04% and 26.30% respectively. Cross-sectional return volatility has a positive predictive coefficient even controlling for aggregate productivity, reflecting information about the firm distribution and future product prices. These are implications of an equilibrium output-price channel, not compensation for independently diversifiable risk in isolation.

That channel vanishes if $\eta=0$, when output price is fixed. Larger inverse demand elasticity strengthens the sensitivity of prices to industry supply and thus the link from cross-sectional dispersion to expected returns. The model also predicts that industries with more asymmetric adjustment technology should display a larger value premium and higher required returns, other things equal. These are refutable structural predictions; they were not all tested with actual firm-level investment data in this article.

## What a successful replication would establish

A meaningful reproduction first verifies policy optimality, capital feasibility, price-law consistency, Euler errors, and aggregation errors before comparing HML statistics. It must preserve cum- versus ex-dividend valuation, monthly calibration, state-dependent SDFs, and the different adjustment regimes. It should then reproduce benchmark moments and the named counterfactuals, reporting Monte Carlo dispersion as well as means if adding diagnostics. The article reports cross-simulation averages but not a complete uncertainty distribution for all calibration targets or a formal statistical model-comparison test.

Several simplifications limit economic interpretation: no financing friction, no endogenous household solution, no developed entry/exit mechanism, homogeneous product demand, Gaussian productivity innovations, and a reduced-dimensional approximate price process. The calibration draws on multiple historical studies, and some parameters have substantial discretion. The numerical solution is sufficiently detailed to reconstruct the method but not to reproduce every table without resolving the missing bounds, conventions, and source inconsistencies. Its durable contribution is the explicit chain from productivity to investment flexibility, state-dependent risk, and expected returns, showing how a value premium can arise from a technological friction within rational valuation.
