# Volatility of the Stochastic Discount Factor, and the Distinction between Risk-Neutral and Objective Probability Measures

**Gurdip Bakshi, Zhiwu Chen, and Erik Hjalmarsson. October 5, 2004 working paper.** Source: [StochasticDiscount_BakshiChenHjalmarsson_2004.pdf](../../Finance/StochasticDiscount_BakshiChenHjalmarsson_2004.pdf). The 23-page local document contains a title page, abstract, 16 numbered main-text pages, two reference pages, and three figure/caption pages. All were inspected. There is no separate appendix in this version. Page references below use printed main-text numbering; Figure 2 is on PDF page 23. This note describes this working-paper version without assuming later publication changes.

## Why this matters

An option-implied distribution is a risk-neutral distribution, not a forecast distribution. Equivalent probability measures agree on which events are impossible, but can disagree sharply about probabilities of rare losses. The paper asks for a quantitative connection between that discrepancy and the stochastic discount factor (SDF) used to price cash flows.

Its central result is elementary but useful: after fixing the objective measure and the risk-free discount factor, the square-integrable likelihood ratio of a risk-neutral measure has distance from one equal to the coefficient of variation of its SDF. Equivalently, a discounted version of that distance equals the SDF's standard deviation. This supplies a probability-measure interpretation of Hansen–Jagannathan volatility bounds. A model that cannot generate enough SDF volatility also cannot generate enough separation, in this particular likelihood-ratio norm, between objective and pricing probabilities to explain the asset-return moments.

The empirical exercise uses only monthly stock-index and short Treasury returns to estimate a lower bound on this separation. Its attraction is that it does not require an option-pricing model, an option surface, or estimated investor preferences. Its cost is partial identification: a moving lower bound need not mean that the actual distance moves. The authors explicitly acknowledge that caveat despite stronger wording in the abstract about a post-1987 widening.

Three distinctions guide interpretation. The SDF's standard deviation is equal to an $L^2$ likelihood-ratio distance, not to total variation. A lower bound for the $L^2$ distance is not automatically a lower bound for total variation. And the distance concerns the underlying state-space measure; a marginal distribution of the stock return need not reveal all the state-price variation in an incomplete market. These are mathematical implications of the definitions, not additional empirical findings.

## Economic environment and admissible measures

Work on a probability space $(\Omega,\mathcal F,P)$, where $P$ is the common objective probability measure. Payoffs belong to $L^2(P)$, with norm $\|x\|_2=(E_P[x^2])^{1/2}$. There are finitely many traded securities with payoff vector $X=(x_1,\ldots,x_N)'$ and price vector $q$. Their linear span $M$ is the set of marketed payoffs. Short positions and linear portfolio combinations are allowed; the model is frictionless.

For a marketed payoff $x$, the price is the minimum cost of a portfolio producing it:

$$
\pi[x]=\min_{a\in\mathbb R^N}a'q
\quad\text{subject to}\quad a'X=x.
$$

Under absence of arbitrage the cost is consistent across replicating portfolios. Nonnegative payoffs that are positive with positive probability have strictly positive prices. The paper assumes the relevant no-arbitrage representation by a strictly positive square-integrable discount factor $d$:

$$
\pi[x]=E_P[dx],\qquad x\in M,\qquad d>0\ P\text{-a.s.}
$$

A risk-free security has gross return $R_f=1+r_0>0$, so its pricing equation fixes $\bar d=E_P[d]=1/R_f$. Define $\mathcal D$ as all positive $L^2(P)$ discount factors pricing the marketed assets. Markets need not be complete; $\mathcal D$ may have many members.

For each such $d$, set

$$
\rho=\frac{d}{\bar d}=R_fd,
\qquad
Q(A)=E_P[\rho\mathbf1_A],
\qquad
\frac{dQ}{dP}=\rho.
$$

Since $\rho>0$ almost surely and $E_P[\rho]=1$, $Q$ is a probability measure equivalent to $P$. Asset prices become $\pi[x]=R_f^{-1}E_Q[x]$. Conversely, an equivalent pricing measure with a square-integrable density relative to $P$ yields $d=R_f^{-1}dQ/dP$. This is a one-to-one correspondence between individual admissible kernels and measures. It is not uniqueness of the market's pricing measure.

The integrability qualification matters in infinite state spaces. Absolute continuity by itself gives an integrable Radon–Nikodym derivative, not necessarily one in $L^2$. The paper's proof says that the Radon–Nikodym theorem gives an $L^2$ density; read that as requiring its stated square-integrable pricing-kernel framework. Otherwise the $L^2$ distance may be infinite and the Hilbert-space calculations cannot be used as finite equalities.

There is also a visible typographical error in equation (14): the printed $Q(A)\equiv E(\mathbf1_A)$ omits $\rho$, whereas the adjacent integral is $\int_A\rho\,dP$. The correct expectation is the one above. Without the density, the proposed definition would simply reproduce $P$.

## The distance identity and its proof

The paper first defines the unhalved absolute distance

$$
\Delta(P,Q)=\int|dQ-dP|=E_P[|\rho-1|].
$$

This is twice the common probability-theory convention for total variation, $\operatorname{TV}(P,Q)=\sup_A|Q(A)-P(A)|$. In a finite state space it equals $\sum_s|q_s-p_s|$. Define its discounted counterpart $\delta_1=\Delta/R_f$ and the second distance

$$
\delta_2(P,Q)=\left\|d-\frac1{R_f}\right\|_2.
$$

Then Theorem 2 (pp. 5–7) states

$$
\delta_1=E_P[|d-\bar d|]
\le\left(E_P[(d-\bar d)^2]\right)^{1/2}
=\delta_2=\operatorname{sd}_P(d).
$$

The first equality substitutes the likelihood ratio. The inequality is Cauchy–Schwarz or Hölder on a probability space. The final equality uses the risk-free pricing equation. Thus the scaled separation is

$$
D(P,Q):=R_f\delta_2
=\sqrt{E_P[(\rho-1)^2]}
=\frac{\operatorname{sd}_P(d)}{E_P[d]}.
$$

In modern divergence notation its square is the Pearson chi-square divergence $\chi^2(Q\Vert P)$. That identification is a mathematical reformulation for clarity. It emphasizes that the reference measure is $P$: generally $\chi^2(Q\Vert P)\ne\chi^2(P\Vert Q)$. The paper uses “distance metric” informally; this likelihood-ratio expression should not be confused with a symmetric metric on arbitrary pairs of probability measures. With a fixed reference measure, the norm of differences of densities is an ordinary $L^2(P)$ norm.

Both distances vanish exactly when $Q=P$, equivalently when $d$ is constant at $1/R_f$. The condition needed for the normalization is $R_f>0$; a strictly positive net interest rate is unnecessary. A zero or mildly negative net rate does not invalidate the identity. The unscaled absolute distance is bounded by 2, while $D$ can be arbitrarily large when a pricing density puts substantial weight on sufficiently rare objective events.

The inequality $\delta_1\le\delta_2$ has only one direction. A large $\delta_2$ does not force a proportionately large $\delta_1$, because rare, very large likelihood ratios can dominate a second moment. Therefore a lower bound on SDF volatility cannot be relabeled a lower bound on total variation. Nor do the two norms necessarily rank candidate kernels in the same order. The paper suggests similar rankings in many applications, but provides no general ordering theorem.

In a finite-state implementation, start with positive state probabilities $p_s$ and a positive pricing vector $d_s$ satisfying $\sum_sp_sd_s=1/R_f$. Compute $q_s=R_fp_sd_s$, check $\sum_sq_s=1$, then calculate $\Delta=\sum_s|q_s-p_s|$ and $D^2=\sum_s(q_s-p_s)^2/p_s$. This directly verifies the theorem. For example, with two equally likely states and $d_s=\bar d(1\pm a)$, $0<a<1$, one gets $D=|a|$ and $\Delta=|a|$. That is an illustrative calculation, not a data result from the paper.

## Pricing-operator interpretation and incomplete markets

Extend a selected pricing functional to all square-integrable payoffs by $\bar\pi[x]=E_P[dx]$. Compare it with discounting objective expected payoffs at the risk-free rate. For any $x$,

$$
\left|\bar\pi[x]-\bar d E_P[x]\right|
=|E_P[x(d-\bar d)]|
\le\|x\|_2\,\operatorname{sd}(d).
$$

For $\|x\|_2=1$, the upper bound is attained by $x=(d-\bar d)/\operatorname{sd}(d)$ when the denominator is nonzero. Consequently,

$$
\sup_{x\in L^2(P),\ \|x\|_2=1}
|\bar\pi[x]-\bar d E_P[x]|=\delta_2.
$$

The distance is the largest pricing error over unit-root-mean-square payoffs caused by treating objective probabilities as pricing probabilities. Normalization by the payoff norm is essential: without it, arbitrary leverage makes the supremum unbounded.

The maximizing payoff may not be traded. Restricting the supremum to $M$ gives only a lower bound, valid for every admissible kernel. Incomplete markets leave components of the kernel orthogonal to traded payoffs unidentified. Adding such components can change its total variance without changing observed asset prices. This explains economically why a few return series identify a bound rather than the full measure distance.

The paper writes a minimum over strictly positive kernels. On a nonclosed strictly positive set, a minimum need not be attained; an infimum is the safe general formulation. This does not change the practical lower-bound inequality. If the optimizer lies at zero in some states, it is a nonnegative limiting kernel rather than a strictly positive equivalent-measure density.

For two positive kernels with the same mean, the paper also obtains

$$
\Delta(Q_1,Q_2)
=E_P\left|\frac{d_1}{E[d_1]}-\frac{d_2}{E[d_2]}\right|
\le\frac{\|d_1-d_2\|_2}{E[d_1]}.
$$

The equal-mean restriction is important. It aligns the risk-free discounting normalizations before comparing pricing densities. This links SDF-distance diagnostics to discrepancies between induced probability measures but does not assert equality between absolute and mean-square distances.

## Hansen–Jagannathan bound with consistent scaling

Let $\mu_X=E[X]$ and let $\Sigma_X=\operatorname{Var}(X)$ be nonsingular for a chosen vector of risky payoffs. Fix $\bar d=1/R_f$. Since $\operatorname{Cov}(X,d)=q-\bar d\mu_X$, linear projection of $d-\bar d$ onto centered payoffs gives

$$
\operatorname{Var}(d)
\ge(q-\bar d\mu_X)'\Sigma_X^{-1}(q-\bar d\mu_X).
$$

Thus

$$
\delta_2\ge B_d:=\sqrt{(q-\bar d\mu_X)'\Sigma_X^{-1}(q-\bar d\mu_X)},
\qquad D\ge R_fB_d.
$$

The projection argument is constructive. A candidate minimum-variance kernel without positivity restrictions is

$$
d_{\mathrm{lin}}=\bar d+(q-\bar d\mu_X)'\Sigma_X^{-1}(X-\mu_X).
$$

It prices the chosen payoffs and achieves the variance bound. It may be negative in some states, so the bound need not be attainable within strictly positive kernels. Enforcing nonnegativity can tighten it. The authors do not use the positivity refinement in the empirical exercise, arguing that prior stock-data applications found its effect small.

There is a scaling omission in the printed equation (32). After announcing multiplication of both sides of (30) by $R_f$, the left becomes $R_f\delta_2$ but the right still displays $B_d$ rather than $R_fB_d$. The equations above carry the multiplication through consistently. If $R_f\ge1$, the printed inequality can still be a weaker consequence, but it is not the stated rescaling and is not generally equivalent. Also, the accompanying prose calls $\Sigma_X^{-1}$ a covariance matrix; it is the inverse covariance.

A constant risk-free payoff makes the covariance matrix singular if included directly. Use its equation to fix $\bar d$ and apply the inverse to risky payoffs, or explicitly use the appropriate generalized-inverse/projection formulation. Do not invert a matrix containing an exact constant row. This qualification makes the displayed mathematical setup implementable.

With one stock-index gross return $R$ priced at one, the consistently scaled bound is

$$
D\ge\frac{|E[R]-R_f|}{\operatorname{sd}(R)}.
$$

For simple stock return $r$, it is $|E[r]-r_0|/\operatorname{sd}(r)$: the absolute Sharpe ratio under a constant risk-free rate. A negative mean excess return still produces a nonnegative bound. This scalar reduction is what makes the empirical exercise possible using index and Treasury returns alone. It bounds the SDF coefficient of variation, not an event probability or a stock-return volatility.

## Power-utility example and numerical implications

Section 3.2 uses a representative-agent endowment model solely as an illustration. Let $u(c)=c^{1-\gamma}/(1-\gamma)$, subjective discount factor $\beta$, and log consumption growth

$$
Y=\log(c_{t+1}/c_t)
\sim N\left(\log\mu_c-\frac12\sigma_c^2,\sigma_c^2\right).
$$

Then $d=\beta e^{-\gamma Y}$ is lognormal. Its mean is

$$
E[d]=\beta\mu_c^{-\gamma}
\exp\left[\frac12\gamma(1+\gamma)\sigma_c^2\right],
$$

and its variance is this mean squared times $e^{\gamma^2\sigma_c^2}-1$. The risk-free rate is endogenous through $R_f^{-1}=E[d]$. Normalizing removes $\beta$ and $\mu_c$:

$$
D=\sqrt{e^{\gamma^2\sigma_c^2}-1}.
$$

Figure 1 plots this expression for $\gamma$ from 0 to 30 and annual consumption-growth standard deviations of 0.5%, 1%, 2%, 3%, and 4%. At $\gamma=30$, the formula gives approximately 0.151, 0.307, 0.658, 1.117, and 1.795, matching the rendered curves. These are calculated values from the illustrative formula, not empirical estimates of consumption risk or preferences. For small $\gamma\sigma_c$, the first-order approximation is $D\approx|\gamma|\sigma_c$.

The corresponding risk-neutral distribution of $Y$ remains Gaussian, with the same variance and mean shifted down by $\gamma\sigma_c^2$. The likelihood ratio is an exponential tilt. Thus increasing SDF volatility here changes the first moment of consumption growth without changing its skewness or kurtosis. The example cannot by itself generate a risk-neutral left tail of a different shape. Richer kernels or non-Gaussian objective distributions are needed for that mechanism.

The equity-premium puzzle obtains a new description: with smooth aggregate consumption and moderate risk aversion, $D$ is too small to match the return-implied bound. A more volatile consumption proxy raises $D$, but choosing such a proxy does not by itself establish that it is the correct representative-agent consumption aggregate. The paper provides no estimated preference parameters, welfare test, or structural model selection in this section.

## Empirical pipeline and exact window timing

Section 4 uses 936 monthly observations, January 1926–December 2003, for S&P 500 returns and a CRSP 30-day Treasury return series, called Treasury bonds in the source. The Treasury series proxies for the monthly risk-free rate. The PDF does not specify CRSP series identifiers, whether the equity series includes dividends, historical index reconstruction details, missing-observation handling, or the sample-standard-deviation divisor. These choices must be documented in a reproduction; silently substituting a price-only modern index is not justified.

For each prescribed window, compute the arithmetic mean stock return $\bar r$, mean Treasury return $\bar r_f$, and standard deviation $s_r$ of stock returns. The scalar, consistently normalized reconstruction is $\widehat B=|\bar r-\bar r_f|/s_r$. The paper describes using stock-return standard deviations, not the standard deviation of realized excess returns. They coincide only for constant Treasury returns. Averaging a time-varying risk-free rate is an empirical approximation to the one-period constant-$R_f$ bound, not an exact conditional-SDF calculation.

Figure 2 has three schedules:

1. Nonoverlapping windows 1926–1935, 1936–1945, 1946–1955, 1956–1965, 1966–1975, 1976–1985, 1986–1995, and the final eight-year window 1996–2003.
2. The same initial five decades, followed by 1976–1986, 1988–1997, and 1998–2003. All 1987 observations are excluded from this schedule; the final window has six years.
3. Ten-year windows advanced one calendar year at a time, starting at 1926–1935 and ending at 1994–2003.

The plotted date is the **start** of the window. An observation plotted at 1988 uses the following decade, 1988–1997. It was not observable to an investor in 1988 and is not a backward-looking contemporaneous risk indicator. The vertical 1987 line marks the event year, while nearby points can contain returns from many later years. Adjacent rolling points share nine years of data and are strongly dependent.

Every panel also shows a dotted bound computed from the full 78-year sample. That is a pooled-moment calculation, not an arithmetic average of the window bounds. The monthly units remain monthly: Figure 1 uses annual illustrative parameters and cannot be compared directly without a model for aggregation. Multiplying a Sharpe-style statistic by $\sqrt{12}$ would require appropriate independence/stationarity assumptions and would still not recover an arbitrary annual SDF divergence.

## What the figures actually show

The source supplies graphs rather than a numerical table. Visual readings from the rendered Figure 2 are approximate: the pooled monthly bound is around 0.06; the first schedule reaches roughly 0.20 in 1946–1955 and about 0.12–0.13 in 1986–1995. The crash-aligned schedule has a much larger bound, around 0.22, for 1988–1997, compared with roughly 0.03 for 1976–1986. Its final six-year period is close to 0.01. These should not be quoted as machine-precision observations.

The rolling panel reaches around 0.28 in some windows starting in the late 1940s and around 0.22–0.23 in windows starting just after 1987. It declines again toward the final available windows. The early 1930s have a small bound, so the 1929 crash does not produce an analogous pattern in this statistic. Long stretches of large and small bounds alternate across the sample.

The arbitrary-decade evidence for a 1987 shift is described as weak by the authors; the schedule explicitly excluding 1987 makes the difference more pronounced. This is consistent with a mechanical property of the estimator: excluding a large negative stock return can raise the average premium and reduce volatility. The figure therefore does not isolate a causal change in risk preferences. It changes the estimation sample at the same time as it compares alleged regimes.

No confidence bands, standard errors, formal structural-break test, or p-values are supplied. The abstract's “significant increase” should consequently be read as a substantive graphical claim, not a demonstrated statistical significance level. A bootstrap or heteroskedasticity/autocorrelation-robust delta-method analysis would be an extension, not a replication of reported inference. It would also need to account for overlapping windows and the data-dependent interest in 1987.

## What can and cannot be concluded

The theory identifies exactly how a positive square-integrable kernel induces pricing probabilities and how its volatility measures an $L^2$ discrepancy from objective probabilities. The observed assets constrain this discrepancy through their covariance with the kernel. They do not identify the full kernel, the objective state distribution, the risk-neutral return density, or the probability of a crash.

A rise in a lower bound from, say, 0.03 to 0.22 is compatible with an unchanged actual distance of 0.50 in both periods. It is also compatible with increases or decreases in the actual distance above the changing bounds. The authors state this explicitly in the main text. An inference that crash fears increased, then dissipated, is therefore an economic interpretation consistent with the figures and prior option literature, not an identified result of this return-only experiment.

The “model-free” claim has a limited and useful meaning: no parametric return process, option formula, or utility specification is required for the volatility inequality. The empirical estimates still rely on stable enough return moments within a window, a Treasury proxy, and a population interpretation of finite-sample means and variances. Estimation error is substantial for expected returns, particularly in six-year and ten-year windows. Historical survivorship and index construction are also outside the formal no-arbitrage theorem.

A careful implementation should therefore output the window endpoints, observation counts, raw means, volatility, normalization convention, and bound together. It should preserve the source's descriptive figures while marking the scaling correction to equation (32), distinguish monthly from annual quantities, and label post-1987 conclusions as lower-bound evidence. The substantive payoff is a disciplined bridge between SDF diagnostics and probability-measure differences, with the identification boundary made explicit.
