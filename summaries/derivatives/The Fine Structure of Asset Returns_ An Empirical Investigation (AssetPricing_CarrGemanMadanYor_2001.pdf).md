# The Fine Structure of Asset Returns: An Empirical Investigation

Peter Carr, Hélyette Geman, Dilip B. Madan, and Marc Yor. *Journal of Business* 75(2), 2002, pp. 305–332. The supplied filename carries 2001; the publication reproduced in the PDF is dated 2002. [Source PDF](../../Finance/AssetPricing_CarrGemanMadanYor_2001.pdf). PDF page 1 is printed page 305; add 304 to PDF page numbers. All 28 supplied pages, including the proofs and references, were read. No separate appendix is included.

## Why this matters

A jump model is not adequately described by saying that returns have fat tails. A finite number of large jumps, infinitely many small jumps with finite total variation, and infinitely many small jumps with infinite total variation produce different paths, simulation problems, and hedging exposures. The CGMY family makes these distinctions estimable through one parameter while retaining a tractable characteristic function. Adding an independent Brownian component permits a direct, albeit model-dependent, comparison of continuous and discontinuous variation.

The second contribution is to estimate the family separately from historical returns and option prices, then express the difference through a jump-size-dependent change of measure. This goes beyond comparing physical and implied volatility. The resulting function can price both large positive and large negative jumps more heavily than the historical model does. The empirical evidence is calibration evidence from a small cross-section and a few dates, not a test of a trading strategy. It provides no realized hedge performance, transaction-cost analysis, or out-of-sample forecast comparison.

The paper's central economic interpretation is that jumps account for index variation, while some single stocks have a material diffusion component, and that risk-neutral jump distributions have greater asymmetry and tail weight. Several of the stronger statements require qualification: daily observations do not reveal arbitrarily small jumps directly; Brownian variance cannot change under an equivalent change of measure on a fixed continuous-time process; the fitted historical and option samples differ; and the printed tables contain exceptions to broad textual claims. Those qualifications affect implementation and interpretation without eliminating the usefulness of the family.

## From variance gamma to CGMY

Let $G_t$ be a gamma subordinator, independent of Brownian motion $W$, with $E[G_t]=t$ and $\operatorname{Var}(G_t)=\nu t$. The variance gamma process is

$$
X_t^{VG}=\theta G_t+\sigma W_{G_t},\qquad
E[e^{iuX_t^{VG}}]=(1-i\theta\nu u+\tfrac12\sigma^2\nu u^2)^{-t/\nu}.
$$

Conditioning on the gamma clock gives this characteristic function directly. Factoring its quadratic denominator also represents VG as the difference of two independent gamma processes. Define

$$
a_+=\sqrt{\theta^2\nu^2/4+\sigma^2\nu/2}+\theta\nu/2,
\qquad
a_-=\sqrt{\theta^2\nu^2/4+\sigma^2\nu/2}-\theta\nu/2.
$$

Then $a_+-a_-=\theta\nu$, $a_+a_-=\sigma^2\nu/2$, and the CGMY parameters for the VG subfamily are $C=1/\nu$, $G=1/a_-$, $M=1/a_+$, and $Y=0$. The paper uses the VG coordinates $(\sigma,\nu,\theta)$ as numerical optimization coordinates even when $Y$ is freely estimated. These are not, in that case, an assertion that the full process remains gamma-time-changed Brownian motion.

The generalization replaces the VG denominator $|x|$ by $|x|^{1+Y}$. Its Lévy density, the expected rate of jumps of log size $x$, is

$$
k(x)=\begin{cases}
C e^{-G|x|}|x|^{-1-Y},&x<0,\\
C e^{-Mx}x^{-1-Y},&x>0.
\end{cases}
$$

Here $C>0$ scales activity, $G$ tempers the negative tail, $M$ tempers the positive tail, and $Y$ controls the singularity at zero. The source permits $G,M\geq0$ and $Y<2$. For the all-moment formulas and the empirical setting it is useful to impose $G,M>0$; at an untempered boundary tail integrability needs separate checking. In particular, $Y<2$ is a small-jump condition, not by itself a guarantee of all global moments. The prose on printed p. 311 momentarily reverses the verbal right/left assignments of $G$ and $M$; equation (7) fixes their meaning. If $G<M$, negative jumps have the slower exponential decay.

The classifications follow from integrals near zero, independently of the exponential tail cutoffs:

| Property of the jump component | Parameter region | Integral determining the boundary |
|---|---|---|
| Finite activity | $Y<0$ | $\int_{\lvert x\rvert<1}k(x)dx<\infty$ |
| Infinite activity | $0\leq Y<2$ | The same integral diverges |
| Finite total variation of jumps | $Y<1$ | $\int_{\lvert x\rvert<1}\lvert x\rvert k(x)dx<\infty$ |
| Infinite total variation of jumps | $1\leq Y<2$ | The absolute-jump integral diverges |
| Finite small-jump quadratic variation expectation | $Y<2$ | $\int_{\lvert x\rvert<1}x^2k(x)dx<\infty$ |

Theorem 2 and Table 1 state open regions; the boundary assignments at zero and one in this table are derived by integrating $x^{-1-Y}$ and $x^{-Y}$. VG lies at the infinite-activity, finite-variation boundary $Y=0$. These are properties of the jump component. Adding a nonzero Brownian component makes the full process have infinite total variation even when its jumps have finite variation.

The density on each half-axis is completely monotone for $Y>-1$, because it is a positive mixture of exponential densities. The proof writes

$$
x^{-1-Y}e^{-\beta x}
=\int_\beta^\infty e^{-ax}\frac{(a-\beta)^Y}{\Gamma(1+Y)}\,da,
\qquad x>0.
$$

At $Y=-1$ the density is itself exponential, so complete monotonicity also holds there; this is a direct boundary extension of the printed strict inequality. For $Y<-1$, the density first increases away from zero, precluding complete monotonicity. The representation is a structural property, not evidence that a finite empirical sample can reliably distinguish every nearby $Y$ value.

## Characteristic exponent, stock normalization, and proof qualifications

With the drift convention used in Theorem 1, write

$$
\psi(u)=C\Gamma(-Y)\left[(M-iu)^Y-M^Y+(G+iu)^Y-G^Y\right],
\qquad E[e^{iuX_t}]=e^{t\psi(u)}.
$$

The complex powers must use a consistent analytic branch; positive $G,M$ keep the arguments in the right half-plane for real $u$. Singular-looking gamma factors at $Y=0$ and $Y=1$ require limits of the complete expression. They should not be evaluated as a gamma pole multiplied numerically by a near-zero bracket. At $Y=0$ the limit recovers the VG characteristic function above.

The printed proof on pp. 313–314 starts from $\int(e^{iux}-1)k(x)dx$ and separates gamma integrals. Read literally, the untruncated jump integral is absolutely integrable at zero only for $Y<1$, and the two separated gamma integrals individually require a narrower range before analytic continuation. For $1\leq Y<2$, a valid Lévy–Khintchine construction uses a compensated integral and a corresponding drift. For example, subtracting $iux$ for all jump sizes gives an integrable expression here, with a finite linear drift added to recover the displayed exponent. Thus the exponent can define the intended process throughout the admissible range, but the printed calculation is not an ordinary absolutely convergent integral proof throughout that range. An implementation must fix this drift convention consistently with the exponential normalization, particularly when simulating compensated small jumps.

For statistical expected stock growth $\mu$, define $\omega=-\psi(-i)$ and add independent Brownian motion with coefficient $\eta\geq0$:

$$
S_t=S_0\exp\left[(\mu+\omega-\eta^2/2)t+X_t+\eta W_t\right].
$$

Provided the exponential moment exists, $E[S_t]=S_0e^{\mu t}$. A convenient sufficient restriction for this moment is $M>1$, since the positive jump tail must integrate $e^x$. This restriction is not stated alongside the source's generic parameter domain. Risk-neutral pricing replaces $\mu$ by the continuously compounded risk-free rate $r$ and uses separately fitted parameters denoted with tildes. A dividend yield would need a consistent carry adjustment; the displayed source equations omit an explicit dividend-yield term.

The complete log-stock characteristic function implied by this construction is

$$
\Phi_{\log S_t}(u)=
\exp\left(iu[\log S_0+(\mu+\omega-\eta^2/2)t]+t\psi(u)-\eta^2u^2t/2\right).
$$

Printed equations (15) and (17) omit $t$ from the final Gaussian factor, and suppress the time argument of the CGMY factor. The $t$ in the Gaussian factor above is a derived correction: $\operatorname{Var}(\eta W_t)=\eta^2t$. This matters for daily density inversion and for options with maturities different from one model-time unit. The source does not provide code with which to determine whether its numerical calculations used the printed or time-consistent expression.

For a European payoff, the model price is its discounted expectation under the fitted risk-neutral law. The paper evaluates option prices through Fourier methods and estimates parameters by nonlinear least squares. It refers to Carr–Madan's Fourier pricing algorithm; it does not reproduce all damping, grid, and quadrature settings needed to reproduce that implementation exactly.

## Moments and variation: formulas suitable for implementation

For $G,M>0$, integration of positive and negative jump powers gives the cumulants per unit time. Set

$$
v=\eta^2+C\Gamma(2-Y)\left[M^{Y-2}+G^{Y-2}\right],
$$

$$
c_3=C\Gamma(3-Y)\left[M^{Y-3}-G^{Y-3}\right],
\qquad
c_4=C\Gamma(4-Y)\left[M^{Y-4}+G^{Y-4}\right].
$$

At horizon $t$, the variance is $tv$, standardized skewness is $c_3/(\sqrt{t}v^{3/2})$, and kurtosis is $3+c_4/(tv^2)$. Consequently a nearly Gaussian annual distribution can coexist with sharply peaked daily returns. The horizon must accompany any quoted kurtosis; annualized volatility does not make skewness and kurtosis invariant to aggregation.

Two printed errors require explicit separation from these derived formulas. The general third-central-moment display on p. 317 includes an added $\eta^2$, although a centered independent Gaussian has zero third cumulant. Equation (19) then adds the negative-tail contribution instead of subtracting it. Odd powers of negative jumps have the opposite sign, and the correct difference vanishes for $G=M$. The paper's tables contain negative skewness, which the printed positive-sum formula could never produce. That establishes an inconsistency, not knowledge of the actual calculation used to produce every table entry.

For the log process, realized quadratic variation is

$$
[X+\eta W]_t=\eta^2t+\sum_{s\leq t}(\Delta X_s)^2.
$$

The jump sum is random. Its expectation and predictable compensator are $t(v-\eta^2)$. The diffusion share used by the paper is therefore

$$
f_D=\frac{\eta^2}{\eta^2+C\Gamma(2-Y)[M^{Y-2}+G^{Y-2}]}.
$$

It is a fitted share of expected quadratic variation, not an observed pathwise fraction. Nor does it identify the proportion of option premium attributable to Brownian risk: valuation depends on the whole risk-neutral distribution and payoff, not only its second moment.

## Historical and option estimation designs

The historical sample is stated as January 1, 1994–December 31, 1998, using daily log price relatives, demeaned before estimating $(\sigma,\nu,\theta,\eta,Y)$. Data came from Morgan Stanley Dean Witter. The named stock universe is AMZN, BA, GE, HWP, IBM, INTC, JNJ, MCD, MMM, MRK, MSFT, WMT, and XON; the eight indices are BIX, BKX, DRG, RUT, SPX, SOX, XAU, and XOI. However, Tables 2 and 4 contain twelve stocks and eight indices, omitting AMZN. The distinction between the stated 21-name universe and the 20 reported historical fits must be preserved. The paper does not give an explicit exclusion rule explaining this omission or observation counts by name.

Rather than invert a characteristic function separately at each observation during every optimization iteration, the authors invert once on an equally spaced return grid, then group observations by their nearest grid point. With Fourier-frequency spacing $0.25$ and $N$ FFT points, the return spacing is $8\pi/N$. They reject $N=4096$, which gives $0.00613592$, as too coarse, and use $N=16384$, giving $0.00153398$. The latter is approximately 15.34 basis points of log return. If $n_j$ observations map to grid point $x_j$, the operational objective is the binned log likelihood

$$
\ell(\vartheta)=\sum_j n_j\log f_\vartheta(x_j),\qquad
\vartheta=(\sigma,\nu,\theta,\eta,Y).
$$

A common bin-width factor would not affect maximization. Evaluating a density at a bin center is still an approximation to integrating the density over the bin. In a very sharply peaked distribution, bin width can therefore influence the apparent small-jump structure. The source gives one chosen grid, not a systematic grid-refinement robustness study. It also does not specify the optimizer, initial values, constraints imposed in code, stopping tolerance, calendar-to-model-time conversion, or handling of nonpositive numerical density values.

Interior standard errors use the inverse information matrix. When $\eta=0$ is estimated at its boundary, the remaining standard errors are conditional on that boundary fit, using a partial information matrix. Some entries are unavailable because the estimated information matrix is not positive definite. For testing a zero diffusion coefficient, the paper uses the King–Wu locally mean most powerful boundary test. It describes the reported positive $Z$ statistic as standard normal under the null. This is preferable to mechanically interpreting a symmetric Wald interval for a nonnegative coefficient, although the paper does not state one uniform decision level for its verbal significance claims.

The option cross-section consists of AMZN, IBM, INTC, MSFT, and SPX on October 14, November 11, and December 9, 1998, and January 13 and February 10, 1999. Only out-of-the-money options are used. The text specifies one- to two-month maturities; Table 3's caption instead identifies a maturity of $0.1014$ years, approximately 37 days. It does not reconcile this caption with all five dates. Where quotes are American, the authors first infer volatility in a finite-difference American model and then compute a European price using that volatility. The calibration target is thus a Europeanized midquote, not necessarily a directly traded European price.

Risk-neutral parameters minimize nonlinear least-squares pricing errors, with the average pricing error reported as APE. The paper supplies neither a full strike-by-strike dataset nor contract counts, bid–ask filters, open-interest screens, interest/dividend inputs, objective weights, or parameter standard errors for these fits. It does not define APE as a percentage, so the numerical values below retain the source's label instead of assigning percentage units. The American-to-European adjustment adds model dependence that is not separately tested.

A reproducible reconstruction would first recover these missing market inputs and numerical conventions. It would then use independent checks of the characteristic function at $u=0$ and $u=-i$, density normalization, nonnegative integrated bin probabilities, and the finite-difference behavior of analytic cumulants. These are implications of the equations, not checks reported as performed by the authors. They are particularly relevant because of the printed formula inconsistencies.

## What the estimates show, and how strongly

The historical SPX fit in Table 2 has $\sigma=0.0739$, $\nu=0.0403$, $\theta=-0.0042$, $\eta=1.9\times10^{-10}$, and $Y=0.2495$ with standard error $0.2082$. The transformed parameters are $C=24.79$, $G=94.45$, and $M=95.79$; the log likelihood is $4258.5$. This is an essentially zero fitted diffusion and an infinite-activity, finite-variation point estimate, but $Y=0$ is not clearly excluded by a simple estimate-to-standard-error comparison. RUT gives $Y=0.3196$ with standard error $0.1831$ and similarly negligible $\eta$.

The point estimates are not uniformly finite variation. BIX has $Y=1.2341$ with no reported standard error, SOX has $Y=1.3814$ with standard error $0.0591$, MCD has $Y=1.50683$ with standard error $0.1449$, and MMM is just above the boundary at $1.0023$ with standard error $0.1592$. Thus the discussion's broad statements about indices need to be read against the actual table. BIX and SOX have infinite-variation point estimates. MMM's location near one is particularly uncertain. On the other side, BA, INTC, and WMT have negative $Y$ estimates, respectively $-0.0719$, $-0.7904$, and $-0.0963$, with large standard errors $0.3461$, $0.6356$, and $0.6482$. These point estimates are finite activity, but they do not establish a strong rejection of VG.

MSFT has the largest reported historical diffusion component: $\eta=0.3815$ with standard error $0.3288$, and the text attributes 62.29% of its expected quadratic variation to diffusion. The corresponding reported diffusion shares are 15.32% for BA, 1.48% for GE, 12.60% for HWP, 0.71% for IBM, 0.23% for JNJ, and 2.61% for WMT. These shares have no reported confidence intervals. The boundary-test $Z$ values for IBM and MSFT are 1.7919 and 1.8599. Under the stated standard-normal positive-tail interpretation, these exceed a one-sided 5% threshold of approximately 1.645, though not 1.96. Consequently the prose description of all positive stock diffusion estimates as insignificant depends on the significance convention; it is not a threshold-free finding.

Figures 2–6 show fitted daily densities and empirical density points. SPX and RUT have narrow, high peaks around zero; MSFT and XAU are broader, and BA illustrates a mixed shape. The visual fit is informative about the center, but it is not a formal goodness-of-fit test. The paper reports no held-out likelihoods, return-dependence diagnostics, or comparison with stochastic-volatility alternatives. An iid Lévy increment model can absorb time variation in volatility into an unconditional mixture-like return shape; the figures alone do not identify the unique structural source of that shape.

The following selected moments are reported in Tables 4 and 5. Volatility is in return units, so 0.1253 corresponds to 12.53% over the model's unit horizon. These are fitted model moments, not raw daily sample moments; the formulas on p. 317 explicitly refer to time one.

| Model and observation | Volatility | Skewness | Kurtosis |
|---|---:|---:|---:|
| Historical SPX | 0.1253 | −0.0028 | 3.0339 |
| Historical RUT | 0.1168 | −0.0047 | 3.0399 |
| Historical IBM | 0.2385 | −0.0461 | 3.0818 |
| Historical MSFT | 0.4834 | 0.00006 | 3.0008 |
| Risk-neutral SPX, October 14 | 0.3999 | −0.6297 | 3.6540 |
| Risk-neutral SPX, November 11 | 0.2706 | −0.8196 | 4.1693 |
| Risk-neutral SPX, December 9 | 0.2453 | −0.7068 | 3.8643 |
| Risk-neutral SPX, January 13 | 0.2849 | −0.6263 | 3.6746 |
| Risk-neutral SPX, February 10 | 0.3198 | −0.4077 | 3.2699 |

The SPX comparison supports greater risk-neutral volatility, negative asymmetry, and excess kurtosis on these selected dates. It does not hold the economic environment fixed: the historical fit spans five years, while each option fit is a short-maturity cross-section around late 1998 or early 1999. The source's prose calls November SPX excess kurtosis 1.693, while Table 5 implies $4.1693-3=1.1693$. The latter is the table-based value, and the discrepancy should not be silently propagated.

Risk-neutral SPX estimates also illustrate uncertainty about categorical labels. Across the five dates, $Y$ is $-0.0901$, $0.1432$, $-0.0008$, $0.2227$, and $0.2155$. Values close to zero are nearly VG, not compelling evidence that every distribution lies strictly in one activity class. IBM on November 11 has $Y=1.0102$, slightly above the finite-variation boundary. AMZN and MSFT have some negative estimates. The source's characterization of the risk-neutral fits as essentially infinite activity and finite variation is a broad description, not a literal statement about all point estimates.

The corresponding SPX APE values are 0.3123, 0.5459, 0.1324, 0.5379, and 0.0632. The authors select the three best-fitting dates per asset to discuss risk-neutral diffusion shares and state that these shares are zero. Yet Table 3 reports SPX diffusion coefficients 0.0312, 0.0254, and 0.0189 for October, December, and February, precisely those three dates. Combining these with Table 5 gives derived fractions of approximately 0.61%, 1.07%, and 0.35%. These are small, but positive. This check uses rounded printed entries, not an independent re-estimation. The stronger claim of exactly zero variation is not reproduced by those entries.

Other table inconsistencies constrain a mechanical replication. Historical INTC has $\nu=0.0020$ but $C=4.94$ in Table 2, although the stated transformation requires $C=1/\nu$, approximately 500. Its Table 4 volatility is 0.0196 and kurtosis 16.1960, making it a conspicuous outlier. One cannot choose which entry to repair without underlying estimates. In Table 3, INTC on November 11 has positive printed $\theta=0.7767$ while $G=18.67<M=31.23$, inconsistent with the stated VG transformation's skew direction. AMZN on January 13 has positive $\theta=0.1727$ and positive Table 5 skewness 0.0165, so a blanket assertion that every option fit is negatively skewed also has an explicit exception.

## Measure changes and the interpretation of jump risk prices

Use $R(x)$ for the density ratio to avoid confusing it with the activity parameter $Y$. If the risk-neutral Lévy density is $k_Q(x)$ and the physical density is $k_P(x)$, define $R(x)=k_Q(x)/k_P(x)$. With a finite jump cutoff $\epsilon>0$, equation (24) becomes

$$
R(x)=\frac{\widetilde C}{C}|x|^{Y-\widetilde Y}
\begin{cases}
\exp[-(\widetilde G-G)|x|],&x<-\epsilon,\\
\exp[-(\widetilde M-M)x],&x>\epsilon.
\end{cases}
$$

The power $Y-\widetilde Y$ follows by dividing the two densities. The visual source equation has this direction correctly; text extraction can scramble its tilde placement. For the truncated compound-Poisson processes the path likelihood ratio is

$$
L_t=\exp\left[-t\int_{|x|>\epsilon}(R(x)-1)k_P(x)\,dx\right]
\prod_{s\leq t:\,|\Delta X_s|>\epsilon}R(\Delta X_s).
$$

The exponential adjusts for the different total jump intensity, and the product reweights realized jumps by size and sign. This is the finite-activity interpretation emphasized on pp. 312–313 and 318–319. It avoids assuming that arbitrarily fitted infinite-activity laws are equivalent at the origin. In the infinite-activity CGMY setting, changing the leading small-jump scale or exponent generally violates the equivalence integrability condition; this is why the paper explicitly introduces the cutoff. An implementer must state the cutoff and small-jump treatment rather than treating the ratio as an unrestricted exact change of measure for the untruncated fitted paths.

There is a further distinction for the diffusion extension. Equivalent changes of measure preserve continuous quadratic variation; they may change Brownian drift but cannot turn a positive constant diffusion coefficient into zero. Separately estimated $\eta$ and $\widetilde\eta$ therefore do not automatically define one physical process and its equivalent pricing measure. The paper's diversification explanation is an economic conjecture about the fitted models, not a mathematical justification for changing that path property. The cutoff addresses infinite jump activity, not this Brownian invariance issue.

Figure 7 plots the SPX ratio for January 13, 1999: it rises for large moves on both sides, more sharply on the negative side. Figure 8 gives a more symmetric U shape for MSFT on December 9, 1998. Figure 9 for INTC on October 14, 1998 shows especially large reweighting of negative moves. The vertical scales differ greatly, so the visual steepness should not be compared without its axis. These are jump-intensity ratios, not ordinary terminal-return density ratios or direct expected excess returns on a specific option portfolio.

For interpretation, the paper writes a ratio involving marginal utility of the investor's position and subjective-to-objective jump beliefs. With rational beliefs and an investor holding only the stock, concave utility gives a ratio decreasing with a positive stock move. That alone cannot generate the U shapes. If a marginal investor instead holds a delta-hedged short-option position $g(x)$, with $g'(0)=0$ and $g''(0)<0$, the position has a local inverted-U shape, and concavity makes its marginal utility rise in both tails. This can rationalize a U-shaped $R(x)$. The authors conjecture that put and call open interest shapes the relative sides. They do not estimate the investor's utility, positions, subjective beliefs, or an open-interest regression, so this remains an interpretation rather than an identified equilibrium mechanism.

## What can be carried into a pricing or risk system

The durable deliverable is a characteristic-function family with explicit control over activity and variation, an FFT estimation route, and a transparent jump-size reweighting formula. It supports a coherent implementation once the drift convention, horizon, moment restrictions, and numerical limits at $Y=0,1$ are specified. Historical and option calibration should remain distinct estimates until restrictions that make them one admissible measure-change pair are checked.

The empirical paper supplies neither trading rules nor portfolio weights, rebalancing dates, execution costs, hedge instruments, or realized hedging errors. There is consequently no basis to infer a profitable volatility trade from its physical/risk-neutral differences. The relevant uncertainty is parameter and model uncertainty: five option dates, conditional boundary standard errors, some nonpositive-definite information matrices, an unreported historical exclusion, no option parameter intervals, and several printed numerical inconsistencies. A production calibration could use the family, but reproducing this particular set of reported fits requires the missing data and numerical conventions, not merely transcribing the tables.

## Source map and bibliography

The source's pp. 305–308 motivate the diffusion/jump comparison; pp. 309–314 derive VG, CGMY, the characteristic function, and path classifications; pp. 315–319 define stock dynamics, moments, variation, and measure changes; pp. 319–321 give data and estimation; Tables 2–5 and Figures 2–9, pp. 322–331, contain the empirical estimates and interpretations. The publication ends with conclusions and references on pp. 331–332. No additional empirical appendix or code is supplied.

Carr, P., H. Geman, D. B. Madan, and M. Yor (2002), “The Fine Structure of Asset Returns: An Empirical Investigation,” *Journal of Business* 75(2), 305–332, is the sole source read for this note. Methodological dependencies cited by that source include Carr and Madan (1998), “Option Valuation Using the Fast Fourier Transform”; Madan, Carr, and Chang (1998), “The Variance Gamma Process and Option Pricing”; and King and Wu (1997), “Locally Optimal One-Sided Tests for Multiparameter Hypotheses.” Their complete algorithms and proofs are not reproduced in the supplied paper and were not independently reviewed here.
