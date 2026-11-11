# A simple exponential model for dependent defaults

Kay Giesecke. *Journal of Fixed Income* 13(3), 74–83 (2003). The supplied 20-page author manuscript identifies that publication on its first page. Source: [original PDF](../../Finance/DependentDefaults_Gieseck2003.pdf). All 20 PDF pages, including the references, were read; page references below use this manuscript's pagination.

## Why this matters

The paper builds a tractable common-shock model of multiple default times. Independent Poisson processes represent shocks that can kill an individual firm, an industry group, a regional group, or any selected subset. A firm defaults when the first shock affecting it arrives. This produces a multivariate exponential distribution, an explicit Marshall–Olkin survival copula, closed-form dependence measures, and direct simulation. The same dependence structure can then be coupled to non-exponential marginal survival curves.

The useful research contribution is the connection between a transparent shock-incidence structure, credit-calibration inputs, portfolio default counts, and first-to-default basket pricing. The underlying multivariate exponential distribution is not new: the paper explicitly identifies Marshall and Olkin (1967) as its reliability-model predecessor. The financial interpretation exposes a major modeling choice: dependence includes positive probability of simultaneous defaults. It is not merely a correlation between smooth hazard-rate paths.

For a practitioner, this is a small model that can serve as a pricing or risk benchmark, a simulator with exact marginal controls, or a way to test how simultaneous losses affect a portfolio. Its tractability does not solve the identification problem. Single-name default curves say how often each firm defaults, but generally cannot identify which shocks are shared. Moreover, the unrestricted model contains a shock for every nonempty subset, so parsimony is necessary for portfolios of realistic size.

The paper presents analytic derivations and stylized numerical graphs. It does not estimate a portfolio from raw historical data, fit observed tranche prices, report a trading strategy, or compare out-of-sample loss forecasts. Pricing is under a risk-neutral measure and risk management under a physical measure; the notation $P$ is used for whichever is appropriate to the application. Estimated parameters must retain that distinction.

## Two-name construction

Let $N_1,N_2,N$ be independent Poisson processes with constant nonnegative intensities $\lambda_1,\lambda_2,\lambda$. The first two processes are idiosyncratic; $N$ affects both firms. Define

$$
\tau_i=\inf\{t\ge0:N_i(t)+N(t)>0\},\qquad i=1,2.
$$

Equivalently, simulate independent exponential times $E_1,E_2,E_0$ with those rates and set $\tau_i=\min(E_i,E_0)$. Let $h_i=\lambda_i+\lambda$. Then

$$
s_i(t)=P(\tau_i>t)=e^{-h_it},\qquad E[\tau_i]=h_i^{-1},\qquad \operatorname{Var}(\tau_i)=h_i^{-2}.
$$

The joint survival probability, equation (1) on p. 4, is

$$
s(t,u)=\exp[-\lambda_1t-\lambda_2u-\lambda\max(t,u)]
=s_1(t)s_2(u)e^{\lambda\min(t,u)}.
$$

The common shock must be absent until the later of the two queried horizons. This maximum is the source of the non-smooth diagonal and singular probability mass. In particular, simultaneous default occurs when $E_0$ wins the three-way exponential race. Its probability is $\lambda/(\lambda_1+\lambda_2+\lambda)$, provided the denominator is positive. This last expression follows directly from the construction; the paper emphasizes positive simultaneous-default probability without needing a separate contagion mechanism.

Joint default probabilities follow from inclusion–exclusion:

$$
P(\tau_1\le t,\tau_2\le u)=1-s_1(t)-s_2(u)+s(t,u).
$$

Conditional event probabilities must preserve the conditioning horizon. For example, the probability that firm 2 has defaulted by $t$ given that firm 1 has defaulted by $t$ is the joint default probability divided by $1-s_1(t)$. It is different from an instantaneous default intensity just after observing a default. The common-shock process generates dependence through shared events; interpreting every conditional increase as causal contagion would add a claim beyond the model.

## Copulas and three distinct correlations

Define the fraction of firm $i$'s total hazard due to the common shock as $\theta_i=\lambda/h_i$. Substituting inverse marginal survival functions yields

$$
C^{\tau}(u,v)=\min\{vu^{1-\theta_1},uv^{1-\theta_2}\}.
$$

This is the survival copula: $s(t,u)=C^{\tau}(s_1(t),s_2(u))$. It satisfies $uv\le C^{\tau}(u,v)\le\min(u,v)$, so the model cannot describe negative default dependence. Zero common intensity gives the independence copula; zero idiosyncratic rates gives comonotonic default times. The ordinary CDF copula is

$$
K^{\tau}(u,v)=C^{\tau}(1-u,1-v)+u+v-1.
$$

It is important not to feed CDF probabilities into a survival-copula formula without this conversion. Simulation can use either convention, but the associated inverse distribution must match it.

The paper distinguishes rank correlation of default times, Pearson correlation of default times, and Pearson correlation of default indicators. On p. 6 it gives

$$
\rho_S(\tau_1,\tau_2)
=\frac{3\theta_1\theta_2}{2\theta_1+2\theta_2-\theta_1\theta_2}
=\frac{3\lambda}{3\lambda+2\lambda_1+2\lambda_2},
$$

$$
\rho(\tau_1,\tau_2)=\frac{\lambda}{\lambda+\lambda_1+\lambda_2},
$$

and at a common horizon $t$,

$$
\rho_D(t)=\frac{s(t,t)-s_1(t)s_2(t)}{\sqrt{[1-s_1(t)]s_1(t)[1-s_2(t)]s_2(t)}}.
$$

The first is invariant to increasing transformations of the marginal times and thus describes the copula. The second depends on the exponential marginals. The third is horizon dependent and describes binary credit events. Their different values do not imply that one is an incorrect estimate of another. The source argues that Pearson measures can understate nonlinear dependence; a more precise interpretation is that they answer different questions and do not by themselves identify the joint law.

Figures 1–3 use idiosyncratic intensities of 0.01 in the symmetric examples. Figure 1 varies the common intensity and shows rank correlation above Pearson time correlation. Figure 2 varies equal idiosyncratic intensities for common rates 0.05, 0.075, and 0.1; rank correlation falls as idiosyncratic risk rises. Figure 3 shows indicator correlations declining with time for common rates 0.01, 0.025, and 0.05. These are mathematical comparative statics, not estimates from issuer data. For example, setting all three rates to 0.01 gives a derived Pearson time correlation of $1/3$ and rank correlation $3/7$; these are useful unit checks rather than tabulated source results.

## Arbitrary shock groups

For $n$ names, introduce an $n\times m$ incidence matrix $A=(a_{ik})$, with $a_{ik}=1$ if shock $k$ kills name $i$. Each shock has an independent Poisson process $N_k$ of intensity $\lambda_k$. The full specification has $m=2^n-1$ columns, one for each nonempty subset. The source's three-name example contains three singleton columns, three pair columns, and the all-name column:

$$
A=\begin{pmatrix}
1&0&0&1&1&0&1\\
0&1&0&1&0&1&1\\
0&0&1&0&1&1&1
\end{pmatrix}.
$$

Deleting a group or setting its intensity to zero imposes a structural restriction. A model retaining only singleton and pair shocks prohibits any single shock from killing three names, although several shocks before the horizon can still default many names.

The default rule and marginal hazard are

$$
\tau_i=\inf\left\{t\ge0:\sum_{k=1}^m a_{ik}N_k(t)>0\right\},\qquad
h_i=\sum_{k=1}^m a_{ik}\lambda_k.
$$

Equation (6), the central computational identity, is

$$
P(\tau_1>t_1,\ldots,\tau_n>t_n)
=\exp\left[-\sum_{k=1}^m\lambda_k\max_i(a_{ik}t_i)\right].
$$

To get a subset survival probability, set the omitted names' horizons to zero. Joint default probabilities then require inclusion–exclusion across subsets. For a pair $i,j$, define their common hazard $h_{ij}=\sum_k a_{ik}a_{jk}\lambda_k$. Its marginal two-name model has common rate $h_{ij}$ and idiosyncratic rates $h_i-h_{ij}$ and $h_j-h_{ij}$. The pairwise formulas above therefore apply directly, with $\theta_i=h_{ij}/h_i$ and $\theta_j=h_{ij}/h_j$.

The construction guarantees a coherent multivariate distribution if all shock intensities are nonnegative. An arbitrary matrix of pairwise correlations need not admit such a representation. Even if every pair independently gives an admissible shared intensity, the implied singleton hazards may be negative after all shared group hazards are deducted. Calibration must impose global feasibility rather than fit each pair in isolation.

## Simulation with chosen marginal survival curves

The four-step algorithm on pp. 11–12 is exact for the specified model. Draw $U_k$ independently uniform on $(0,1)$ and compute shock times $E_k=-\log(U_k)/\lambda_k$. For zero rates use infinity, avoiding division by zero. Set $T_i=\min_{k:a_{ik}=1}E_k$, then $V_i=e^{-h_iT_i}$. Finally choose desired marginal survival functions $q_i$ and return

$$
Z_i=q_i^{-1}(V_i).
$$

The generated times satisfy $P(Z_1>t_1,\ldots,Z_n>t_n)=C^{\tau}(q_1(t_1),\ldots,q_n(t_n))$. If $q_i(t)=e^{-h_it}$, steps three and four cancel and $Z_i=T_i$. With piecewise hazard curves, invert cumulative hazard: $Z_i=H_i^{-1}(-\log V_i)$.

This separation permits a chosen structural or stochastic-intensity marginal model to be coupled to the exponential dependence structure. It does not retain every interpretation of the original shock process. In particular, equal underlying shock times need not map to equal calendar default times under different marginal transformations. The transformed model retains copula singularity but does not necessarily retain simultaneous defaults at identical dates. An implementation should therefore distinguish using the copula as a dependence device from claiming literal common-shock timing in calendar time.

For sparse $A$, simulate only active shock groups and update the minima of affected names. Expected computational work per path is proportional to the number of nonzero incidence entries. Generating the unrestricted $2^n-1$ shock universe is not practical for large $n$. No random seed, simulation path count, programming implementation, runtime benchmark, or numerical convergence criterion is supplied in the paper.

## Calibration and what is identifiable

The source proposes first selecting the incidence matrix and then fitting its intensities. Under constant hazards, single-name survival observations give the linear restrictions

$$
-\frac{\log s_i(t)}t=\sum_k a_{ik}\lambda_k.
$$

Risk-neutral survival can be inferred from bond or CDS prices given a recovery and discounting convention. Physical survival can be estimated from historical issuer defaults or rating-class averages. The paper names those sources but supplies no actual calibration dataset, quote date, instrument set, recovery assumption, or estimation window.

Page 13 suggests that multiple quoted maturities may provide enough equations to determine all intensities. There is an identification caveat: with constant intensities and a fixed incidence matrix, maturities repeat the same row sums after dividing by $t$. They improve estimation of each total hazard or expose a failure of the exponential assumption, but do not by themselves separate idiosyncratic from common hazards. Basket or other dependence-sensitive observations are needed, or one must impose additional structural restrictions. This is a linear-algebra consequence of equation (9), not an external correction attributed to the author.

For a joint survival observation at unequal horizons, $-\log s(t_1,\ldots,t_n)$ is another linear combination of shock rates with coefficients $\max_i(a_{ik}t_i)$. A practical calibration can solve nonnegative least squares with weights reflecting quote reliability, although the paper does not prescribe weights or regularization. More complex restrictions can be imposed by tying group rates across pairs or sectors.

The parsimonious pair-shock model with one common rate for every pair has $n+1$ parameters: $n$ singleton rates plus one tied pair rate. It is not a model with one shock hitting all names. Pair default-event correlations can inform the shared rates through the explicit formula. Rank correlations are also proposed, but the paper acknowledges that they are rarely observed reliably.

A second physical calibration route uses Moody's Diversity Score $d$. Let $M_t$ be the number of surviving firms. Replace the original equal-notional portfolio by $d$ independent names, each with survival $q(t)$ and notional scaled by $n/d$. Matching first and second moments gives

$$
nq(t)=\sum_i s_i(t),
$$

$$
\frac{n^2}{d}q(t)[1-q(t)]
=\sum_i s_i(t)[1-s_i(t)]+\sum_{i\ne j}[s_{ij}(t,t)-s_i(t)s_j(t)].
$$

Equation (10) calls the quantities default counts, while its indicators are survival indicators; the moment equations are valid with the latter convention, and default counts have the same variance. One diversity score identifies an aggregate covariance quantity, not a full dependence model. Its usefulness therefore depends on symmetry restrictions or other prior choices about shock allocation.

The source's suggestion that a rank-correlation matrix and individual survival curves can determine a fully general model also needs qualification. Pairwise information cannot generally identify all $2^n-1$ subset intensities. For three names, pairwise shared intensities each include the triple-shock rate, leaving a free component unless additional higher-order data or restrictions fix it. A quant implementation should inspect the rank of the calibration system and report non-uniqueness.

## Default-count distribution and an important numerical inconsistency

Under equal unit exposures and zero recovery, loss is the number of defaulted names, $L_t=n-M_t$. The general distribution follows by inclusion–exclusion:

$$
P(M_t=k)=\sum_{i=k}^n {i\choose k}(-1)^{i-k}
\sum_{J\subseteq\{1,\ldots,n\}:|J|=i}P(\tau_j>t\ \forall j\in J).
$$

For an exchangeable model, write $\pi_k(t)$ for survival of any specified $k$ names and set $\pi_0=1$. Then

$$
P(M_t=k)=\sum_{j=0}^{n-k}(-1)^j
\frac{n!}{j!k!(n-k-j)!}\pi_{k+j}(t).
$$

In the homogeneous singleton-plus-pair model, singleton intensity is $\lambda$ and each pair's intensity is $\bar\lambda$. A selected group of $k$ names is exposed to $k$ singleton shocks, ${k\choose2}$ within-group pair shocks, and $k(n-k)$ pair shocks crossing the group boundary. Consequently,

$$
\pi_k(t)=\exp\left[-t\left(k\lambda+\bar\lambda\left\{{k\choose2}+k(n-k)\right\}\right)\right].
$$

The source uses $n=30$ and a ten-year horizon in Figures 4–6. Figure 4 shows $\bar\lambda=0,0.0005,0.001$; Figure 6 shows larger values including 0.0075, 0.01, and 0.05. Figure 5 plots mean and variance as common intensity rises. The figures depict loss mass moving markedly to the right and eventually toward 30 defaults.

Page 16 simultaneously says the one-year default probability is held at 1% and that expected default count rises with common intensity. Those cannot both hold under constant hazards. Since each marginal total hazard is $h=\lambda+(n-1)\bar\lambda$, fixing the one-year PD at 1% requires

$$
h=-\log(0.99),\qquad \lambda=h-29\bar\lambda\ge0.
$$

Thus $\bar\lambda\le-\log(0.99)/29\approx0.00034656$, and at ten years the expected count is always $30[1-0.99^{10}]\approx2.8685$. The plotted pair rates 0.0005 and 0.001 already violate that fixed-marginal feasibility bound. The increasing mean and eventual near-certain total default are consistent with holding an idiosyncratic rate fixed while adding common hazard, rather than holding total marginal PD fixed. The PDF does not state an official resolution; the discrepancy is verified from its formulas and graph labels.

This is consequential for interpretation. Increasing correlation at unchanged marginals alters tail risk and dispersion without changing expected default count. Increasing shared intensity while leaving singleton intensity unchanged alters both dependence and marginal credit quality. A reproduction should run and label these as separate experiments. Treating the source's Figure 5 as pure correlation sensitivity would conflate them.

The alternating count-probability sum can suffer severe cancellation for large $n$. Use higher precision or a carefully tested probability recursion, and compare a moderate-sized case against the direct shock simulator. Required checks are nonnegative probabilities within numerical tolerance, total mass one, and mean $\sum_i[1-s_i(t)]$. The paper does not analyze numerical stability or provide a general large-portfolio implementation.

## First-to-default digital baskets

Let $\tau=\min_i\tau_i$. The first default is the first shock hitting any reference name, so

$$
P(\tau>t)=e^{-\Lambda t},\qquad
\Lambda=\sum_k\lambda_k\max_i a_{ik}.
$$

Under constant risk-free rate $r$, a unit payment at default before maturity $T$ has value

$$
c=\frac{\Lambda}{r+\Lambda}\left(1-e^{-(r+\Lambda)T}\right).
$$

If a fixed payment $R$ is made at each date $t_j$ conditional on survival and there is no accrued premium on default, the fee leg is

$$
f=R\sum_{j:t_j\le T}e^{-(r+\Lambda)t_j},\qquad
R=\frac{c}{\sum_j e^{-(r+\Lambda)t_j}}.
$$

Here $R$ is the payment at each coupon date as defined by the paper. To express it as an annualized spread with accrual fractions, insert those fractions in the annuity denominator. The distinction is material in the semiannual example. This is a unit digital payoff, not a default payment proportional to a stochastic loss given default.

Figure 7 uses five homogeneous names, $r=0$, $T=1$, and coupon dates 0.5 and 1. It varies individual one-year PD across 5%, 7%, and 10%. In this example the text explicitly decreases the singleton intensity as pair intensity increases, keeping the individual PD constant. With $h=-\log(1-p)$,

$$
\lambda=h-4\bar\lambda,\qquad
\Lambda=5\lambda+10\bar\lambda=5h-10\bar\lambda,
\qquad0\le\bar\lambda\le h/4.
$$

Therefore the first-to-default payment declines with dependence at fixed marginals. Defaults become more clustered, reducing the probability of at least one default for the same total expected number. Higher individual PD still increases the required payment. These statements follow exactly from the formulas; the graph supplies no price table or bid–ask comparison. The feasibility ceiling differs by PD, so plotted curves should be evaluated only on their admissible intensity domains.

## Extensions and reproducibility boundaries

The nonfatal-shock extension independently marks shocks by which names actually default. In the bivariate case, an idiosyncratic shock kills firm $i$ with probability $q_i$, while a common shock kills both, only name 1, or only name 2 with probabilities $q_{11},q_{10},q_{01}$. Poisson thinning gives effective rates $\gamma_1=\lambda_1q_1+\lambda q_{10}$, $\gamma_2=\lambda_2q_2+\lambda q_{01}$, and $\gamma=\lambda q_{11}$. This is still the same exponential distribution, with more primitive parameters than the distribution can separately identify.

Deterministic time-varying intensities replace each rate-times-time term by an integrated hazard. The marginal expressions printed on p. 10 omit a minus sign, visibly in both the deterministic and stochastic versions. The corrected survival form derived from a no-event probability is $s_i(t)=\exp[-\int_0^t(\lambda_i(u)+\lambda(u))du]$; the stochastic version takes its expectation under suitable conditional Poisson assumptions. Positive integrated hazards without that minus sign would generate survival probabilities above one. The joint expressions on the same page already contain the negative signs. This note records a source diagnostic, not an official erratum.

Stochastic intensities can enrich spread dynamics, but their joint law, dependence on rates, and calibration are not developed here. Arbitrary marginal substitution likewise retains the chosen copula rather than yielding a fully specified dynamic credit-market model. Hedging multi-name products requires more than their unconditional default-time distribution.

A usable implementation therefore consists of explicit shock groups, nonnegative rates under a declared probability measure, exact survival formulas, a sparse shock simulator, and tested count or basket-payoff routines. Data needed for market calibration include recovery conventions, discount curves, single-name quotes, and dependence-sensitive observations; physical calibration needs default definitions, exposure histories, and uncertainty treatment. The article supplies the mathematical machinery but none of those empirical inputs. Its main strength is an auditable dependence benchmark, with the restriction to positive dependence, simultaneous shocks, and carefully separated marginal and dependence sensitivity made explicit.
