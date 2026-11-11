# On the origin of power-law tails in price fluctuations

J. Doyne Farmer and Fabrizio Lillo. *Quantitative Finance* 4(1), C7–C11 (2004), commentary. DOI: 10.1088/1469-7688/4/1/C01.

Source: [local published commentary](../../Finance/stockreturns_DoyneFarmerLillo_2003.pdf), five pages, including the note added in proof. The filename carries 2003, corresponding to the working-paper period; the journal volume is 2004. [Publisher bibliographic record](https://www.tandfonline.com/doi/abs/10.1088/1469-7688/4/1/C01). The note below summarizes this source's experiments and criticisms, not the complete later debate or a general rejection of every square-root impact model.

## Why this matters

A relation between total volume and squared returns can appear to confirm a model of transaction-level impact even when that model is false by construction. Farmer and Lillo demonstrate this using actual correlated order flow and artificial price changes with a known impact exponent. Their point concerns identification: an aggregate conditional moment does not uniquely recover the microscopic response function when cross-transaction dependencies contribute to that moment.

The paper also measures immediate transaction impact with an error calculation designed for persistent observations, compares trade-volume and return tails, and distinguishes electronic from privately negotiated trading. These pieces jointly challenge a proposed deterministic explanation of large price moves. A reproducible exercise should therefore test both the transformation of volume into returns and the inference procedure used to establish that transformation. Merely fitting a straight line to an aggregated scatterplot does not resolve the mechanism.

This is a short empirical commentary with three figures. It provides a concrete counterexample and diagnostic method, not a fully calibrated alternative structural model. Its strongest conclusion is that volume, mean impact, and temporal dependence cannot be collapsed into one deterministic exponent calculation without checking the underlying assumptions.

## The theory being examined

The criticized theory starts with a survival tail for transaction volume $V$,

$$
\Pr(V>x)\sim Cx^{-\gamma},\qquad \gamma\approx1.5,
$$

and a deterministic monotone relation between a transaction's size and the magnitude of its price impact,

$$
|r|=kV^\beta,\qquad k>0,\quad\beta>0.
$$

Changing variables gives

$$
\Pr(|r|>x)=\Pr\left(V>(x/k)^{1/\beta}\right)
\sim Ck^{\gamma/\beta}x^{-\gamma/\beta}.
$$

Thus the return survival exponent is $\alpha=\gamma/\beta$. Setting $\gamma=1.5$ and $\beta=0.5$ produces $\alpha=3$. These are survival exponents; density exponents would be larger by one.

The algebra is valid under the deterministic transformation. The empirical question is whether an estimated **conditional mean impact** can substitute for that deterministic relation when individual responses are noisy and liquidity varies. In general it cannot: $E[r\mid V]$ does not determine the full distribution of $r\mid V$, especially its tails. A stochastic response coefficient, gaps in the order book, or dependence between impact and order size can change the tail transformation. These are the mechanisms the commentary says require attention, rather than assumptions established by its own complete alternative model.

The trade is also an operational unit. It refers to the incoming order, or immediately executed part of an order, that changes the quotes. It does not necessarily mean a large investor's complete parent order spread over time. Results about immediate child-order response should not be generalized automatically to the execution cost of a metaorder.

## Why the aggregate squared-return test is ambiguous

Let transaction $i$ have sign $\epsilon_i\in\{-1,+1\}$, volume $V_i$, and log-price change

$$
r_i=k\epsilon_iV_i^\beta+u_i.
$$

For a block of $M$ transactions, define total signed return $R=\sum_i r_i$ and unsigned volume $Q=\sum_iV_i$. Expanding the square gives

$$
R^2=k^2\sum_iV_i^{2\beta}
+2k^2\sum_{i<j}\epsilon_i\epsilon_jV_i^\beta V_j^\beta
+2k\sum_{i,j}\epsilon_iV_i^\beta u_j
+\left(\sum_i u_i\right)^2.
$$

Under strong assumptions that make the cross terms vanish conditionally, $\beta=1/2$ makes the first term proportional to total volume. With fixed $M$, independent zero-mean noise of variance $\sigma_u^2$ contributes $M\sigma_u^2$, giving the familiar affine form $E[R^2\mid Q]=a+bQ$.

The qualification “conditionally” matters. Unconditional lack of correlation alone is not enough to eliminate all cross terms after conditioning on $Q$. With random transaction counts, the noise contribution becomes $\sigma_u^2E[M\mid Q]$ and need not be a constant. This expanded derivation makes explicit the assumptions behind the source's schematic affine argument; it is not an additional estimated result.

Actual order signs and transaction sizes are serially dependent. Persistent sign sequences make the cross-transaction sum economically and statistically material. Consequently, an approximately linear relation between total volume and squared aggregate return can emerge for impact exponents other than one-half. Observing the aggregate relation therefore does not identify the transaction-level exponent.

## Counterexample using real order flow

Section 1 and Figure 1 use Vodafone transactions from May 2000 through December 2002, approximately one million trades. Preserve the chronological sequence of actual transaction signs and share volumes. Replace the observed price response with an artificial deterministic response

$$
\widetilde r_i=k\epsilon_iV_i^{0.3}.
$$

There is no added noise in this construction. The impact exponent is known and intentionally differs from one-half. The constant $k$ changes scale, not the exponent or the essential linearity comparison; the source does not give a numerical calibration or fully specify every plotting normalization.

For each block, compute $\widetilde R=\sum_i\widetilde r_i$ and $Q=\sum_iV_i$, then estimate the conditional average $E[\widetilde R^2\mid Q]$ by volume groups. Figure 1(a) uses fixed trade counts $M=2,5,10,20,40$. For short blocks the curve retains curvature associated with $V^{0.6}$. At larger $M$, the relationship becomes approximately linear. Forty transactions is roughly the average activity in fifteen minutes for this sample.

The source reports that, using error bars specified by the criticized study, it cannot reject a linear relation at the 95% confidence level for the large blocks. This is a failure to reject the aggregate null despite a false microscopic square-root rule. It is not a 95% confidence statement that the true impact exponent equals one-half. The commentary does not provide the full original test's implementation or numerical rejection statistic, so that exact significance calculation requires additional material.

Figure 1(b) repeats the exercise in fixed fifteen-minute windows, allowing the transaction count to vary. The apparent linearity is even clearer. This rules out the suggestion that the counterexample depends only on fixing the number of trades rather than elapsed time.

Figure 1(c) randomizes the transaction order. A faithful implementation should shuffle the paired events $(\epsilon_i,V_i)$ together, preserving the sign-size association within each event while disrupting their temporal sequence. The shuffled construction remains visibly nonlinear even at 40 trades, exposing the exponent of 0.3. The comparison demonstrates that dependence in the chronological order flow changes what the aggregate diagnostic detects.

The source does not report a random seed, the number of independent shuffle repetitions, exact volume-bin edges, or a distribution of test power over many simulated samples. It demonstrates a concrete counterexample rather than a formal universal power theorem. Replication should save all of those choices and distinguish reproduction of the displayed realization from a broader assessment of the test's reliability.

## Measuring immediate impact directly

Section 2 replaces the aggregate diagnostic with event-level measurement. For each immediately executed order component, record midpoint quotes immediately before and after the execution:

$$
r_i=\log p_{a,i}-\log p_{b,i}.
$$

The price is the bid–ask midpoint, not the transaction price. This reduces the direct bid–ask bounce that would arise from alternating transaction prices, although quote synchronization and stale quotes can still matter. Buys and sells are analyzed separately. Figure 2 displays buy-initiated events.

For the London Stock Exchange, the electronic SETS data identify order direction directly. For NYSE data, direction is inferred from trades and quotes using the Lee–Ready procedure. The source additionally groups transactions sharing a timestamp and order code. These are substantive market-specific preprocessing differences, not cosmetic details. The exact quote-matching latency, ambiguity handling, and complete cleaning filters are not specified in this commentary.

The illustrated stocks are Lloyds (LLOY), Shell (SHEL), and Vodafone (VOD) on the LSE during May 2000–December 2002, and General Electric (GE), Procter & Gamble (PG), and AT&T (T) on the NYSE during 1995–1996. The LSE analysis contains roughly a million observations per illustrated stock. The markets are observed in different periods, so the comparison does not isolate exchange design from every historical or firm-level difference.

Group same-sign events by volume into bins with approximately equal observation counts. Within each bin, plot mean volume against mean midpoint return. Equal-count bins differ from equal-width volume bins and provide more even sampling precision across the curve. The bin count and exact edges are not supplied. Zero-impact events should not be discarded without an explicit documented reason: they contribute to the conditional mean response of transactions.

## Long-memory error calculation

The authors argue that conventional iid standard errors understate uncertainty in these conditional means. Persistent magnitudes imply that returns selected into a volume bin can remain dependent even when they are separated in event time. Long memory is described by autocorrelation proportional to lag raised to $-\kappa$, with $\kappa<1$, so its infinite-lag sum is not finite in the idealized model.

For one volume bin with $K$ chronologically ordered observations, choose a block size $n$ and divide the records into $m=K/n$ adjacent blocks. Compute a mean within each block,

$$
\bar r_j^{(n)}=\frac1n\sum_{i\in B_j}r_i,
$$

and the sample standard deviation of these block means, denoted $s(n)$. Repeat across block sizes and fit

$$
s(n)=An^{H-1},\qquad
\log s(n)=\log A+(H-1)\log n.
$$

Ordinary least squares on the log-log variance plot produces $\widehat A$ and $\widehat H$. Extrapolate the standard error of the full-bin mean to a block containing all $K$ observations:

$$
\widehat{\operatorname{se}}(\bar r)=\widehat A K^{\widehat H-1}.
$$

The text says to extrapolate to “$m=K$,” but its formula clearly requires **$n=K$**. Treat that as a notation slip, not an instruction to extrapolate to blocks of one observation. The full-bin standard error cannot be estimated as an across-block sample standard deviation at $n=K$, because only one block remains; the fitted scaling curve supplies the extrapolation.

For iid observations, $H=1/2$ gives the familiar inverse-square-root rate. When $H>1/2$, precision improves more slowly with sample size. The paper finds Hurst estimates substantially above one-half in small-volume bins and closer to one-half in large-volume bins. Because bins have similar counts, the authors argue that this difference cannot simply be explained by different average intervals between selected events.

No numerical table of Hurst estimates, exact fitted block-size range, treatment of remainders, or confidence level for Figure 2's error bars is provided. The extrapolation also relies on a scaling relation continuing toward the full sample. The authors explicitly do not estimate regression standard errors for the final impact exponent. The figure therefore supports a visual comparison using dependence-aware point uncertainties, not a fully specified joint hypothesis test of a common exponent across all six stocks.

## Impact and tail results

For NYSE stocks, the measured mean impact is not one power law over the whole volume range. At small volumes, an effective slope near 0.5 is plausible, whereas at large volumes it appears below 0.2. The discussion cites earlier evidence that the transition occurs at smaller volumes for lower-capitalization firms. This large-volume region is precisely the region relevant to transforming a far volume tail into a far return tail.

For the illustrated LSE stocks, a power-law approximation is more plausible across the displayed range, but the least-squares exponent is approximately 0.26, well below 0.5. The authors regard the bin-level error bars as inconsistent with a square-root curve in both markets. The source does not provide a confidence interval around 0.26. The Paris logarithmic-impact observation is attributed to other work and is not newly estimated in these figures.

Even retaining the deterministic transformation logic with a NYSE volume survival exponent of about 1.5, an illustrative impact exponent of 0.25 implies a return exponent of about six, rather than the commonly observed value near three. This is an order-of-magnitude inconsistency in the proposed mechanism; it is not a calibrated forecasting model or a claim that all NYSE impact exponents equal 0.25.

Section 3 then examines LSE transaction volumes normalized by each stock's sample mean. Figure 3(a) plots a **density**, while Figure 3(b) plots a **return survival function**. Comparing their graphical slopes without converting density to survival would be incorrect. The volume curves for LLOY, SHEL, and VOD are strikingly similar, and the authors report similar behavior for roughly twenty stocks studied. They find no convincing power-law volume tail in this electronic-market sample.

If one forces a tail fit over normalized volumes of roughly 10–100, the implied volume survival exponent is highly uncertain but at least about three. Combined with an impact exponent near 0.3, the deterministic formula would imply a return index near ten. Instead, the reported rough return-tail estimates are 2.2 for SHEL, 2.5 for LLOY, and 4.3 for VOD. These estimates lack detailed uncertainty and fit specifications in the commentary. Their significance is the qualitative mismatch: nearly matching volume distributions coexist with materially different return tails, and VOD's relatively steep return tail goes in the opposite direction from the simple exponent-ratio prediction based on its impact curve.

## The note added in proof and scope of the conclusion

The final note qualifies a potentially misleading broad reading of the volume evidence. Privately negotiated “upstairs” LSE trades can have power-law size distributions, whereas the electronic “downstairs” SETS sample analyzed here does not show the same pattern. Upstairs trades are arranged privately and reported after agreement; the source says order splitting there is rare. Therefore, the correct statement is about the sampled electronic market, not all London trading volume.

The note also cites later work attributing large moves in NYSE and electronic LSE data to fluctuations in liquidity, with the conditional tail of price responses relatively insensitive to order size. Those are reported findings from cited studies, not an additional fully documented experiment in this five-page commentary. The alternative direction proposed here is stochastic order placement and variable price response, potentially driven by order-book liquidity. No estimated gap distribution, complete simulator, or liquidity forecasting equation is supplied.

The paper rejects the adequacy of a specific evidentiary chain: a linear aggregate conditional moment, interpreted as proof of deterministic square-root transaction impact, used with a universal volume tail to explain return tails. It does not establish that volume never matters, that every execution-impact model fails, or that a square-root relationship cannot arise for other definitions such as larger parent orders or different horizons.

## Reimplementation priorities

The most discriminating replication is the controlled response experiment: hold real signs and volumes fixed, impose the known exponent 0.3, aggregate at the stated trade counts and fifteen-minute intervals, then compare chronological and shuffled data. This separates the truth of the microscopic response rule from the apparent success of the aggregate diagnostic.

The event-level counterpart needs order direction, aligned pre/post midpoint quotes, explicit treatment of executed order components, equal-count volume bins, and chronological block-mean error estimation. Preserve venue and sample-period labels. Then compare volume density, correctly converted survival exponents, and return survival tails without confusing a conditional average with a deterministic transformation.

Exact reproduction remains limited by absent raw extracts, detailed quote alignment and filters, bin definitions, block-size fitting choices, normalization constants in the synthetic plots, the original aggregate test's complete error calculation, and shuffle seeds. The source's lasting methodological contribution is nevertheless precise: serial dependence can invalidate the identification claimed by an aggregate moment test, and matching conditional means is insufficient to explain extreme conditional outcomes.
