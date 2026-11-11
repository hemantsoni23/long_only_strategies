# On the Predictive Content of Technical Analysis
**Authors:** Stefan Reitz
**Year:** 2006
**Journal/Venue:** North American Journal of Economics and Finance 17, 121–137
**Source file:** `Finance/AbnormalReturnsTechnicalAnalysis_Reisz_2006.pdf`

## Question
Why do moving-average rules forecast, especially in FX, even though univariate models fail to beat a random walk on MSE (Diebold–Nason 1990)? Most explanations rely on herding or self-fulfilling prophecies. Reitz proposes an information-based rationale instead: if a fundamental is observed only with a lag, the price itself carries information about a regime shift in that fundamental. A short-versus-long moving-average oscillator is then an approximate Bayesian sign forecast, a "cheap proxy for Bayesian learning." The paper also implies that the rule should work mainly in low-volatility periods.

## Model (Lewis 1989 learning framework)
The log exchange rate obeys $e_t=\alpha z_t+\gamma E_t[e_{t+1}]$, with forward solution
$$e_t=\frac{\alpha}{1+\gamma}\sum_{j\ge0}\Big(\frac{\gamma}{1+\gamma}\Big)^j E_t[z_{t+j}].$$
The fundamental is $z_t=\tilde\mu+\vartheta_t$, $\vartheta_t\sim N(0,\sigma^2)$, and its mean may switch from $\mu_0$ to $\mu_1$ at a known date $\tau$ (for example, an announced policy change that is not fully credible). Agents know $\mu_0,\mu_1$ and update $P_{1,t}$ by Bayes' rule. With a flat prior at $\tau$,
$$\log\frac{P_{1,t}}{P_{0,t}}=\sum_{j=\tau}^{t}\frac{(\mu_0^2-\mu_1^2)+2(\mu_1-\mu_0)z_j}{2\sigma^2}.$$
After $\tau$, the price has an expectations term $\frac{\gamma\alpha}{1+\gamma}(P_{0,t}\mu_0+P_{1,t}\mu_1)$ plus a contemporaneous term $\frac{\alpha}{1+\gamma}(\mu_1+\vartheta_t)$, and it converges to $\alpha\mu_1+\frac{\alpha}{1+\gamma}\vartheta_t$ as $P_{1,t}\to1$. Forecast errors are serially biased during learning but rational conditional on information at the time.

**Sign rule with observable $z$.** $P_{1,t}>P_{0,t}$ if and only if $\frac{1}{t-\tau+1}\sum_{j=\tau}^t z_j>\frac{\mu_0+\mu_1}{2}$.

**Delayed observation (lag $\delta$).** For $\tau<t<\tau+\delta$, expectations are frozen at $P_{1,\tau}$. The price moves only through the contemporaneous term, so it is a linear transformation of the hidden $z$. Applying the same Bayesian logic to prices:
$$E_{\tau+\kappa}[\Delta e_{\tau+\kappa+1}]>0\iff \frac{1}{\kappa+1}\sum_{j=\tau}^{\tau+\kappa}e_j>\frac{E[e\mid\mu_0]+E[e\mid\mu_1]}{2},\quad \kappa=1,\dots,\delta.$$
If the shift occurred, the expected gap between the two sides converges to $\frac{\alpha}{1+\gamma}\frac{\mu_1-\mu_0}{2}$. If it did not, the gap is zero and no signal is generated.

**From midpoint to oscillator.** The midpoint is unknown, so it is approximated by a longer moving average of past prices, which straddles pre- and post-shift observations. With certainty about the shift the right span would be $2\delta$. With $P_{1,\tau}<1$ the span $\rho$ must be shorter; the paper gives $\rho$ as a function of $\delta$, $\gamma$ and $P_{1,\tau}$. The result is the standard crossover rule (Schulmeister 1987): long when $\text{MA}_{short}>\text{MA}_{long}$. Because the break date is unknown in practice, spans are arbitrary. But as long as $\rho>\delta$ a signal arises only if the shift actually occurred, which predicts that performance is insensitive to MA lengths.

**Failure modes built into the model:**
1. *Fads.* If agents put $P_{1,t}>0$ on a shift that never happens, prices move anyway and the oscillator signals a break it cannot tell apart from a real one. Technical trading can therefore also feed bubbles.
2. *Noise.* With an extra FX-market disturbance, observations in high-volatility periods are less informative about $z$. The Bayesian rule down-weights them, and the MA signal should work mainly when volatility is low.

The paper stresses that this is a model of the information content of TA, not a trading model.

## Empirical test
- **Data:** daily USD spot rates against DM, GBP, JPY and CHF, January 1980–December 1996 (data from Chris Neely). Overnight interbank rates are used for interest differentials. The PPP fundamental is $\log cpi^f-\log cpi^{US}$ from monthly IFS data, held constant within each month (interpolating instead does not change results).
- **Two-state Markov switching model (Engel–Hamilton type)** with regime-specific constant variances, estimated by QML with robust standard errors:
  - fundamentalist regime: $\mu_{0t}=f_0\Delta e_{t-1}+f_1(\text{int. diff.})+\theta(\tilde e_{t-1}-e_{t-1})$
  - chartist regime: $\mu_{1t}=c_0\Delta e_{t-1}+c_1(\text{int. diff.})+\psi(\text{MA}_{short,t-1}-\text{MA}_{long,t-1})$

  The baseline uses a 14/200-day MA pair. A regime-dependent drift was insignificant and dropped.

**Table 1 (percent units, t-stats in parentheses):**

| | DM | GBP | JPY | CHF |
|---|---|---|---|---|
| $\psi$ (chartist) | 0.889 (3.66) | 0.656 (1.90) | 0.614 (3.04) | 0.697 (2.79) |
| $\theta$ (PPP reversion) | 0.353 (2.35) | 0.385 (1.59) | 0.220 (1.79) | 0.427 (2.68) |
| $\sigma$ fundamentalist regime | 0.925 | 0.920 | 0.917 | 1.001 |
| $\sigma$ chartist regime | 0.468 | 0.461 | 0.369 | 0.545 |
| $P$ (stay fundamentalist) | .9455 | .9608 | .7474 | .9550 |
| $Q$ (stay chartist) | .9657 | .9777 | .8475 | .9715 |
| Unconditional chartist prob. | .61 | .64 | .62 | .61 |
| Expected duration F / C (days) | 18 / 29 | 26 / 45 | 4 / 7 | 22 / 35 |

- All $\psi$ and $\theta$ have the predicted sign. The text says every $\psi$ is significant at 1%, but GBP's $\psi$ is only significant at 10% (t = 1.90), and GBP's $\theta$ is insignificant.
- The chartist regime is the **low-volatility** regime in every currency: its $\sigma$ is roughly half that of the fundamentalist regime. It is also the more frequent (about 61–64% unconditionally) and more persistent regime. The yen's regimes are much less persistent than the others ($P,Q<0.85$), so the old summary's "above 0.94 everywhere" does not hold for the yen.
- A significant $\psi$ means the MA gap predicts the magnitude of changes, not only their sign.
- **Diagnostics (Table 2):** Ljung–Box tests show no residual autocorrelation up to lag 5. There is no remaining ARCH for DM, GBP and CHF, but significant ARCH(3–5) remains for the yen.
- **Assignment check (footnote):** a four-state model with independent mean and variance switching did not converge. Putting both forecasts in both regimes gives an insignificant PPP term in the low-volatility regime and an insignificant MA term in the high-volatility regime, which supports the chosen assignment.
- **MA-span robustness (Table 3, DM):** short spans 10/14/38 days crossed with long spans 100/150/200 days all give significant $\psi$ between 0.88 and 1.52 and a stable $\theta$ of about 0.34–0.35, consistent with the span-insensitivity prediction.
- **Fig. 2:** the smoothed chartist probability for USD/DM is high through the dollar appreciation of 1982 to mid-1985, broken only by high-volatility episodes, and during the subsequent decline it is high in the low-volatility stretches.

## Assessment
- **Contribution:** The theory is neat and the mapping is explicit: Bayesian sign prediction about a lagged-observed regime mean reduces to an MA crossover, and the span-insensitivity and low-volatility predictions follow from it. It relates to Muth (1960) and Barsky–De Long, where exponential smoothing estimates a permanent component, and to Dewachter (1997), who treats charts as proxies for Bayesian inference.
- **Weak link between theory and test:**
  - The empirical regimes are identified mainly by variance. Because the chartist equation is assigned to the low-volatility state, "chartism works when volatility is low" is partly built into the specification rather than tested. The footnote check helps but is not a formal test.
  - Nothing in the estimation identifies hidden-fundamental episodes or announcement dates. Any trend-following predictability in a calm regime (for example central-bank smoothing, as in LeBaron 1999) fits equally well.
  - Estimates are in-sample, with smoothed (ex-post) regime probabilities. There is no out-of-sample forecast evaluation, no trading P&L and no transaction costs.
  - The sample is 1980–1996, the period in which FX trend-following profits were strongest and which later work shows decayed afterward.
- **Practical relevance:** Useful as a structural story for why trend signals should be volatility-conditioned. Scale or down-weight trend exposure when realized volatility is high, and expect weak sensitivity to lookback choice. The model also warns that the same signal cannot tell a real fundamental break from a fad-driven repricing. As evidence that FX MA rules pay after costs, the paper adds little.
