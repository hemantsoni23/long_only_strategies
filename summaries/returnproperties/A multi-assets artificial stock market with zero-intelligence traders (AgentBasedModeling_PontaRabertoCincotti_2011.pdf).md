# A multi-assets artificial stock market with zero-intelligence traders

L. Ponta, M. Raberto, and S. Cincotti, *EPL* 93 (2011), article 28002, DOI 10.1209/0295-5075/93/28002. Accepted January 4, 2011; published online February 2, 2011. The local PDF contains a download cover and the complete six-page article. References below use article pages p1–p6.

Source: [AgentBasedModeling_PontaRabertoCincotti_2011.pdf](../../Finance/AgentBasedModeling_PontaRabertoCincotti_2011.pdf).

## Why this matters

Correlated returns, sector-like eigenmodes, and clustered volatility need not uniquely identify informed investors or common beliefs. This simulation generates such properties from random allocation, finite wealth, volatility-sensitive order prices, and restrictions on which sectors each trader can hold. Its contribution is to extend the Genoa Artificial Stock Market to multiple stocks and isolate allocation-universe structure as a source of cross-sectional dependence.

The result is a demonstration of sufficiency within a constructed market, not evidence that real investors are random or that fundamentals do not matter. In particular, the agents' behavior is not entirely structure-free: recent volatility explicitly changes their order-price distribution, and the sector allocation restrictions are imposed by the researcher.

## State, accounting, and allocation decisions

There are $S$ economic sectors, stocks indexed by sector–firm pair $(s,j)$, and $N$ traders. At discrete step $h$, trader $i$ owns cash $c_i(h)$ and integer stock quantities $a_i^{s,j}(h)$. Its risky and total wealth are

$$
W_i^r(h)=\sum_{s,j}a_i^{s,j}(h)p^{s,j}(h),
\qquad W_i(h)=c_i(h)+W_i^r(h).
$$

Conditional risky-portfolio weights are $\omega_i^{s,j}=p^{s,j}a_i^{s,j}/W_i^r$. They sum to one when risky wealth is positive. Holdings are nonnegative; the model disallows short selling. The zero-risky-wealth case requires an implementation convention not provided by this ratio.

Each trader activates with a given probability. An activated trader draws a desired risky fraction $\gamma_i$ uniformly from $[0,1]$ and targets risky wealth $\widehat W_i^r(h+1)=\gamma_iW_i(h)$. It then draws nonnegative random weights across eligible stocks, normalized to sum to one. Desired quantities and orders are

$$
\widehat a_i^{s,j}(h+1)=
\left\lfloor\widehat\omega_i^{s,j}(h+1)
\frac{\widehat W_i^r(h+1)}{p^{s,j}(h)}\right\rfloor,
\qquad
\Delta_i^{s,j}=\widehat a_i^{s,j}-a_i^{s,j}(h).
$$

Positive $\Delta$ means buy, negative means sell. Desired weights need not be achieved because executions require counterparties. Integer rounding also leaves residual cash. The paper's text says weights are uniform draws subject to normalization; it does not specify whether implementation normalizes independent uniforms or samples uniformly on the simplex. Those procedures have different concentration distributions and must not be treated as interchangeable.

The source describes assets as traded sequentially. Because they share trader cash balances, execution order and treatment of cash reserved for outstanding orders can affect feasible fills. The article does not fully give those bookkeeping details, activation probability, total trader count, or the exact order in which asset markets clear. It points to earlier GASM papers for market-clearing mechanics.

## Orders and endogenous volatility feedback

Let $G_i$ be a Gaussian draw with mean 1.01 and stock-specific standard deviation $\sigma_i^{s,j}$. The buy and sell limit prices are

$$
d_i^{s,j}(h+1)=p^{s,j}(h)G_i,
\qquad o_i^{s,j}(h+1)=p^{s,j}(h)/G_i.
$$

Limit-price uncertainty is linked to historical log-return volatility:

$$
\sigma_i^{s,j}=\alpha\sigma^{s,j}(T_i).
$$

The scale $\alpha$ is common to traders, while $T_i$ is trader-specific memory. High realized volatility widens order-price dispersion, which can generate further volatile prices. Thus clustered volatility is partly attributable to an explicitly specified feedback, rather than emerging from independent identically distributed orders with a constant price distribution.

Demand and supply curves aggregate orders at each step; their intersection determines the new price. The source does not fully specify partial fills, ties, no-crossing cases, cancellations, cash-shortage resolution, negative Gaussian draws, or numerical clipping. A Gaussian multiplier can be zero or negative with nonzero probability; the displayed formulas alone do not ensure globally positive order prices. Both $\alpha$ and the distribution of $T_i$ are missing from this short version, limiting exact replication.

The random fraction $\gamma_i$ concerns risky allocation, while $\alpha$ controls limit-price dispersion; neither should be confused with the coefficient called $a_1$ in the dividend model. Keeping these roles separate is necessary to reconstruct the simulator.

## Sector restrictions and dividends

The experiment uses 100 stocks divided into ten sectors of ten firms. The main treatment is the number $L$ of sectors accessible to an individual trader. At $L=10$, every trader can invest in every sector. At $L=5$, each trader restricts its universe to five randomly selected sectors. This creates a structured overlap network even though individual asset choices remain random.

The article does not state a full resampling schedule for sector eligibility. A reproduction must disclose whether restrictions are fixed for a trader throughout a run or redrawn over time. Fixed restrictions preserve a persistent network; redrawing them every step can substantially weaken that structure.

Two funding environments are compared: conserved resources without dividends or external cash injection, and dividend-paying stocks that add cash to investors. Dividends arrive every $Q=63$ steps, approximately a quarter, according to

$$
q_n^{s,j}=a_0^s+a_1q_{n-1}^{s,j}+b^{s,j}\epsilon_n^s,
\qquad q_0^{s,j}=a_0^s/(1-a_1).
$$

Here $a_0^s$ ranges from 0.05 to 0.095 in increments of 0.005 across the ten sectors, $a_1=0.9$, and each stock's coefficient $b^{s,j}$ is drawn uniformly from $[0,0.02]$. A sector shares its Gaussian innovation $\epsilon_n^s$, but individual coefficients differ. The source does not explicitly specify every innovation-normalization detail beyond calling the draws normal.

The initial mean dividend therefore ranges from 0.5 to 0.95 per share, a direct calculation from the stated parameters. Cash rises by the dividend per share times holdings. Agents do not use dividend information in choosing their allocations. Dividend cash nevertheless affects their purchasing power and therefore prices; absence of deliberate dividend-based decisions does not imply absence of every dividend-to-price channel.

Initial endowments are equal across agents: EUR 10,000,000 cash and 1,000 shares of each stock. The treatment must be reconciled with any initial sector-eligibility restriction in an actual implementation; the paper does not detail disposal or exclusion of initially held but ineligible securities. Price plots begin near 100 and extend to about 2,000 steps, but exact initialization and the complete burn-in/measurement schedule are not documented.

## Time-series diagnostics and their interpretation

Figures 1–2 show illustrative prices and returns with and without dividend payments. The conserved-resource market fluctuates around a roughly stable level; the dividend-funded example trends upward. Return paths exhibit periods of larger and smaller fluctuations, while the survival-function comparison in Figure 3 shows heavier tails than a Gaussian reference.

The paper invokes Jarque–Bera tests for normality and Ljung–Box tests for serial correlation but gives no full statistics, lag choices, p-values, rejection counts, or confidence intervals. Those tests are not enough, as reported, to reconstruct a quantitative claim about the size or significance of every simulated stylized fact.

At 5% significance, the variance-ratio test rejects a random walk in both funding environments. An augmented Dickey–Fuller regression with a constant rejects a unit root without dividends but does not reject it with dividends. Lag selection and variance-ratio horizons are unspecified. Failure to reject a unit root is not proof of a unit root, and mean reversion in a fixed-resource simulation does not establish a predictive trading edge in real markets.

Table 1 reports the following cross-stock averages:

| Estimator | Dividends, $L=10$ | Dividends, $L=5$ | No dividends, $L=10$ | No dividends, $L=5$ | S&P sample |
|---|---:|---:|---:|---:|---:|
| Hurst | 0.4887 | 0.4789 | 0.4819 | 0.4726 | 0.4898 |
| Podobnik | 0.3482 | 0.3639 | 0.3472 | 0.3699 | 0.4520 |
| DFA | 0.4359 | 0.3228 | 0.3207 | 0.3547 | 0.3720 |

The article calls these power-law exponents and discusses return tails. Hurst and DFA quantities generally concern scaling and dependence, so they should not be silently reinterpreted as an estimated Pareto survival-tail exponent. The source does not supply a mapping or enough estimator settings to resolve that terminology. The values are reported as given, without inferring nonexistent tail probabilities or finite-moment thresholds from them.

## Correlation spectra: experiment and empirical reference

Construct a return correlation matrix using 100 stocks and 800 observations. The empirical comparison draws 100 S&P 500 stocks over an approximately 800-day closing-price window spanning 2001–2004. Full security membership, exact dates, vendor, adjustments, and missing-data handling are not supplied.

As an implementation reconstruction, standardize each stock's returns within the measurement window and form the sample correlation matrix. Under an ideal iid unit-variance reference with $q=100/800=0.125$, the Marchenko–Pastur upper edge is

$$
\lambda_+=(1+\sqrt q)^2\approx1.8321.
$$

This calculation reproduces the stated 1.83 reference line. It is an asymptotic null edge under restrictive independence assumptions, not an exact finite-sample 95% threshold or a proof that every eigenvalue above it represents a fundamental sector.

Figures 4–7 compare the full spectra. At $L=10$, one especially large outlier dominates. Restricting traders to $L=5$ creates multiple eigenvalues above the null edge, resembling the empirical sample's combination of market and sector modes. The authors report that inverse-participation analysis associates the leading eigenvector with the whole market and other outliers with sectors. They do not print all eigenvector loadings or participation values, so detailed sector identification is not independently verifiable from those claims alone.

The distinction is between ten accessible sectors and five accessible sectors per trader; both main experiments contain ten labeled economic sectors. A sentence describing a “single business sector” should therefore not be used to recode $L=10$ as a one-sector economy. The important treatment is the degree of restriction on allocation, not changing the total number of stocks or sector labels.

The eigenvalue rank fits use the ten largest eigenvalues, with reported positive exponent magnitudes:

| Environment | $L=10$ | $L=5$ |
|---|---:|---:|
| With dividends | 1.0878 | 0.5703 |
| Without dividends | 1.1040 | 0.5894 |

The empirical reference is 1.25. Figure 9 shows a histogram of fitted negative slopes over 1,000 random S&P samples, approximately in the −1.4 to −1.05 range. Table 2 reports positive magnitudes, while the histogram uses signed slopes; these should not be compared without accounting for the sign convention.

A useful qualification is that the $L=10$ rank exponent is closer to the empirical reference, while $L=5$ is the treatment that produces multiple sector-like outliers. Matching one summary statistic therefore does not establish that a single parameter setting reproduces every observed cross-sectional property. The paper reports similar structural results with dividends and says external cash inflow gives the same qualitative outcome, but does not provide a full inflow rule or separate sensitivity table.

## What a reconstruction can and cannot reproduce

The specified ingredients support a transparent simulator skeleton: initialize cash and holdings; assign sectors and eligible universes; activate traders; draw risky fractions and eligible-stock allocations; convert target values into integer orders; generate volatility-dependent limits; clear each asset; update holdings and cash; pay scheduled dividends; and measure returns and correlation spectra over a documented window.

Exact reproduction needs additional choices for the number of traders, activation probability, memory distribution, volatility multiplier, random weight law, market-clearing tie rules, sequential cash availability, initialization, seeds, and sample extraction. Those are not supplied completely in the article. They should be published as assumptions or obtained from the cited GASM implementation rather than attributed to this paper without evidence.

A meaningful validation would first check cash and share conservation in the no-dividend treatment and reconcile dividend cash injections in the other treatment. It would then compare the four dividend-by-eligibility configurations across independent seeds, using the same windows and diagnostics. The original article reports illustrative paths and spectral summaries, not such a complete uncertainty analysis or a calibrated fit to actual order-book data.

The model's economic message is that constrained participation and shared financial resources can create common return structure without sophisticated forecasting. Its empirical limit is equally important: reproducing a few stylized facts with random traders does not identify the actual mechanism in real financial markets or justify treating all spectral outliers as exploitable information.
