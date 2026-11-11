# Capital Market Equilibrium with Restricted Borrowing

Fischer Black. *The Journal of Business* 45(3), July 1972, pp. 444–455. [Source PDF](../../Finance/AbnormalReturnsVolatility_Black_1972.pdf). The supplied file contains a JSTOR cover followed by the complete twelve-page article; printed page 444 is PDF page 2. All thirteen PDF pages were read visually because this copy is scanned.

## Why this matters

Black shows that the familiar linear relation between expected return and market beta can survive the removal of unrestricted riskless borrowing. What changes is the intercept. A risky portfolio with zero covariance with the market replaces the riskless asset in the pricing relation. In the economically binding lending-only case, that portfolio's expected return lies above the lending rate, giving a flatter security market line and positive conventional CAPM alphas for low-beta assets.

This is a precise equilibrium explanation for a particular pattern often grouped with low-volatility anomalies. It does not predict that higher beta necessarily means a lower unadjusted expected return. Nor does it derive a negative premium for idiosyncratic volatility. Its implication is that expected returns increase less rapidly with beta than the unrestricted borrowing CAPM would predict. An empirical strategy using total volatility, residual volatility, minimum variance, or low beta therefore needs an additional mapping from its signal to this mechanism.

The contribution is theoretical. Black supplies no new portfolio backtest, return table, transaction-cost calculation, or estimated constraint parameter. He discusses earlier evidence from Pratt, Friend and Blume, Miller and Scholes, and Black, Jensen, and Scholes. Those studies motivate the model; their samples and conclusions are not experiments newly performed in this article. The important practical result is a change in the benchmark used to interpret apparent alpha, together with a clear statement of which market restrictions preserve two-fund separation.

## Market, preferences, and the two restrictions

Let $R_i$ be the one-period simple total return on risky asset $i$, including distributions. Write the vector of expected returns as $\mu$, its covariance matrix as $\Sigma$, and the fully invested portfolio weights as $x$, with $\mathbf 1'x=1$. Short positions in risky assets are permitted without limit. The market portfolio $m$ is the value-weighted aggregate of outstanding risky assets, not an arbitrary stock index chosen after estimation.

Investors share beliefs about the joint return distribution, maximize expected utility of terminal wealth, and are risk averse. Joint normality makes mean and variance sufficient for the portfolio choice considered here. The introductory discussion also mentions joint stable distributions, but the displayed covariance and inverse-covariance derivation requires finite second moments; it cannot literally be applied to a stable law with infinite variance. Black observes that exact normality over a finite horizon admits negative terminal asset prices and presents the assumption as an approximation, particularly over short intervals.

The ordinary CAPM is

$$
\mu_i=R_f+\beta_i(\mu_m-R_f),\qquad
\beta_i=\frac{\operatorname{Cov}(R_i,R_m)}{\operatorname{Var}(R_m)}.
$$

Black studies two alternatives. First, no riskless asset is available and neither riskless borrowing nor lending is possible. Second, investors can hold a riskless asset but cannot short it: its portfolio weight must be nonnegative. In both alternatives, risky long and short positions remain unrestricted. The second case is therefore not a general model of a long-only investor, margin requirements on every asset, securities-lending scarcity, or borrowing at a spread. Those restrictions would change the feasible set and can destroy the common two-fund representation.

The analysis takes asset moments and equilibrium prices as consistent with investor choices and market clearing. It does not solve a dynamic economy for expected returns from primitives such as dividend processes, individual endowments, or a distribution of margin limits. The security market line is an equilibrium restriction conditional on the market being the aggregate efficient risky portfolio.

## The mean–variance program and separation

For a target expected return $\mu_k$, Black's equations (6)–(9), pp. 447–448, minimize

$$
\min_x x'\Sigma x
\quad\text{subject to}\quad
x'\mu=\mu_k,\qquad \mathbf 1'x=1.
$$

His Lagrangian uses multipliers $S_k$ and $T_k$:

$$
\mathcal L=x'\Sigma x-2S_k(x'\mu-\mu_k)-2T_k(\mathbf 1'x-1).
$$

The first-order condition is

$$
\Sigma x_k=S_k\mu+T_k\mathbf 1.
$$

For a positive-definite covariance matrix this condition is sufficient, and

$$
x_k=S_k\Sigma^{-1}\mu+T_k\Sigma^{-1}\mathbf 1.
$$

Thus all minimum-variance portfolios for specified means belong to a two-dimensional linear span. Full investment reduces that span to an affine line in weight space. Black constructs two normalized funds from the vectors $\Sigma^{-1}\mu$ and $\Sigma^{-1}\mathbf 1$ and observes that any other nonsingular pair spanning the same set can replace them. His normalization of the first vector presumes its weights have a nonzero sum; the underlying separation result does not depend on that particular normalization.

A directly implementable equivalent, derived here from the same first-order conditions, avoids this normalization issue. Define

$$
A=\mathbf 1'\Sigma^{-1}\mathbf 1,\quad
B=\mathbf 1'\Sigma^{-1}\mu,\quad
C=\mu'\Sigma^{-1}\mu,\quad D=AC-B^2.
$$

Assuming $D>0$, the target-mean frontier portfolio and its variance are

$$
x(\mu_k)=\Sigma^{-1}\left[
\frac{A\mu_k-B}{D}\mu+
\frac{C-B\mu_k}{D}\mathbf 1\right],
$$

$$
v(\mu_k)=\frac{A\mu_k^2-2B\mu_k+C}{D}.
$$

The global minimum-variance portfolio has weights $g=\Sigma^{-1}\mathbf 1/A$, mean $\mu_g=B/A$, and variance $1/A$. The upper branch is efficient for investors who prefer higher mean and lower variance. The lower branch solves the equality-constrained variance problem but is dominated in mean–variance space. Maintaining this distinction prevents the word “efficient” from incorrectly assigning desirable investor choices to every portfolio in the spanning line.

Market clearing combines individual risky holdings into the market portfolio. With common beliefs and the stated preferences, the aggregate lies in the same frontier span. Black chooses a basis consisting of a fund with market beta one and a fund with market beta zero; the beta-one frontier fund is the market, and the beta-zero frontier fund is the minimum-variance zero-beta portfolio, denoted $z$. An efficient risky portfolio can consequently be written

$$
R_k=\beta_k R_m+(1-\beta_k)R_z.
$$

The coefficients are portfolio weights and can fall outside $[0,1]$. A high-beta portfolio uses a negative weight in $z$; it is not necessarily created by borrowing the riskless asset. Unlimited shorting of risky assets is precisely what permits that distinction in Black's economy.

## Deriving the zero-beta pricing equation

For any asset $i$, the componentwise first-order condition for frontier portfolio $k$ is

$$
\operatorname{Cov}(R_i,R_k)=S_k\mu_i+T_k.
$$

Subtract the condition for asset or portfolio $j$ to eliminate $T_k$:

$$
\operatorname{Cov}(R_i,R_k)-\operatorname{Cov}(R_j,R_k)
=S_k(\mu_i-\mu_j).
$$

Set $k=m$ and $j=z$. By construction $\operatorname{Cov}(R_z,R_m)=0$, giving

$$
\operatorname{Cov}(R_i,R_m)=S_m(\mu_i-\mu_z).
$$

Applying this identity to $i=m$ yields $\operatorname{Var}(R_m)=S_m(\mu_m-\mu_z)$. Dividing produces Black's central equation (27), p. 450:

$$
\boxed{\mu_i=\mu_z+\beta_i(\mu_m-\mu_z).}
$$

The argument prices every risky asset, not merely the frontier funds used in the derivation. It also implies that every fully invested zero-beta portfolio has expected return $\mu_z$. Among those portfolios, $z$ has minimum variance. Other zero-beta portfolios can carry additional residual risk without receiving a higher expected return in this model.

Zero beta means zero covariance with the market, not zero variance. Under joint normality, the zero-covariance return pair is independent. Without normality, uncorrelatedness is the property used in the variance algebra; independence need not follow. In particular, a strategy market-neutral in this sense can still have substantial losses and tail dependence outside the model's distributional assumptions.

A useful reconstruction of $z$ follows directly from constrained variance minimization. For a specified fully invested market weight vector $m$, solve

$$
\min_z z'\Sigma z
\quad\text{subject to}\quad
\mathbf 1'z=1,\qquad z'\Sigma m=0.
$$

Let $v_m=m'\Sigma m$ and $v_g=1/A$. For a nondegenerate market with $v_m>v_g$, the solution is

$$
z=\frac{v_m g-v_g m}{v_m-v_g},\qquad
v_z=\frac{v_gv_m}{v_m-v_g}.
$$

These formulas are a derivation for this note, not an additional empirical claim by Black. They verify full investment and zero covariance immediately because $\operatorname{Cov}(R_g,R_m)=v_g$ for every fully invested $m$. They also show why a zero-beta fund becomes unstable as the market approaches the global minimum-variance portfolio: the denominator becomes small. At the exact global minimum, every fully invested portfolio has covariance $v_g$ with the market, so a fully invested zero-beta portfolio does not exist. The pricing construction presumes the nondegenerate efficient market case.

When $m$ lies on the frontier, its zero-beta counterpart also lies on the frontier's affine weight span. The formulas give

$$
\mu_z=\frac{v_m\mu_g-v_g\mu_m}{v_m-v_g}.
$$

For an upper-branch market, $\mu_m>\mu_g$, implying $\mu_z<\mu_g<\mu_m$. This is consistent with a risky zero-beta counterpart lying on the lower frontier branch. It must not be confused with the global minimum-variance portfolio itself.

## The second covariance factor

Black's equations (30)–(32), pp. 451–452, establish that an asset's covariance with $z$ is proportional to $1-\beta_i$. An especially transparent equivalent follows from the fact that $z$ is minimum variance subject to its zero-beta constraint. The proportionality constant is pinned down by applying the identity to $z$ itself:

$$
\operatorname{Cov}(R_i,R_z)=(1-\beta_i)v_z.
$$

Consequently the linear projection on the two orthogonal funds can be represented as

$$
R_i=\beta_iR_m+(1-\beta_i)R_z+\varepsilon_i,
$$

with $E[\varepsilon_i]=0$ and $\varepsilon_i$ orthogonal to both funds under the equilibrium moment restrictions. This derived representation clarifies the empirical two-factor expression discussed earlier in the article. It does not establish that all residuals $\varepsilon_i$ are mutually independent. Such a cross-sectional residual restriction is stronger than the mean–variance pricing result and should not be silently imported into a risk model.

The pricing equation is still a one-dimensional expected-return relation in market beta: the coefficient on the second fund is constrained to $1-\beta_i$. Calling this an unrestricted two-factor expected-return model would obscure its testable structure. The zero-beta factor supplies the intercept and portfolio span; it is not a freely chosen second risk premium that can fit arbitrary cross-sectional means.

Black also critiques a proposed “portfolio sharing” construction in which investors receive a multiple of market returns. A sharing vehicle cannot generally sell all its claims at equilibrium terms without introducing an offsetting constant transfer. Adding a return of the form $R_f+\beta(R_m-R_f)$ effectively recreates borrowing and lending. One cannot remove riskless financing from the assumptions and then restore it through an intermediary's payoff contract without changing the economy (p. 451).

## Riskless lending without borrowing

In the second model, let $w_f\geq0$ be the weight in the riskless asset. The risky weights sum to $1-w_f$. If the investor holds a strictly positive riskless position, the first-order condition for that asset gives $T_k=-S_kR_f$. All such investors therefore hold the same relative risky allocation,

$$
t=\frac{\Sigma^{-1}(\mu-R_f\mathbf 1)}
{\mathbf 1'\Sigma^{-1}(\mu-R_f\mathbf 1)},
$$

when the normalizing denominator and the relevant tangency solution are well defined. They differ only in the fraction invested in $t$ versus cash. Investors whose desired risk is higher are constrained at $w_f=0$ and select portfolios on the risky frontier. The risky parts of both groups remain in the common two-fund span, so aggregate risky holdings again give the market portfolio and the zero-beta pricing relation for risky assets.

Writing a portfolio in the $(m,z,f)$ basis gives Black's equations (35)–(38):

$$
\mu_k=w_{km}\mu_m+w_{kz}\mu_z+w_{kf}R_f,
$$

$$
v_k=w_{km}^2v_m+w_{kz}^2v_z,
\qquad w_{km}+w_{kz}+w_{kf}=1,
\qquad w_{kf}\geq0.
$$

The missing covariance term follows from zero market covariance, not from $z$ being riskless. Tangency fund $t$ maximizes $(\mu_t-R_f)/\sqrt{v_t}$. The efficient opportunity set has a straight segment from cash to $t$, followed by the risky frontier beyond $t$. Riskless leverage would extend the straight segment; the borrowing prohibition removes that extension.

Black states the strict inequality $R_f<\mu_z<\mu_m$ in equation (39), p. 453, and uses it to conclude that borrowing restrictions flatten the risky-asset security market line. The strict lower inequality should be read as the economically binding case. If the constraint is slack for the aggregate investor configuration and the market coincides with the tangency portfolio, $\mu_z=R_f$ gives the ordinary CAPM boundary. Merely writing $w_f\geq0$ does not force a strictly positive shadow cost of borrowing in every possible equilibrium. This is a qualification of the source's strict statement, not a replacement of its central result.

The riskless asset itself does not have to satisfy the same line as the risky zero-beta portfolio. Both have beta zero, but only one can be shorted without limit. The constraint prevents the unconstrained arbitrage-style substitution that would otherwise force their expected returns to coincide. Mixing a risky asset with cash can consequently produce points off the risky-assets line while remaining in the overall constrained feasible set.

## What conventional alpha measures here

Subtract the ordinary CAPM prediction from Black's pricing relation:

$$
\alpha_i^{\mathrm{CAPM}}
=\mu_i-R_f-\beta_i(\mu_m-R_f)
=(1-\beta_i)(\mu_z-R_f).
$$

For a positive intercept wedge, low-beta assets have positive conventional alpha, beta-one assets have zero alpha, and high-beta assets have negative alpha. This is an exact model implication. It does not require pricing mistakes or irrational demand. It also does not make a constrained investor able to implement every portfolio that an unconstrained CAPM arbitrage argument would propose.

For example, as a purely illustrative calculation, if the zero-beta premium above lending is 2 percentage points per year, a beta-0.5 asset has a conventional alpha of 1 point and a beta-1.5 asset has alpha of −1 point. These numbers are not estimates from the article. Both assets can still have increasing expected returns with beta because the slope $\mu_m-\mu_z$ remains positive. A negative empirical slope, or a negative relation between returns and residual volatility holding beta fixed, calls for more than this model alone.

A long low-beta/short high-beta position is not automatically market-neutral. Its market exposure depends on both beta differences and position sizes. Nor is the zero-beta portfolio necessarily a low-volatility long-only basket. Recovering $z$ generally involves risky short positions, and its estimated weights can be extreme. The model should therefore inform benchmark construction before it is converted into a claim about a feasible institutional strategy.

## Reconstructing and testing the model

Given population $\mu$, $\Sigma$, and market weights, a numerical reconstruction is straightforward: verify positive definiteness; compute the frontier; solve the zero-beta constrained variance program; check $\mathbf 1'z=1$ and $z'\Sigma m=0$; and compare $\mu_i$ with $\mu_z+\beta_i(\mu_m-\mu_z)$. For the lending-only economy, compute $t$, identify the cash-plus-tangency segment, and verify the $w_f=0$ boundary for higher-risk investors. These are algebraic validation steps, not a reported simulation in the source.

An empirical implementation must estimate quantities that the theory treats as known. Beta measurement error can flatten an estimated security market line even without borrowing constraints. An incomplete market proxy can fail to be mean–variance efficient even when the true aggregate wealth portfolio is efficient. Changing investment opportunities, heterogeneous beliefs, taxes, trading costs, and risky shorting limits can each invalidate a step of the separation argument. Sample means and inverse covariance estimates also make direct recovery of the zero-beta fund fragile.

A meaningful test should distinguish the risky-assets cross-sectional restriction from a mechanically fitted intercept. It needs a declared market proxy, formation and test periods, return horizon, beta-estimation procedure, treatment of errors in variables, and inference allowing dependence across assets. If a zero-beta portfolio is estimated using the same returns used to evaluate its pricing power, the in-sample fit is not independent evidence. Black specifies none of these empirical design choices because the paper proves an equilibrium result rather than proposing an estimator.

The discussion of earlier evidence covers Pratt's 1926–1960 study, Friend and Blume's 1960–1968 sample, and Black, Jensen, and Scholes' 1926–1966 evidence, with particular emphasis on the later 1946–1966 period. The article reports their qualitative rejection patterns, not a self-contained data reconstruction or new uncertainty estimates. It also suggests that partial borrowing restrictions should produce related effects, but does not supply a calibrated model of heterogeneous margin limits or an estimated mapping from a borrowing cap to the intercept wedge.

Black's enduring result is therefore a disciplined interpretation of low-beta alpha: a flat empirical security market line can be consistent with rational equilibrium once financing opportunities are restricted. The precision comes from retaining the assumptions that make the proof work, especially homogeneous moments and unlimited risky shorting, and from treating the zero-beta expected return as an endogenous risky-portfolio intercept rather than as a substitute name for the Treasury rate.

## Source map and bibliography

Black, Fischer (1972), “Capital Market Equilibrium with Restricted Borrowing,” *The Journal of Business* 45(3), 444–455. Introductory assumptions and motivating evidence: pp. 444–446. Mean–variance separation: equations (4)–(18), pp. 446–449. Zero-beta pricing proof: equations (20)–(27), pp. 450–451. Covariance with the zero-beta fund: equations (30)–(32), pp. 451–452. Lending-only equilibrium: equations (33)–(42), pp. 452–454. Conclusions: p. 455. The source has footnotes containing references but no separate appendix, tables, or numerical experiments. The closed-form frontier and zero-beta weights in this note are explicitly derived from the source's optimization problem.
