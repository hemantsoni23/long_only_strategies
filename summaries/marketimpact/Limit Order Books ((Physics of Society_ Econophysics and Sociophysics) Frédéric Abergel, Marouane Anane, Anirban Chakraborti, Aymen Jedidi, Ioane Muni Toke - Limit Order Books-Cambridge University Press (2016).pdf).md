# Limit Order Books — Detailed Quantitative Research Notes

**Authors:** Frédéric Abergel, Marouane Anane, Anirban Chakraborti, Aymen Jedidi, Ioane Muni Toke | **Year:** 2016 | **Venue:** Cambridge University Press, series *Physics of Society: Econophysics and Sociophysics* (foreword by J.-P. Bouchaud) | **Source file:** `Finance/(Physics of Society_ Econophysics and Sociophysics) Frédéric Abergel, Marouane Anane, Anirban Chakraborti, Aymen Jedidi, Ioane Muni Toke - Limit Order Books-Cambridge University Press (2016).pdf` (the extracted text stops at the end of Chapter 5, about p. 58. Chapters 6–10 are described only from the table of contents and figure/table lists.)

---

## Scope and stance

The book is a monograph from the CentraleSupélec (formerly Ecole Centrale Paris) Chair of Quantitative Finance, funded by BNP Paribas. It compiles the authors' papers: Chakraborti et al. 2011a,b; Abergel–Jedidi 2013, 2015; Muni Toke 2011, 2015; Anane–Abergel 2015. The method is that of an experimental physicist: stylized facts first, then statistical (mostly "zero-intelligence") models, then simulation, then predictability.

The book works with a stylized price/time-priority book with only three order types: limit, market, cancel. **It explicitly does not address market impact.** Strategic, utility-based models (Parlour–Seppi) and trading strategies are left out, except for Chapter 10.

Structure:
- Part I: empirics (Ch. 2–4).
- Part II: models (Ch. 5 survey; Ch. 6 zero-intelligence mathematics; Ch. 7 queueing; Ch. 8 interacting agents and Hawkes).
- Part III: simulation (Ch. 9).
- Part IV: predictability (Ch. 10).
- Appendices: order types, data, point-process notions, prediction tables.

## Part I — Empirical properties (Euronext Paris, mainly 2007–2008)

### Ch. 2: Stylized facts

Stocks: BNPP.PA and other CAC names; BNP data runs Sep/Oct 2007 to May 2008.

- **Durations.** Market-order inter-arrival times are clearly non-exponential, and a Weibull fits well. Counts of trades in a window $\tau$ fit neither a lognormal nor a gamma well. This motivates ACD models (Engle–Russell), time-changed Poisson processes, and Hawkes processes.
- **Order sizes.** Market-order sizes normalized by their mean have a power-law tail, $1+\mu\approx 2.7$ by Hill estimator, versus 2.3–2.7 in Gopikrishnan et al. and Maslov–Mills. Limit orders give $1+\mu\approx 2.1$, but the curves collapse poorly across stocks. Sizes cluster at round lots.
- **Placement** relative to the same-side best quote. The density peaks at $\Delta p=0$ and is heavy-tailed. Placement is asymmetric because in-spread placement is bounded by the spread. Literature exponents are exchange-specific: $1+\mu\approx 1.6$ (Paris), 2.0 (NYSE), 2.5 (LSE). Mike–Farmer fit a Student-t with 1.3 degrees of freedom.
- **Lifetimes.** Order IDs are missing, so lifetimes are reconstructed by matching price and quantity. Both cancelled and executed orders show power laws with $1+\mu\approx 1.3$–1.6. Challet–Stinchcombe report 2.1 (cancelled) and 1.5 (executed). There is a cut-off near 20,000 s because overnight orders are dropped.
- **Average shape.** Mean depth *increases* over the first five levels, so the maximum sits away from the best quote. The average gap between levels is constant: <1 tick for FTE, 1.5 for BNPP, 2.0 for SOGN, 2.5 for RENA. The mean spread is about 1.5–2.4 times the mean gap.
- **Seasonality.** Order counts are U-shaped over the day. Counts per 5-minute interval vary by about a factor of 10 intraday. Market- and limit-order activity are highly correlated.

### Ch. 3: Book shape vs. limit-order size (Muni Toke 2015)

Sample: 14 CAC 40 stocks, 30-minute bins from 10:00 to 16:00, $T=391$ bins per stock, 5,474 observations in total. The model is a fixed-effects panel regression:
$$B_k(t)=\beta_1L_k(t)+\beta_2V^L_k(t)+\beta_3L_kV^L_k+\beta_4M_k(t)V^M_k(t)+\delta_k+\eta_{k,t},$$
Here $B$ is cumulative depth within 5 or 10 ticks of the *opposite* best, or the 6–10 tick band. $L$ is the number of limit orders, $V^L$ their mean euro size, and $M V^M$ the traded volume. The published table labels are garbled in places ($V^M$ printed where the text means $V^L$).

Robust result, raw and deseasonalized: holding total flow fixed, **fewer, larger limit orders make a deeper book**. $\beta_1<0$ and $\beta_2>0$ in every specification. Deseasonalized $B^{10}$, without the interaction term, gives $\hat\beta_1=-0.666$ ($t=-15.7$), $\hat\beta_2=50.95$ ($t=34.8$), $R^2=0.21$. Raw $B^5$ gives $\hat\beta_1=-0.245$ ($t=-12.2$), $\hat\beta_2=8.71$ ($t=11.6$), $R^2=0.08$.

The traded-volume effect is positive in raw data, which echoes Næs–Skjeltorp, but it turns negative after deseasonalization, so it is not robust. Chapter 7 (Sec. 7.4–7.5) gives the queueing model that produces the size effect.

### Ch. 4: Market making and market taking in physical time (Muni Toke 2011)

- **Spread in calendar time vs. event time.** Time-weighting concentrates mass on common spreads, so **wide spreads close faster**. The mean wait to the next event is 320 ms in the smallest-spread tercile and 200 ms in the largest.
- **Liquidity replenishment ("market making").**
  - The time from a market order to the next limit order is 1.3 (BNPP) to 2.6 (LAGA) times shorter than a generic inter-event time.
  - On FTSE futures, 40% of all inter-event gaps are under 50 ms; for market-to-limit gaps the share is about 70%.
  - The effect does not depend on side: the following limit order has the same sign 48.8% (BNPP), 51.9% (PEUP) and 50.7% (LAGA) of the time.
  - Kolmogorov–Smirnov, Cramér–von Mises and Wilcoxon tests reject the independent-Poisson null.
- **Reciprocal effect (limit then market).** No such effect appears when all orders are pooled. For equities, limit-to-market gaps are stochastically *longer*; futures show no difference.
- **Aggressive vs. passive split.** Superscript 1 marks an order that moves the mid; superscript 0 marks one that does not. Daily averages: 48k limit orders, 41k cancels and 7.8k market orders, 97k events in total.

Conditional next-event probabilities, conditioned on the previous event, versus the unconditional rate:

| Previous event | Next event | Conditional | Unconditional |
|---|---|---|---|
| $M^0_{buy}$ | $M^0_{buy}$ | 34.6% | 3.0% |
| $L^1_{buy}$ | $M^1_{sell}$ (market taking) | 10.7% | 1.3% |
| $L^1_{buy}$ | $C^1_{buy}$ (fleeting quotes, possibly spoofing) | 5.8% | 0.85% |
| $M^1_{buy}$ | $L^1_{buy}$ | 11.5% | 2.1% |
| $M^1_{buy}$ | $L^1_{sell}$ | 8.0% | 2.1% |

The $M^0_{buy}\to M^0_{buy}$ row reflects order splitting and momentum. The $M^1_{buy}$ rows show replenishment on both sides.

- **Lagged correlation matrices** $\rho^h_\tau(i,j)=\mathrm{Corr}\big(N_i(t+h+\tau)-N_i(t+\tau),\,N_j(t+h)-N_j(t)\big)$, with $h=0.1$ s and $\tau\in\{0.1,\dots,0.9\}$ s. $M^1_{buy}$ intensity loads on past $M^0_{buy}$ and $M^1_{buy}$ (clustering) and on $L^1$ from *both* sides (market taking). Bid and ask behave symmetrically, which justifies pooling the two sides.

## Part II — Models

### Ch. 5: Survey of agent-based / zero-intelligence (ZI) models (fully read)

| Model | Mechanism | Outcome / defect |
|---|---|---|
| Stigler (1964) | Uniform random bids/asks on $L=10$ ticks, unit size, cancelled after $N=25$ steps | Slanina's replication with $L=N=5000$ gives a return tail exponent of about 0.3, and the grid truncates the tails |
| Garman (1976) | Poisson buy/sell flows on a price grid; book state is a vector $(n_i)$ | Microstructure explains negative autocorrelation of price changes; no analytical solution, so Monte Carlo |
| Gode–Sunder (1993) | ZI traders, constrained vs. unconstrained | Allocative efficiency without intelligence; criticized by Cliff–Bruten (1997) |
| Bak–Paczuski–Shubik (1997) | Reaction–diffusion $A+B\to\emptyset$; orders random-walk | $\Delta p\sim t^{1/4}(\ln t/t_0)^{1/2}$, so $H=1/4$ (subdiffusive), no fat tails; moving orders are unrealistic |
| Maslov (2000) | Limit w.p. $q_l$ at offset $U[0,4]$; market orders; fixed lifetime or capacity | Return tail exponent about 3.0 (realistic), but $H=1/4$ |
| Challet–Stinchcombe (2001) | Deposition/evaporation/annihilation; Gaussian placement with $\sigma=Ks(t)+C$ | $H=1/4$ at short scales, $H\to 1/2$ at long scales; never superdiffusive |
| Mike–Farmer (2008) | Student-t placement; cancellation hazard $A(1-e^{-y})(N_{imb}+B)/N_t$; order signs from fractional Brownian motion with $H=1-\beta/2$ | Good return and spread distributions, but fits only about half of 24 other stocks. Needs an ad hoc floor of at least 2 orders per side, active exactly in tail events. fBm signs induce return autocorrelation and blow up long-horizon variance |
| Smith et al. (2003) | Poisson limit ($\lambda_L$), market ($\lambda_M$) and cancel ($\lambda_C$) flows on an infinite grid; mean-field | Dimensional scaling: depth $\sim\lambda_L/\lambda_C$, spread $\sim(\lambda_M/\lambda_L)f(\epsilon,\Delta P/p_c)$, short- and long-horizon diffusion $\sim(\lambda_M^2\lambda_C/\lambda_L)\,\epsilon^{\mp1/2}$; no proof of a Wiener limit |
| Cont–Stoikov–Talreja (2010) | Markov queueing: limit rate $\lambda_i$ by distance $i$ to the opposite best, market rate $\mu$, per-order cancel rate $\theta$ | Stationarity; computable probabilities that the mid moves up and that an order executes before the mid moves |

The authors read the history as a gradual reduction to essentials: one order is the atom, event time is the clock, and market orders plus cancellations are required. They argue that the long memory of trade signs comes from execution strategies (order splitting) and so must be modelled through agent behaviour, not injected exogenously.

### Ch. 6–8 (from the table of contents; text not extracted)

- **Ch. 6**, mathematical structure of ZI models (Abergel–Jedidi 2013): a "perfect market making" approximation; Poisson arrivals in a moving reference frame with boundary conditions; the infinitesimal generator; **ergodicity** of the book; convergence of the rescaled price to a Wiener process (Theorem 6.5, cited in Ch. 5); interpretation of the asymptotic volatility; the role of cancellations.
- **Ch. 7**, the book as a queueing system (Muni Toke 2015): links order flows to the average shape, compares with Smith et al. and the Bouchaud–Mézard–Potters (2002) shape, and adds variable limit-order sizes, which gives the theoretical counterpart of Ch. 3.
- **Ch. 8**, interacting agents: herding (Cont–Bouchaud), fundamentalists vs. trend followers, threshold behaviour. Also a **Hawkes-driven LOB** with generator, stability conditions and a large-scale price limit.

## Part III–IV (from the table of contents and figure/table lists only)

- **Ch. 9**, simulation. A Poisson ZI simulator calibrated to SCHN.PA over 23 days in March 2011. Validation covers depth profile, spread distribution, autocorrelation of increments, Q–Q plots and the signature plot $\sigma_h^2=V[P(t+h)-P(t)]/h$. It notes "anomalous diffusion at short time scales" and runs a CAC 40 cross-sectional regression of model vs. data liquidity and diffusion. A Hawkes simulator, estimated with parameters for aggressive limit and market orders across CAC 40 stocks, revisits market making and taking.
- **Ch. 10**, predictability (Anane–Abergel 2015). Conditional-probability matrices (binary and 4-class; Deutsche Telekom 2013 example) and OLS, ridge (HKB and Ledoit–Wolf shrinkage), LASSO and elastic net predicting single-stock returns. Scored by AUC and accuracy at 1-minute and 30-minute horizons, and by daily gains with and without costs (0.5 bp in one table). The authors frame this as evidence of market imperfection. The extracted text does not include the result magnitudes.

## Assessment

- **Useful.**
  - A consolidated, reproducible set of stylized facts on a single-venue, price/time-priority book, with numbers.
  - A clear statistical design for measuring cross-excitation: conditional probabilities, conditional waiting times and lagged correlation matrices. It transfers directly to Hawkes calibration.
  - The Ch. 5 table of what each ZI ingredient buys (tails, $H$, spread) is a good checklist for building a backtest simulator. Poisson ZI dynamics give subdiffusive short-scale prices and miss sign long memory. Book stability usually needs ad hoc boundary rules. Queue position, cancellations and replenishment speed matter for passive fill modelling.
- **Fragile or dated.**
  - Data is Euronext Paris in 2007–2011, primary book only, with fragmentation after MiFID ignored.
  - Lifetimes are reconstructed heuristically.
  - Ch. 3 $R^2$ is 0.08–0.21 and the regressors are jointly endogenous with depth, so the result is associational.
  - Conditional tables are in event time and do not condition on queue sizes. Queue-reactive models (Huang–Lehalle–Rosenbaum) are not covered.
  - Fleeting-order "manipulation" readings are speculative.
- **For a quantitative PM.** This is not an execution-cost or impact reference; the book says so itself. For impact, pair it with the propagator and square-root-law literature, and with Almgren–Chriss or Obizhaeva–Wang for schedules. The value here is in microstructure simulation, fill-probability modelling and short-horizon signal research.
