# How to measure risk?

Georg Ch. Pflug, IIASA and University of Vienna. Undated local manuscript dedicated to Franz Ferschl on his seventieth birthday. The supplied PDF does not identify a publication venue or year; its references include works dated 1998. No publication year is inferred from the filename or assigned to this version.

Source: [RiskMeasures_Pflug.pdf](../../Finance/RiskMeasures_Pflug.pdf), 21 PDF pages. All pages, including every proof, the vector-risk figure, conclusion, and references, were read visually. The PDF’s character mapping makes ordinary text extraction unreliable. Page references below refer to PDF pages, not the anomalous printed page number on the final reference page.

## Why this matters

A scalar objective for portfolio choice usually combines a desirable location, such as expected wealth, with an undesirable spread. The choice of spread changes more than the economic interpretation: it changes whether optimization is convex, whether diversification is rewarded, and whether an objectively better payoff can perversely receive a worse score. Pflug organizes these requirements in a common language of distributions, acceptance sets, and stochastic orders.

The most useful constructive part is the treatment of mean minus downside-deviation objectives. It extends familiar mean–variance and mean–absolute-deviation criteria to transformed downside deviations and Minkowski gauges, and studies conditions under which these objectives respect second-order stochastic dominance. A separate section shows how risk of an aggregate differs from the average risk borne by individuals, producing a measure of risk-sharing inequality.

This is a methodological synthesis with mathematical propositions and examples, not an empirical investment study. It contains no asset-return dataset, estimation windows, portfolio performance table, costs, or statistical tests. Its usefulness is in selecting and implementing an objective whose properties match the decision problem. Some printed property lists and formulas contain inconsistencies. The note therefore gives a consistent wealth/loss convention, reconstructs the key calculations, and distinguishes derived corrections from the manuscript’s literal assertions.

## Conventions: distributions, risk, and safety

Let $W$ denote terminal wealth and $G(u)=P(W\le u)$ its distribution function. A safety functional $S(W)$ is maximized; a corresponding risk functional $\rho(W)=-S(W)$ is minimized. A loss variable is $Y=-W$. A risk functional on losses can equivalently be defined as $\rho_Y(Y)=\rho(-Y)$. These conventions prevent a cash addition to wealth from being confused with a cash addition to losses.

The manuscript requires law invariance: only the distribution of the variable matters, not the particular probability-space representation. Distribution translation is $T_cG(u)=G(u-c)$, the law of $W+c$. Positive scaling is $S_aG(u)=G(u/a)$ for $a>0$, the law of $aW$. Ordinary convolution gives the sum of independent variables. The generalized convolution set $G_1\otimes G_2$ contains every possible law of $W_1+W_2$ with the specified marginal laws and arbitrary dependence.

That last distinction matters for portfolio construction. Marginal distributions alone do not determine portfolio risk. A property required for every member of $G_1\otimes G_2$ must survive all dependence structures. Computing a particular portfolio score, however, requires a joint scenario model, not just the two marginal distributions.

For wealth, consistent cash translation is

$$
S(W+c)=S(W)+c,\qquad \rho(W+c)=\rho(W)-c.
$$

For losses, $\rho_Y(Y+c)=\rho_Y(Y)+c$. Page 4 prints a plus sign for a risk functional while defining translation of wealth; the acceptance-set proof on p. 6 instead correctly uses a minus sign. The formulas in this note adopt the latter wealth convention. This is an algebraic reconciliation of the manuscript, not an official erratum.

Positive homogeneity means $\rho(aW)=a\rho(W)$ for $a>0$. Subadditivity of risk is $\rho(W_1+W_2)\le\rho(W_1)+\rho(W_2)$ and is equivalent to superadditivity of safety. A mean-minus-dispersion safety score often has the latter property because the dispersion penalty is subadditive. Several manuscript passages call the safety functional itself “subadditive”; the actual inequality must be checked rather than carried over by name.

Two kinds of convexity must also be separated. Convexity in the distribution function concerns a mixture of laws, meaning an external lottery that selects which distribution is used. Convexity in portfolio payoffs concerns $\theta W_1+(1-\theta)W_2$ on a common probability space. The manuscript calls the latter generalized-convolution convexity. It is this second property that turns a linear-payoff portfolio optimization into a convex problem. A functional can behave differently under mixing distributions and mixing positions.

## Stochastic orders and acceptance sets

The manuscript defines successive integrated distribution functions by $G^{(1)}=G$ and $G^{(k)}(u)=\int_{-\infty}^uG^{(k-1)}(v)\,dv$. Under its notation $G_1\prec_{SD(k)}G_2$ means $G_1^{(k)}(u)\ge G_2^{(k)}(u)$ for every $u$: distribution 2 is preferable. First-order dominance corresponds to larger expectations for every increasing utility. Second-order dominance corresponds to larger expectations for every increasing concave utility, with the required integrability.

For second-order dominance, the identity

$$
\int_{-\infty}^{x}G(u)\,du=E[(x-W)^+]
$$

connects the integrated CDF to expected shortfall below a fixed target. The proof on p. 3 uses negative positive-part functions as building blocks for increasing concave utilities. This gives a route from dominance to downside-deviation comparisons. It is stronger information than a statement about variance alone because the mean and the whole lower distribution enter.

The manuscript also considers orders generated by functions with nonnegative $k$th derivative. The second-order member of that family uses convex test functions and is distinct from increasing-concave stochastic dominance. Confusing these two orderings would reverse the interpretation of some property lists.

An acceptance set $\mathcal A$ is a collection of wealth distributions deemed acceptable. The induced capital requirement is

$$
\rho_{\mathcal A}(W)=\inf\{c:\mathcal L(W+c)\in\mathcal A\}.
$$

Positive cash shifts should preserve acceptance. A positive cone generates positive homogeneity; closure under all sums generates subadditivity; convexity under payoff averaging generates convexity of the capital requirement. Conversely, the zero sublevel set $\mathcal A_\rho(0)=\{G:\rho(G)\le0\}$ recovers a cash-additive risk functional by this construction. With suitable closedness and upward-cash stability, the acceptance set can likewise be recovered from its capital requirement.

The proof is constructive. For a cash-additive wealth risk functional, $\rho(W+c)\le0$ is equivalent to $c\ge\rho(W)$, so taking the infimum gives exactly $\rho(W)$. For convexity, shift each of two wealths into the acceptable set, average the shifted positions, then let arbitrarily small slack tend to zero. The domain and topology still matter: weak convergence does not automatically control unbounded moments. The manuscript’s broad reference to weakly closed sets should not be read as a theorem that every moment-based acceptance set is weakly closed on all distributions without integrability restrictions.

## Families of scalar objectives

The paper first reviews expected-utility safety scores $S(W)=E[U(W)]$. They are linear in the probability distribution and concave in portfolio weights if $U$ is concave and wealth is linear in the weights. Increasing concave utilities respect second-order stochastic dominance. They do not generally have monetary cash translation or degree-one scaling: adding a currency unit changes utility by an amount dependent on wealth, and power utility scales in its own degree. The manuscript includes power utility, logarithmic utility, expected payoff above a fixed threshold, and probability of exceeding a threshold as examples of distribution-linear criteria.

A second family uses two independent draws $W,W'$ from the same distribution:

$$
S(W)=E[W]-\delta E[h(W-W')],
$$

where $h$ is symmetric and convex. With $h(z)=z^2$, $E[(W-W')^2]=2\operatorname{Var}(W)$, so the objective is $E[W]-2\delta\operatorname{Var}(W)$. With $h(z)=|z|$, the penalty is the Gini mean difference $E|W-W'|$. The factor two in the variance example is easy to miss when translating a quoted risk-aversion coefficient into code.

A third family measures deviation from the mean directly:

$$
S(W)=\mu-\delta E[h(W-\mu)],\qquad \mu=E[W].
$$

Examples include upper and lower semivariance and mean lower absolute deviation. Define $z^-=( -z)^+$, a nonnegative number. Then

$$
\operatorname{Var}^{-}(W)=E[((W-\mu)^-)^2],\qquad
\operatorname{MLAD}(W)=E[(W-\mu)^-].
$$

Since the centered variable has mean zero, its expected positive and negative parts are equal. Hence $\operatorname{MLAD}=\tfrac12E|W-\mu|$. The penalty measures deviation below the mean, not below zero wealth or a fixed required return. Changing the benchmark changes the objective and its properties.

Cash translation holds because centering removes the shift. Positive homogeneity fails for raw variance and semivariance penalties because they scale quadratically while the mean scales linearly. Convexity in portfolio positions often survives: the centered portfolio payoff is linear in weights and $h$ is convex. But raw variance is not subadditive for arbitrary dependence; perfectly positively dependent positions provide an immediate counterexample. Thus the broad subadditivity labels in the source’s raw dispersion list cannot be used without additional conditions on the penalty.

Pflug then takes an inverse transform of a downside moment:

$$
S_h(W)=\mu-\delta h^{-1}\!\left(E[h((W-\mu)^-)]\right).
$$

For $h(z)=z$, this is mean minus MLAD. For $h(z)=z^2$ on nonnegative arguments, it is mean minus lower semistandard deviation. More generally $h(z)=z^p$, $p\ge1$, produces the $L^p$ size of downside deviation. In these power cases the penalty has payoff units and is homogeneous of degree one.

## Dominance for downside measures and the role of normalization

Proposition 2.1 studies the inverse-transform functional under an increasing convex differentiable $h$ for which $u\mapsto h'(h^{-1}(u))$ is concave. For $0\le\delta\le1$, it gives second-order-dominance consistency. The argument bounds the effect of shifting a downside variable by a constant: the transformed certainty-equivalent deviation cannot change faster than the shift under the stated curvature condition. Combining this with the dominance inequality for an increasing concave shortfall transformation yields the desired ordering.

The point is not that every downside statistic respects dominance. The scale of the penalty relative to the mean matters. If the risk-aversion coefficient is too large, a modest increase in expected wealth accompanied by some newly introduced dispersion can reduce the safety score even when every realized payoff improves. The restriction on $\delta$ is part of the theorem, not a tuning suggestion that can be omitted.

The manuscript next defines the Minkowski gauge

$$
\|Z\|_h=\inf\left\{a>0:E\left[h\left(\frac{|Z|}{a}\right)\right]\le1\right\},
$$

with $h$ increasing and convex on nonnegative arguments and $h(0)=0$. This is a Luxemburg-type gauge. Under nondegeneracy and finiteness conditions it is homogeneous and obeys a triangle inequality. For $h(z)=z$, $z^2$, and $z^p$, it gives $E|Z|$, $\sqrt{E[Z^2]}$, and $(E|Z|^p)^{1/p}$ respectively. The safety score is

$$
S(W)=E[W]-\delta\|(W-E[W])^-\|_h.
$$

The subadditivity proof applies to the downside penalty: after centering, $(Z_1+Z_2)^-\le Z_1^-+Z_2^-$, and monotonicity plus the gauge triangle inequality bounds the penalty of the sum. Therefore safety is superadditive and risk $-S$ is subadditive. Homogeneity then gives concavity of safety in portfolio positions.

There is a missing normalization in the manuscript’s general dominance statement for this gauge. Its proof treats the gauge of a constant $b$ as $b$, which requires $h(1)=1$ in the usual strictly increasing case. In general,

$$
\|b\|_h=\frac{|b|}{h^{-1}(1)}.
$$

The natural sufficient coefficient restriction is consequently $\delta/h^{-1}(1)\le1$, or one first normalizes the gauge so constants retain their currency magnitude. The examples $h(z)=z^p$ already satisfy $h(1)=1$, so their stated $0\le\delta\le1$ restriction is consistent.

A derived counterexample shows why this detail is substantive. Let $W$ take 0 and 1 equally, let $h(z)=8z$, and set $\delta=1$. This wealth first-order dominates constant zero. Yet its mean is 0.5, its mean downside deviation is 0.25, its gauge penalty is 2, and its safety score is $-1.5$, below the score zero of constant-zero wealth. The source’s unrestricted gauge claim cannot hold for that normalization. This calculation is an independent diagnostic, not an example reported by Pflug.

## Quantiles and the optimization tradeoff

Section 2.4 considers functionals linear in the quantile function and identifies VaR as a quantile of a loss distribution. With terminal wealth convention, the corresponding lower quantile is a safety measure; its negative is a risk measure. Quantiles preserve ordinary stochastic ordering but need not be convex in portfolio weights or subadditive across positions. This is the source’s principal computational criticism of VaR optimization: a linear portfolio payoff can still lead to a nonsmooth, nonconvex quantile objective.

The general printed inverse-linear representation requires care with endpoints and integration by parts for unbounded support. A generic integral of a transformed CDF over the entire real line need not be finite. A practical spectral or distortion functional should therefore be defined with its tail conventions, normalization, and domain rather than implemented by copying the displayed integral without those qualifications.

The source favors mean–MLAD and mean–lower-semideviation objectives because they combine cash translation, homogeneity, and convex optimization in portfolio positions with dominance consistency under their parameter restrictions. Its concluding sentence says these measures are not coherent because they respect second-order rather than first-order dominance. That reason is not valid as stated: first-order dominance implies second-order dominance, so consistency with the latter includes consistency with the former on the relevant domain. Under normalized gauges, $0\le\delta\le1$, suitable integrability, and the corrected safety/risk sign convention, the negative safety score does have the cash-additive, homogeneous, subadditive, and monotone properties at issue. The note retains the functional construction while correcting this logical implication.

Mean–variance retains a different advantage. For a portfolio of known component means and variances, covariances suffice to compute aggregate variance. For other nonlinear deviation functionals, full joint-distribution information is generally needed. The manuscript’s remark that only a correlation is additionally required presumes the individual means and scales are available; the two scalar mean–variance scores alone do not identify all the components needed for aggregation.

## Vector risk, unequal burdens, and mutual insurance

For a vector of losses $\mathbf Y=(Y_1,\ldots,Y_N)$, let $\bar Y=N^{-1}\sum_iY_i$ and use a convex loss-risk functional $\rho_Y$. Define social risk, individual risk, and the source’s “unfairness” measure by

$$
S_\rho(\mathbf Y)=\rho_Y(\bar Y),\qquad
I_\rho(\mathbf Y)=\frac1N\sum_i\rho_Y(Y_i),\qquad
U_\rho(\mathbf Y)=I_\rho(\mathbf Y)-S_\rho(\mathbf Y)\ge0.
$$

The nonnegativity follows from convexity. The labels distinguish risk of the average burden from average risk before sharing. They are not an assertion that every form of ethical unfairness is captured: with a mean–variance functional, deterministic differences in loss levels do not enter $U$ because the expectation terms cancel.

For $\rho_Y(Y)=E[Y]+\delta\operatorname{Var}(Y)$, straightforward expansion gives

$$
U_\rho(\mathbf Y)=\delta\left\{\frac1N\sum_i\operatorname{Var}(Y_i)-\operatorname{Var}(\bar Y)\right\}
=\frac{\delta}{2N^2}\sum_{i\ne j}\operatorname{Var}(Y_i-Y_j).
$$

The last sum is over ordered pairs. The source’s main formula has this factor $1/(2N^2)$; a line in its subsequent covariance expansion omits a factor one half. The displayed identity above follows directly by expanding each pairwise variance.

The analytic example takes independent Bernoulli losses with common probability $p$. It yields

$$
S_\rho=p+\frac{\delta}{N}p(1-p),\qquad
I_\rho=p+\delta p(1-p),\qquad
U_\rho=\delta\frac{N-1}{N}p(1-p).
$$

If all individuals instead experience exactly the same Bernoulli loss, the marginals and individual risks stay unchanged, but $S_\rho=I_\rho=p+\delta p(1-p)$ and $U_\rho=0$. Aggregate volatility is greater in the common-shock case, while unequal realized burdens disappear. That contrast explains why a planner may need more than one risk criterion.

Vector dominance requires social risk, individual risk, and unfairness all to be no greater. Figure 1 illustrates the alternatives dominating the point $(S_\rho,I_\rho)=(4,6)$, whose unfairness is 2. The admissible region lies between the diagonal $I=S$ and the line $I=S+2$, with $S\le4$. It is a partial order, so not every pair of policies can be ranked without further preferences. The manuscript supplies no empirical weights for resolving such tradeoffs.

For proportional pooling, define retained losses as

$$
\widetilde Y_i=\alpha Y_i+(1-\alpha)\bar Y,\qquad0\le\alpha\le1.
$$

The average loss is unchanged. Convexity gives $\rho_Y(\widetilde Y_i)\le\alpha\rho_Y(Y_i)+(1-\alpha)\rho_Y(\bar Y)$, and averaging and subtracting the unchanged social risk yields

$$
U_\rho(\widetilde{\mathbf Y})\le\alpha U_\rho(\mathbf Y).
$$

In this displayed contract, $\alpha$ is the retained individual fraction: full pooling is $\alpha=0$, and no pooling is $\alpha=1$. Pages 18–19 call it a reimbursed fraction and identify $\alpha=1$ with full sharing; that verbal orientation contradicts the contract. The source’s intermediate risk expression also nests $\rho(\bar Y)$ where the random loss $\bar Y$ belongs. The corrected derivation above follows the actual contract and convexity. For the mean–variance example, direct variance expansion strengthens the bound to the exact identity $U_\rho(\widetilde{\mathbf Y})=\alpha^2U_\rho(\mathbf Y)$.

## Reimplementation from scenarios

For a finite scenario model with probabilities $p_s$ and portfolio wealth $w_s(x)=b_s+r_s^\top x$, first compute $\mu(x)=\sum_sp_sw_s(x)$. Then compute downside deviations $d_s(x)=(\mu(x)-w_s(x))^+$. Mean–MLAD maximizes $\mu-\delta\sum_sp_sd_s$; mean–lower-semideviation maximizes $\mu-\delta(\sum_sp_sd_s^2)^{1/2}$. These formulas require a joint scenario matrix because each scenario must preserve the dependence among assets.

The following optimization formulations are direct implementations derived from the manuscript’s functionals. With linear portfolio constraints, mean–MLAD becomes a linear program by introducing $z_s\ge0$ and $z_s\ge\mu-w_s$, then maximizing $\mu-\delta\sum_sp_sz_s$. For lower semideviation, introduce a variable $t$ and the second-order-cone constraint $\|(\sqrt{p_s}z_s)_s\|_2\le t$, then maximize $\mu-\delta t$. These formulations retain payoff convexity and avoid differentiating a kink at zero downside deviation.

For a general gauge, find the smallest $a>0$ with $\sum_sp_sh(d_s/a)\le1$, observing its normalization and finite-moment domain. A one-dimensional solve suffices for evaluating a fixed portfolio; optimizing the portfolio requires the appropriate perspective/epigraph representation and a solver supporting the chosen $h$. The manuscript does not provide algorithms, solver tolerances, runtime comparisons, or a calibrated choice of $h$ and $\delta$.

Validation should check cash shifts, position scaling, and diversification using identical scenarios, and test monotonicity only under the coefficient and normalization restrictions actually imposed. For vector risk, compare the pairwise-variance identity against the difference between average individual risk and social risk, then verify that pooling leaves $\bar Y$ unchanged. These are meaningful mathematical consistency checks; they do not substitute for estimating the future joint distribution.

The research value of this manuscript is the connection between objective properties, acceptance-set geometry, and tractable downside optimization. Its practical limits are equally specific: estimated means and tail dependence remain inputs, distributional mixtures must not be confused with portfolio combinations, and several printed sign and normalization statements require correction before coding. No return premium, optimal empirical coefficient, or realized investment advantage is established by the source.
