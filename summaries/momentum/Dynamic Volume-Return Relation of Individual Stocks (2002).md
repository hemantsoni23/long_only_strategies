# Dynamic Volume-Return Relation of Individual Stocks
**Authors:** Guillermo Llorente, Roni Michaely, Gideon Saar, Jiang Wang
**Year:** 2002
**Journal/Venue:** Review of Financial Studies 15(4), 1005-1047
**Source file:** Finance/MomentumReversal_Llorente_2002.pdf

## Question

When does a return accompanied by high volume reverse, and when does it continue? The paper (a simplified, closed-form version of Wang 1994) argues the answer depends on the mix of trading motives: **hedging (risk-sharing) trades** push price away from unchanged fundamentals and reverse; **speculative trades on private information** move price only partially toward the signal and continue. Cross-sectional variation in information asymmetry should therefore produce cross-sectional variation in the sign of the volume-conditioned daily autocorrelation. This reconciles Campbell-Grossman-Wang (1993) and LeBaron (1992) (high-volume reversals for indices/large stocks) with Antoniewicz (1993) and Stickel-Verrecchia (1994) (high-volume continuation in pooled individual stocks). It is a daily-horizon mechanism paper, not a 6-12 month momentum-sort paper.

## Model

- Stock pays $D_{t+1}=F_t+G_t$. $F_t$ is public; $G_t$ is observed only by class-1 investors (weight $\omega$). Private information is short-lived (revealed next period); shocks are i.i.d. normal; investors are myopic CARA (risk aversion normalized to 1), zero net supply, $r=0$.
- Each investor holds $Z^i_t$ units of a nontraded asset paying $N_{t+1}$, correlated with $D$ ($\sigma_{DN}$); changes in $Z$ generate hedging trade.
- Equilibrium price (Prop. 1): $P_t=F_t+aG_t-(b_1Z^1_t+b_2Z^2_t)$. With two classes, volume $V_t=\omega|X^1_t-X^1_{t-1}|$ adds nothing to participants' information; it is informative only to outside observers.
- Public news moves price without volume and generates white-noise returns (no income effect under CARA). Trade-generated returns carry volume and are serially correlated. Volume thus (imperfectly) separates trade-driven from news-driven returns.

Prop. 2 (with $Z^2\equiv0$): with $\tilde V_t=V_t/E[V_t]$,
$$E[R_{t+1}\mid \tilde V_t,R_t]=\theta_1R_t-\theta_2\tilde V_t\tanh(\theta\tilde V_tR_t)\approx-(\theta_1+\theta_2\tilde V_t^2)R_t .$$

Prop. 3: with no asymmetry ($\sigma_G^2=0$), $\theta_1=0$ and $\theta_2>0$ (high-volume returns reverse, as in CGW). For small $\sigma_G^2>0$, holding total dividend risk $\sigma_D^2$ and price risk fixed, $\theta_1$ increases and $\theta_2$ decreases in $\sigma_G^2$ (numerically confirmed over the whole range). So more asymmetry means less reversal (or continuation) after high volume. The $\theta_1$ result (more negative no-volume autocorrelation under asymmetry) is flagged as fragile: it is also produced by noise-trader models, bid-ask bounce, and changes sign with persistent hedging needs. The $\theta_2$ prediction is the one taken to data. A model limitation acknowledged by the authors: here $\theta_2\ge0$ always, while with long-lived information (Wang 1994) the high-volume coefficient can switch sign; the empirics allow this.

## Empirical design

- NYSE/AMEX common stocks, Jan 1993 - Dec 1998 (TAQ start); stocks trading on at least 1000 of 1516 days: **2226 stocks** (from 3538). Market cap ranges from \$3.6m to \$148bn.
- Volume: detrended log turnover, $V_t=\log(\text{turn}_t+0.00000255)-\frac{1}{200}\sum_{s=-200}^{-1}\log(\text{turn}_{t+s}+0.00000255)$.
- Stage 1, per stock:
$$R_{i,t+1}=C_{0,i}+C_{1,i}R_{i,t}+C_{2,i}V_{i,t}R_{i,t}+\varepsilon_{i,t+1},$$
with $C_2\leftrightarrow-\theta_2$ (linear rather than squared volume, for comparability with CGW).
- Stage 2: $C_{2,i}=a+bA_i+u_i$, with $A_i$ the ordinal rank (scaled to $[0,1]$) of the average opening percentage spread (ORDBA, opening spread chosen to capture the adverse-selection component) or of average market cap (ORDCAP); rank correlation between the two is $-0.876$. Prediction: $b>0$ for spread, $b<0$ for size.

## Results

Spread terciles (Table 2):

| Spread group | mean $C_1$ | mean $C_2$ | # $C_2<0$ (of 742) | # $|t_{C_2}|>1.64$ |
|---|---|---|---|---|
| Low | 0.013 | -0.003 | 378 | 240 |
| Medium | 0.011 | 0.003 | 357 | 257 |
| High | -0.120 | 0.035 | 141 | 438 |

Cross-section: $b=0.0557$ ($t=15.9$, $R^2=10.2\%$) on ORDBA; $b=-0.0442$ ($t=-12.4$, $R^2=6.4\%$) on ORDCAP. Size terciles give mean $C_2$ of 0.030 / 0.005 / 0.001 (small to large). Spearman correlations: 0.33 with ORDBA, -0.26 with ORDCAP. Mean spreads fall from 4.1% (small) to 0.84% (large).

A liquidity/price-impact story predicts the opposite sign (illiquid stocks should reverse more after high volume), so if present it is dominated by the information effect.

$C_1$ pattern: raw first-order daily autocorrelation is -0.088 for high-spread and -0.076 for small stocks, about zero for large/liquid; consistent with the model but also with microstructure explanations, so the authors do not lean on it.

## Robustness (all preserve sign and significance of $b$)

- AR(1)-AR(5) error structures selected by Breusch-Godfrey tests, ML estimation (Table 4): $b\approx0.060$ (ORDBA), $-0.047$ (ORDCAP).
- Market return as extra regressor, and Scholes-Williams market-model residuals (Table 5): $b$ drops to 0.035-0.043 (spread) and -0.024 to -0.031 (size), $t$ between 7 and 13. A one-step Amemiya random-coefficient GLS on an earlier 1983-1992 sample agrees.
- Two-stage least trimmed squares in the time series or the cross-section (Table 6).
- **Microstructure** (Table 7): end-of-day and 10:00 AM TAQ midquote returns (kills bid-ask bounce and last-trade timing; small-stock autocorrelation roughly halves, -0.076 to -0.036) and a number-of-trades × return control. Effects shrink materially ($R^2$ 1-5%; e.g., ORDCAP $b=-0.016$, $t=-4.9$ with 10 AM quotes) but remain significant. Note bid-ask bounce and stale last trades bias toward the paper's finding for illiquid stocks, so this is the key test; they cannot explain the negative $C_2$ of liquid stocks.
- Turnover-equalized intervals (1-, 2-, 5-day by median-turnover tercile) and a 10-year 1989-1998 window (Table 8).
- Volume definitions (Table 9): raw turnover works; squared $\log(1+\text{shares})$, closer to the model's $\tilde V^2$, gives the strongest fit ($R^2$ 20% and 16%).
- Analyst following (I/B/E/S, 2035 covered firms, Table 10): more analysts, lower $C_2$ ($b=-0.027$, $t=-7.4$ on rank); weaker than spread/size.
- **Firm-specific components** (Table 11): market-model residual returns and residual volume (Lo-Wang market model of turnover) still give $b=0.039$ ($t=11.3$) and $-0.026$ ($t=-7.6$).

## Assessment

- Convincing: a clean two-motive mechanism with a signed, cross-sectional prediction, and an unusually thorough battery of microstructure controls. The residual-volume result shows the effect is not a market-volume artifact.
- Fragile: the proxies (spread, size, analysts) are all highly correlated with liquidity, trading frequency and specialist participation, so identification of "information asymmetry" rests on proxy interpretation and on the argument that liquidity would predict the opposite sign. Cross-sectional $R^2$ is modest (2-20%), and magnitudes shrink by half or more with midquote returns. Daily per-stock coefficients are noisy; the paper is about average cross-sectional tilt, not stock-level prediction. The model is static with one-period information and CARA, and the empirical interaction uses linear rather than squared volume.
- Practical relevance: for short-horizon reversal/residual-reversal signals, conditioning on abnormal volume is valuable, but the sign of the conditioning should differ by stock type: high-volume moves in large, liquid names are better reversal candidates; high-volume moves in small, wide-spread names tend to continue. This is a microfoundation often cited for volume-conditioned momentum (Lee-Swaminathan 2000 find a related effect at 6-month horizons), but it does not itself test portfolio returns or net-of-cost profitability.
