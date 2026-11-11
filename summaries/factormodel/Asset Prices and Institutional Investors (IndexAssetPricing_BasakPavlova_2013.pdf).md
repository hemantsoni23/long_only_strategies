# Asset Prices and Institutional Investors

**Authors:** Suleyman Basak and Anna Pavlova. **Source version:** August 2012 manuscript, despite the 2013 year in the library filename. **Source:** [IndexAssetPricing_BasakPavlova_2013.pdf](../../Finance/IndexAssetPricing_BasakPavlova_2013.pdf), 62 pages: title page, main text pp. 1–35, references pp. 36–39, and included online appendix pp. X1–X22. The complete source, including Appendices A–D, was inspected. Main-text page numbers are one below PDF page numbers; X1 starts at PDF page 41. This is a theoretical equilibrium paper with illustrative calibrations, not an empirical estimation or causal event study.

## Why this matters and the actual contribution

Benchmark incentives can alter prices and covariance without changing beliefs or the underlying dividends. An institution whose marginal value of additional wealth is especially high when its benchmark performs well demands a portfolio that pays in those states. In equilibrium, its extra demand raises the prices of benchmark constituents and creates a shared return component. Institutions also gain wealth relative to ordinary investors after favorable benchmark news, reinforcing the demand effect. The model produces an index premium, greater constituent volatility, excess within-index correlation, and a countercyclical market Sharpe ratio in closed form.

The contribution is not simply that benchmarked managers overweight their benchmark. Earlier agency and portfolio-choice models already establish that possibility. The distinctive combination is tractable dynamic equilibrium, multiple risky assets, endogenous wealth redistribution and analytically transparent covariance implications. Constant-absolute-risk-aversion models suppress the wealth effects central here; more conventional relative-performance preferences often require numerical equilibrium solutions. Basak and Pavlova obtain explicit formulas by adopting logarithmic utility multiplied by an affine function of the terminal index.

The distinction between primitive preferences and derived quantities matters. “Institutions” denotes professional managers with benchmark-dependent objectives; the paper does not fully model the households who delegate to them, endogenous fund formation, fees negotiated in equilibrium, heterogeneous skill or investor learning. The main model assumes frictionless complete markets. The resulting extra covariance is an equilibrium response to preferences and wealth, not an execution-cost or temporary order-book impact model. It can inform risk-model design, but it does not deliver an estimated trading-impact coefficient.

## One-stock economy: primitives and objective

Time is continuous on $[0,T]$. A single stock, in unit positive net supply, pays a terminal dividend $D_T$ and no intermediate dividends. A zero-net-supply bond has interest rate zero. There is no intermediate consumption, so the interest-rate normalization does not suppress an independently determined consumption-saving condition. The dividend-news process follows

$$
dD_t=\sigma D_t\,dB_t,\qquad \sigma>0,
$$

and the endogenous stock price follows

$$
dS_t=S_t(\mu_{S,t}\,dt+\sigma_{S,t}\,dB_t),\qquad S_T=D_T.
$$

$D_t$ is news about the eventual payoff, not a flow of distributed cash. Its physical drift is initially zero. Dividend growth and a nonzero constant interest rate are added in Appendix B. The stock diffusion must be nonzero so that stock and bond span the one Brownian shock.

At time zero the institution owns a fraction $\lambda$ of the stock and the retail investor owns $1-\lambda$, giving $W_{I0}=\lambda S_0$ and $W_{R0}=(1-\lambda)S_0$. This is an initial endowment share; the institution's subsequent wealth share is stochastic and generally differs from $\lambda$. Each chooses a self-financing stock weight $\phi_i$, so

$$
dW_{it}=\phi_{it}W_{it}(\mu_{S,t}\,dt+\sigma_{S,t}\,dB_t).
$$

The expected terminal objectives are

$$
E[\log W_{RT}],\qquad E[(1+bD_T)\log W_{IT}],\quad b>0.
$$

The general affine coefficient $a+bD_T$ is normalized to $a=1$, since only $b/a$ affects choices. The key property is $\partial^2u_I/\partial W\partial D_T=b/W>0$: institutions especially value wealth in high-benchmark states. This is a reduced-form representation of relative-performance incentives, not log utility of the wealth-to-index ratio. Indeed, $\log(W/I)=\log W-\log I$ would leave marginal utility of wealth unchanged and would not produce the mechanism.

Whether the level of utility rises or falls with the benchmark is not decisive for portfolio choice. Adding a benchmark-only term changes utility levels but leaves $u_W$ unchanged. The paper uses this observation to reconcile its convenient form with contracts that penalize a manager when the benchmark outperforms. A specification based on the return $S_T/S_0$ produces analogous results but requires solving for the endogenous initial price appearing in the preference coefficient. The baseline formulas below apply to benchmark levels, as in Sections 2–3.

## Solving individual choice and the pricing kernel

Let $\xi_t$ be the state-price density, normalized arbitrarily at time zero. With zero interest it is a martingale satisfying

$$
d\xi_t=-\xi_t\kappa_t\,dB_t,\qquad
\kappa_t=\mu_{S,t}/\sigma_{S,t}.
$$

Complete markets turn dynamic budget feasibility into $E[\xi_TW_{iT}]=\xi_0W_{i0}$. First-order conditions give $W_{IT}=(1+bD_T)/(y_I\xi_T)$ and $W_{RT}=1/(y_R\xi_T)$. Budget constraints determine the multipliers because $E[D_T]=D_0$:

$$
W_{IT}=\frac{\lambda\xi_0S_0}{\xi_T}\frac{1+bD_T}{1+bD_0},\qquad
W_{RT}=\frac{(1-\lambda)\xi_0S_0}{\xi_T}.
$$

Conditional expectations then give deflated wealth processes

$$
\xi_tW_{It}=\lambda\xi_0S_0\frac{1+bD_t}{1+bD_0},\qquad
\xi_tW_{Rt}=(1-\lambda)\xi_0S_0.
$$

Match the Brownian terms in these identities to the wealth equations to obtain Lemma 1:

$$
\phi_{Rt}=\frac{\mu_{S,t}}{\sigma_{S,t}^2},\qquad
\phi_{It}=\frac{\mu_{S,t}}{\sigma_{S,t}^2}
+\frac{bD_t}{1+bD_t}\frac{\sigma}{\sigma_{S,t}}.
$$

Both hold the instantaneous mean–variance portfolio; only the institution holds the positive benchmark-hedging increment. “Hedging” here means hedging an incentive to match favorable index outcomes, which increases rather than reduces stock exposure. This derivation also makes clear that the extra demand is state dependent, even though local relative risk aversion with respect to wealth is one for both agents.

Terminal goods-market clearing requires $W_{IT}+W_{RT}=D_T$. Define $A=1+(1-\lambda)bD_0$ and $C=\xi_0S_0/(1+bD_0)$. Then

$$
\xi_T=C\left(\frac{A}{D_T}+\lambda b\right),\qquad
\xi_t=C\left(\frac{Ae^{\sigma^2(T-t)}}{D_t}+\lambda b\right).
$$

The constant term is the institutional contribution to the kernel. Relative to the retail-only inverse-dividend kernel, it reduces sensitivity to poor aggregate outcomes. Prices follow from $S_t=E_t[\xi_TD_T]/\xi_t$. This terminal-allocation route is the model's computational shortcut: no nonlinear dynamic-programming equation needs to be solved for the baseline equilibrium. Appendix A supplies the formal derivations.

## Exact price, volatility and risk premium

For implementation define $\tau=T-t$, $q=e^{-\sigma^2\tau}$, $X=A+\lambda bD_t$ and $Z=A+\lambda bqD_t$. Propositions 1, 2 and 4 become

$$
\overline S_t=qD_t,\qquad S_t=qD_t\frac{X}{Z},
$$

$$
\sigma_{S,t}=\sigma+\frac{\lambda b\sigma(1-q)AD_t}{ZX},
\qquad
\kappa_t=\sigma\frac{A}{Z},\qquad
\mu_{S,t}=\kappa_t\sigma_{S,t}.
$$

Bars denote the otherwise identical retail-only economy, equivalently $b=0$. With $b>0$, $\lambda>0$ and $t<T$, the price and volatility exceed the retail-only values and the Sharpe ratio is lower. All prices converge to the same terminal dividend; the premium therefore disappears at maturity. The positive institutional price effect is not an arbitrary additive distortion: it is consistent with a different stochastic discount factor and with both agents' optimal choices.

Volatility follows by applying Itô's lemma to $S=\overline S X/Z$: its diffusion loading is $\sigma+\sigma_X-\sigma_Z$. The excess term is positive because $q<1$. The Sharpe ratio follows directly from the negative diffusion of $\xi$. These checks are simpler and less error prone than differentiating the expanded stock-price formula twice. Expected returns should be obtained through $\mu_S=\kappa\sigma_S$ or an independently checked Itô drift calculation.

Sharpe ratios fall as $D_t$ rises and as the institutional initial share increases. Good news shifts wealth toward the investor willing to bear more benchmark risk. Expected returns need not inherit every monotonicity of the Sharpe ratio: volatility rises while the Sharpe ratio falls. The authors find the Sharpe effect dominates in their usual calibrations, but explicitly give $T=50$ as a case in which expected returns can rise for small institutional shares. A universal claim that institutional ownership lowers conditional expected returns would overstate the theorem.

Volatility and borrowing can be hump shaped in institutional size. At small $\lambda$, expanding institutions increases risk demand and borrowing; at large $\lambda$, there are fewer retail counterparties to lend. This does not imply volatility returns exactly to its retail-only level at $\lambda=1$: an economy entirely populated by benchmark-sensitive investors still has a different kernel. Borrowing, by contrast, is zero at both homogeneous endpoints because the bond has zero net supply. The article's Figure 1 indeed shows volatility still above its benchmark at the all-institution endpoint.

## Wealth redistribution, portfolios and a numerical checkpoint

Equilibrium wealth shares follow directly from deflated wealth:

$$
\frac{W_{It}}{S_t}=\frac{\lambda(1+bD_t)}{X},\qquad
\frac{W_{Rt}}{S_t}=\frac{(1-\lambda)(1+bD_0)}{X},
$$

$$
\frac{W_{It}}{W_{Rt}}=\frac{\lambda}{1-\lambda}\frac{1+bD_t}{1+bD_0}.
$$

The institution gains relative wealth after positive dividend news. Its weight in stock exceeds one for $0<\lambda<1$, whereas the retail investor lends. Number of shares is $n_i=\phi_iW_i/S$; converting weights to shares is necessary for market clearing and for interpreting Figure 2. The institution buys shares after favorable news and the retail investor sells. This is a wealth effect, not a change in fundamental beliefs or a mechanically imposed fund-flow rule.

Figure 1's baseline is $b=1$, $D_0=1$, $\sigma=0.15$, $t=1$, $T=5$. The institutional-size plot holds $D_t=2$; the state plot holds $\lambda=0.2$. Substituting both state values yields the following independently calculated checkpoint from the paper's equations, not an empirical estimate or a tabulated source result:

| Quantity | Value |
|---|---:|
| Retail-only price | 1.827862 |
| Institutional-equilibrium price | 1.856921 |
| Price increase relative to retail-only | 1.5898% |
| Return volatility | 0.151951 versus 0.150000 |
| Instantaneous Sharpe ratio | 0.124678 versus 0.150000 |
| Expected return, zero interest | 0.018945 versus 0.022500 |
| Institutional wealth share | 0.272727, from initial 0.20 |
| Retail stock weight | 0.820516 |
| Institutional stock weight | 1.478623 |
| Institutional bond position | −0.242390 in price units |

The small volatility increase is deliberate: the paper acknowledges that logarithmic preferences produce modest magnitudes and conjectures that higher risk aversion or habit might increase them. The example should not be presented as a fitted explanation of actual stock-market volatility. The institutions' leverage is endogenous borrowing between the two types, not a haircut constraint or banking balance-sheet multiplier.

## Multiple stocks: what must be specified carefully

Section 4 introduces $N$ Brownian shocks, $N$ risky stocks and a bond. Stock-volatility matrix $V_t$ has one stock's Brownian loadings per row; mean returns form the column vector $\mu_t$. The first $M$ stocks form the value-weighted benchmark, whose level is the sum of their share prices. Aggregate terminal cash flow is $D_T$ and benchmark terminal cash flow is $I_T$, with news processes

$$
dD_t=D_t\sigma^\top dB_t,\qquad
dI_t=I_t\sigma_I^\top dB_t.
$$

For the individually specified stocks, $dD_{jt}=D_{jt}\sigma_j^\top dB_t$. Their fundamental shocks are taken to be mutually orthogonal, and nonindex names have $\sigma_j^\top\sigma_I=0$, while index names have a positive loading on index news. All loadings are constant. The institution now maximizes $E[(1+bI_T)\log W_{IT}]$ and initially owns fraction $\lambda$ of the whole market, not just the benchmark.

A substantial modeling qualification is footnote 14: the $M$th and $N$th dividends are residual claims chosen to reconcile the aggregate processes with sums of individual dividends. They are not independent constant-volatility geometric Brownian motions like the other individually specified names. A sum of independent lognormals is not itself a single geometric Brownian motion. Accordingly, Propositions 6–7 explicitly state individual-stock formulas for $j=1,\ldots,M-1$ and $k=M+1,\ldots,N-1$. A simulation must construct and inspect residual payoffs and prices; it cannot simultaneously simulate all names as independent GBMs and impose the specified aggregate GBMs. Positivity and economically acceptable behavior of residual claims are additional implementation checks not fully developed in the paper.

Assuming an invertible $V$, the optimal weights are

$$
\phi_R=(VV^\top)^{-1}\mu,\qquad
\phi_I=(VV^\top)^{-1}\mu+\frac{bI_t}{1+bI_t}V^{-\top}\sigma_I.
$$

The second term exactly spans index-news exposure. The proof of Lemma 2 temporarily substitutes the traded index for one stock, observes that its diffusion is collinear with $\sigma_I$, and then maps the index holding back into its constituent stocks. This yields a three-fund decomposition: mean–variance portfolio, benchmark-hedging portfolio and bond. The extra portfolio has positive index weights and zero nonindex weights in the baseline model. The main-text lemma's reference to index stocks through $N-1$ conflicts with its own definition of only $M$ index constituents; use the established index membership, not that printed range.

## Multi-stock prices and the asset-class covariance effect

For this section redefine $A=1+(1-\lambda)bI_0$, $L=\lambda bI_t$, $c=\sigma_I^\top\sigma$, $h_j=\sigma_j^\top\sigma_I$ and $\tau=T-t$. Then the formulas of Proposition 6 can be implemented as

$$
S_{MKT,t}=e^{-\|\sigma\|^2\tau}D_t
\frac{A+L}{A+Le^{-c\tau}},
$$

$$
S_{jt}=e^{-\sigma_j^\top\sigma\tau}D_{jt}
\frac{A+Le^{(-c+h_j)\tau}}{A+Le^{-c\tau}}.
$$

For a nonindex name with $h_j=0$, numerator and denominator cancel and the price equals its retail-only value. For an ordinary index name with $h_j>0$, the multiplicative ratio exceeds one before maturity. The cancellation depends on the stated orthogonality structure; it is not a general theorem that nonindex assets in every benchmark economy are unaffected.

Define $B_0=Le^{-c\tau}$ and $B_j=Le^{(-c+h_j)\tau}$. Differentiating the price gives the particularly convenient diffusion expression

$$
v_j=\sigma_j+f_j\sigma_I,\qquad
f_j=\frac{B_j}{A+B_j}-\frac{B_0}{A+B_0}.
$$

For index stocks $f_j>0$; for the orthogonal nonindex stocks it is zero. This is algebraically equivalent to Proposition 7's longer expression. The market loading is

$$
v_{MKT}=\sigma+\left(\frac{L}{A+L}-\frac{B_0}{A+B_0}\right)\sigma_I.
$$

Build the covariance matrix from the rows $v_j$, using $VV^\top$, and correlations from normalized inner products. For distinct ordinary index stocks with independent fundamentals,

$$
v_j^\top v_\ell
=f_\ell\sigma_j^\top\sigma_I+f_j\sigma_\ell^\top\sigma_I
+f_jf_\ell\|\sigma_I\|^2>0.
$$

This expansion uses the correctly crossed coefficients; the proof's displayed A37 labels the two linear terms differently, which does not affect its positivity argument but should not be copied literally for unequal stocks. The common index-news component generates excess correlation even though the fundamental shocks were orthogonal. Both its strength and the institutional wealth distribution vary with the state. Correlations can be hump shaped rather than monotonically increasing in every state or institutional share.

Figure 5 uses $M=3$, $N=6$, ordinary constituent loadings $\sigma_j=0.15e_j$, $\sigma_I=0.15(e_1+e_2+e_3)/\sqrt3$, and $\sigma=0.15\mathbf1/\sqrt6$, with $I_0=1$, $I_t=2$, $D_t=5$ and the earlier horizon/preferences. The square-root normalizations hold aggregate volatility norms fixed when the number of assets changes. Figure 6 uses two ordinary index names, 1 and 2, and nonindex names $M+1$ and $M+2$, avoiding the residual claims. Individual cash-flow levels must also be supplied for price-level plots; they should not be silently inferred from the aggregate level if the caption does not explicitly give them.

## Recovering expected returns and the benchmark portfolio

Appendix A32 also supplies the missing bridge from the price and covariance formulas to expected returns. With the notation above, the multi-stock state-price density is

$$
\xi_t=C\frac{e^{\|\sigma\|^2\tau}}{D_t}(A+B_0),
\qquad C=\frac{\xi_0S_{MKT,0}}{1+bI_0}.
$$

Its Brownian diffusion yields the vector market price of risk

$$
\kappa_t=\sigma-\frac{B_0}{A+B_0}\sigma_I,
\qquad \mu_t=V_t\kappa_t.
$$

These are direct algebraic consequences of the source's equilibrium kernel and the zero-interest no-arbitrage relation. They make the multi-stock model executable without estimating a separate expected-return process. For each ordinary name, calculate its loading $v_j$, then use $\mu_j=v_j^\top\kappa$. Volatility is $\|v_j\|$ and its instantaneous Sharpe ratio is $\mu_j/\|v_j\|$. That scalar is generally different from the norm of the vector price of risk, which describes the maximum instantaneous Sharpe ratio available across the complete opportunity set. Comparing those quantities without distinguishing them would create an artificial discrepancy.

The traded index can be priced by the same claim-pricing operation with terminal payoff $I_T$:

$$
S_{I,t}=e^{-c\tau}I_t
\frac{A+L e^{(\|\sigma_I\|^2-c)\tau}}{A+L e^{-c\tau}}.
$$

This is the ordinary-claim formula with its payoff loading set to $\sigma_I$, as the appendix's proof of the portfolio separation result requires. The index diffusion is consequently collinear with $\sigma_I$, making it a perfect hedge for index-news risk even though its level is not simply $I_t$ before maturity. Confusing dividend news $I_t$ with traded benchmark value $S_{I,t}$ would give the wrong hedging weight.

The same budget identities give institutional wealth share $\lambda(1+bI_t)/(A+L)$ and retail wealth share $(1-\lambda)(1+bI_0)/(A+L)$. Use these wealth levels together with portfolio weights to check share clearing, including the two residual stocks. In code, a useful independent verification is to price each residual payoff by subtracting constituent prices from the appropriate aggregate price, then differentiate that residual price and compare aggregate exposures. The source's claims are conditional on an admissible spanning economy; neither a nonsingular matrix nor positive residual cash flows follows merely from choosing arbitrary GBM coefficients. A numerical experiment violating those restrictions is outside the model even if its ordinary-stock formulas return finite numbers.

The analytical comparative statics should also be separated from finite-difference exercises in which several primitives move together. Increasing $\lambda$ means changing initial institutional ownership while keeping preference intensity, payoff dynamics, and the terminal horizon fixed. Increasing $I_t$ changes the current news state after the initial allocation, so it also changes the endogenous distribution of wealth. Increasing $b$ changes the objective itself. Although each can increase index demand, they are different experiments and need not yield identical volatility or correlation profiles.

A transparent numerical reconstruction would first reproduce the single-stock cross-sections at the stated fixed horizon, then build the multi-stock loadings and current payoff state, and only then compute shares, correlations, and expected returns. At each grid point retain the retail-only values from the same payoff state as the comparison. Comparing an institutional equilibrium at high dividends against a benchmark at low dividends would confound the institutional premium with fundamental news. Likewise, an apparent change in correlation caused by changing the normalization of aggregate loading vectors would not isolate the model's asset-class effect.

The equilibrium has no estimated sampling uncertainty: confidence intervals on the analytical curves would require an additional statistical model for the primitives. Sensitivity to $b$, ownership, horizon, and loading assumptions is therefore the appropriate uncertainty analysis within the paper's own design. Empirically identifying those primitives from observed institutional holdings is a further inverse problem, because holdings and wealth shares are endogenous outcomes rather than direct observations of preference intensity.

## Extensions, policy experiments and their scope

Appendix B allows constant dividend drift $\mu_D$ and interest rate $r$. Replace current news in the preference terms by $D'_t=e^{\mu_D(T-t)}D_t$, initial news by $D'_0=e^{\mu_DT}D_0$, and the retail price by $e^{(\mu_D-r-\sigma^2)(T-t)}D_t$. Portfolio mean–variance demand uses $(\mu_S-r)/\sigma_S^2$; the hedging term uses $bD'_t/(1+bD'_t)$. These changes preserve the mechanism without claiming that real-world interest rates are constant or exogenous in an economy with intermediate consumption.

Section 3.4 adds passive, buy-and-hold institutions. The original institution share $\lambda$ is split into leveraged fraction $\theta$ and passive fraction $1-\theta$. Retail investors keep share $1-\lambda$. Among active investors the effective institutional share is

$$
\lambda'=\frac{\lambda\theta}{1-\lambda+\lambda\theta}.
$$

Substitute $\lambda'$ into the baseline pricing formulas. Reducing $\theta$ is the paper's deleveraging experiment, implemented as a time-zero transfer to passive holders; increasing it represents a capital transfer toward active leveraged institutions. More active institutional wealth raises prices; the leverage and volatility responses depend on where the economy lies on the hump. This is not the solution to a regulator imposing a binding leverage cap on an otherwise unchanged optimizer, and it does not value fiscal costs, welfare gains, bailout moral hazard or fire-sale externalities. The paper expressly makes no welfare comparison.

Appendix C removes the traded bond and uses $N+1$ stocks to span $N$ shocks. Let $V$ now have dimension $(N+1)\times N$, and form $\widetilde V=[V\ \mathbf1]$. Portfolio weights must satisfy both exposure and full-investment constraints:

$$
V^\top\phi_I=\kappa+\frac{bI_t}{1+bI_t}\sigma_I,\qquad
\mathbf1^\top\phi_I=1.
$$

Thus solve the square system

$$
\phi_I=\widetilde V^{-\top}
\begin{pmatrix}\kappa+\frac{bI_t}{1+bI_t}\sigma_I\\1\end{pmatrix},\qquad
\phi_R=\widetilde V^{-\top}\begin{pmatrix}\kappa\\1\end{pmatrix}.
$$

These follow directly from C1–C4. The later printed Lemma 2′ has inconsistent matrix factors, so these defining linear equations are the safe implementation. Index overweighting is then financed by reducing nonindex positions. The appendix reports this weight-sign pattern numerically over a wide range; it does not prove it generally. Shorting can still occur in some parameter regions, so removing an explicit bond is not an imposed universal long-only constraint. Complete spanning permits a synthetic bond, and the authors retain the same pricing implications conditional on unchanged terminal primitives.

Appendix D provides an agency rationale for benchmark-dependent marginal utility, not an exact endogenous derivation of the affine-log objective. A manager privately observes the state, then diverts fraction $p_T$ of portfolio value; the principal observes reported wealth $\widehat W_T=(1-p_T)W_T$ and a correlated public index. The principal wishes to implement an exogenously specified diversion level $p^*$ and chooses the least costly contract satisfying participation. Action follows the shock, and the principal is risk neutral. The manager's objective is $E[u(v(c_T)+g(p_T))]$.

The diversion first-order condition integrates to $c(\widehat W,I)=v^{-1}(H\log\widehat W+K(I))$, where $H=(1-p^*)g'(p^*)$. With $v(c)=\log c$ and $u(x)=e^{(1-\gamma)x}/(1-\gamma)$, $\gamma>1$, the principal determines $K$ using conditional moments of the pricing kernel given the index. Under the appendix's two independent Brownian shocks, index loadings on one shock and negative kernel exposure to it, compensation falls with the index at fixed reported wealth while marginal utility of wealth rises. An independent index would add no useful signal. These assumptions and the fixed action target qualify the microfoundation; it is not a general contracting theorem for arbitrary benchmark compensation.

## Reimplementation and limits

The baseline requires only $b,\lambda,D_0,D_t,\sigma,t,T$; no estimator, transaction-cost model or simulation seed is needed to evaluate its closed forms. Check terminal payoff equality, recovery of the retail-only case at $b=0$ or $\lambda=0$, wealth shares summing to one, stock holdings summing to one share and bond holdings summing to zero. For the multi-stock extension, additionally supply all loading vectors, initial and current dividends, index membership, and economically feasible residual claims. Verify covariance positive semidefiniteness and the rank condition before inverting the volatility matrix. These are implementation checks implied by the model, not additional empirical findings.

A simulation can use exact GBM transitions and analytical prices at every time step, but realized finite-horizon sample correlations should not be confused with the conditional instantaneous correlations proved here. Likewise, the paper's quoted empirical index-addition effects—5.45% at announcement and a further 3.45% to inclusion in an external study—are literature motivation, not estimates produced by this model. The model explains an announcement response to changed anticipated demand; it lacks a separate delayed passive-trading mechanism for inclusion-day returns.

The main limitations are terminal-only consumption, finite horizon, stylized preferences, exogenous benchmarking intensity, complete markets, no costs or endogenous security supply, and the special aggregate-dividend construction. The results establish a coherent channel from benchmark incentives to covariance and valuation. They do not prove that institutional growth always increases volatility, that nonindex stocks never respond, or that capital support improves welfare. For an applied researcher, the usable implication is that common ownership mandates and state-dependent institutional wealth can create return dependence beyond dividend fundamentals; measuring that channel requires additional data and identification absent from this theoretical paper.
