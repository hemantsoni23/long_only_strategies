# The dynamics of the leverage cycle

Christoph Aymanns and J. Doyne Farmer, *The dynamics of the leverage cycle*, Journal of Economic Dynamics and Control, DOI 10.1016/j.jedc.2014.09.015. This source is a 25-page accepted article in press, accepted September 11, 2014; its filename uses 2015. Page references below refer to this PDF, including Appendices A–D.

Source: [Deleveraging_AymannsFarmer_2015.pdf](../../Finance/Deleveraging_AymannsFarmer_2015.pdf).

## Why this matters

A bank can satisfy a backward-looking risk constraint and still help create the crash against which that constraint is intended to protect it. Low recent volatility permits borrowing and asset purchases. Purchases raise prices; rising equity and falling measured risk permit further expansion. A sufficiently large price movement reverses the process: measured volatility increases, target leverage falls, and sales depress prices further. The authors produce recurring bubbles and crashes through this feedback, even without a sequence of large fundamental shocks.

Their contribution is a dynamical model with a tractable market-clearing mechanism, two reduced versions, and controlled parameter experiments. It distinguishes leverage cycles from a single downward liquidity spiral. It also shows why countercyclical risk limits, longer estimation windows, and leverage caps have parameter-dependent effects. This is a qualitative simulation study, not a calibrated estimate of an actual financial system or an empirical demonstration that a particular regulation causes crises.

## Bank accounting, information, and allocation

In the full model there are banks, an unlevered noise investor, and $N_f$ stocks, each with one share outstanding. For a bank, cash is $c$, stock holdings are $n$, prices are $p$, debt is $L$, assets are $A=c+n^Tp$, equity is $E=A-L$, and leverage is $\lambda=A/E$. Stocks are held long. Lenders accommodate borrowing without an endogenous credit-supply constraint. Cash earns no interest. Stock dividend income is assumed to offset debt interest and bank distributions, so equity changes through asset revaluation rather than retained operating income.

The bank estimates dividend yields using an exponential average, with gain $\gamma$:

$$
\widehat r_{i,t+1}=(1-\gamma)\widehat r_{i,t}
 +\gamma\Pi_{i,t}/p_{i,t}.
$$

These are expected dividend yields, rather than a general model of expected total returns. With log prices $x_t$, the estimated mean and covariance follow the paper's ordering:

$$
\widehat\mu_t=\delta x_{t-1}+(1-\delta)\widehat\mu_{t-1},
\qquad
\Sigma_t=(1-\delta)\Sigma_{t-1}
 +\delta(x_{t-1}-\widehat\mu_t)(x_{t-1}-\widehat\mu_t)^T.
$$

This timing matters: the newly updated mean enters the covariance update. The estimated covariance is used as the next-period covariance forecast. The gain $\delta$ sets the response speed, with smaller values giving longer effective memory.

A simple allocation heuristic assigns each stock a dividend-yield-to-volatility ratio $s_i=\widehat r_i/\sigma_i$. If the fixed cash share is $w_c$, stock weights are

$$
w_i=(1-w_c)\frac{\exp(\beta s_i)}{\sum_k\exp(\beta s_k)}.
$$

At $\beta=0$ stock holdings are equally weighted; high $\beta$ concentrates the risky allocation in the highest-ratio stock. This is not an unconstrained Markowitz optimizer. Portfolio variance is $v=w^T\Sigma w$, including the stock weights' scaling by the risky asset share.

For centered Gaussian portfolio returns, the one-dollar loss quantile is $z_a\sqrt v$, where $z_a=\Phi^{-1}(a)$ and $a$ is the confidence level. Requiring total VaR not to exceed equity gives

$$
A z_a\sqrt v\le E,
\qquad
\bar\lambda=\frac{\alpha}{\sqrt v},
\qquad \alpha=1/z_a.
$$

A larger $\alpha$ therefore means greater risk tolerance and higher permitted leverage. Increasing the confidence level decreases $\alpha$. The Gaussian 99% value is approximately $0.43$. This normal-quantile interpretation is conditional on the assumed return distribution, rather than a demonstrated coverage property of the simulated endogenous returns.

The general leverage target used for the experiments is

$$
\bar\lambda_t=\alpha_t(v_t+v_0)^b.
$$

Here $b=-1/2$ is inverse-volatility or procyclical leverage, $b=0$ is constant target leverage, and $b>0$ makes target leverage increase with measured risk. For negative $b$, a positive variance offset $v_0$ limits leverage when measured variance approaches zero. Most main experiments use $v_0=0$.

Before market clearing, the bank chooses borrowing or repayment

$$
\Delta B_t=\bar\lambda_t E_t-A_t.
$$

The choice uses the bank's current balance sheet. The bank does not solve for a borrowing amount that anticipates its own execution-induced price change. Consequently target and realized post-clearing leverage need not coincide exactly.

## Noise investor, fundamentals, and price formation

The noise investor has no debt. Its stock weights are $(1-w_c)v_i/\sum_kv_k$, where the unnormalized propensities evolve through mean reversion, relative expected dividend yield, and independent Gaussian shocks:

$$
\frac{dv_i}{v_i}=\rho(1/N_f-v_i)
 +\zeta\left(\widehat r_i-\frac1{N_f}\sum_k\widehat r_k\right)
 +\eta\,dW_i.
$$

The simulation uses an additive update $v_{i,t+1}=v_{i,t}+dv_{i,t}$. A fall in a stock's price raises its dividend yield and attracts this investor's capital, counteracting the bank's destabilizing sales. Mean reversion also limits persistent allocation imbalances. The paper does not specify a general clipping or reflection rule ensuring positive weights under every possible Gaussian shock.

Dividend innovations are multiplicative, $d\Pi_i/\Pi_i=\mu+\phi\,dW_i$, independently across stocks. The discrete implementation is therefore an Euler-style multiplicative update; interpreting it as an exact exponential geometric-Brownian update would change the specified simulation.

Let $W_{t+1}$ collect investors' proposed stock weights and $N_t$ their existing holdings. The price vector solves the simultaneous unit-share market-clearing equations:

$$
p_{t+1}=(I-W_{t+1}N_t)^{-1}W_{t+1}(c_t+\Delta B_t).
$$

Each investor's post-clearing wealth depends on the value of existing shares at the newly determined prices. This is why a matrix inverse appears even though individual weights are chosen beforehand. A reproduction should check matrix invertibility, positive prices, cash balances, and equity at each step. These feasibility properties are not guaranteed for every parameter combination simply by the displayed equation.

Table 1 specifies one bank, three stocks, initial bank equity 23, initial bank leverage 5, bank cash share 0.2, $\delta=0.1$, $\alpha=0.1$, $b=-0.5$, $\gamma=0.1$, and $\beta=0.1$. The noise investor starts with assets 115, matching the bank's initial $23\times5=115$ assets; its parameters are $\rho=0.05$, $\zeta=5$, and $\eta=0.2$. Dividend parameters are $\mu=10^{-5}$ and $\phi=0.05$. Initial prices, covariance initialization, random seeds, and all numerical safeguards are not fully supplied.

Figures 2–3 compare passive debt management, $\Delta B=0$, with active risk-based leverage management. Passive leverage can still change when asset prices change. Active management produces much larger price excursions and repeated gradual increases followed by sharp crashes. Stock prices comove even though their dividend shocks are independent, because the bank's common balance sheet links their demand. These are illustrative simulated paths, without estimated real-world magnitudes or statistical confidence intervals.

## Constant-equity reduction and the instability mechanism

Section 4.1 removes the noise investor, keeps one stock and one investor, sets the stock weight and holdings to one, and fixes equity externally at $E$. Clearing gives $p_t=E\bar\lambda_t$. With $b=-1/2$ and $v_0=0$,

$$
v_{t+1}=(1-\delta)v_t+
 \frac{\delta}{4}\left[\log(v_t/v_{t-1})\right]^2.
$$

Writing $z_1=v_t$ and $z_2=v_{t-1}$ gives a two-dimensional map:

$$
z_{1,t+1}=(1-\delta)z_{1,t}
 +\frac\delta4[\log(z_{2,t}/z_{1,t})]^2,
\qquad z_{2,t+1}=z_{1,t}.
$$

Both equity and risk tolerance cancel. For a general exponent the analogous feedback term involves $b^2$, losing the distinction between positive and negative cyclicality. This reduction can explain recurring volatility and leverage movements, but cannot establish how absolute leverage, endogenous equity loss, or countercyclical policy changes systemic stability.

Figure 4 uses $\delta=0.2$, shows an illustrative price segment, and plots a 20,000-step phase trajectory. During a quiet expansion the variances move close to zero along a nearly straight path, so the inverse-volatility target grows. Departures from this path generate a large logarithmic-ratio term, raising estimated variance and collapsing target leverage and prices. The trajectory then returns toward the quiet phase. The phase plot suggests a chaotic attractor; the displayed visual evidence is not, by itself, a full mathematical proof of chaos.

Appendix B provides a local Jacobian. With $\ell=\log(z_2/z_1)$ it is

$$
J=
\begin{pmatrix}
1-\delta-\delta\ell/(2z_1)&\delta\ell/(2z_2)\\
1&0
\end{pmatrix}.
$$

Along $z_2=mz_1$, $m>1$, one eigenvalue tends to $1/m$, while the other tends to negative infinity. The printed PDF's latter result is $-\infty$, which text extraction can corrupt into a finite-looking symbol. However, describing the origin as an ordinary hyperbolic fixed point requires qualification: $\log(z_2/z_1)$ is undefined at $(0,0)$ and the map has no path-independent continuous extension there. For example, approaching along a fixed ratio other than one leaves a nonzero squared-log term. The appendix supports singular sensitivity near the zero-risk boundary; it should not be restated as a standard smooth fixed-point theorem at the origin.

## Variable-equity model: explicit reconstruction

Section 4.2 retains one bank and one noise investor trading one stock. For fixed noise weight the state is $(p_t,p_{t-1},v_t,L_t,n_t)$, where $n_t$ is the bank's fraction of the outstanding share. The bank stock weight $w_B$ is fixed, and the noise weight is $w_N$. Before redistribution,

$$
A_t=n_tp_t/w_B,\qquad E_t=A_t-L_t,
\qquad c_{B,t}=(1-w_B)n_tp_t/w_B,
$$

$$
c_{N,t}=(1-w_{N,t})(1-n_t)p_t/w_{N,t}.
$$

The model applies $dE_t=\xi(E_0-E_t)$, adding it to bank cash and subtracting it from noise-investor cash. This conserves aggregate equity but externally replenishes or removes bank capital. Use the pre-transfer equity and cash ordering explicitly when implementing the source equations; re-estimating the leverage decision after a transfer would define a different update scheme.

Variance, debt, and holdings update as

$$
v_{t+1}=(1-\delta)v_t+\delta[\log(p_t/p_{t-1})]^2,
\quad L_{t+1}=L_t+\Delta B_t,
$$

$$
n_{t+1}=\frac{w_B[n_tp_{t+1}+c_{B,t}+\Delta B_t]}{p_{t+1}}.
$$

The explicit reduced variance update uses stock log returns as printed, without inserting an additional factor $w_B^2$. The reduced model's operational definition should take precedence over an assumed translation from the multiasset portfolio-variance notation.

There is a timing discrepancy in printed Equation 25. Its clearing-price numerator uses $w_{N,t+1}c_{N,t}$, but its denominator is $1-w_Bn_t-(1-n_t)w_{N,t}$. Simultaneous clearing with the new noise weight would instead put $w_{N,t+1}$ in both places. The versions agree for fixed weights, but differ in stochastic simulations. A reproduction should report which version it uses and test the actual share-clearing residual, rather than silently correcting this discrepancy.

In stochastic experiments the noise weight follows

$$
\frac{dw_{N,t+1}}{w_{N,t}}=(0.5-w_{N,t})\rho+\eta dW_t,
\qquad w_{N,t+1}=w_{N,t}+dw_{N,t+1}.
$$

This adds a state dimension and mean reverts toward 0.5. No general boundary projection is specified. Table 2 gives $E_0=10$, initial leverage 5, $w_B=0.05$, initial bank stock ownership 0.1, redistribution speed $\xi=1.2$, noise $\rho=0.9$, and noise standard deviation $\eta=0.01$. The bank balance-sheet identities imply an initial price of 25 from these inputs. Policy experiments vary $\alpha$, $\delta$, and $b$.

Appendix D compares example leverage paths with and without redistribution. Both cycle, but without redistribution the bank gradually loses equity and the cycles' amplitude grows. This establishes a useful illustrative robustness check, not proof that redistribution leaves every stability boundary unchanged. Figure 5 similarly displays deterministic cycles and noisy fluctuations, using a 5,000-step trajectory and 500-step excerpts.

## Experiments and numerical conclusions

The outcome for the main parameter sweeps is the coefficient of variation of **price levels**, $CV=\operatorname{sd}(p)/\operatorname{mean}(p)$. It is not return volatility, a tail-loss probability, or a welfare measure. Runs generally last 5,000 steps, discarding the first 20%, leaving 4,000 observations. Numerical grid resolution and reproducible seed schedules are not given.

For risk tolerance versus memory, Figure 6 varies $\alpha\in(0,0.7]$ and $\delta\in(0,0.5]$, with $b=-0.5$ and $v_0=0$. Stochastic outcomes are averaged over 40 seeds at each combination. Low-risk blue regions have $CV<10^{-1.5}\approx0.0316$. Lower $\alpha$ and moderately longer memory usually stabilize the system. However, stability deteriorates again for very small gains, around $\delta\lesssim0.04$. The authors tentatively link this cusp to the noise trader's characteristic time scale; they do not establish a general optimal estimation horizon.

For cyclicality, Figure 7 varies $\alpha\in(0,300]$ and $b\in[-0.5,0.5]$ in the deterministic model, fixing $\delta=0.1$ and $v_0=0$. Four regions emerge: convergence toward a fixed point, persistent leverage cycles, bank bankruptcy, and numerical divergence. Bankruptcy is negative bank equity. Divergence means a variable exceeds floating-point range. The heatmap assigns these cases artificial CV values $10^4$ and $10^5$ respectively; these colors are classification markers rather than measured economic volatility.

The unstable region contracts as $b$ rises. Countercyclical leverage supports purchases after a negative shock, but a positive shock can increase variance, induce higher leverage, and amplify the upward move. Thus it does not remove instability at every risk-tolerance level. Comparisons across $b$ also alter the units and baseline level of $\alpha(v+v_0)^b$; they do not hold average leverage constant. One sentence on page 18 says stronger procyclicality raises the stability threshold, contrary to the surrounding discussion and figure. The figure and main conclusions support the opposite direction for the stated sweep.

The temporal policy experiment introduces smoothed signed returns $q$ and dynamic risk tolerance:

$$
q_{t+1}=(1-\delta_\alpha)q_t+\delta_\alpha\log(p_t/p_{t-1}),
\qquad \alpha_{t+1}=\alpha_t+d\alpha_{t+1}.
$$

**Equation 28 prints** $d\alpha_{t+1}=\rho_\alpha(\alpha_0-\alpha_t)+\theta q_t$. For positive $\theta$, this raises risk tolerance after positive trends. The prose repeatedly states the opposite policy: increase tolerance after falling prices and reduce it after rising prices. That intention would require $-\theta q_t$ with the defined signed return. The discrepancy is visible in the original formula, not merely OCR. The paper therefore does not unambiguously identify the implemented controller; its figure results cannot be guaranteed by blindly coding the printed plus sign.

Figure 8 studies $\theta\in[0,7]$ and $\delta_\alpha\in[0,0.7]$, with $\alpha_0=0.1$, $\delta=0.1$, $b=-0.5$, $v_0=0$, deterministic dynamics, and $\rho_\alpha=0.5$. An intermediate band reduces CV by approximately an order of magnitude; weak or excessive control is less effective. The noisy illustration in Figure 9 uses $\alpha_0=0.5$, $\delta_\alpha=0.2$, and compares $\theta=0$ with 3. Low-frequency amplitudes shrink, but rapid small fluctuations appear. Because the source lacks the implementation resolving the sign, a replication should run both controller variants and label that sensitivity explicitly.

For leverage limits, Section 4.2.4 uses $\alpha=0.2$, $\delta=0.1$, and $b=-0.5$. The offset implies an effective ceiling $\lambda_m=\alpha v_0^b$. Actual target leverage is no larger and normally lower because $v>0$. Figure 10 illustrates ceilings about 0.4, 13.5, and 50; low ceilings suppress variation, while increasing an already nonbinding ceiling has little effect. A ceiling below one is allowed by the displayed model, so this experiment should not be equated automatically with a conventional positively indebted bank.

## Appendices, implementation limits, and takeaways

Appendix A changes the distributional interpretation of risk tolerance. For a centered symmetric finite-variance loss, symmetry and Chebyshev give $P(X>k\sigma)\le1/(2k^2)$. Setting the upper bound to 1% gives $k\approx7.07$, hence $\alpha\approx0.1414$, compared with roughly 0.43 under Gaussian losses. This is a conservative moment bound over distributions, not identification of one universally “maximally heavy-tailed” law or calibration of actual crash probabilities.

Appendix C replaces softmax allocation with numerical maximization of expected returns under nonnegative holdings and a printed quadratic risk constraint $E-a w^T\Sigma w\ge0$. The appendix calls $w$ portfolio weights but does not fully resolve normalization, dimensional scaling against equity, or the optimizer implementation. It reports similar leverage cycles in an example path and approximately twentyfold faster runtime for the simple heuristic. This is evidence that a single optimizer substitution preserves the qualitative example, not a general equivalence theorem for portfolio rules.

A careful implementation should first reproduce deterministic paths, verify balance-sheet and share-clearing identities, and only then add random weights. Record initial covariance, all weights and prices, seeds, feasibility interventions, timing conventions, policy sign, and numerical failure flags. Those choices materially affect reproducibility and are not all specified in the source; author code is offered on request, rather than included in the PDF.

The practical implication is to evaluate risk rules jointly with market impact, equity dynamics, and estimation speed. The paper gives mechanisms and numerical warning signs for stress-model design. It does not supply a regulator-ready parameter calibration, a validated crisis forecast, transaction-cost estimates, or evidence that eliminating bank risk management improves welfare.
