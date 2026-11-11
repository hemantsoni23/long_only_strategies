# Spectral measures of risk: A coherent representation of subjective risk aversion

**Carlo Acerbi.** *Journal of Banking & Finance* 26 (2002), 1505–1518. PII S0378-4266(02)00281-9. **Source:** [RiskManagement_Acerbi_2002.pdf](../../Finance/RiskManagement_Acerbi_2002.pdf), 14 pages, read in full including the necessity proofs, finite-sample construction, and references. Printed page numbers are used below. This theoretical paper contains no empirical dataset, performance backtest, or simulation study.

## Why this matters and the actual contribution

Expected shortfall treats every outcome inside a chosen tail equally and every outcome outside it as irrelevant. An investor may instead want a smooth decline in attention from catastrophic losses to moderate losses, while still requiring coherent aggregation, cash accounting, and diversification incentives. Acerbi characterizes exactly which weighted averages of ordered portfolio outcomes meet those requirements.

The central result is a necessary-and-sufficient condition on a probability-rank weight function: it must be nonnegative, nonincreasing from worst to best outcomes, and integrate to one. The paper proves the continuous-distribution-functional version, a finite-scenario version valid at every sample size, and consistency of a proposed discretization under explicit integrability conditions. Its novelty is the representation and complete characterization within the spectral class, not the invention of coherence or expected shortfall.

This distinction matters for implementation. Coherent finite-scenario measurement does not require an asymptotic approximation. Estimating the corresponding population quantity does. A chosen spectrum encodes preferences about adverse ranks, while the scenario generator encodes beliefs about probabilities and dependence. The paper does not estimate either investor preferences or the market's probability law.

## Profit convention, domain, and axioms

Let $X$ denote portfolio profit and loss; low values are bad. On a chosen probability space with law $P$, define the lower quantile

$$
q_X(p)=\inf\{x:P(X\le x)\ge p\},\qquad 0<p<1.
$$

A spectral measure is

$$
M_\phi(X)=-\int_0^1q_X(p)\phi(p)\,dp.
$$

Positive values represent required capital; negative values represent a surplus under the chosen risk criterion. Outcomes are expressed in money, and the spectrum is a dimensionless density over probability ranks. The integral therefore has monetary units. With this convention, a worse outcome receives a larger weight when $\phi$ decreases with $p$. A loss-variable formulation sorts in the opposite direction and uses increasing weights; mixing these conventions reverses the intended risk aversion.

The four coherence axioms in Definition 2.1 are monotonicity, $X\le Y\Rightarrow M(X)\ge M(Y)$; subadditivity, $M(X+Y)\le M(X)+M(Y)$; positive homogeneity, $M(cX)=cM(X)$ for $c>0$; and cash translation, $M(X+a)=M(X)-a$. The cash return is normalized to one. None of these assumes independence between positions.

The natural domain is

$$
\mathcal V_\phi=\left\{X:\int_0^1|q_X(p)\phi(p)|\,dp<\infty\right\}.
$$

A convenient sufficient condition is $E|X|<\infty$ and bounded $\phi$. It is not sufficient in general that $\phi$ and $q_X$ are separately integrable; a product of two integrable functions may fail to be integrable near zero. The source acknowledges the weighted-integrability requirement in Remark 2.6. Its assertion that practical applications always satisfy finite-moment conditions should be treated as a modeling assumption, not a guarantee supplied by a finite database.

The spectrum is formally an element of $L^1([0,1])$. Altering it at individual points does not alter the population integral. Admissibility means that it has a nonnegative, nonincreasing representative and integral one. The source formulates positivity and decrease through interval integrals to avoid making an equivalence class depend on point values. This detail becomes consequential when discretizing by point sampling.

## Building spectral measures from expected shortfall

The elementary coherent building block is

$$
\operatorname{ES}_\alpha(X)=-\frac1\alpha\int_0^\alpha q_X(p)\,dp,
\qquad 0<\alpha\le1.
$$

Here $\alpha$ is the adverse-tail probability, not the usual high coverage probability. At $\alpha=1$, ES is $-E[X]$; the limiting worst-case measure is $\operatorname{ES}_0(X)=-\operatorname{ess\,inf}X$, where finite. The latter can require a stronger domain than ordinary expected shortfall.

A convex combination of coherent measures is coherent. Nonnegative coefficients preserve monotonicity and subadditivity; coefficients summing to one preserve cash translation. Equations (6)–(9) parameterize such a combination through a positive measure $\mu$ satisfying $\int_{(0,1]}\alpha\,d\mu(\alpha)=1$:

$$
M_\mu(X)=\int_{(0,1]}\alpha\operatorname{ES}_\alpha(X)\,d\mu(\alpha).
$$

Interchanging integrals under the required integrability conditions gives

$$
M_\mu(X)=-\int_0^1q_X(p)\phi(p)\,dp,
\qquad \phi(p)=\int_{[p,1]}d\mu(\alpha).
$$

Thus $\phi$ is decreasing because raising $p$ removes mass from the integration set. Fubini's theorem gives $\int_0^1\phi(p)dp=\int\alpha d\mu(\alpha)=1$. A probability measure $\nu$ over ES levels can be used instead, with $d\nu(\alpha)=\alpha d\mu(\alpha)$ and $\phi(p)=\int_{[p,1]}\alpha^{-1}d\nu(\alpha)$.

There is an endpoint convention worth making explicit. Writing only $d\mu=-d\phi$ on the open interval loses a nonzero terminal level of the spectrum. For a decreasing spectrum with terminal limit $\phi(1-)>0$, include an atom of mass $\phi(1-)$ in $\mu$ at $\alpha=1$. For example, $\phi\equiv1$ corresponds entirely to ES at level one, although its ordinary derivative is zero. This is an implementation clarification of the source's Stieltjes notation, not a new risk measure.

Footnote 3 permits an additional share of $\operatorname{ES}_0$, represented formally by a Dirac mass at $p=0$. The main theorems restrict attention to nonsingular $L^1$ spectra. A regular density near zero and a point mass exactly at zero have different tail-domain requirements, and should not be interchanged numerically.

## What subjective risk aversion means here

For ES at level $\alpha$, the spectrum is $\phi(p)=\alpha^{-1}1_{(0,\alpha]}(p)$. At a 5% tail level, the density is 20 over the worst 5% and zero elsewhere. This is a probability weighting function, not an estimate of a utility curvature coefficient and not a portfolio holding.

Section 3 interprets a decreasing spectrum as giving weakly greater importance to worse ranks. Any admissible shape is coherent; the axioms alone do not pick a uniquely rational shape. A spectrum positive throughout $(0,1)$ responds to improvements outside an extreme tail, whereas an ES cutoff ignores them until their ranks enter the selected region.

For a source-consistent illustrative family, one can choose a finite convex combination of ES levels. If $M=\lambda\operatorname{ES}_a+(1-\lambda)\operatorname{ES}_b$, with $0<a<b\le1$ and $0\le\lambda\le1$, then

$$
\phi(p)=\frac\lambda a1_{p\le a}+
\frac{1-\lambda}{b}1_{p\le b}.
$$

The worst region receives both contributions, the intermediate region only the broader-tail contribution, and the rest receives zero. This construction makes the preference transparent and preserves coherence exactly. It is an explanatory example, not a spectrum calibrated or recommended by the author.

A steep spectrum makes the measure more sensitive to a small number of extreme observations. The paper's preference interpretation does not imply that such a spectrum can be estimated precisely from a short history. Selection of $\phi$, model calibration, and assessment of statistical uncertainty are separate decisions.

## Necessity: how each condition can fail

Theorem 4.1 is stronger than a recipe for producing examples. It shows that within the quantile-weighted representation, each admissibility condition is necessary for coherence over a sufficiently unrestricted class of risks and probability laws.

For nonnegativity, suppose an interval $I=(q_1,q_2]$ has negative total weight. Construct three ordered outcomes and increase only the middle outcome by a small positive amount $a$, preserving its order. The resulting portfolio $Y$ is everywhere at least as good as $X$, but

$$
M_\phi(Y)-M_\phi(X)=-a\int_I\phi(p)dp>0.
$$

Risk has increased after a statewise improvement, violating monotonicity. The proof requires no smooth distribution; a three-atom construction is enough.

For monotonicity of the spectrum, suppose adjacent equal-length rank intervals $I_2=(q-\epsilon,q]$ and $I_3=(q,q+\epsilon]$ have more weight on the better interval: $\int_{I_2}\phi<\int_{I_3}\phi$. Use a four-state distribution with probabilities $q-\epsilon,\epsilon,\epsilon,1-q-\epsilon$. Order $X$ normally, but swap the two middle outcomes of $Y$, while choosing the values so the sums remain ordered. Equation (22) computes

$$
M_\phi(X+Y)-M_\phi(X)-M_\phi(Y)
=-(Y_3-Y_2)\left\{\int_{I_2}\phi-\int_{I_3}\phi\right\}>0.
$$

Thus an upward step in rank weights can make aggregation increase the required capital beyond the sum of stand-alone requirements. This is the precise link between decreasing weights and subadditivity. It is not merely an aesthetic preference for a smooth tail profile.

For normalization, a constant shift gives

$$
M_\phi(X+a)=M_\phi(X)-a\int_0^1\phi(p)dp.
$$

Cash translation for arbitrary $a$ forces the integral to equal one. Otherwise adding one unit of cash would reduce the reported capital by something other than one unit.

The necessity result is a universal characterization, not a diagnostic based on one observed portfolio. An inadmissible spectrum may accidentally satisfy the inequalities on a restricted family of risks. Conversely, failure of a theorem's assumptions cannot be excused by obtaining an apparently reasonable answer on a particular sample.

## VaR, terminology, and a source sign error

VaR is represented formally by a Dirac mass at an interior probability rank. It assigns weight to the threshold while assigning no weight to more severe losses. Such an object is not a decreasing ordinary spectrum. The discussion in Section 3 uses this to explain why the quantile threshold is outside the coherent spectral class. A Dirac mass is also outside $L^1$, so its role is illustrative rather than a literal application of Theorem 4.1.

Equation (5) calls the conditional tail mean both TCE and CVaR and warns that it can be noncoherent with atoms. Modern implementations must distinguish that convention from the convex optimization definition of CVaR, which equals properly atom-corrected ES. The formulas determine the property. The companion Acerbi–Tasche paper resolves this terminology explicitly; the present note uses ES only for the quantile-integral definition.

There is also a substantive sign error in the introductory example, equation (1) on p. 1506. It prints $-\max\{E_{P_1}X,E_{P_2}X\}$ as a coherent measure. The coherent worst-loss construction is

$$
\max\{E_{P_1}[-X],E_{P_2}[-X]\}
=-\min\{E_{P_1}X,E_{P_2}X\}.
$$

The distinction can be checked without external theory: put all mass under $P_1$ on the first of two states and all mass under $P_2$ on the second; take $X=(1,0)$ and $Y=(0,1)$. The printed formula gives $-1$ for each individual and $-1$ for their sum, violating $-1\le-2$. The corrected supremum of losses is subadditive. This correction affects the motivating example, not the spectral characterization proved later.

## Exact finite-scenario measures

For scenario outcomes $X_1,\ldots,X_N$, sort $X_{1:N}\le\cdots\le X_{N:N}$ and define

$$
M_w^{(N)}(X)=-\sum_{i=1}^Nw_iX_{i:N}.
$$

Definitions 5.1–5.2 and Theorem 5.3 say that this is coherent on the equal-probability scenario space if and only if $w_i\ge0$, $w_i\ge w_{i+1}$, and $\sum_iw_i=1$. The result holds for each finite $N$. Independence is needed for the paper's sampling consistency theorem, not for the algebraic coherence of a fixed common scenario matrix.

The proof assigns probability $1/N$ to each observation and uses the piecewise-constant spectrum $\phi_N(p)=Nw_i$ on $((i-1)/N,i/N]$. Its quantile integral equals the weighted sum exactly. Conversely, a negative weight breaks monotonicity, an increasing adjacent pair permits a subadditivity counterexample, and a sum different from one breaks cash translation.

Aggregation must use outcomes from the same scenarios before sorting. To compare $X$, $Y$, and $X+Y$, form $Z_i=X_i+Y_i$ at each original scenario index and only then sort the three vectors separately. Adding separately sorted outcomes imposes comonotonic dependence and changes the joint risk being measured.

A useful direct computational interpretation is to assign the largest admissible weights to the smallest profits. By the rearrangement inequality, the weighted sum with decreasing $w$ and increasing profits is the minimum over assignments of the weights to the original scenario indices. Its negative is a maximum of linear functions of the scenario profits. This derived representation explains convexity and piecewise linearity and supplies a finite-dimensional proof of subadditivity. It does not imply differentiability at ties or a unique optimal portfolio.

## Decomposing discrete spectra and computing marginal risk

A finite version of the ES-mixture representation can be derived without integration. Set $w_{N+1}=0$ and define

$$
\beta_j=j(w_j-w_{j+1}),\qquad j=1,\ldots,N.
$$

The coefficients are nonnegative, and telescoping gives $\sum_j\beta_j=\sum_iw_i=1$. At the empirical tail level $j/N$, ES is the negative average of the first $j$ order statistics. Therefore

$$
-\sum_{i=1}^Nw_iX_{i:N}
=\sum_{j=1}^N\beta_j\operatorname{ES}_{j/N}^{\rm empirical}(X).
$$

To check the identity, an outcome of rank $i$ receives coefficient $\sum_{j=i}^N\beta_j/j=\sum_{j=i}^N(w_j-w_{j+1})=w_i$. The final coefficient $\beta_N=Nw_N$ is essential: it is the contribution of the whole-sample mean. This is the discrete counterpart of the terminal mass in the continuous Stieltjes construction. Dropping it would break cash normalization whenever the best outcomes still have positive weight.

The identity supplies a second implementation of a spectral statistic and shows exactly which ES thresholds are needed by a stepped spectrum. It is also useful for portfolio optimization: each ES component has a positive-part auxiliary-threshold representation, so a finite mixture can be optimized with one such representation per nonzero $\beta_j$. This is an implementation consequence of the source's representation, not a solver experiment reported in this paper.

For asset profits $R_{ik}$ in scenario $i$ and holdings $a_k$, write $X_i(a)=\sum_ka_kR_{ik}$. Away from ties or changes in rank, if permutation $\pi$ orders current profits, the local derivative is

$$
\frac{\partial M_w(X(a))}{\partial a_k}
=-\sum_{i=1}^Nw_iR_{\pi(i),k}.
$$

It uses the scenario ranking of the **whole portfolio**, not separate rankings of each asset. At a tie, a subgradient can be obtained from a maximizing assignment of weights to tied scenarios, and convex combinations of such assignments remain subgradients. The scalar risk is well defined, but a unique derivative need not exist. Hence a gradient-based implementation should recognize ties instead of treating a sorting routine's arbitrary tie order as an economic identification result.

Positive homogeneity implies that, where differentiable, multiplying each derivative by its holding and summing recovers total risk. This provides an attribution check. It does not mean that the rank ordering, and therefore marginal capital, remains fixed when holdings change materially.

## Discretizing a chosen population spectrum

The paper proposes the normalized point-sampling rule

$$
w_i=\frac{\phi(i/N)}{\sum_{k=1}^N\phi(k/N)}.
$$

Where the denominator is positive, a nonnegative decreasing representative produces an admissible vector, and the weights sum to one exactly. Theorem 5.4 establishes almost-sure convergence to $M_\phi(X)$ for independent identically distributed samples, bounded admissible $\phi$, and integrable $X$. The proof invokes the strong law for linear functions of order statistics; the article does not provide rates, confidence intervals, or a finite-sample error bound.

Two qualifications matter in code. First, the denominator can be zero: for a spectrum supported on $(0,\alpha)$ and $N\alpha<1$, every grid point $i/N$ lies outside the support. Second, endpoint values matter to the finite rule although they do not matter to the population $L^1$ class. With an ES cutoff exactly at $i/N$, including or excluding the endpoint can change one finite-sample weight. Neither issue invalidates the asymptotic theorem once the sequence is defined for sufficiently large $N$, but both contradict an unqualified claim that this particular formula always works for every sample size.

An exact empirical-CDF alternative, derived directly from the defining integral, is

$$
w_i=\int_{(i-1)/N}^{i/N}\phi(p)dp.
$$

These cell-integrated weights are automatically nonnegative, decreasing, and normalized. They are invariant to changes in point values and cannot have the zero-denominator problem. For ES they include a fractional cutoff observation whenever $N\alpha$ is not an integer. This is a reconstruction of the population definition, explicitly distinguished from the paper's point-sampling prescription.

A small arithmetic check illustrates the issue. With $N=4$, $\alpha=0.375$, and profits $(-10,-2,1,5)$, the exact empirical ES uses weights $(2/3,1/3,0,0)$ and is $22/3\approx7.333$. Point sampling the rectangular spectrum at $i/4$ gives $(1,0,0,0)$ and risk 10. Both weight vectors define coherent finite-scenario measures, but only the first is the empirical ES at the stated tail level. This is a derived diagnostic, not a numerical experiment reported in the article.

## Reimplementation, scope, and economic limits

To implement the construction, choose one currency and horizon, generate a joint scenario matrix, value each portfolio under each scenario, choose an admissible spectrum independently of the number of scenarios, and convert it to a finite weight vector with a documented rule. Sort the resulting portfolio P&L and calculate the weighted loss average. Cash-shift and scale identities should hold exactly up to floating-point error. Subadditivity should be tested on jointly aligned scenarios, including ties and discrete atoms.

The article's mathematical completeness refers to quantile-weighted measures, not to all coherent risk measures. Remark 4.4 cites the characterization involving law invariance and comonotonic additivity, under the appropriate probability-space and representation assumptions. General coherent measures can involve multiple probability models and need not be represented by one spectrum relative to one fixed law. A supremum of several spectral measures is coherent but need not itself be a single comonotonic-additive spectral functional.

Law invariance means that equal P&L distributions receive equal risk values. Comonotonic additivity means that two profits increasing with the same underlying rank receive no diversification benefit when aggregated. For spectral measures, comonotonic quantiles add, so the integral is additive. This identifies the preference class more narrowly than coherence alone.

Section 6 discusses capital adequacy as a prospective application, not as a regulatory rule established by the paper. It suggests that different business models may merit different spectra and speculates that a common benchmark could synchronize reactions. No calibration exercise or systemic-risk model establishes the magnitude of either effect. Allowing heterogeneous spectra does not by itself prove that correlated deleveraging disappears.

The practical achievement is a transparent bridge from rank preferences to a coherent monetary statistic and a coherent finite-scenario implementation. The remaining choices are substantial: the horizon, scenario distribution, joint dependence, valuation model, spectrum, statistical uncertainty, transaction costs, and liquidity treatment all remain outside the characterization. The paper makes the final aggregation step mathematically controlled; it does not make the inputs objectively known.
