# Carry Trade and Momentum in Currency Markets

**Craig Burnside, Martin Eichenbaum, Sergio Rebelo · 2011 · *Annual Review of Financial Economics* 3, 511–535 (doi 10.1146/annurev-financial-102710-144913) · Source: `Finance/CarryMomentum_BurnsideEichenbaumRebelo_2011.pdf` · Data: 20 major currencies vs USD, monthly, Feb 1976–Dec 2010; J.P. Morgan options on 10 currencies, 1995–2009**

## Claim
A review with new estimates: (i) equally weighted carry and (time-series) momentum portfolios in currencies both earn ~4.5%/yr with Sharpe ratios 0.89 and 0.62, nearly uncorrelated, so a 50/50 mix reaches SR 0.98; (ii) **neither conventional risk factors nor currency-specific factors (DOL, HML$_{FX}$, global FX volatility) explain momentum** — pricing error ≈ 5%/yr; (iii) the 2008 crisis cannot be the "rare disaster" that rationalizes both strategies, because momentum made money when carry crashed; an options-based peso-problem analysis implies a peso state with **moderate losses but a very high SDF**; (iv) **price pressure** (downward-sloping FX demand) can explain positive *average* profits with zero *marginal* profit.

## Strategy definitions
USD is home currency; $S_t$ = USD per FCU, $i_t$, $i_t^*$ domestic/foreign rates, $F_t$ one-month forward.
- Long FCU: $z^L_{t+1}=(1+i^*_t)\frac{S_{t+1}}{S_t}-(1+i_t)$.
- **Carry:** $z^C_{t+1}=\operatorname{sign}(i^*_t-i_t)\,z^L_{t+1}$; forward version $z^F_{t+1}=\operatorname{sign}(F_t-S_t)(F_t-S_{t+1})$ — proportional to $z^C$ under CIP (CIP deviations were small except post-2008).
- **Momentum:** $z^M_{t+1}=\operatorname{sign}(z^L_t)\,z^L_{t+1}$, look-back **one month** — own-sign (time-series) momentum per currency vs USD, not a cross-sectional sort.
- Portfolios: equal-weight average of up to 20 individual trades, total bet normalized to USD 1; 50-50 = average of the carry and momentum portfolios (when the two disagree on a currency, the net position is zero).
- Both are $z_{t+1}=u_tz^L_{t+1}$ with different $u_t$. Under UIP $E_t z^L_{t+1}=0$ both would earn nothing. With $E_tS_{t+1}\approx S_t$ (Meese–Rogoff), $E_tz^F_{t+1}\approx|F_t-S_t|>0$. Hit rates: $\Pr[\operatorname{sign}z^L_{t+1}=\operatorname{sign}(S_t-F_t)]=0.571$ (carry), $\Pr[\operatorname{sign}z^L_{t+1}=\operatorname{sign}z^L_t]=0.569$ (momentum).

## Payoffs (Table 1, annualized; GMM s.e. in parentheses)

| | Mean % | SD % | Sharpe | Skew | Excess kurt. | ρ(carry) | ρ(mom) |
|---|---|---|---|---|---|---|---|
| Individual carry (avg of 20) | 4.6 | 11.3 | 0.42 | | 1.6 | | |
| Individual momentum (avg) | 4.9 | 11.3 | 0.43 | | 1.5 | | |
| **Carry portfolio** | 4.6 (0.9) | 5.1 | **0.89** (0.21) | −0.53 (0.40) | 4.1 (1.5) | 1 | 0.10 |
| **Momentum portfolio** | 4.5 (1.2) | 7.3 | **0.62** (0.16) | +0.08 (0.32) | 2.9 (0.9) | 0.10 | 1 |
| **50-50** | 4.5 (0.8) | 4.6 | **0.98** (0.16) | | 2.5 (0.5) | 0.63 | 0.84 |
| US stocks (VW excess) | 6.5 (2.8) | 15.7 | 0.41 (0.19) | −0.78 | 2.3 | ≈0.09 | ≈0.09 |

- Diversification across currencies cuts carry volatility by >50%, doubling the Sharpe ratio.
- Skewness of carry is insignificant and smaller than equities'; momentum is (insignificantly) positively skewed. Excess kurtosis reflects central peakedness.
- Cumulative value of \$1 (T-bill account re-bet each month): carry \$30.09, momentum \$27.98, stocks \$40.22. Aug 2000–Dec 2010: stocks +14.9%, T-bills +26.7%, carry +93.9%, momentum +76.1%.
- Burnside et al. (2006): a CRRA investor with risk aversion 5 would allocate three times as much to diversified carry as to US stocks.

## Risk-based explanations
Linear SDF $M_t=1-(f_t-\mu)'b$; $E(z)=\operatorname{cov}(z,f)b=\beta'\lambda$. Time-series betas (eq. 14) and iterated GMM with pricing-error test $J=T\hat\alpha'\hat V^{-1}\hat\alpha\sim\chi^2_{n-k}$.

**Conventional factors** (test assets: FF25 + carry + momentum). Models: CAPM, FF3, quadratic CAPM (Harvey–Siddique), CAPM + realized stock vol + interaction (monthly); C-CAPM (nondurables+services growth) and Yogo's extended C-CAPM (+ durables service flow + market; quarterly, 1976Q2–2010Q1).
- Table 2: all betas insignificant except carry's FF market beta 0.045 (s.e. 0.018) — implying only 0.3%/yr expected carry return vs 4.6% actual. $R^2\le0.04$.
- Tables 3–4: every model rejected ($J$ p-values 0.00); annualized pricing errors carry 4.2–4.7%, momentum 4.6–5.3%, all significant. Only FF3 has positive cross-sectional $R^2$ (0.38) and predicts 0.2% for both currency strategies.

**Currency-based factors** (Lustig–Roussanov–Verdelhan; Menkhoff et al.). Five forward-discount-sorted portfolios S1–S5 (mean returns S1…S5 printed as 0.7 [sign lost in extraction], 0.3, 2.8, 3.6, 5.3% — described as monotonically increasing, as implied by a near-martingale spot); DOL = mean of S1–S5; HML$_{FX}$ = S5 − S1; VOL = monthly average of daily FX log-change standard deviations.

| Table 5 betas | DOL | HML$_{FX}$ | $R^2$ | VOL beta (with DOL) | $R^2$ |
|---|---|---|---|---|---|
| S1 | 1.03 | −0.48 | 0.93 | +2.1 (sig.) | 0.75 |
| S5 | 1.03 | +0.52 | 0.94 | −1.3 (sig.) | 0.73 |
| Carry portfolio | 0.20 | 0.26 | 0.38 | −0.8 (sig.) | 0.15 |
| Momentum portfolio | 0.03 | −0.10 | 0.02 | +0.1 (insig.) | 0.00 |

- Low-rate currencies hedge volatility; carry loads negatively on VOL. The S1–S5 beta pattern is partly mechanical (factors built from the sorted portfolios).
- Table 6 (test assets S1–S5 + momentum): HML$_{FX}$ has significant positive $b$ (7.4) and $\lambda$ (0.57); VOL significant negative ($b=-3.9$, $\lambda=-17.93$). Cross-sectional $R^2<0.04$ for both; DOL–HML$_{FX}$ rejected ($J$=18.90, p=0.00), DOL–VOL not rejected ($J$=6.51, p=0.16) only because it is imprecise. **Momentum pricing error 5.1% (DOL–HML$_{FX}$) and 4.6% (DOL–VOL)** — momentum has ~zero DOL beta, negative HML$_{FX}$ beta and a "paradoxical" positive VOL beta (it hedges volatility).

## Rare disasters and peso problems
Two-state model: $(1-p)E^N(Mz)+pM'z'=0$, $z'<0$, $E^N(M)=1$. With in-sample disaster frequency $\hat p<p$ the sample mean of $Mz$ is $(p-\hat p)(E^N(Mz)-M'z')>0$. Nakamura et al. (2010): annual disaster probability 0.017 ⇒ monthly $p=0.0014$; over 456 months $P(\text{no disaster})\approx53\%$.
- **2008 is not the disaster.** Pricing implies $E^N(Mz_1)/E^N(Mz_2)=z_1'/z_2'$. Aug–Nov 2008: carry −≈10% (its worst 4-month loss), momentum +≈24% (its best 4-month gain) ⇒ RHS negative, LHS positive. Same in early 1991 and late 1992. Escape routes: segmented markets (different $M'$ — implausible) or multiple disaster states (then momentum's profitability stays unexplained).
- **Peso problem ($\hat p=0$) via options.** Hedged payoff $z^H$ (buy ATM put/call; bounded loss $h$): $(1-p)E^N(Mz^H)+pM'E^N(h)=0$ ⇒ with $\operatorname{cov}^N(M,z)=\operatorname{cov}^N(M,z^H)=0$,
$$z'=E^N(h)\frac{E^N(z)}{E^N(z^H)},\qquad r\equiv\frac{pM'}{1-p}=\frac{E^N(z)}{-z'}=\frac{E^N(z^H)}{-E^N(h)}.$$
  Momentum sometimes takes the opposite side of carry (naturally hedged), so the test uses carry and the **50-50** portfolio. Separate estimates: peso-state losses $|z_1'|=0.037$ (s.e. 0.014) for carry, $|z_2'|=0.091$ (0.006) for 50-50; $r$ = 0.095 (0.059) and 0.159 (0.091), equal by Wald test (p=0.23). Joint GMM: $|z_1'|=0.040$ (0.020), $|z_2'|=0.027$ (0.015), $r=0.089$ (0.064), overidentification not rejected (p=0.27). With $p=0.0014$, $r=0.089$ ⇒ **$M'\approx63$**. Conclusion: data do not reject the peso hypothesis, but the peso state involves moderate losses and an enormous marginal utility.

## Price pressure (Section 5)
Price $p_0=a$, $\dot p_t=bm_t$. A risk-neutral trader splitting $x$ evenly over the day pays $ax+\tfrac12bx^2$; profit $E\pi=vx-\int_0^x(a+bz)dz$ ⇒ $x^*=(v-a)/b$, last unit priced at $v$ (zero marginal profit) but $E\pi=\frac{(v-a)^2}{2b}>0$. With $n$ traders in random order: $x=\frac{2(v-a)}{b(1+n)}$, average $E\pi=\frac{2(v-a)^2}{b(1+n)^2}>0$, trader $j$ earns $\frac{2(v-a)^2}{b(1+n)^2}[n+2(1-j)]$ — about half lose for large $n$. An econometrician measuring average payoffs sees "money left on the table" that does not exist at the margin. Open questions: empirical plausibility and source of the price pressure.

## Critical assessment
- **Convincing:** the carry–momentum complementarity (ρ ≈ 0.1, SR 0.98 combined) and the 2008 argument are simple and robust; the failure of both conventional and FX-specific factors to price 1-month TS momentum is clear (pricing error ≈ the whole mean).
- **Caveats:** no transaction costs (bid–ask) in the reported payoffs, equal-weighted G10+ currencies vs USD only; 1-month look-back only; the peso-state estimates rest on a single disaster state, zero normal-state covariance with $M$, ATM options and a 1995–2009 option sample on 10 currencies; $M'\approx63$ is "consistent" rather than evidence. The price-pressure model is a stylized illustration with no calibration. Momentum's defence against the disaster story relies on a few carry-crash episodes.
- Extraction note: several minus signs are lost in the PDF text; signs above for skewness, HML$_{FX}$/VOL betas and $z'$ follow the authors' verbal descriptions. S1's mean return sign could not be read (printed "0.7").

## Practical relevance for a quant PM
- Combine FX carry with 1-month TS momentum: near-zero correlation and momentum's positive payoff in carry crashes (2008, 1991, 1992) make it a natural crash hedge for carry books.
- Diversification across currencies is the single largest Sharpe driver (0.42 → 0.89 for carry).
- Do not expect DOL/HML$_{FX}$ or VOL to explain momentum; treat it as a separate factor. When assessing capacity, the price-pressure logic warns that average backtest profits overstate marginal profitability of scaling up.
