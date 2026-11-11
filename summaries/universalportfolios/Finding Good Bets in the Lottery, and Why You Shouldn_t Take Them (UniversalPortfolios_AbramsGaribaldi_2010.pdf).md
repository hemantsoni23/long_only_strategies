# Finding Good Bets in the Lottery, and Why You Shouldn't Take Them

Aaron Abrams and Skip Garibaldi. *The American Mathematical Monthly* 117(1), January 2010, pp. 3–26. DOI: 10.4169/000298910X474952. [Source PDF](../../Finance/UniversalPortfolios_AbramsGaribaldi_2010.pdf). The complete supplied 25-page PDF, including its cover, proofs, figures, tables, references, and added-in-proof qualification, was read. Printed page 3 is PDF page 2. All game rules, tax conventions, sales observations, and market estimates below describe the historical source; they are not current lottery specifications or tax advice.

## Why this matters

A lottery ticket can have positive expected return without deserving a material place in an investment portfolio. This paper makes the distinction quantitative. Its first contribution is an exact finite-ticket formula incorporating shared jackpots and smaller pari-mutuel prizes. Its second is a normalized break-even diagram that explains why the advertised jackpot alone is a poor investment signal. Its third is a conditional mean–variance allocation argument: even a favorable ticket can receive a negligible portfolio weight because its variance is enormous.

The most reusable mathematics concerns a payoff pool divided among a random number of winners. The same accounting issue appears in betting pools and other contingent claims with endogenous dilution. The investment conclusion is less universal than the paper's rhetoric. Its portfolio theorem uses one historical covariance matrix, a particular normalization of short positions, a zero-covariance assumption for lottery returns, and a minimum meaningful allocation. General risk aversion does not reduce every distribution to mean and variance. Several printed numerical details also do not reproduce exactly; those qualifications are separated below from the valid payoff identities.

## Historical game model and units

A ticket costs one monetary unit. There are $t$ equally likely distinct winning combinations, and $N$ tickets are sold, including the ticket being valued. The draw is independent of ticket choices. Other tickets are independently and uniformly selected from the $t$ combinations; repeated combinations are allowed. This is a sampling-with-replacement model of purchases, not a model in which every ticket is unique.

The jackpot $J$ is the after-tax cash amount available to the winning tickets. It is not the advertised annuity amount. Non-jackpot prizes have two forms. A fixed category pays $a_i$ and contains $t_i^{\mathrm{fix}}$ combinations. A pari-mutuel category contains $t_i^{\mathrm{pari}}$ combinations and divides a pool $r_iN$ among its winning tickets. The categories are disjoint because each ticket receives only its highest applicable prize. Define

$$
f=1-\sum_i a_i\frac{t_i^{\mathrm{fix}}}{t},\qquad
F=f-\sum_i r_i,\qquad J_0=Ft.
$$

The maintained restrictions are $0<F\leq f\leq1$. Here $f$ is ticket cost less expected fixed-prize receipts, while $F$ additionally subtracts the maximum expected contribution of the smaller pooled prizes. The jackpot cutoff $J_0$ has monetary units. The quantities $f$ and $F$ are after-tax model parameters, not literal estimates of the lottery operator's accounting margin.

The historical Mega Millions game selects five of 56 main numbers and one of 46 extra numbers, giving $t=\binom{56}{5}46=175,711,536$. The modeled Powerball version selects five of 55 and one of 42, giving $146,107,962$ combinations. The latter rules cover August 28, 2005 through the end of 2008; optional higher-price tickets and variable fixed payouts are omitted. Lotto Texas selects six of 54 and New Jersey Pick 6 selects six of 49. These have $25,827,165$ and $13,983,816$ combinations respectively.

The authors deduct an assumed 25% tax from large payouts and ignore state taxes. Their Texas and New Jersey models pay a fixed three-match prize of three units. Four-match pools are respectively $0.033N$ and $0.05N$; five-match pools after the assumed tax are $0.0167N$ and $0.0413N$. These rules are sufficient to reconstruct category probabilities using hypergeometric counts: for a six-number game with $m$ possible numbers, the probability of exactly $k$ matches is $\binom6k\binom{m-6}{6-k}/\binom m6$.

Table 3B, printed p. 8, reports the following rounded calibration:

| Game | $f$ | $F$ | $J_0$ |
|---|---:|---:|---:|
| Mega Millions | 0.838 | 0.838 | 147 million |
| Powerball | 0.821 | 0.821 | 120 million |
| Lotto Texas | 0.957 | 0.910 | 23.5 million |
| New Jersey Pick 6 | 0.947 | 0.855 | 11.9 million |

The Texas row is not fully consistent with the printed six-of-54 rules: those rules give $f=1-3\binom63\binom{48}3/\binom{54}6=0.95981905$, and subtracting the printed pool rates gives $F=0.91011905$. The reported $F$ and cutoff are consistent with that reconstruction, whereas the printed $f=0.957$ is not ordinary three-decimal rounding of it. A replication should derive its parameters from a single coherent prize schedule, rather than combine inconsistent rounded entries.

## Exact sharing identity

Let $p$ be the probability that a random ticket wins a particular category. Conditional on one's ticket winning, the other $N-1$ tickets produce a binomial number of additional winners. The unconditional expected fraction of the pool paid to one's ticket is

$$
s(p,N)=\sum_{w=1}^{N}\frac1w\binom{N-1}{w-1}p^w(1-p)^{N-w}.
$$

The factor $p^w$ includes the probability that the ticket being valued wins. Omitting that factor would confuse conditional payout with unconditional expected return. Since $\binom{N-1}{w-1}/w=\binom Nw/N$, the binomial theorem gives the exact simplification

$$
s(p,N)=\frac{1-(1-p)^N}{N}.
$$

This is Proposition 4.4, printed p. 9. An alternative derivation integrates the binomial expansion of $(1-p+pu)^{N-1}$ over $u\in[0,1]$ and multiplies by $p$. No Poisson approximation is required. The continuous extension to positive real $N$ is useful for calculus, although an actual drawing has integer $N\geq1$.

Put $p_i=t_i^{\mathrm{pari}}/t$ and $p_J=1/t$. The exact expected net rate of return per ticket is

$$
R(N,J)=-f+\sum_i r_i\bigl[1-(1-p_i)^N\bigr]
+\frac JN\bigl[1-(1-1/t)^N\bigr].
$$

Equation (4.5), printed p. 9, includes the probability that no ticket wins a category: in that event its current pool contributes nothing to the valued ticket. A non-jackpot pari-mutuel category contributes less than $r_i$, approaching that amount as sales increase. Its total pool expands with sales, while a fixed jackpot is diluted by competing tickets.

For numerical work, evaluate $1-(1-p)^N$ as $-\operatorname{expm1}(N\operatorname{log1p}(-p))$. Directly subtracting two numbers near one loses precision for rare events. A Poisson replacement, $1-e^{-Np}$, is often accurate here but should be identified as an approximation. The exact formula is nearly as easy to compute.

The calculus results behind the later diagrams follow directly. Write $a=-\log(1-p)>0$. Then $s=(1-e^{-aN})/N$ decreases with $N$, since its derivative has numerator $e^{-aN}(1+aN)-1<0$. Meanwhile $Ns=1-e^{-aN}$ increases from zero to one. For real $N\downarrow0$, $s\to a$; for the actual minimum $N=1$, $s=p$. These distinct endpoints matter when interpreting a continuous curve as a ticket-selling model.

## A necessary jackpot cutoff and historical examples

Because each smaller pooled prize contributes at most $r_i$,

$$
R(N,J)\leq-F+Js(1/t,N)\leq-F+J/t.
$$

Consequently $J<J_0$ guarantees negative expected return. A jackpot above $J_0$ merely clears a necessary hurdle: sales can still make the expected return negative. For $N>1$ the final bound is strict. The source's occasional strict formulation at $N=1$ needs the obvious endpoint qualification.

Table 4, printed p. 9, illustrates the distinction. All jackpot and sales figures are rounded estimates:

| Drawing | After-tax cash $J$ | Tickets $N$ | Reported $R$ | $J/J_0$ | $N/J$ |
|---|---:|---:|---:|---:|---:|
| Lotto Texas, April 7, 2007 | 33.8 million | 4.2 million | +30% | 1.44 | 0.13 |
| Mega Millions, March 6, 2007 | 175 million | 212 million | −26% | 1.19 | 1.22 |
| Powerball, February 18, 2006 | 133 million | 157 million | −26% | 1.11 | 1.18 |
| Powerball, October 19, 2005 | 123.3 million | 161 million | −31% | 1.03 | 1.31 |

The favorable Texas drawing had an advertised jackpot of 75 million and a cash value of about 45 million before the assumed tax. The March 2007 Mega Millions advertisement was 390 million, but the modeled cash prize after tax was only 175 million. Using the advertisement directly in the sharing formula would substantially exaggerate expected return.

The paper estimates Powerball sales from counts of prize-winning tickets, Mega Millions sales from its two smallest prize categories, and Texas sales from a third-party historical series. It does not provide a complete machine-readable drawing panel, a likelihood for sales estimation, confidence intervals, or propagated uncertainty for the expected-return estimates. Near a break-even boundary, sales forecast uncertainty would be more important than additional decimal places in the formula.

Among roughly 700 Mega Millions and Powerball drawings under the covered rules through December 2008, the authors identify only three with $J\geq J_0$; those three are negative-return examples in the table. They report no New Jersey drawing exceeding its cutoff during 2007. These are sample-specific historical findings. They do not establish a theorem about future rules, sales behavior, or jackpot sizes.

## Break-even geometry and universal bounds

Normalize the state of a drawing as

$$
x=N/J,\qquad y=J/J_0.
$$

Substitution gives equation (6.1):

$$
R(x,y)=-f+\sum_i r_i\left[1-(1-p_i)^{xyJ_0}\right]
+\frac{1-(1-1/t)^{xyJ_0}}x.
$$

For fixed positive $x$, this is continuous and strictly increasing in $y$. Its limiting values are $-f$ at $y=0$ and $-F+1/x$ as $y\to\infty$. Therefore there is exactly one break-even height $y=\ell(x)$ for $0<x<1/F$. The implicit-function theorem makes the curve smooth because the derivative with respect to $y$ is positive. For $x\geq1/F$, no finite jackpot height can produce positive expected return while preserving that sales-to-jackpot ratio.

If there are no smaller pooled prizes, $F=f$ and the curve is explicit:

$$
\ell(x)=\frac{\log(1-fx)}{xJ_0\log(1-1/t)},\qquad0<x<1/f.
$$

It is increasing and convex. One transparent proof expands $-\log(1-fx)/x=\sum_{k\geq1}f^kx^{k-1}/k$: its positive coefficients give positive first and second derivatives inside the domain. With smaller pooled prizes, their contribution increases with sales and the source does not assert that the exact curve must remain increasing. Smoothness and unique height still follow from monotonicity in $y$.

The central general result, Theorem 6.5 on printed pp. 14–16, covers $t\geq500$ and $F\geq0.8$. Since $(1-1/t)^t$ increases toward $e^{-1}$ and exceeds $0.36$ at $t=500$, one obtains

$$
-1+\frac{1-0.45^{xy}}x<R(x,y)
<-0.8+\frac{1-0.36^{xy}}x.
$$

The constants use both $0.8\leq F\leq1$ and $f\leq1$. For example, $(1-1/t)^{Ft}$ lies strictly between $0.36$ and $0.45$; raising this base to $xy$ and combining the non-jackpot bounds gives the result. The lower expression defines curve $U$ where it equals zero, and the upper expression defines $L$. Above $U$ expected return is positive; below or to the right of $L$ it is negative. The intervening band needs the actual prize schedule.

The small-sales illustration $N<0.2J$ and $J>1.4J_0$ is conservative: the lower bound at $(0.2,1.4)$ is approximately $0.001754$, already positive. Its exact zero height at $x=0.2$ is $1.397254$. The large-sales illustration has a small rounding problem. The source treats $(1.12,2)$ as lying on $L$, but the upper bound there is $0.0023048$, positive. The exact height of $L$ at $1.12$ is approximately $1.978034$. Thus the printed rectangle $N>1.12J$, $J<2J_0$ is not justified by that bound alone. A conservative derived replacement is $N\geq1.13J$, $J\leq2J_0$: the upper expression at its corner is about $-0.002980$, and decreases as $x$ increases or $y$ decreases. This repairs the sufficient condition without changing the theorem itself.

## Nonuniform ticket choices and forecasting limits

Uniform ticket choice matters only for sharing, not for the lottery's probability of drawing any particular combination. The paper cites 70–80% computer-generated quick picks and suggests selecting combinations unpopular with people. That can reduce the conditional number of co-winners without increasing the chance of the combination being drawn.

A precise extension clarifies the required inputs. If a chosen combination has draw probability $1/t$ but each other buyer selects it with probability $q$, its jackpot contribution is

$$
\frac Jt E\frac1{1+\operatorname{Bin}(N-1,q)}
=\frac J{tNq}\left[1-(1-q)^N\right],
$$

with continuous limit $J/t$ at $q=0$. This is a derived extension, not a fitted model in the paper. It shows why one must not simply substitute $q$ for the winning probability in every factor. The authors' suggested effective-sales substitution $N'=0.7N$ is a heuristic bound for eliminating manually chosen competitors. Smaller prize categories and their actual pools need separate treatment; changing the number of competing tickets must not silently change the total sales that fund those pools.

The argument that the two large multistate games will remain bad bets depends on extrapolating past sales and rollover behavior. Under $N\geq J\geq J_0$, the chance of $k$ further rollovers is bounded using $(1-1/t)^{kJ_0}$, approximately $e^{-kF}$. Taking $F>0.82$, a historical jackpot growth factor no larger than 1.27 per rollover, and a largest observed starting ratio of 1.19, the authors estimate that reaching $2J_0$ needs three rollovers, with probability below roughly $1/11$. Combining this with an assumed two-year arrival interval gives an illustrative 22-year waiting scale.

The probabilistic calculation is conditional on the sales and growth assumptions. It is not proof that a positive-return drawing will never occur. Indeed, an added-in-proof footnote reports that the August 28, 2009 Mega Millions drawing had $J\approx159$ million and $N\approx149$ million, violating the historical $N>J$ pattern while still giving an estimated −23% return. This explicit qualification should accompany the paper's forward-looking language.

## Mean–variance investment calculation

The investment illustration uses five assets: AGG bonds, MSCI EAFE, FTSE/NAREIT REITs, S&P 500, and NASDAQ. Weekly adjusted returns span January 31, 1972–June 4, 2007, except AGG begins September 29, 2003. The article does not document how the unequal histories are reconciled for covariance estimation. There is no rolling training/test split, out-of-sample allocation exercise, trading-cost model, or parameter-uncertainty analysis.

Table 10 gives mean weekly returns in percent and covariances in squared percentage points:

$$
\mu=(0.057,0.242,0.266,0.109,0.147)' ,
$$

$$
C=\begin{pmatrix}
.198&.128&.037&-.077&-.141\\
.128&5.623&2.028&.488&.653\\
.037&2.028&4.748&.335&.419\\
-.077&.488&.335&10.042&10.210\\
-.141&.653&.419&10.210&12.857
\end{pmatrix}.
$$

With positive weekly risk-free return $R_F$, also measured in percent, the paper uses

$$
Z=C^{-1}(\mu-R_F\mathbf1),\qquad X=Z/\sum_k|Z_k|.
$$

It describes the absolute-weight normalization as collateralized or “Lintnerian” short selling. This is the stipulated risky-portfolio construction; a different financing, collateral-remuneration, leverage, or long-only convention requires solving its own constrained problem. The scale allocated between this risky portfolio and cash remains a separate choice.

A lottery position is assumed uncorrelated with every conventional asset. Adding it produces a block-diagonal covariance matrix and an additional unnormalized coefficient $Z_L=(R_L-R_F)/v$, where $R_L$ is the lottery return in percent and $v$ its variance in percent squared. This gives the exact algebraic share within the model:

$$
X_L=\frac{(R_L-R_F)/v}{\sum_{k=1}^5|Z_k|+(R_L-R_F)/v},\qquad R_L>R_F.
$$

The paper approximates one-ticket variance by retaining the jackpot contribution to the second moment:

$$
v_1\approx10^4\sum_{w\geq1}\left(\frac Jw-1\right)^2
\binom{N-1}{w-1}(1/t)^w(1-1/t)^{N-w}.
$$

This omits smaller-prize and losing-ticket contributions and the squared mean. Jackpot magnitudes make those omissions small in the example, but this is not the exact variance identity. The $10^4$ factor is essential when matching a covariance matrix expressed in percent squared. For a syndicate buying $S$ tickets, the authors use $v\approx v_1/S$ when $S\ll t$. This approximation needs a purchase and dependence model; it does not apply unchanged to a complete buyout, repeated identical tickets, or a large purchase that changes sales and sharing.

## What the negative-allocation theorem establishes

The paper's theorem says that an allocation falls below a practical threshold $\theta$ if

$$
v\geq\frac{R_L-R_F}{0.022\theta}.
$$

Its proof bounds $X_L<Z_L/|Z_2|$ and claims $Z_2>0.022$ for every positive $R_F$, using equation (10.2). The algebra is valid conditional on that coefficient bound. However, the printed Table 10 inputs do not reproduce the intercepts in equation (10.2). Direct inversion of the displayed matrix gives, as a derived consistency check,

$$
C^{-1}\mu\approx(.277262,.019192,.044607,-.008762,.019004)',
$$

$$
-C^{-1}\mathbf1\approx(-5.117748,.013062,-.164906,-.013513,-.118462)' .
$$

The risk-free slopes match the paper, but the second and third intercepts do not match its $0.023$ and $0.037$. Consequently the printed data support $Z_2>0.019$ for $R_F>0$, giving a conservative reconstructed theorem with $0.019$ in place of $0.022$. This is an independent calculation from rounded published inputs; the authors' underlying unrounded data and code are unavailable, so the source of the discrepancy cannot be identified conclusively.

For Texas the authors use $R_L\approx30\%$, $v_1\approx4\times10^{11}$ percent squared, total investable wealth of \$1,000, and $\theta=1/2000$, corresponding to rounding sub-\$0.50 allocations to zero. Their displayed calculation gives a variance threshold about $2.73\times10^6$ and an approximate syndicate-size cutoff of 145,000 tickets. The corrected conservative constant gives $30/(.019/2000)\approx3.158\times10^6$ and $S\approx126,667$ using the same rounded variance. Either scale remains conditional on the variance approximation. Exceeding it merely makes this sufficient exclusion bound fail; it does not prove that the exact optimal allocation becomes material.

There is also a conceptual limitation in the justification of mean–variance preferences. Printed p. 21 claims that Jensen's inequality makes lower variance preferable whenever two portfolios have equal means and utility is increasing and concave. That implication is false without a stronger distributional ordering. For a concrete derived counterexample, let positive terminal wealth $A$ equal $0.01$ with probability $0.1$ and $1.11$ otherwise, while $B$ equals $0.5$ or $1.5$ with equal probability. Both means are one; variances are $0.1089$ and $0.25$. Yet $E\log A\approx-0.366593<E\log B\approx-0.143841$: the smaller-variance wealth has lower expected log utility.

Jensen compares a gamble with its mean, or applies under a suitable conditional mean-preserving spread; variance alone does not order arbitrary distributions. Quadratic utility on an appropriate domain, restricted distribution families, or an explicitly controlled local approximation can justify mean–variance analysis. A rare enormous jackpot is precisely a setting where a casual second-order utility expansion needs scrutiny. The theorem therefore demonstrates negligible allocation under its specified mean–variance model and operational threshold, not that every increasing concave expected-utility investor must reject every favorable lottery opportunity.

## Reimplementation and scope

A faithful implementation first fixes a dated prize schedule and cash-versus-annuity convention, enumerates category probabilities, and derives $f,F,J_0$ without mixing rounded tables. For each drawing it estimates final sales and the relevant cash jackpot before evaluating the exact sharing formula. It should report expected return over plausible sales and payout ranges, distinguish observed final sales from information available when buying, and use the exact normalized curve when a universal bound is inconclusive.

For allocation, independently reproduce the empirical covariance inputs, preserve percentage units, specify the risk-free horizon and short-sale financing, and calculate the full lottery distribution or a justified variance approximation. Syndicate diversification requires its own joint-ticket design and cost accounting. Ticket indivisibility, organizer fees, purchase limits, prize claims, tax treatment, and operational overhead are outside the clean formula. The source explicitly excludes a full buyout analysis because buying all combinations changes several of these mechanisms.

The useful conclusion is conditional and quantitative: shared prizes can make a huge advertised jackpot a negative-expectation claim; a positive-expectation claim can still have a very small allocation under a stated portfolio objective. The exact sharing identity, normalized cutoff, and break-even bounds are reusable. Historical extrapolations, approximated variances, and utility claims need the qualifications documented above.
