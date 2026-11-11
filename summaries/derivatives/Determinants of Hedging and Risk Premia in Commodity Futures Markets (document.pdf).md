# Determinants of Hedging and Risk Premia in Commodity Futures Markets

David Hirshleifer, *Journal of Financial and Quantitative Analysis* 24(3), September 1989, pp. 313–331. [Source PDF](../../Finance/futures/document.pdf). The supplied file contains a JSTOR cover and nineteen article pages. Printed p. 313 is PDF p. 2. This note covers the model, all four propositions, the Appendix proofs, Figure 1, and Table 1. It preserves the source's two-date setting and distinguishes exact covariance results from its small-dispersion approximation.

## Why this matters

A commodity futures contract can have little covariance with a broad stock portfolio and still require a substantial premium. The missing exposure may be a farmer's or producer's privately held operating income. Consumers could take the other side of some of that risk, but they generally do not participate in the relevant futures market. Pricing then reflects the risks of those who actually trade, not an average over everyone whose welfare is affected by commodity prices.

Hirshleifer develops this argument beyond a generic hedging-pressure term. Commodity demand elasticity, harvest costs, correlated supply and demand shocks, and the ability to change production determine the covariance between producer income and a futures payoff. Stock-market wealth shocks also change commodity demand, so the stock-market and producer-income components interact economically even though the pricing equation separates them additively. The distinctive contribution is this connection between commodity-market primitives and the two components of the premium.

The useful object is the expected payoff of a long contract, not a prediction based only on whether producers are short. A short hedge can be valuable even at an unfavorable expected price; conversely, price–quantity offsets can make producers want to buy futures. Several statements in the abstract and comparative-static prose conflict with the equations. The reconstruction below uses the covariance formulas to identify the applicable signs and explicitly labels corrections.

## Economic setting and timing

There are two dates, a terminal commodity market, and consumption only at the terminal date. $G$ producers or handlers own nonmarketable commodity output. $M$ consumers generate commodity demand. Of $N$ potential outside investors, only $\widehat N$ enter the futures market. A fixed setup cost $t$ discourages some outsiders but, by assumption, no producers. The cost represents such things as learning or overcoming barriers to participation; it is not a proportional bid–ask spread per contract.

All participating producers and speculators use the same mean–variance criterion,

$$
U(C)=E[C]-\frac{\alpha}{2}\operatorname{Var}(C),\qquad \alpha>0.
$$

Beliefs are homogeneous and correct for the distributions posited by the model. This objective is exact as a stated preference over moments. Interpreting it as expected exponential utility requires additional distributional conditions. Footnote 8 correctly notes that even jointly normal price and output do not make their product, producer revenue, normal. The later Taylor expansion introduces a second and separate approximation; one should not merge these two qualifications.

Let $q>0$ be the representative producer's stochastic output; a speculator has $q=0$. Let $h\ge0$ be the unit harvest or marketing cost, $P>0$ the terminal spot price, $f$ the date-0 futures price, and $\xi$ the number of contracts held long. A stock position of size $S$ pays $S R_M$, where $R_M$ is the gross stock-market return. For a participant, the source's consumption equation is

$$
C=W-t+(P-h)q+\xi(P-f)+S R_M.
$$

A nonparticipant omits $t$ and the futures position. The source writes stock exposure in terminal-payoff form without an explicit initial stock-purchase debit in this equation; its stock first-order condition accordingly uses $E[R_M]$. A numerical implementation that introduces a cash account and a date-0 budget must reformulate that part consistently, normally using excess payoffs. The futures covariance and clearing arguments below follow the equation as stated.

The producer cannot sell fractional claims on $(P-h)q$. A futures contract and the stock asset are the available risk-sharing instruments. Consumers enter through demand rather than an explicit portfolio problem. Their nonparticipation makes it plausible to neglect the feedback from futures profits into their commodity demand, but it also makes this a partial-equilibrium demand specification rather than a complete consumption-allocation model.

Commodity demand is

$$
Q=M\delta P^{\eta},\qquad \eta<0,\quad \delta>0,
$$

where $\eta$ is price elasticity and $\delta$ a multiplicative demand shock. Equating supply and demand gives

$$
P=k\left(\frac{q}{\delta}\right)^{1/\eta},\qquad k=(G/M)^{1/\eta}>0.
$$

More output lowers price; a higher demand shifter raises it. Inelastic demand means $-1<\eta<0$, unit elasticity means $\eta=-1$, and elastic demand means $\eta<-1$. These signed conventions are essential for checking the paper's comparative statics.

There is no storage or carryover. Because settlement occurs only at the terminal date, the distinction between daily-margined futures and terminally settled forwards vanishes. The model cannot identify a multiperiod futures convexity adjustment, an inventory convenience yield, or a roll yield. Its term “premium” is in terminal commodity price units:

$$
\pi=E[P-f]=E[P]-f.
$$

A positive $\pi$ is a favorable expected payoff for a long contract and a downward bias of futures relative to expected terminal spot. It is not necessarily a downward-sloping futures curve or a price below today's spot.

## Optimal positions and equilibrium pricing

For an interior optimum, differentiating the mean–variance objective gives Eq. (5), p. 318:

$$
\pi=\alpha\operatorname{Cov}(P,C),\qquad E[R_M]=\alpha\operatorname{Cov}(R_M,C).
$$

With $Y=(P-h)q$, the futures first-order condition can be rearranged as

$$
\xi=\frac{\pi/\alpha-\operatorname{Cov}(P,Y+S R_M)}{\operatorname{Var}(P)}.
$$

This is Eq. (6). The first numerator term is speculative demand; the second offsets exposure already present in production income and stock holdings. It is a conditional expression in $S$, not a solution that permits stock exposure to be ignored when $S$ is chosen simultaneously. For a speculator, $Y=0$. Even if $\pi=0$, positive stock exposure and positive covariance between $P$ and $R_M$ create a short futures demand to diversify stock risk.

For reconstruction, the two position choices can be solved together. Define $v_P=\operatorname{Var}(P)$, $v_R=\operatorname{Var}(R_M)$, and $c=\operatorname{Cov}(P,R_M)$. The source's first-order conditions imply

$$
\begin{pmatrix}v_P&c\\c&v_R\end{pmatrix}
\begin{pmatrix}\xi\\S\end{pmatrix}
=
\begin{pmatrix}\pi/\alpha-\operatorname{Cov}(Y,P)\\E[R_M]/\alpha-\operatorname{Cov}(Y,R_M)\end{pmatrix}.
$$

This displayed matrix is a derived implementation form, not a new assumption. A positive-definite covariance matrix gives a unique interior optimum. Singular covariance requires a separate spanning or arbitrage analysis; the division formulas cannot simply be applied with zero residual variance. Position constraints, margin rules, and limited liability are absent from the source.

Sum the futures positions across the $G+\widehat N$ participants and impose zero net supply. Let

$$
b=\frac{G}{G+\widehat N},\qquad \bar S=bS^g+(1-b)S^n.
$$

Here $b$ is the fraction of futures *participants* who are producers. It is not the fraction of producers who enter; all producers enter in the maintained setting. Market clearing yields the exact Eq. (7),

$$
\pi=\underbrace{\alpha\bar S\operatorname{Cov}(R_M,P)}_{\pi^M}
+\underbrace{\alpha b\operatorname{Cov}((P-h)q,P)}_{\pi^H}.
$$

The market component $\pi^M$ prices covariance with stock exposure; the hedging component $\pi^H$ prices nonmarketable producer income. The latter is multiplied by the participant composition. Averaging the individual first-order conditions also gives $\pi=\alpha\operatorname{Cov}(P,C^*)$, with $C^*$ the mean consumption of futures participants. Replacing $C^*$ with society-wide consumption would change the model.

Participation is endogenous in principle. A speculator enters when the gain in optimized mean–variance utility exceeds the fixed fee. For example, under the displayed unconstrained payoff convention, partialling out the stock position gives residual price variance $v_{P\cdot R}=v_P-c^2/v_R$ and residual expected payoff $\pi-cE[R_M]/v_R$. The improvement from adding futures is

$$
\Delta U=\frac{[\pi-cE[R_M]/v_R]^2}{2\alpha v_{P\cdot R}}-t.
$$

This is a derived entry expression for a speculator with $v_R>0$ and $v_{P\cdot R}>0$. It explains why the covariance premium can attract additional traders, but the source does not specify a distribution of participation fees or solve for a numerical equilibrium $\widehat N$. One cannot obtain calibrated $b$, $\bar S$, or $f$ from the qualitative propositions alone.

## Demand shocks and the interaction with stock-market wealth

With fixed output $q$, harvest cost is nonrandom and drops out of the covariance. Therefore

$$
\pi^H=\alpha bq\operatorname{Var}(P)\ge0.
$$

Higher demand raises both price and the producer's revenue. Producers wish to sell that risk; outsiders require a positive expected payoff to hold the opposing long exposure. This exact result does not require a Taylor expansion or normal commodity shocks.

To relate demand to aggregate wealth, the source sets $\delta=aR_M^{\epsilon}$, where $a>0$ and $\epsilon$ is income elasticity. Fixed output then gives $P=K R_M^{-\epsilon/\eta}$, with $K=k(q/a)^{1/\eta}$. Equation (10) becomes

$$
\pi^M=\alpha\bar S K\operatorname{Cov}(R_M,R_M^{-\epsilon/\eta}),\qquad
\pi^H=\alpha bqK^2\operatorname{Var}(R_M^{-\epsilon/\eta}).
$$

For positive aggregate stock exposure, the market component is positive for a normal or superior good, $\epsilon>0$, and negative for an inferior good, $\epsilon<0$. The proof uses monotone ordering: a variable has nonnegative covariance with an increasing function of itself and nonpositive covariance with a decreasing function. The hedging term remains nonnegative for either sign of income elasticity. Strict signs require nondegenerate risk and nonzero exposure. At $\epsilon=0$, this particular source of demand risk disappears.

Figure 1, p. 321, illustrates a market component crossing zero with income elasticity and a nonnegative hedging component on both sides. It is schematic, without observations, parameter values, or numerical axes. It is not an estimated cross-commodity premium curve. The exact formulas support the sign comparison; global monotonicity of the variance of $R_M^{-\epsilon/\eta}$ as absolute income elasticity changes would require further distributional and normalization conditions. The crucial interaction is that stock wealth changes not only the stock covariance term but also the variance of the producer's revenue.

## Output uncertainty, harvest costs, and distributional risk

Hold $\delta$ fixed and write $A=k\delta^{-1/\eta}$. Then $P=Aq^{1/\eta}$ and

$$
\pi^H=\alpha bA^2\operatorname{Cov}(q^{1+1/\eta},q^{1/\eta})
-\alpha bhA\operatorname{Cov}(q,q^{1/\eta}).
$$

This is Eq. (16) in the Appendix. Since $1/\eta<0$, output and price are oppositely ordered: $\operatorname{Cov}(q,q^{1/\eta})\le0$. Thus the harvest-cost contribution is nonnegative and increases with $h$, holding participation fixed. At unit elasticity, gross revenue $Pq=A$ is constant, but a large crop costs more to harvest. Net income is highest when the crop is small and price is high. Selling futures then hedges a risk that gross revenue alone would miss.

Without harvest costs, the sign is positive for inelastic demand and negative for elastic demand. Under inelastic demand, both price and revenue fall as output rises. Under elastic demand, price falls but revenue rises. At unit elasticity their covariance is zero. The positive-cost term makes the premium strictly positive for nondegenerate output and inelastic or unit-elastic demand; for elastic demand it can offset a negative gross-revenue term.

The paragraph opening p. 322 reverses the elastic/inelastic signs. Proposition 2 and the Appendix covariance formula give the signs just derived. The Appendix also describes the second covariance itself as positive, although it is negative; it is the *minus-signed contribution* that is positive. These are source inconsistencies, not a change of elasticity convention in this note.

This example illustrates distributional risk. A crop failure can improve growers' net income under unit-elastic demand while harming consumers. A society-wide consumption statistic can obscure the transfer. If consumers do not trade futures, the risk allocation among participants reflects the producers' exposure without an equal and opposite consumer hedge. The source does not claim that every supply shock increases aggregate resources or that producer gains measure social welfare.

## Joint shocks: the exact object and the approximation

With zero harvest cost and random $q$ and $\delta$, the exact hedging object is

$$
\pi^H=\alpha bk^2\operatorname{Cov}\left(q^{1+1/\eta}\delta^{-1/\eta},q^{1/\eta}\delta^{-1/\eta}\right).
$$

Proposition 3 approximates this covariance for small dispersion, neglecting terms of third and higher order. For a reproducible version, let $r=1/\eta$, define $P_0=k(\bar q/\bar\delta)^r$, and write $x=(q-\bar q)/\bar q$, $y=(\delta-\bar\delta)/\bar\delta$. First-order payoff changes are $P-P_0\approx P_0r(x-y)$ and $Pq-P_0\bar q\approx P_0\bar q[(1+r)x-ry]$. Their product gives the second-order covariance,

$$
\pi^H\approx\alpha b\bar qP_0^2
\left[r(1+r)\operatorname{Var}(x)+r^2\operatorname{Var}(y)-r(1+2r)\operatorname{Cov}(x,y)\right].
$$

This compact expression is algebraically equivalent to Eq. (20). It also supplies a direct way to check every sign. It is not an exact formula for arbitrary large shocks or heavy-tailed distributions. Positive means, finite required moments, and a distribution concentrated sufficiently near the expansion point are needed for a useful approximation.

For $-2<\eta<0$, $r<-1/2$ and $r(1+2r)>0$. Consequently, increasing the correlation of output and demand, holding their marginal means and variances fixed, lowers the hedging premium. Negative correlation raises it. Common weather can increase wheat and rye output simultaneously; because they are substitutes, higher rye output shifts wheat demand down. That produces a negative correlation between wheat output and its demand shock, reinforcing the hedging premium. Complementarity or opposite weather effects can instead generate positive correlation and weaken or reverse that premium.

The abstract says positive correlation raises the premium. Proposition 3(3), Table 1, the body discussion, and Eq. (20) give the opposite direction under the specified elasticity range. The equation-based result is the one retained here. For $\eta<-2$, the cross coefficient changes sign, so the stated range cannot be dropped.

At fixed correlations, changing a standard deviation also changes covariance. Let $s_x$ and $s_y$ denote the standard deviations of normalized output and demand, and $\rho$ their correlation. Differentiating the bracket with respect to $s_x$ gives

$$
2r(1+r)s_x-r(1+2r)\rho s_y.
$$

For elastic demand in the admitted range, $-2<\eta<-1$, and positive correlation, both terms are negative: more output dispersion lowers the premium. For inelastic demand and negative correlation, both are positive: more output dispersion raises it. Proposition 3(4) prints these two directions in reverse. The discussion on p. 323, explaining the inelastic/negative-correlation case, agrees with the corrected positive direction. In other sign combinations the two effects compete, so a universal direction would be unjustified.

The derivative with respect to $s_y$ is $2r^2s_y-r(1+2r)\rho s_x$. It is positive when $\rho\le0$, reproducing Proposition 3(5). The market component has the first-order representation

$$
\pi^M\approx\alpha\bar S P_0r\left[\operatorname{Cov}(R_M,x)-\operatorname{Cov}(R_M,y)\right].
$$

Higher output covariance with the stock market lowers this component; higher demand covariance raises it. Changing the output–demand correlation alone does not affect this first-order expression when the two stock covariances are held fixed. Such comparative changes must remain feasible for the full joint covariance matrix.

There is also an exact benchmark beyond the small-shock approximation. With $\eta=-1$, $P=k\delta/q$ and revenue equals $k\delta$, giving

$$
\pi^H=\alpha bk^2\operatorname{Cov}(\delta,\delta/q).
$$

Under independence and finite moments, this becomes $\alpha bk^2E[1/q]\operatorname{Var}(\delta)\ge0$. Positive dependence can reverse it, but a Pearson correlation alone does not generally sign an arbitrary nonlinear covariance. A full joint distribution is required for large shocks.

## Flexible supply and the cost-response proof

The final extension changes the timing and technology. A futures position is chosen first; then a demand or weather shock is revealed; the producer chooses output and completes production without further shocks. Marginal cost is $Bq^{1/\omega}$, where $B>0$ is a cost or adverse-weather shifter and $\omega>0$ is supply elasticity. Price taking gives $P=Bq^{1/\omega}$. Combining this with commodity demand yields

$$
q=k^{-\eta\omega/(\omega-\eta)}\delta^{\omega/(\omega-\eta)}B^{\eta\omega/(\omega-\eta)},
$$

$$
P=k^{-\eta/(\omega-\eta)}\delta^{1/(\omega-\eta)}B^{\omega/(\omega-\eta)}.
$$

Total cost is $Bq^{1+1/\omega}/(1+1/\omega)$. Since $Pq=Bq^{1+1/\omega}$, net operating income is $Pq/(1+\omega)$. This envelope-like simplification makes the proof reconstructable:

$$
\pi^H=\frac{\alpha b}{1+\omega}\operatorname{Cov}(Pq,P),\qquad
\pi^M=\alpha\bar S\operatorname{Cov}(R_M,P).
$$

With only demand shocks, both $Pq$ and $P$ increase with $\delta$, so the hedging component is positive. With only weather shocks, price increases with $B$, while revenue has a $B$ exponent $\omega(1+\eta)/(\omega-\eta)$. The premium is therefore positive for inelastic demand, negative for elastic demand, and zero at unit elasticity. The cost adjustment preserves that elasticity boundary even though both output and expenditure respond to the shock.

Substituting the output and price formulas into the covariance gives

$$
\pi^H=\frac{\alpha b}{1+\omega}k^{-\eta(\omega+2)/(\omega-\eta)}
\operatorname{Cov}\left(
B^{\omega(1+\eta)/(\omega-\eta)}\delta^{(\omega+1)/(\omega-\eta)},
B^{\omega/(\omega-\eta)}\delta^{1/(\omega-\eta)}
\right).
$$

The exponent of $k$ in printed Eq. (22), p. 329, has denominator $\omega+\eta$. Direct substitution from Eqs. (14) and (21) requires $\omega-\eta$, as displayed above. This is a derived correction; the qualitative covariance signs in Proposition 4 do not depend on this positive scale factor.

As supply elasticity tends to infinity, $P$ tends to $B$. Subject to finite moments and sufficient integrability to pass the limit through the covariance, the factor $1/(1+\omega)$ sends the hedging component toward zero. The stock component tends to $\alpha\bar S\operatorname{Cov}(R_M,B)$, which need not vanish. With pure demand shocks, $B$ is constant and both components vanish. Flexible output absorbs demand disturbances; flexible production cannot remove a stochastic marginal-cost shock. These are limiting statements, not a proof of monotonic decline at every finite elasticity under every joint distribution or endogenous participation response.

## What can be implemented and what remains unspecified

An implementation requires the joint distribution of output, demand, stock returns, and any cost shocks; the scale of stock exposure; absolute risk aversion; the producer/entrant mix; and compatible commodity units. Given those inputs, one can compute spot prices state by state, calculate net production income, estimate the two covariances, clear the futures market, and solve the two-asset position equations. For small shocks, the normalized approximation provides a diagnostic against direct state-by-state covariance calculations. For large shocks, exact Monte Carlo or quadrature should use the original nonlinear payoff functions rather than extrapolate Eq. (20).

The paper supplies no historical sample, calibration, numerical simulation, statistical estimates, standard errors, transaction-cost estimate, or out-of-sample trading result. Table 1 is a qualitative map of signs, with conditions distributed through the text; Figure 1 is conceptual. The source therefore supports structural hypotheses, not a numerical premium forecast. A backtest would additionally need contract sizes, margins, delivery specifications, position constraints, information timing, and an empirically identified demand/supply system. Elasticities inferred from equilibrium price–quantity correlations without separating the two shocks would not implement the model's primitives.

The model clarifies why commodity characteristics and the composition of market participants matter together. A commodity demand shock changes producer income and the contract payoff; an income shock changes commodity demand; a participation barrier changes who absorbs the resulting risk. The exact covariance decomposition remains usable after correcting the source's sign slips. Its empirical strength ultimately depends on measuring those exposures and on establishing that the two-date, mean–variance, and local-expansion assumptions are adequate for the intended application.
