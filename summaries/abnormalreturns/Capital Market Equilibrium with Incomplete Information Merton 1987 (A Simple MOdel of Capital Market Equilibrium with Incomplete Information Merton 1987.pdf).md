# A Simple Model of Capital Market Equilibrium with Incomplete Information (Merton 1987) — Detailed Quantitative Research Notes

**Robert C. Merton** (AFA Presidential Address, 1986) · *Journal of Finance* 42(3), July 1987, pp. 483–510 · Source file: `Finance/A Simple MOdel of Capital Market Equilibrium with Incomplete Information Merton 1987.pdf`

---

## Question and thesis

Can well-documented CAPM violations (flat security market line, size, neglected-firm and listing effects) be reconciled with rational, optimizing agents by adding one modest friction rather than abandoning the paradigm? Merton's friction: **incomplete diffusion of awareness** — each investor holds only securities he "knows about", and different securities are known by different fractions of the investor population.

The prologue motivates this with a time-scale argument: institutions, regulation and information technology adjust far more slowly than prices and portfolios. Examples: dealer capital is fixed on trading horizons, so the short-run marginal cost of capital for market makers can swing sharply; information that fits standard channels (earnings) diffuses quickly, but an academic anomaly (the small-firm effect, still disputed six years after the first study) needs documentation, belief, model building, client marketing and prudence approvals before capital corrects it. He also warns that weak-form EMH tests implicitly assume past investors had access to price histories and computing power they did not have, biasing tests against the null.

## Model

**Technology and returns.** $n$ firms with end-of-period cash flow
$$\tilde C_k = I_k\left[\bar A_k + a_k \tilde Y + s_k \tilde\varepsilon_k\right],\qquad E\tilde Y=0,\ E\tilde Y^2=1,$$
$\tilde\varepsilon_k$ mean zero, mutually uncorrelated and uncorrelated with $\tilde Y$. With market value $V_k$,
$$\tilde R_k = \bar R_k + b_k \tilde Y + \sigma_k\tilde\varepsilon_k,\quad \bar R_k=I_k\bar A_k/V_k,\ b_k=a_kI_k/V_k,\ \sigma_k=s_kI_k/V_k$$
(Sharpe diagonal / one-factor APT). Two inside securities in zero net supply: a riskless asset with gross return $R$, and a factor-mimicking security $\tilde R_{n+1}=\bar R_{n+1}+\tilde Y$ (riskless plus a cash-settled forward on $Y$). Frictionless otherwise: no taxes, no trading costs, unrestricted borrowing and short sales.

**Investors.** $N$ price-taking mean-variance investors, $U_j = E(\tilde R^jW_j) - \frac{\delta_j}{2W_j}\mathrm{Var}(\tilde R^jW_j)$. Everyone knows $R$, the factor security and the return structure. Investor $j$ knows $(\bar R_k,b_k,\sigma_k)$ only for $k\in J_j$; those who know a security agree on its parameters (conditional homogeneous beliefs), so there is no Grossman–Stiglitz adverse selection within a name. **Key assumption:** $j$ holds $k$ only if $k\in J_j$. Justified by a fixed "receiver"/set-up cost of following a firm, distinct from the signalling costs of transmitting specific news. Contrast with Klein–Bawa and Barry–Brown estimation-risk models: those vary the *depth* (precision) of information across securities; Merton holds precision fixed and varies the *breadth* of cognizance. Merton explicitly frames the results as reduced-form: short-sale limits, prudence rules, taxes, segmentation etc. that keep an investor out of a name act the same way.

**Individual optimum.** With $\Delta_k\equiv\bar R_k - R - b_k(\bar R_{n+1}-R)$ and a Kuhn–Tucker multiplier $\lambda_k^j$ on the constraint $w_k^j=0$ for $k\notin J_j$:
$$b^j=\frac{\bar R_{n+1}-R}{\delta_j},\qquad w_k^j=\frac{\Delta_k}{\delta_j\sigma_k^2}\ (k\in J_j),\qquad w_k^j=0,\ \lambda_k^j=\Delta_k\ (k\notin J_j).$$
The shadow cost of not knowing $k$ equals $\Delta_k$ for every uninformed investor (footnote 16: this holds for all concave utilities given the return structure).

**Equilibrium** (identical $\delta$ and $W$). With $q_k=N_k/N$ the fraction of investors aware of $k$ and $x_k=V_k/M$ the market weight, market clearing gives $x_k=q_k\Delta_k/(\delta\sigma_k^2)$, hence
$$\bar R_k = R + b_k\delta b + \frac{\delta x_k\sigma_k^2}{q_k}\tag{16}$$
$$V_k=\frac{I_k}{R}\left[\bar A_k-\delta b\,a_k-\frac{\delta s_k^2I_k}{q_kM}\right],\qquad V_k=V_k^*-\frac{\delta(1-q_k)s_k^2I_k}{q_kMR}.\tag{17–18}$$
Value is always lower under incomplete information. The aggregate (per-investor) shadow cost is $\lambda_k=(1-q_k)\Delta_k\ge 0$, and
$$V_k=\frac{V_k^*}{1+\lambda_k/R},\qquad \bar R_k-\bar R_k^*=\lambda_k\,\bar R_k^*/R,$$
so incomplete information acts like an extra discount rate. Footnote 17: with unequal wealth, $q_k$ becomes the fraction of national wealth held by investors aware of $k$.

**SML.** With $\beta_k=(b_k\delta b + x_k\sigma_k^2)/\mathrm{Var}(R_M)$ and $\lambda_M=\sum_k x_k\lambda_k$,
$$\bar R_k-R=\beta_k(\bar R_M-R)+\lambda_k-\beta_k\lambda_M,\qquad \alpha_k=\lambda_k-\beta_k\lambda_M.\tag{25–26}$$
The market portfolio is not mean-variance efficient; a fully informed investor tilts by $w_k^*-x_k=\lambda_k/(\delta\sigma_k^2)$ (27).

## Cross-sectional predictions (Section III)

Elasticities of $\bar R_k-R$ from (16):
$$\eta(b_k)=\frac{q_kb_k\delta b}{q_kb_k\delta b+x_k\sigma_k^2}>0,\quad \eta(x_k)=\eta(\sigma_k^2)=1-\eta(b_k)>0,\quad \eta(q_k)=-\eta(x_k)<0.$$
What matters is not firm size relative to national wealth but size relative to the wealth of *aware* investors, $x_k/q_k=V_k/(N_kW)$. For factor-heavy firms, or when $x_k\sigma_k^2/q_k\ll b_k\delta b$, the CAPM is recovered; non-market pricing is concentrated in lesser-known names ($q_k\ll1$).

- **Flat SML.** Holding $\lambda_k$ fixed across $\beta$, $\partial\alpha_k/\partial\beta_k=-\lambda_M<0$. If $E[\lambda_k\mid\beta_k]=\lambda_M$, then $E[\alpha_k\mid\beta_k]=(1-\beta_k)\lambda_M$ — observationally identical to Black's zero-beta CAPM when sorting on beta alone (consistent with Black–Jensen–Scholes, Fama–MacBeth, Blume–Friend). Unlike Black, alphas also load on $\sigma^2$, $x$, $q$.
- **At fixed $\beta$** (31): $\partial\alpha/\partial x=\delta(1-q)\sigma^2/q>0$; $\partial\alpha/\partial\sigma^2=\delta(1-q)x/q>0$ (consistent with residual-variance pricing found by Friend–Westerfield–Granito); $\partial\alpha/\partial q=-\delta x\sigma^2/q^2<0$.
- **Size.** The *conditional* size effect is positive, apparently contradicting Banz/Reinganum. The unconditional relation $d\alpha/dx$ includes $(\partial\alpha/\partial q)(dq/dx)$ and $(\partial\alpha/\partial\sigma^2)(d\sigma^2/dx)$; since small firms have fewer holders and more idiosyncratic risk, $d\alpha/dx<0$ is possible "but surely not required". A sufficient condition is $d(x/q)/dx<0$.
- **Supporting evidence as $q$-proxies:** Barry–Brown (1984) — a listing-period effect survives controls for size, beta and January, and the size×listing interaction is more significant than size itself; Arbel–Carvell–Strebel (1983, 1971–1980) — strong negative relation between risk-adjusted returns and institutional holdings, with no residual small-firm effect once institutional holdings and beta are controlled.

**Calibration.** Total variance 0.16, half idiosyncratic ($\sigma^2=0.08$), $\delta=2$ give $\lambda_k=0.16(1-q_k)x_k/q_k$.
- GE, Ford, IBM have market value per shareholder of about \$53k, \$27k, \$97k; with ~45 million investors the implied $q$ are 0.011, 0.007, 0.017 — which would imply absurdly large $\lambda$. Merton says these naive numbers vastly overstate $\lambda$ for large caps: their idiosyncratic variance is smaller and institutional (indirect) ownership multiplies the effective investor base.
- A \$200M firm in a \$2T market ($x=10^{-4}$) with 22,500 shareholders and no institutional holders: $q=22{,}500/45\text{M}=0.0005$, $\lambda\approx0.16\times10^{-4}/0.0005\approx0.032$, i.e. >300 bp above the complete-information required return.
- **Table I** (1,387 Compustat firms with shareholder counts, 31 Dec 1985, size deciles): top decile holds 63.47% of market value, top two ~79%; bottom five deciles 4.31%. Market value per shareholder (relative to sample average) runs from 0.161 (decile 1) to 1.957 (decile 10) — a ~12x range versus ~600x in firm value. Treating MV/shareholder as a proxy for $x/q$, implied $q_k/q_{10}$ is 0.02, 0.03, 0.04, 0.05, 0.06, 0.09, 0.13, 0.18, 0.34, 1.00. Note Merton's own admission: on this proxy $d(x/q)/dx>0$, i.e. the sufficient condition for a negative size–alpha relation fails, although the proxy is biased upward for large, institutionally held firms.

## Firm behavior (Section IV)

$\partial V_k/\partial q_k = V_k\delta x_k\sigma_k^2/(q_k\bar R_k)>0$: widening the investor base lowers the cost of capital, most for small-$q$, high-idiosyncratic-risk firms. Implications:
- Advertising aimed at investors, PR, exchange listing and agency ratings (which make the firm eligible under prudent-investor rules — such constraints are equivalent to non-awareness) have value even with no new cash-flow information. A widely circulated story repeating known facts can move the price because it changes the expected path of $q_k$ (footnotes 20–21; a dynamic model is needed to make this rigorous).
- With convex marketing cost $F(N_k)$, $F'>0$, $F''>0$, $F'(N)=\infty$, the optimal base solves $F'(N_k)=\delta s_k^2I_k^2/(RN_k^2W)$ (34): larger dollar idiosyncratic cash-flow variance ⇒ larger optimal base; $N_k$ rises with risk aversion and falls with per-capita wealth and the interest rate.
- The elasticity of the required excess return with respect to scale is positive, $\eta(I_k)=(\delta\sigma_k^2x_k/q_k)/(q_kb_k\delta b+\sigma_k^2x_k)$ (35): low-$q$, high-$\sigma$ firms face downward-sloping demand for their shares, relevant for issuance. Joint optimum: $I_k=N_kW[\bar A_k-R-\delta b a_k]/(2\delta s_k^2)$ (36), smaller than under complete information; investment and investor-base expansion tend to coincide, and often with new security issues.
- Merton does not treat marketing as a driver of fads: advertising leaves the base unchanged if fundamentals do not justify it, and exploitation of cognitive errors is assumed immaterial (footnotes 24–25).

## Robustness and extensions (Section V)

- **General covariance:** $\alpha_k=\lambda_k-\beta_k\lambda_M$ still holds, but $\lambda_k^j$ varies across investors and can be negative (an uninformed investor would short). The comparative statics need $\partial\lambda_k/\partial q_k<0$, which Merton conjectures can be guaranteed under reasonable conditions by analogy with Errunza–Losq mild segmentation. With correlated names, learning about a correlated stock is cheaper but less valuable for diversification — net effect on $q$ ambiguous.
- **Short-sale costs** accentuate the effects: a constrained investor who would short looks like an uninformed one, and the ban lowers the value of paying the set-up cost (like giving away a put), most for high-$\sigma$ names. Shorting is cheap mainly for large, widely held stocks that also have options/futures.
- **Institutions** cut per-investor set-up cost by $(K-1)/K$ but do not produce complete information: they must themselves be marketed, individual investors hold few funds, institutional portfolios overlap heavily and deviate from market weights. Aggregate $q_k$ comes from direct plus indirect holdings.
- **Indexers:** with $A_N$ full-market indexers, equilibrium is as in (15) with $q_k=N_k/(N-A_N)$ (fraction of active investors aware). If indexers hold only large, widely held names, they raise effective $q$ there and lower it for excluded names, amplifying the effect. A "naive APT" investor holding only the factor security is already nested (knows no individual stock).
- **Arbitrage capacity.** For the \$200M firm, suppose required return is 13% vs 10% under complete information. If the gap lasts one year, undervaluation is ~3% (\$6M); in perpetuity, ~23% (\$46M) — less than a nickel per share on Exxon. With a 5% ownership cap, the maximum gain to an institution is \$0.3–2.3M, before price impact, monitoring and "nuisance" costs. Marketing a generic neglected-stock fund has a free-rider problem (footnote 32). Hence rational large managers can leave sizable percentage alphas unexploited, and correction can be slow and incomplete.

## Assessment

**Convincing.** The model is a clean, one-parameter departure from CAPM with closed-form pricing, and it delivers several patterns at once: a flat SML without borrowing constraints, priced idiosyncratic risk, neglected-firm and listing effects, value of IR/listing/ratings, and price reactions to stale-news publicity. The distinction between breadth and depth of information is sharp and empirically separable. The capacity argument (percentage alpha vs. dollar alpha) is the most durable practical point and anticipates later limits-to-arbitrage work.

**Fragile.**
- Results depend on the diagonal covariance structure and identical preferences/wealth; the general-covariance sign of $\partial\lambda/\partial q$ is conjectured, not proved.
- $q_k$ is exogenous in the pricing section; the "awareness" friction is a reduced form for many different frictions, which makes it hard to falsify separately from segmentation, shorting costs or liquidity.
- The paper's own data cut against the naive size prediction: MV per shareholder rises with size, so the model's size effect relies on an unmeasured institutional correction.
- One-period model: the valuation effect of a $q$ change depends entirely on how persistent the premium is (3% vs 23% in Merton's own example), which the model does not pin down.
- Evidence cited is indirect (other authors' sorts reinterpreted as $q$-proxies); there is no direct test in the paper.

**For a quantitative PM/researcher.**
- The expected-return premium is $\delta(1-q)x\sigma^2_\varepsilon/q$: idiosyncratic variance scaled by size relative to the aware investor base. Practical proxies for $q$: shareholder counts, institutional ownership breadth, analyst coverage, index membership, listing age, media reach.
- Predicted event signatures: price rises and subsequent expected returns fall when $q$ jumps (index inclusion, uplisting, coverage initiation, options listing); issuance without base expansion faces a price discount.
- Passive indexing restricted to large caps should *widen* recognition premia in the excluded tail — a testable implication with modern ETF data.
- Recognition premia are concentrated where capacity is smallest; they can be real but uninvestable at scale.
