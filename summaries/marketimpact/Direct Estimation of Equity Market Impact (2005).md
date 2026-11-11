# Direct Estimation of Equity Market Impact

**Authors:** Robert Almgren, Chee Thum, Emmanuel Hauptmann, Hong Li
**Year:** 2005
**Journal/Venue:** Working paper, University of Toronto / Citigroup Global Quantitative Research, May 10, 2005 (original version December 20, 2004); condensed version published as "Equity market impact", *Risk*, July 2005, pp. 57--62.
**Source file:** Finance/MarketImpact_Almgren_2005a.pdf

## Question

Using proprietary institutional parent-order data (with known start/end times, sign and fills), estimate the functional form and coefficients of permanent and temporary impact as functions of order size and **execution rate**, in a form that plugs directly into Almgren--Chriss scheduling and pre-/post-trade cost estimation (Citigroup BECS).

## Data

- Citigroup US equity desks, Dec 2001--Jun 2003: 682,562 orders before filtering.
- Filters: S&P 500 names only; drop ~400 orders in stocks with daily vol > 12.5%; drop market-on-open/close (a few hundred), VWAP-instructed orders (~16%, long and slow), orders with any fill after 4:10pm (~10%, mostly block-desk fills with unreliable timestamps); keep orders with $\ge 2$ transactions, $\ge 1000$ shares and $\ge 0.25\%$ ADV. Final sample: **29,509 orders**; median ~5 executions (max 548), median duration ~0.5 hour.
- Sample (Table 2): $|X|$/ADV mean 1.51%, median 0.62%, Q3 1.36%, max 88.6%; duration median 0.32 day (volume time); daily vol median 2.2%; mean spread median 11 bp. Signed costs are nearly symmetric around zero (mean total cost 4 bp).
- Filled size is used instead of requested size; results are "almost exactly the same" with or without partially filled orders, so limit-order fill bias is judged small.

## Measurement

- $S_0$: TAQ mid just before the first transaction; $\bar S$: fill-weighted average price; $S_{\text{post}}$: first mid after $t_n + 30$ min (carried to next morning if after close -- accepted despite overnight noise because it gave more consistent fits than truncating). The 30-min lag was chosen because the fitted coefficients stop varying with the lag around that point.
- Permanent $I=(S_{\text{post}}-S_0)/S_0$; realized $J=(\bar S-S_0)/S_0$ (the actual cost, including spread since $S_0$ is a mid).
- **Volume time** $\tau\in[0,1]$: fraction of an average day's volume traded by clock time $t$; constant rate in $\tau$ = VWAP in clock time. Implicitly assumes the intraday volatility profile matches the volume profile (Fig. 2: approximately true). $VT$ is measured directly as the 10-day average volume traded between the order's clock start and end times, so $T$ never has to be estimated separately.
- $V$: 10-day average daily volume; $\sigma$: intraday realized-vol estimator using all trades; both tracked through time per stock.

## Model

Constant trade rate $v=X/T$ in volume time; arithmetic BM with permanent drift and additive temporary impact:

$$dS = S_0\,g(v)\,d\tau + S_0\sigma\,dB,\qquad \tilde S(\tau)=S(\tau)+S_0\,h(v).$$

Integrating over $[0,T]$ and to $T_{\text{post}}=\tau_{\text{post}}-\tau_0$:

$$I = T\,g\!\left(\tfrac{X}{T}\right)+\sigma\sqrt{T_{\text{post}}}\,\xi,$$
$$J-\tfrac{I}{2} = h\!\left(\tfrac{X}{T}\right)+\sigma\left[\sqrt{\tfrac{T}{12}\left(4-3\tfrac{T}{T_{\text{post}}}\right)}\,\chi-\tfrac{T_{\text{post}}-T}{2\sqrt{T_{\text{post}}}}\,\xi\right],$$

$\xi,\chi$ independent $N(0,1)$. The $I/2$ term is the permanent impact of earlier fills borne by later fills (exact for linear $g$). The noise expressions are used only as heteroskedastic regression weights. Permanent impact with linear $g$ is independent of $T$ ("stealth" trading impossible by construction). No cross-impact; buy/sell symmetric coefficients (asymmetry tested informally, not needed).

Power laws $g(v)=\pm\gamma|v|^\alpha$, $h(v)=\pm\eta|v|^\beta$. Priors: $\alpha=1$ is the only no-quasi-arbitrage value (Huberman--Stanzl 2004; nonlinear temporary impact does not create arbitrage); $0<\beta<1$ from the empirical literature, with $\beta=1/2$ (Barra 1997) the common candidate.

Cross-sectional scaling: size is measured relative to expected volume during execution, $X/(VT)$, and price moves in units of $\sigma$. Permanent impact gets a liquidity factor $(\Theta/V)^\delta$, $\Theta$ = shares outstanding (inverse turnover). Spread showed no consistent effect; market cap (a "price effect") has a weak persistent effect that is dropped; temporary impact needed **no** stock-specific factor beyond $\sigma$ and $V$.

$$\frac{I}{\sigma}=\gamma\,T\,\operatorname{sgn}(X)\left|\frac{X}{VT}\right|^{\alpha}\left(\frac{\Theta}{V}\right)^{\delta}+\text{noise},\qquad \frac{1}{\sigma}\left(J-\frac{I}{2}\right)=\eta\,\operatorname{sgn}(X)\left|\frac{X}{VT}\right|^{\beta}+\text{noise}.$$

## Results

Nonlinear (modified Gauss--Newton, weighted) fit of exponents, $\pm$ one s.e.:

$$\alpha=0.891\pm0.10,\qquad \delta=0.267\pm0.22,\qquad \beta=0.600\pm0.038.$$

- $\alpha=1$ not rejected (about 1.1 s.e. away); adopted.
- $\delta\approx1/4$ adopted -- but note the s.e. is nearly as large as the estimate: $\delta=0$ is also not rejected.
- $\beta=1/2$ rejected at 95% (about 2.6 s.e.); $\beta=3/5$ adopted. Relative to square root this gives slightly lower cost for small rates and higher for large.

Weighted linear fit with exponents fixed: $\gamma=0.314\pm0.041$ ($t=7.7$), $\eta=0.142\pm0.0062$ ($t=23$). $R^2<1\%$, as expected when volatility dominates single-order outcomes. Final "universal" model:

$$I=\gamma\,\sigma\,\frac{X}{V}\left(\frac{\Theta}{V}\right)^{1/4},\qquad J=\frac{I}{2}+\operatorname{sgn}(X)\,\eta\,\sigma\left|\frac{X}{VT}\right|^{3/5}.$$

Worked example (Table 3), buying 10% of ADV:

| | IBM | DRI |
|---|---|---|
| $\Theta/V$ | 263 | 87 |
| $\sigma$ | 1.57% | 2.26% |
| $I/\sigma$ | 0.126 | 0.096 |
| $I$ (bp) | 20 | 22 |
| $K=J-I/2$ (bp), $T=0.1/0.2/0.5$ day | 22 / 15 / 8 | 32 / 21 / 12 |
| $J$ (bp), $T=0.1/0.2/0.5$ | 32 / 25 / 18 | 43 / 32 / 23 |

Lower turnover (IBM) means more permanent impact per unit of ADV traded; temporary cost as a fraction of $\sigma$ depends only on participation $X/(VT)$ (0.142, 0.094, 0.054 for $T=0.1,0.2,0.5$).

Residuals: $\xi,\chi$ have mean near 0, variance near 1, small correlation, but are strongly fat-tailed (normal for short-horizon returns); the Gaussian fits the core. Single-stock fits (exponents fixed) were too noisy to be useful, motivating the pooled cross-sectional specification.

## Assessment

**Convincing.** Parent-order data with timestamps, the use of volume time, and the explicit noise model (giving proper heteroskedastic weights) are the paper's real contributions; the $\sigma\cdot f(\text{participation})$ normalization is simple and has held up in later work. The IBM/DRI table is a practical sanity-check calibration: for 10% ADV over a half day, total cost of order 20 bp in a large cap.

**Fragile.**
- "Permanent" impact is the price 30 minutes after completion. Later work (propagator models, Bouchaud et al.; Moro et al.; Bershova--Rakhlin) finds substantial post-trade reversion over longer horizons, so part of $I$ is transient; the $J-I/2$ decomposition then misallocates cost between the two components.
- Endogeneity: execution duration $T$ is chosen by traders, likely in response to realized prices, urgency or alpha; identification of $h$ comes from cross-order variation in $T$ and is exposed to this selection. Client alpha (information in the order itself) is also absorbed into $I$.
- $\delta$ is essentially unidentified ($0.267\pm0.22$); the $(\Theta/V)^{1/4}$ factor is a modeling choice more than an estimate, and $\gamma$'s $t$-stat is conditional on it.
- Exponent standard errors assume Gaussian residuals, which are visibly fat-tailed; the rejection of $\beta=1/2$ is at about 2.6 s.e. and would be sensitive to robust errors and sample (later studies with metaorder data commonly find exponents near 1/2 for total impact vs. $Q/V$; note that here $\beta$ is an exponent in *rate*, not total size, so the comparison is not one-to-one).
- One broker, one 19-month period, S&P 500 only, orders mostly $<$ a few % ADV; the authors explicitly disclaim larger orders. Out-of-sample backtests are promised but not shown.
- Constant-rate (VWAP-in-$\tau$) approximation of actual trajectories; no spread term despite $J$ including spread crossing (spread showed no consistent dependence, possibly because the sample is liquid large caps).

**Practical use.** A ready-to-use large-cap cost model: permanent linear in $X/V$ (so, for linear-impact portfolio optimization, a quadratic cost in trade size with coefficient $\propto\sigma/V$), plus a concave rate-dependent temporary term that drives the speed/risk trade-off in scheduling. For a PM, the key takeaways are the scaling (cost $\propto\sigma$, participation $X/VT$) and the magnitudes; the exponents and the turnover factor should be re-estimated on one's own fills, as the authors themselves note that coefficients, exponents, and even forms should be updated continually.
