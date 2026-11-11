# A Generalized Measure of Riskiness

Turan G. Bali, Nusret Cakici, and Fousseni Chabi-Yo. *Management Science* 57(8), August 2011, pp. 1406–1423. DOI: 10.1287/mnsc.1110.1373.

Source: [RiskManagement_BaliCakiciChabiyo_2011.pdf](../../Finance/RiskManagement_BaliCakiciChabiyo_2011.pdf), 18 PDF pages, read in full including all six tables, four figures, and references. PDF p. 1 corresponds to journal p. 1406. The separate 28-page online appendix, dated April 11, 2011, was subsequently retrieved and read in full: [local appendix PDF](../../tmp/pdfs/daily-2026-10-10/risk/BaliCakiciChabiYoMS2011_OnlineAppendix.pdf), [author-linked external copy](https://drive.google.com/file/d/1COQVJaPeGYy41MImRKPg6XkPL5tz-TQr/view). Its PDF page 2 is printed appendix page 1. Appendix page references below use PDF numbering; Tables I–IV are supplementary, while Arabic-numbered tables refer to the main article. The supplement supplies the proofs, risk-aversion estimation, and alternative-physical-riskiness results discussed below.

## Why this matters

The paper connects three objects that are often treated separately: a minimum wealth reserve for accepting a gamble, investor risk aversion, and a forward-looking distribution extracted from option prices. Its generalized measure assigns larger reserve requirements to more risk-averse investors, then uses a static option-spanning identity to estimate the measure under risk-neutral probabilities. The empirical question is whether that option-implied scalar helps rank stocks by subsequent excess return per unit of realized volatility.

The main empirical result is a negative association: optionable stocks with greater implied riskiness have lower reported risk-adjusted returns. The corresponding historical, moment-based measure performs much less consistently. This distinction is useful for signal research because it separates information embedded in option prices from the generic claim that a particular nonlinear transformation of historical returns improves selection.

Several limitations prevent treating the paper as a ready-made portfolio backtest. The return-timing description is not fully consistent across the prose and table notes, the reported outcome is a return-to-volatility ratio rather than a tradable long–short return, and no turnover or implementation-cost analysis is supplied. There are also substantive qualifications to the theoretical interpretation of the generalized threshold. The formulas below reconstruct the measurable objects while identifying where the printed statements exceed what follows mathematically.

## Generalized reserve and preference parameter

A gamble $g$ has finite support, positive mean, and a positive probability of loss. Write $L(g)=-\min g>0$. The paper follows a sequential accept/reject model in which wealth changes from $W_t$ to $W_t+g_{t+1}$ if the gamble is accepted and otherwise stays constant. Candidate wealth thresholds are homogeneous in gamble size. Future offers may depend on history, with a finite generating set of distributions.

For $\delta\le0$, define the increasing concave transformation

$$
h_\delta(z)=
\begin{cases}
\{(1+z)^\delta-1\}/\delta,&\delta<0,\\
\log(1+z),&\delta=0,
\end{cases}
\qquad z>-1.
$$

The generalized reserve $R_\delta(g)$ solves

$$
E[h_\delta(g/R_\delta(g))]=0,\qquad R_\delta(g)>L(g).
$$

This is a scalar indifference condition. For utility $u(W)=W^\delta/\delta$ when $\delta<0$, relative risk aversion is $\theta=1-\delta$. The limiting $\delta=0$ case is logarithmic utility and $\theta=1$. Therefore lowering $\delta$ increases risk aversion and increases the reserve required to accept a fixed gamble. The empirical baseline uses $\delta=-2$, corresponding to relative risk aversion three.

Appendix A, Lemma 1 (supplement PDF p. 2), proves existence and uniqueness through strict concavity. Reconstructing its argument also clarifies that the required solution is the nonzero root. Let $x=1/R$ and $\phi_\delta(x)=E[h_\delta(xg)]$ for $0\le x<1/L$. Then $\phi_\delta(0)=0$, $\phi'_\delta(0)=E[g]>0$, and

$$
\phi''_\delta(x)=(\delta-1)E[g^2(1+xg)^{\delta-2}]<0.
$$

The function tends to minus infinity at the loss boundary. It therefore has exactly one positive zero in addition to zero itself. Solve for this nonzero root using a safeguarded bracket; evaluate the power expression through `expm1(delta*log1p(x*g))/delta` to avoid cancellation near zero. Check that the resulting reserve exceeds every modeled loss and that all transformed payoff arguments remain positive.

At $\delta=0$, the definition exactly reproduces Foster–Hart riskiness. The paper also invokes Aumann–Serrano’s exponential index, but its actual discussion establishes closeness in an appropriate small-payoff/large-reserve limit, not equality with the unscaled generalized reserve at an arbitrary finite $\delta$. The second-order expansion gives $R_\delta\approx(1-\delta)E[g^2]/(2E[g])$ when normalized payoffs are small. Thus the risk-aversion parameter changes the level even when the payoff distribution is fixed.

Appendix A supplies the arguments for the properties stated in Section 3. The natural domain remains admissible gambles for which the reserve exists; these results do not authorize negative-mean samples or unbounded-loss positions. Distribution dependence is immediate, and rescaling the nonzero root proves positive homogeneity. A reserve strictly above maximum loss follows from the loss-boundary divergence. The printed lemma includes zero in its uniqueness interval even though zero is always a root; uniqueness means exactly one **positive** root in the open admissible interval.

For subadditivity, set $a=R_\delta(g)$, $b=R_\delta(h)$, and $\lambda=a/(a+b)$. Concavity gives

$$
E h_\delta\!\left(\frac{g+h}{a+b}\right)
\ge \lambda E h_\delta(g/a)+(1-\lambda)E h_\delta(h/b)=0.
$$

The reserve sign criterion then gives $R_\delta(g+h)\le a+b$, provided $g+h$ remains in the gamble domain. No independence is required. Homogeneity plus subadditivity yields convexity. For dilution, independently replace the gamble with zero with probability $1-q$, without reducing its nonzero payoff sizes. The transformed expectation becomes $qE h_\delta(g/R)$, so its positive root is unchanged. This differs from multiplying every payoff by $q$, which multiplies the reserve by $q$. These are Appendix A equations (A17)–(A27), supplement pp. 5–6.

Independence adds the lower bound $R_\delta(g+h)\ge\min\{R_\delta(g),R_\delta(h)\}$, proved in (A28)–(A33), supplement pp. 6–8. One domain case should be made explicit. Let $a=R_\delta(g)\le R_\delta(h)$ and $\rho=1/a$. If $a\le L(g+h)$, the lower bound follows directly from $R_\delta(g+h)>L(g+h)$. Otherwise all factors below are positive; independence of finite-support gambles implies $L(g+h)=L(g)+L(h)$. Put $A=1+\rho g$, $B=1+\rho h$. The inequality $\{(1-x)^\delta-1\}/\delta\le-x$ and independence imply

$$
E h_\delta(\rho(g+h))
\le \frac{E[A^\delta]E[B^\delta]-1}{\delta}
-\rho^2E[gA^{\delta-1}]E[hB^{\delta-1}].
$$

For $\delta<0$, the first term is nonpositive because $E[A^\delta]=1$ and $\rho$ is at or beyond the positive root for $h$. Both derivative expectations in the second term are negative by strict concavity beyond the corresponding roots. Hence the left side is negative and the sum's reserve exceeds $a$. For $\delta=0$, write $\log(1+\rho(g+h))=\log A+\log B+\log(1-\rho^2gh/(AB))$. Applying $\log(1-x)\le-x$ and independence gives the upper bound $E\log A+E\log B-\rho^2E[g/A]E[h/B]<0$ by the same root and derivative signs. This is a property of independent gambles; offsetting dependent exposures can have much less combined riskiness.

Stochastic-dominance monotonicity follows by evaluating the increasing, strictly concave function $h_\delta(\cdot/R_\delta(g))$ on a dominated gamble. Under the paper's strict first-order dominance or nontrivial mean-preserving spread, the dominated gamble has negative transformed expectation and needs a higher reserve. If that trial reserve is outside the dominated gamble's loss domain, the maximum-loss bound already gives the ordering.

Proposition 3 additionally requires uniformly bounded payoffs, $g_n\to g$ in probability, and convergence of maximum losses $L(g_n)\to L(g)$. These assumptions give $R_\delta(g_n)\to R_\delta(g)$. The proof on supplement pp. 8–11 compares expected transformed payoffs at trial reserves separated from the loss boundary, where bounded convergence applies, and uses the unique crossing to bracket the roots. Tracking maximum loss matters: vanishing-probability disasters may disappear under convergence in probability while continuing to constrain required wealth. The appendix introduces an $L_0$ notation for the limiting loss and a maximum with $R_\delta(g)$, but the published proposition's maintained condition is $L_0=L(g)$; no unrestricted continuity under weak distributional approximation follows.

For a position of $\alpha$ units, homogeneity gives $R_\delta(\alpha g)=\alpha R_\delta(g)$. A reserve-based position constraint is therefore $\alpha\le W/R_\delta(g)$. This limits an exposure; it is not a first-order condition for maximizing expected utility or the Sharpe ratio. Cross-asset allocations still require a joint payoff distribution, portfolio constraints, and a chosen optimization objective.

## Theoretical qualifications and printed inconsistencies

The article’s Theorem 1 describes $R_\delta$ as a necessary and sufficient no-bankruptcy boundary for each $\delta\le0$. That interpretation needs correction under the original physical-probability no-bankruptcy criterion. Foster–Hart’s minimal threshold is $R_0$. For $\delta<0$, the more risk-averse utility requires $R_\delta>R_0$ for a nondegenerate gamble, but any homogeneous threshold lying between these two still guarantees no-bankruptcy in the Foster–Hart model. Consequently $R_\delta$ is a preference-dependent acceptance threshold and a sufficient conservative reserve; it is not generally the unique minimal reserve needed solely to avoid bankruptcy. This is a direct logical implication of the definitions and Foster–Hart theorem, not an official erratum.

The appendix proof does not repair the necessity claim. Appendix A's proof of Theorem 1 (supplement pp. 3–5) addresses sufficiency and also contains a gap in its chosen martingale argument. It defines utility increments

$$
Y_t=\frac{W_{t+1}^\delta-W_t^\delta}{\delta}
=W_t^\delta h_\delta(g_{t+1}/W_t)
$$

for an accepted gamble. Bounds (A13)–(A14) bound the normalized payoff term but retain the multiplier $W_t^\delta$. For $\delta<0$, that multiplier is unbounded as wealth approaches zero. Thus the asserted uniform bound on $Y_t$, and hence on the centered martingale increments, does not follow. A realized losing gamble can also make $Y_t<0$; the acceptance condition controls its conditional expectation, not its pathwise sign.

A direct alternative proves the valid sufficiency conclusion. For $\delta<0$, acceptance only when $W_t\ge R_\delta(g_{t+1})$ implies

$$
E\!\left[\left.(1+g_{t+1}/W_t)^\delta\right|\mathcal F_t\right]\le1.
$$

With positive initial wealth and admissible conditional gamble distributions, $Z_t=W_t^\delta$ is therefore a nonnegative supermartingale; rejection leaves it unchanged. Its finite initial expectation implies convergence to a finite limit almost surely. Since $W_t\to0$ would force $Z_t\to\infty$, bankruptcy in that sense has probability zero. This is an independently derived repair of sufficiency, not the appendix's printed proof, and it supplies no necessity result for the higher preference-dependent threshold. The $\delta=0$ case remains the Foster–Hart logarithmic result.

The article itself uses both strict and weak threshold language. Its early restatement uses $J>R$ for no-bankruptcy, whereas the original theorem uses $J\ge R$; strict inequality belongs to stronger sustained-growth conclusions in a shares setup. Retaining this distinction avoids turning asymptotic nonconvergence to zero into a positive wealth floor.

The introductory CRRA example on p. 2 prints $\delta=3.0813$ with utility $W^\delta/\delta$, while p. 3 gives $\delta^*=-2.0813$ and the rest of the paper defines $\theta=1-\delta$. The internally consistent interpretation is relative risk aversion $\theta=3.0813$, hence $\delta=-2.0813$. Under that interpretation the equiprobable $+120/-100$ gamble requires approximately 1,850 units of reserve, versus 600 at log utility. A positive exponent 3.0813 would instead describe convex utility and is inconsistent with the concavity argument.

Equations (7)–(8) describe the ratio $h_\delta(g/R)/\log(1+g/R)$ as a personalized probability-density change. This positive ratio is a useful weighting device, but as printed it is not normalized to have expectation one. A genuine density must divide it by its expectation. That normalization leaves the zero indifference equation unchanged, so the reserve computation survives; it does matter if interpreting the weights as probabilities. The value at a zero payoff is defined by continuity.

These qualifications do not invalidate computing the option-implied statistic or examining its empirical associations. They narrow the interpretation of those calculations. In particular, a reserve computed under risk-neutral probabilities does not automatically furnish a physical-world survival guarantee: the probability measure in the expected-utility or expected-log condition matters.

## Deriving the option-implied equation

Let current spot price be $S_0$, terminal price at maturity $\tau$ be $S_T$, and simple price return be $g=S_T/S_0-1$. Define $H_R(S)=h_\delta((S/S_0-1)/R)$. Its first derivative at $S_0$ is $1/(S_0R)$; its negative second derivative is

$$
f_R(K)=\frac{1-\delta}{(S_0R)^2}
\left(1+\frac{K/S_0-1}{R}\right)^{\delta-2}.
$$

The spanning identity in equation (16) expresses $H_R(S_T)$ as its value and tangent at $S_0$, plus integrals of terminal call and put payoffs weighted by $H_R''$. Under the pricing measure, discounting those payoffs converts them into option prices. In the source’s no-dividend carry formulation, $E^Q[S_T]=S_0(1+r_f)$, where $r_f$ is the simple risk-free return over the option horizon. Imposing $E^Q[H_R(S_T)]=0$ yields equations (18)–(19):

$$
\frac{r_f}{(1+r_f)R}
=\int_{S_0}^{\infty}f_R(K)C(S_0,K,\tau)\,dK
+\int_0^{S_0}f_R(K)P(S_0,K,\tau)\,dK.
$$

Both integrals depend on the unknown reserve, so it must be solved numerically. Units are consistent: option prices have currency units, $f_R$ has inverse currency-squared units when $R$ is expressed in return units, and integration over strike leaves a dimensionless result. This is equation (18) itself; the sentence introducing it calls $1+R$ the fixed point, which should not be taken as an instruction to add one to the computed root.

A practical implementation must specify the strike interpolation and extrapolation, quadrature, boundary behavior near zero price, and root tolerance. The theoretical formula uses a continuum of strikes over the entire positive price line. The dataset supplies a much narrower standardized delta range. “Model-free” here means that the spanning identity does not posit a parametric terminal return distribution; it does not eliminate the need to complete the unobserved option surface.

Dividends and American exercise require consistent handling. The paper’s OptionMetrics description says its pricing procedure accommodates discrete dividends or continuous dividend yield using a proprietary binomial-tree method. It does not provide a complete recipe for reconciling those adjusted prices with the simple carry term in the displayed theoretical equation. Reproduction should explicitly state whether returns include dividends and how the forward, discount factor, and European-equivalent prices are constructed.

Appendix B (supplement pp. 12–13) explicitly reproduces this simple-return spanning argument, including discounting and the kernel. The payoff must be defined on the relevant support: $R>1$ is a sufficient domain condition if terminal stock prices can approach zero and the integration is taken over the full positive price line. For $R<1$, an explicit lower support bound above $S_0(1-R)$ or another payoff extension is needed; finite quote coverage alone does not supply that economic assumption. At $R=1$, positivity holds for positive prices, but the relevant negative moments must still be integrable.

Appendix C (supplement p. 14) now makes the log-return construction inspectable. For $g=\log(S_T/S_0)$, set $z_R(K)=1+\log(K/S_0)/R$. Differentiating $h_\delta(\log(S/S_0)/R)$ gives the negative second derivative

$$
f_R^{\log}(K)=\frac{z_R(K)^{\delta-2}}{K^2}
\left[\frac{1-\delta}{R^2}+\frac{z_R(K)}{R}\right].
$$

This agrees with (C3) on its admissible domain. The derivative at $S_0$ is still $1/(RS_0)$, so the linear stock-payoff term produces the same simple-carry left side $r_f/[(1+r_f)R]$ in (C2). That step does not assume $E^Q[\log(S_T/S_0)]=r_f$.

The domain is consequential: $z_R(K)>0$ requires $K>S_0e^{-R}$. For every finite $R$, the displayed put integral from zero crosses that interior boundary. With a usual positive price distribution having support arbitrarily close to zero, the transformed payoff is not defined on part of the support, and the kernel is singular at the boundary. Even at integer $\delta=-2$, algebraically extending powers through negative arguments does not restore positive wealth or remove the singularity. A bounded log-loss model with a specified positive lower stock-price bound, or an explicitly altered payoff with its own spanning formula, is needed. The supplement supplies neither a support rule nor a tail treatment resolving this issue. Its statement that simple- and log-return empirical results are similar does not validate the unrestricted formula. This is a derived domain qualification, not an announced author correction.

## Data, observation timing, and outcome construction

The main sample is January 1996 through September 2008. Option data come from the OptionMetrics Volatility Surface, which provides daily kernel-smoothed standardized implied volatilities and prices. Surfaces for calls and puts are computed separately, using contemporaneous quotes; the article says no forward information enters the daily interpolation. Month-end observations use maturities 30, 91, 182, and 365 days, referred to as one, three, six, and twelve months.

Out-of-the-money calls have deltas 0.20–0.50, puts have deltas $-0.20$ to $-0.50$, and the at-the-money reference deltas are 0.50 and $-0.50$. A standardized option is included only when enough underlying quote data exist. Stock returns come from CRSP, and the three-month Treasury-bill rate proxies the risk-free rate. The exact monthly cross-section sizes, identifier mapping, share-code and exchange filters, delisting treatment, bid–ask screens, and surface-tail completion rules are not given in the local article.

The dependent variable is excess return divided by realized volatility. The source uses both average and cumulative holding-period returns over windows of one, three, six, and twelve months. Its equation (20) defines realized volatility as

$$
\sigma_{i,t}=\left[\sum_{d=1}^{D_t}(r_{i,d}-\bar r_i)^2\right]^{1/2}.
$$

There is no divisor $D_t$ or $D_t-1$ in this printed expression. It is therefore an accumulated volatility scale rather than the ordinary sample standard deviation of daily returns. A replication must not silently substitute the latter: it changes levels of return-to-risk ratios, comparisons across windows, and regression slopes. Units of average returns, holding-period returns, and the Treasury-bill rate must likewise be aligned explicitly.

Timing is a material unresolved source ambiguity. Equation (26) and table notes regress a variable labeled $t+1$ on the option-implied measure at $t$, and repeatedly call it “one-month-ahead.” The same notes construct that $t+1$ ratio using the past one, three, six, or twelve months of daily data. The prose also calls the results forecasts one, three, six, and twelve months ahead. These are different designs: a trailing twelve-month ratio measured one month later overlaps almost entirely with information available at formation, while a forward twelve-month return does not. The local article does not resolve this with explicit start/end dates. Its results below are therefore reported under the table labels, without asserting that every column is a clean forward holding-period backtest.

## Main cross-sectional evidence

Each month, the authors run a Fama–MacBeth cross-sectional regression of the reported risk-adjusted return on $R^Q_{\delta,i,t}$ and average the monthly coefficients. Newey–West $t$ statistics and Hodrick $p$ values are reported. The local article does not state the exact lag choices or provide replication code for their treatment of overlapping windows.

Table 1 gives these slopes, with Newey–West statistics in parentheses:

| Horizon label | Average-return ratio | Holding-period-return ratio |
|---|---:|---:|
| 1 month | $-0.0131$ ($-3.41$) | $-0.0131$ ($-3.41$) |
| 3 months | $-0.0049$ ($-3.21$) | $-0.0201$ ($-2.62$) |
| 6 months | $-0.0181$ ($-2.82$) | $-0.0335$ ($-2.29$) |
| 12 months | $-0.0215$ ($-2.21$) | $-0.0049$ ($-1.86$) |

The last holding-period slope is the number printed in Table 1; nearby prose gives a range extending to $-0.0490$, which is inconsistent with that cell. The table’s twelve-month holding-period Hodrick $p$ value is 5.16%, so describing every specification as significant at 5% would overstate the result.

Quintiles are sorted monthly on implied riskiness. In Table 2, the lowest-riskiness quintile has average-return ratios 0.1033, 0.1035, 0.1019, and 0.1021 across the four horizons; the highest-riskiness quintile has $-0.0492$, $-0.0492$, $-0.0430$, and $-0.0218$. The ordered quintiles decline monotonically in all four columns. High-minus-low spreads are $-0.1525$, $-0.1527$, $-0.1449$, and $-0.1239$, with $t$ statistics $-3.72$, $-3.72$, $-3.40$, and $-2.98$.

For holding-period-return ratios, the high-minus-low spreads are $-0.1525$, $-0.2471$, $-0.3277$, and $-0.4011$, with corresponding statistics $-3.72$, $-3.71$, $-3.67$, and $-3.90$. These are differences between reported ratios, not percentage monthly returns on a self-financing long–short portfolio. In particular, subtracting two asset-level Sharpe-like ratios does not equal the Sharpe ratio of their long–short combination.

Controls in Section 6.4 include an option-volatility smirk measure,

$$
QSKEW=IV_{\mathrm{OTM\ put}}-\frac{1}{2}(IV_{\mathrm{ATM\ call}}+IV_{\mathrm{ATM\ put}}),
$$

and 1% or 5% historical VaR and expected shortfall estimated from the preceding year’s daily returns. VaR and ES are not included together because of high cross-sectional correlation. Table 3 runs one- and three-month specifications with skewness and one downside-risk variable. The implied-riskiness slopes remain negative in every displayed specification. For example, controlling for skewness and 1% VaR gives one-month slope $-0.0075$ ($t=-2.91$) and three-month slope $-0.0100$ ($t=-3.33$); controlling for skewness and 1% ES gives $-0.0090$ ($t=-3.33$) and $-0.0116$ ($t=-3.58$). This supports incremental association beyond those particular controls, not independence from all known equity characteristics.

## Historical benchmark, approximation failure, and the riskiness premium

The historical comparator is not computed from the exact empirical expected-utility equation. Section 7 approximates it through a third-order Taylor expansion around the mean. Write $\mu=E[g]$, $v=\operatorname{Var}(g)$, $m_3=E[(g-\mu)^3]$, and $T_R(g)=h_\delta(g/R)$. The estimated physical reserve solves

$$
0\approx T_R(\mu)+\frac{v}{2}T_R''(\mu)+\frac{m_3}{6}T_R'''(\mu),
$$

where

$$
T_R''(\mu)=\frac{\delta-1}{R^2}(1+\mu/R)^{\delta-2},\qquad
T_R'''(\mu)=\frac{(\delta-1)(\delta-2)}{R^3}(1+\mu/R)^{\delta-3}.
$$

The mean, standard deviation, and skewness are estimated from daily returns over the preceding one, three, six, and twelve months; $\delta=-2$. This comparator combines sampling error in moments with truncation error in the nonlinear expansion. Its weaker performance cannot be attributed solely to the physical versus risk-neutral probability measure.

Table 4’s average-return-ratio slopes are $-0.2055$, $-0.0553$, $-0.1426$, and 0.0216, with $t$ statistics $-0.54$, $-0.19$, $-0.51$, and 0.14. Table 5’s physical-riskiness quintile spreads are also weak: for average-return ratios, high-minus-low values are $-0.0186$, $-0.0004$, 0.0121, and 0.0075, with statistics $-1.30$, $-0.03$, 0.92, and 0.53. The quintiles do not exhibit a stable monotone ranking.

Negative sample means sometimes produce negative approximate “physical riskiness,” as Figure 3 visibly shows. Such values violate the original positive-mean domain and positive-reserve interpretation. They are outputs of the approximation outside its admissible theoretical setting; they should not be interpreted as negative capital requirements. For an exact concave-utility equation with nonpositive expected payoff, a favorable finite positive reserve need not exist.

The paper responds with a positive expected market-return assumption of 6% annually and, for individual stocks, a CAPM-implied mean $E[R_i]=r_f+\beta_i(E[R_m]-r_f)$, with beta estimated over matching historical windows. The text alternates between calling the 6% assumption an expected return and a market risk premium. A replication must settle that distinction, annual-to-daily conversion, and treatment of negative estimated betas. The retrieved supplementary Tables II–IV now permit inspection of those tests. They show several significant individual specifications, but no uniformly significant physical-riskiness relation across the four horizons; the complete slope and spread comparisons are reported below.

The riskiness premium is the difference $R^Q-R^P$. Table 6 reports average-return-ratio high-minus-low quintile spreads of $-0.1327$, $-0.1476$, $-0.1180$, and $-0.0848$, with statistics $-3.64$, $-3.71$, $-3.76$, and $-3.35$. Holding-period-ratio spreads are $-0.1327$, $-0.2043$, $-0.2573$, and $-0.2181$, with statistics $-3.64$, $-3.76$, $-4.02$, and $-3.23$. This difference is predictive in the reported design, but because the two measures use different numerical constructions and estimated means, it is only loosely interpretable as a pure price of risk.

## How the supplement estimates risk aversion

Section II of the supplement (PDF pp. 15–17, Table I on p. 21) provides the empirical justification for setting $\theta$ near three and $\delta$ near minus two. The motivating Merton relation is $E_t[r^e_{m,t+1}]=\theta E_t[\sigma^2_{m,t+1}]$ when intertemporal hedging demands are sufficiently small. The estimated specification includes an intercept and a GARCH(1,1) conditional variance:

$$
r^e_{m,t+1}=\omega+\theta v_{t+1}+\varepsilon_{t+1},
\qquad
v_{t+1}=\gamma_0+\gamma_1\varepsilon_t^2+\gamma_2v_t.
$$

Here $v_{t+1}$ is known at time $t$, and $E_t[\varepsilon_{t+1}^2]=v_{t+1}$. The four market proxies are the value-weighted NYSE/AMEX/NASDAQ index, the NYSE index, the S&P 500, and the Dow Jones Industrial Average. The common estimation sample runs from July 1, 1963 through December 31, 2009, with 11,707 daily observations. These are separate aggregate-market time-series fits, not monthly estimates of each optionable stock's preference parameter.

The appendix reports maximum-likelihood estimates and Bollerslev–Wooldridge robust $t$ statistics. Its full parameter estimates are:

| Market proxy | $\omega$ | $\theta$ (robust $t$) | $\gamma_0$ | $\gamma_1$ | $\gamma_2$ |
|---|---:|---:|---:|---:|---:|
| NYSE/AMEX/NASDAQ | 0.00028 | 3.0882 (2.53) | $6.70\times10^{-7}$ | 0.0856 | 0.9096 |
| NYSE | 0.00027 | 3.1482 (2.52) | $6.43\times10^{-7}$ | 0.0833 | 0.9121 |
| S&P 500 | 0.00010 | 3.0520 (2.63) | $5.08\times10^{-7}$ | 0.0744 | 0.9232 |
| Dow Jones | 0.00006 | 3.1692 (2.43) | $7.55\times10^{-7}$ | 0.0700 | 0.9243 |

The variance persistence sums range from 0.9943 to 0.9976. Conditional variance is consequently persistent, and initialization can matter. Approximate standard errors inferred as estimate divided by reported $t$ are 1.22, 1.25, 1.16, and 1.30 for $\theta$, respectively. Thus the results support positive aggregate slopes while leaving considerable uncertainty about their magnitude. The conversion $\delta=1-\theta$ produces approximately $-2.05$ to $-2.17$; setting $\delta=-2$ is a rounded preference calibration.

For implementation, residuals and the variance recursion must be updated jointly as parameters change. A Gaussian quasi-likelihood implementation would minimize

$$
\frac12\sum_t\left[\log v_t+
\frac{(r^e_{m,t}-\omega-\theta v_t)^2}{v_t}\right].
$$

That displayed objective is a reconstruction of a conventional implementation, not an objective explicitly printed in the appendix. Such an implementation should impose positivity of conditional variance, document the initial $v_t$ and residual, and specify whether a stationary-variance restriction $\gamma_1+\gamma_2<1$ is enforced. The supplement does not identify the innovation likelihood, initialization, numerical optimizer, convergence tolerances, parameter constraints, or exact daily cash-rate construction. Robust standard errors do not eliminate these missing replication inputs.

The authors compare $252\theta\sigma^2$, using empirical daily market volatility of approximately 0.96%–1.00%, with the sample's roughly 6% annual excess return. Their estimate is approximately 7% annually; using the extremes of the reported ranges gives approximately 7.08%–7.99%. This checks the scale of the variance-linked component, not the full fitted mean when $\omega\ne0$. In particular, the first row's intercept alone annualizes arithmetically to $252(0.00028)=7.056\%$. Omitting it when interpreting the fitted expected premium is consequential. The note does not claim the fitted total mean equals the observed 6% excess return.

Interpreting $\theta$ as structural relative risk aversion additionally requires the maintained Merton restrictions and a suitable market proxy. A positive GARCH-in-mean coefficient is not by itself identification of preferences independent of changing investment opportunities. The estimation sample also extends through 2009, beyond the 1996–2008 stock-ranking sample. The fixed $\delta=-2$ exercise is a full-sample calibration, not evidence that a real-time investor estimated that parameter using only information available at each historical formation date.

## Supplementary tests with CAPM-implied physical means

Section III and Tables II–IV replace each stock's noisy sample mean by the CAPM-implied mean described above while retaining the moment approximation to the physical reserve. They do not replace it with an exact solution of the empirical expected-utility equation. The stock-ranking panel remains January 1996–September 2008. The captions again label the dependent variable one-month-ahead while constructing return and volatility measures from “past” windows, so the supplement does not resolve the timing ambiguity in the main article.

Table II reports the following average Fama–MacBeth slopes and Newey–West statistics:

| Horizon label | Average-return-ratio slope ($t$) | Holding-period-ratio slope ($t$) |
|---|---:|---:|
| 1 month | $-6.9331$ ($-3.84$) | $-6.9331$ ($-3.84$) |
| 3 months | $-0.1179$ ($-0.97$) | $-0.1584$ ($-1.20$) |
| 6 months | $-0.1896$ ($-1.39$) | $-0.2652$ ($-1.93$) |
| 12 months | $-0.2772$ ($-2.10$) | $-0.2994$ ($-1.62$) |

Every slope is negative, but significance is concentrated in the one-month columns and the twelve-month average-return column. The unusually large one-month coefficient is the printed estimate, not a decimal adjustment. Its magnitude depends on the units and cross-sectional scale of the constructed physical reserve; it cannot be compared directly with the option-implied slope as an economic effect without normalizing the predictors. No scale-normalized effect or multiple-testing adjustment is supplied.

Tables III and IV give these high-minus-low quintile differences, still in return-per-risk units rather than tradable portfolio returns:

| Sort characteristic | Outcome convention | 1 month | 3 months | 6 months | 12 months |
|---|---|---:|---:|---:|---:|
| Alternative $R^P$ | Average return | $-0.0546$ ($-3.20$) | $-0.0177$ ($-1.47$) | $-0.0263$ ($-2.11$) | $-0.0277$ ($-1.97$) |
| Alternative $R^P$ | Holding-period return | $-0.0546$ ($-3.20$) | $-0.0149$ ($-0.85$) | $-0.0427$ ($-2.01$) | $-0.0341$ ($-1.84$) |
| $R^Q-R^P$ using alternative $R^P$ | Average return | $-0.0664$ ($-2.50$) | $-0.1045$ ($-3.57$) | $-0.0501$ ($-2.39$) | $-0.0274$ ($-1.52$) |
| $R^Q-R^P$ using alternative $R^P$ | Holding-period return | $-0.0664$ ($-2.50$) | $-0.1140$ ($-3.16$) | $-0.1337$ ($-2.99$) | $-0.1427$ ($-2.90$) |

The alternative physical measure produces stronger evidence than the original sample-mean comparator, especially at one and six months, but not uniform significance. The twelve-month average-return spread has $t=-1.97$, just beyond a nominal two-sided normal 5% cutoff, even though the accompanying prose groups that horizon with the weak results. It is more precise to describe it as borderline and convention-dependent than to declare all twelve-month results insignificant.

The premium's eight spreads are negative, but its twelve-month average-return result, $t=-1.52$, is an explicit exception to statistical significance. The appendix's footnote acknowledges that exception. Nor are these supplementary quintile profiles monotone. For example, Table III's one-month average-return ratios are $0.0413,0.0798,0.0399,0.0320,-0.0133$: quintile two exceeds quintile one. Table IV's corresponding sequence is $0.0338,0.0649,0.0653,0.0599,-0.0326$, with the middle quintiles above the low-premium quintile. Negative endpoint spreads therefore do not establish a steadily declining relation throughout the cross-section.

Supplement Figures 1–3 reproduce the preference-scaled allocation, option-implied comparison, and unstable sample-mean physical riskiness plots. Figure 4 illustrates the positive-mean alternative. Its caption claims January 1996–September 2008, while the displayed axes stop at December 2000; Section III's prose instead refers to a December 2008 endpoint. Those inconsistent labels should be retained as a source limitation, not repaired by inventing unshown plot observations. The full dated series and code would be necessary to reconcile the graphic with the stated sample.

## What an implementable extension would need

Figures 1–2 use S&P 500 options to contrast $\delta=0$ and $\delta=-2$. The plotted relative allocation is the ratio $R^Q_0/R^Q_{-2}$ and lies roughly between 33% and 38%, depending on horizon and date. That ratio scales an exposure normalized by the log-utility reserve. It is not, without a stated wealth normalization, an independently optimized share of total household wealth. The paper supplies neither an optimal multi-asset allocation nor realized net returns from trading this time series.

A faithful replication should preserve the reported monthly panel and compute both exact and approximate physical reserves, tagging observations outside the admissible domain. It should log convergence failures and quote coverage; show how omitted strikes contribute to the option integrals; and compare the results under explicit dividend and carry conventions. The return test then needs an unambiguous formation date, a disjoint forward evaluation interval, and a documented choice between the printed accumulated-volatility denominator and a sample standard deviation. Each choice can materially change the published ratios.

A separate investment test would require portfolio weights, rebalancing rules, overlapping-horizon treatment, financing, stock-borrow availability, delisting returns, turnover, and transaction costs. The source does not report these or a net-of-cost performance benchmark. It supports further investigation of option-implied riskiness as a stock-ranking characteristic, while the survival interpretation, moment-approximation domain, and timing of the predictive experiment require more care than the article’s broad summary claims suggest.

## Supplement verification and remaining gaps

The main article and the separate online appendix have now both been read in full. All 28 supplement pages, including the proofs, references, four tables, and four figures, were inspected as text, with critical proof, option-kernel, estimation, table, and figure pages visually checked. The appendix resolves the earlier missing-source limitation; it does not supply the original stock/option panel, estimation code, complete option-tail rules, or an unambiguous forward-return calendar. The sufficiency repair, loss-domain qualifications, inferred parameter standard errors, and arithmetic checks in this note are explicitly derived analysis rather than author-issued corrections.
