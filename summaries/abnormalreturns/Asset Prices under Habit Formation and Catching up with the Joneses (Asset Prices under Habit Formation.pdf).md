# Asset Prices under Habit Formation and Catching up with the Joneses

Andrew B. Abel, *American Economic Review* 80(2), Papers and Proceedings, May 1990, pp. 38–42. JSTOR stable identifier 2006539. The six-page local PDF includes a cover followed by the complete five-page article.

Source: [Asset Prices under Habit Formation.pdf](../../Finance/Asset Prices under Habit Formation.pdf).

## Why this matters

Habit formation and comparison with other consumers can look identical in a representative-agent equilibrium, where everyone consumes the same amount. They nevertheless imply different asset prices because an individual internalizes the effect of its own consumption on its future habit but does not internalize its effect on an external aggregate benchmark. Abel provides one preference specification nesting both cases, derives equilibrium prices, and shows the gains and problems when using these preferences to address the equity-premium puzzle.

The paper's contribution is a compact analytical pricing model and calibration. It is not an estimated consumption process, an out-of-sample test, or a cross-sectional trading strategy. The calibration improves the average equity premium under relative consumption, but also generates excessive variation in conditional expected returns. Habit formation creates pronounced parameter sensitivity rather than an unqualified empirical resolution.

## Preferences and the internal-versus-external distinction

An individual chooses consumption $c_t$ to maximize expected discounted period utility, with discount factor $\beta$:

$$
U_t=\sum_{j=0}^{\infty}\beta^j u(c_{t+j},v_{t+j}),
\qquad
v_t=[c_{t-1}^{D}C_{t-1}^{1-D}]^\gamma,
$$

$$
u(c,v)=\frac{(c/v)^{1-a}}{1-a},\qquad a>0.
$$

In the second display the symbol $u$ denotes period utility. The benchmark is $v_t$; it is not a tradable asset or an independent shock. $C_t$ is aggregate per-capita consumption, taken as external by an individual. The parameter $\gamma$ determines benchmark strength; $D$ controls the own-consumption contribution. The displayed family permits $D\ge0$, with its three principal cases at $D=0$ or 1.

At $\gamma=0$, preferences reduce to ordinary time-separable isoelastic utility. At $\gamma>0,D=0$, the benchmark uses lagged aggregate consumption: “catching up,” rather than contemporaneous comparison. At $\gamma>0,D=1$, the benchmark uses the individual's own prior consumption, creating internal habit formation. Intermediate $D$ combines internal and external effects.

When differentiating lifetime utility with respect to $c_t$, hold aggregate consumption fixed. Current consumption affects current utility directly and next-period utility through $v_{t+1}$:

$$
\frac{\partial U_t}{\partial c_t}
 =u_c(c_t,v_t)+\beta u_v(c_{t+1},v_{t+1})
             \frac{\gamma Dv_{t+1}}{c_t}.
$$

The second term is the internal habit cost. Dropping it and then substituting representative-agent consumption would incorrectly make internal habit and external comparison equivalent.

For isoelastic utility this derivative is

$$
\frac{\partial U_t}{\partial c_t}
 =\frac{(c_t/v_t)^{1-a}}{c_t}
 \left[1-\beta\gamma D
 \left(\frac{c_{t+1}}{c_t}\right)^{1-a}
 \left(\frac{v_t}{v_{t+1}}\right)^{1-a}\right].
$$

The log-utility limit is $a=1$. Parameter $a$ is the standard relative-risk-aversion coefficient in the time-separable case; with intertemporal dependence, it should not be interpreted as a complete measure of all effective risk aversion.

## Endowment equilibrium and the pricing kernel

The economy is a Lucas-style exchange economy with perishable endowment $y_t$. Identical consumers consume all output, $c_t=C_t=y_t$. Let gross consumption growth be $x_t=y_t/y_{t-1}$. Then $v_t=y_{t-1}^\gamma$ and $v_{t+1}/v_t=x_t^\gamma$.

Define $\theta=\gamma(a-1)$. Equilibrium lifetime marginal utility contains

$$
H_{t+1}=1-\beta\gamma D x_{t+1}^{1-a}x_t^\theta.
$$

Because $H_{t+1}$ contains a future realization, the relevant date-$t$ marginal valuation is its conditional expectation. Write $J_t=E_t[H_{t+1}]$. An adapted representation of the pricing kernel, obtained by taking the appropriate conditional expectations in the paper's Euler equation, is

$$
m_{t+1}=\beta\frac{J_{t+1}}{J_t}x_t^\theta x_{t+1}^{-a},
\qquad E_t[m_{t+1}R_{t+1}]=1.
$$

This form is equivalent for date-$t+1$ measurable payoffs to the article's representation using the next lifetime derivative. It makes the information timing explicit. Under $D=0$, $J_t=1$; with internal habit it generally varies with state. Positive marginal valuations are necessary for the intended economic pricing interpretation.

The paper gives a sufficient parameter restriction ensuring positive lifetime marginal utility for its bounded two-point habit example: when $\gamma=D=1$ and $\beta=0.99$, approximately $0.858<a<1.142$. It is a sufficient condition tied to that bounded support, not a universal admissibility interval for lognormal growth or arbitrary habits. Price formulas also require finite moments and convergent infinite-horizon present values.

## Closed-form iid prices

Assume $x_t$ is iid and define its moment function $M(k)=E[x^k]$. Let

$$
k=(1-a)(1-\gamma),\quad
J(x)=1-\beta\gamma D M(1-a)x^\theta,
$$

$$
A=\frac{\beta M(1-a)[1-\beta\gamma D M(k)]}
 {1-\beta M(k)},
$$

$$
q=M(-a)-\beta\gamma D M(1-a)M(\theta-a),
\qquad Q=\frac{\beta q}{1-\beta M(\theta-a)}.
$$

Equations 14–16 give the ex-dividend stock price-dividend ratio $w_t$, the price $s_t$ of a bill paying one next period, and the ex-coupon price $p_t^c$ of a consol paying one per period:

$$
w_t=A\frac{x_t^\theta}{J(x_t)},\qquad
s_t=\beta q\frac{x_t^\theta}{J(x_t)},\qquad
p_t^c=Q\frac{x_t^\theta}{J(x_t)}.
$$

The actual stock price is $p_t^s=w_ty_t$. The three assets differ in their cash flows even though their state dependence shares a common factor. Return formulas are

$$
R_{t+1}^s=\frac{(1+w_{t+1})x_{t+1}}{w_t},
\qquad R_{t+1}^b=1/s_t,
\qquad R_{t+1}^c=\frac{1+p_{t+1}^c}{p_t^c}.
$$

One can reconstruct the stock-price solution directly from the Euler equation. Substitute $w_t=A x_t^\theta/J_t$ into $w_t=E_t[m_{t+1}x_{t+1}(1+w_{t+1})]$. Independence reduces the unknown coefficient to

$$
A=\beta\{M(1-a)-\beta\gamma D M(1-a)M(k)+AM(k)\},
$$

which yields the expression above. This algebra also shows why the denominator $1-\beta M(k)$ matters. A zero or negative denominator cannot simply be passed through as a normal positive price without checking the economic existence conditions.

For $D=0$, the unconditional expected gross returns simplify to

$$
E[R^s]=M(-\theta)\{M(1)+AM(1+\theta)\}/A,
$$

$$
E[R^b]=M(-\theta)/(\beta q),
\qquad
E[R^c]=M(-\theta)\{1+QM(\theta)\}/Q.
$$

Internal habit can instead be evaluated by direct finite-state averaging using the price functions. There is no need to simulate a long path to replicate the two-point table.

## Calibration and an explicit replication recipe

The calibration sets $\beta=0.99$, mean gross growth $E[x]=1.018$, and standard deviation 0.036. Panels A–B compare a two-point iid growth distribution with a lognormal distribution matching those moments. A symmetric two-point distribution placing probability one-half at 0.982 and 1.054 reproduces the reported two-point table to rounding; this reconstruction was checked by direct evaluation of all thirteen parameter rows.

For each $(\gamma,D,a)$, calculate moments and $A,q,Q$. Evaluate prices at each current growth state. Average stock and consol returns over the four equally likely current/next-state combinations, and average bill returns over the two current states. Report $100(E[R]-1)$, since the table contains percentage net returns, whereas the formulas use gross returns.

For the matched lognormal case, reconstruct log-variance and log-mean as

$$
s^2=\log[1+(0.036/1.018)^2],\qquad
\ell=\log(1.018)-s^2/2,
\qquad M(k)=e^{k\ell+k^2s^2/2}.
$$

This is a moment-matching implementation of the stated distribution, not an estimated lognormal law. Lognormal comparisons are reported only for the time-separable and external-relative-consumption panels; the article does not give a corresponding lognormal habit panel with global marginal-utility admissibility established.

The empirical target comes from Mehra–Prescott's cited US 1889–1978 averages: stocks 6.98% real, bills 0.80%, and an equity premium of 618 basis points. Abel's own table uses iid growth, whereas the cited earlier model used growth autocorrelation −0.14. The numerical comparison therefore changes preferences while also using a simplified growth process; it is not an identical-process re-estimation of that earlier model.

## Numerical results

Selected and bounding rows of Table 1 are shown below. All entries are annual percentage net returns under the two-point calibration.

| Preferences | $a$ | Stocks | Bills | Consols |
|---|---:|---:|---:|---:|
| Time separable, $\gamma=0$ | 0.5 | 1.93 | 1.87 | 1.87 |
| Time separable | 1.0 | 2.83 | 2.70 | 2.70 |
| Time separable | 6.0 | 10.34 | 9.52 | 9.52 |
| Time separable | 10.0 | 14.22 | 12.85 | 12.85 |
| External comparison, $\gamma=1,D=0$ | 0.5 | 2.80 | 2.76 | 2.73 |
| External comparison | 1.0 | 2.83 | 2.70 | 2.70 |
| External comparison | 6.0 | 6.70 | 2.07 | 5.84 |
| External comparison | 10.0 | 14.73 | 1.59 | 13.16 |
| Internal habit, $\gamma=D=1$ | 0.86 | 33.56 | 4.53 | 35.25 |
| Internal habit | 0.94 | 6.83 | 3.48 | 7.44 |
| Internal habit | 1.00 | 2.83 | 2.70 | 2.70 |
| Internal habit | 1.06 | 8.43 | 1.93 | 7.40 |
| Internal habit | 1.14 | 38.28 | 0.93 | 35.16 |

Time-separable preferences raise bills along with stocks as $a$ increases, leaving an equity premium far below the historical target. At $a=6$, its premium is about 82 basis points. Under external comparison at the same parameter, it is 463 basis points, with a much lower 2.07% bill rate. At $a=10$, the external-comparison premium rises to about 1,314 basis points; success at increasing the premium is not a unique calibrated fit.

The matched lognormal values differ little in the reported range. For example, external comparison at $a=6$ gives stocks 6.72%, bills 2.06%, and consols 5.86%, versus 6.70%, 2.07%, and 5.84% in the two-point case. At $a=10$ the corresponding figures are 14.95%, 1.55%, and 13.32%. Distributional robustness here concerns these selected unconditional averages, not every aspect of conditional risk or admissibility.

At $a=1$ all three preference specifications deliver the same listed expected returns. Internal habit outcomes change sharply on either side of that value: moving from 1.06 to 1.14 raises expected stock return from 8.43% to 38.28%. This sensitivity accompanies small positive conditional marginal-valuation factors near the sufficient-condition boundary. It should not be described as a stable solution to the puzzle with innocuous parameter changes.

Most importantly, the external-comparison case at $a=6$ produces a 17.87% standard deviation of the conditional expected bill return under the two-point calibration. A one-period bill is riskless conditional on the state, but its next-period yield changes as the state changes. The model can therefore move average bill and stock returns toward their historical targets while making the time variation of expected returns implausibly large.

## Implications and scope

The reusable theoretical insight is the distinction between an equilibrium identity and an individual's derivative. Even when personal and aggregate consumption coincide in equilibrium, internalizing tomorrow's benchmark changes today's marginal valuation and therefore the stochastic discount factor. A habit specification cannot be replaced by an external consumption benchmark merely because the observed consumption paths look the same.

For replication, the paper is unusually tractable: its two-state numerical table follows from moment calculations and finite-state averaging. No optimizer, sampling seed, transaction-cost model, portfolio rebalance schedule, or regression inference is involved. The historical moments are calibration inputs and the historical return targets are external benchmarks, rather than observations used to estimate all preference parameters statistically.

The limitations are economic and quantitative. Consumption equals dividends, aggregate risk is represented by one iid growth shock, individual heterogeneity is absent, and the admissibility and price-convergence conditions constrain parameter choices. Matching unconditional premia does not ensure realistic conditional yields, volatility, or asset-price dynamics. Extensions with intermediate benchmark weights and non-iid growth are suggested, but are not completed empirical results in this short article.
