# Momentum and Crash Sensitivity
**Authors:** Stefan Ruenzi, Florian Weigert
**Year:** 2018
**Journal/Venue:** Economics Letters
**Source file:** Finance/AbnormalReturnsMomentum_RuenziWeigert_2018.pdf (accepted manuscript)

## Question

Is the momentum premium compensation for exposure to systematic crash risk? The paper runs a spanning test: does a factor built from stocks' lower-tail dependence (LTD) with the market absorb the alpha of UMD? It does not estimate crash sensitivity itself; the CRASH factor is imported from Chabi-Yo, Ruenzi and Weigert (2017, JFQA) for the U.S. and Weigert (2016, RAPS) internationally.

## Data and construction

- **UMD (U.S.):** Kenneth French's factor, annual returns, 1963-2012. Six value-weighted size x prior-return ($t-12$ to $t-1$) portfolios; UMD = average of the two high-past-return portfolios minus average of the two low ones. Summary stats: mean 8.72% p.a., skewness $-2.38$, excess kurtosis 12.91.
- **CRASH:** each stock's lower-tail dependence with the market estimated by copulas on daily returns; CRASH = **equal-weighted** top-quintile minus bottom-quintile crash-sensitivity portfolio return.
- **International:** 23 developed markets; UMD and FF factors from Asness, Frazzini and Pedersen (QMJ data), CRASH from Weigert (2016). Samples mostly 26 annual observations (16-28), ending 2012.

## Specification

Annual time-series regressions, Newey-West (2 lags):

$$
UMD_t = \alpha + \beta_1 (MKT-RF)_t + \beta_2 SMB_t + \beta_3 HML_t + \beta_4 RMW_t + \beta_5 CMA_t + \beta_6\, CRASH_t + \varepsilon_t,
$$

with FF3 or FF5 as the baseline, with and without CRASH.

## Results

**U.S. (Table 2, $N=50$ for FF3, $49$ for FF5):**

| Spec | $\alpha$ (p.a.) | $t(\alpha)$ | $\beta_{CRASH}$ | $t$ | $R^2$ |
|---|---|---|---|---|---|
| FF3 | 11.9% | 4.32 | - | - | 0.08 |
| FF3 + CRASH | 1.8% | 0.52 | 0.574 | 5.73 | 0.18 |
| FF5 | 13.2% | 5.95 | - | - | 0.10 |
| FF5 + CRASH | 2.9% | 0.91 | 0.547 | 4.81 | 0.18 |

Adding CRASH also makes the UMD market beta significantly negative ($-0.40$, $t=-2.54$ in FF3) and flips HML from $-0.29$ to about zero. Footnote: robust to alternative factor models and to a value-weighted CRASH factor.

**International (Table 3, FF3 baseline):**
- $\beta_{CRASH} > 0$ in 22/23 countries (all but Singapore), significant at 10% in 13; average 0.378.
- Alpha falls in 22 countries; average 3-factor alpha 11.6% -> 8.6% (average change $-3.0\%$ p.a.). Japan is the exception with a tiny increase.
- Adjusted $R^2$ rises in 20 countries, by 0.11 on average (large in ITA +0.34, NZL +0.37, AUT +0.31, FRA +0.29).
- Many alphas remain significant after CRASH (e.g. BEL 16.2%, DNK 20.2%, NZL 13.6%, all $t>3.8$); alpha is eliminated mainly in CAN, AUT, FIN, NLD, SWE. The international reduction is thus clearly partial, much smaller than in the U.S.

The authors conclude that "at least a substantial part" of momentum profits is a crash-risk premium, without excluding behavioral channels.

## Critical assessment

- **Tiny samples.** 50 annual observations in the U.S. and about 26 per country; alpha and loading standard errors are wide, and the "insignificant" residual alpha (1.8%, $t=0.52$) is not evidence of zero alpha. The international evidence is the more informative part, and there the reduction is modest.
- **Contemporaneous spanning, not a pricing test.** A positive time-series loading of UMD on CRASH shows co-movement of two long-short portfolios; it does not establish that crash sensitivity is the priced risk. Both portfolios could load on a common omitted component (e.g. overlapping holdings if recent winners tend to have high estimated LTD, or both being short-volatility-like in rebounds). No cross-sectional test, holdings overlap analysis, or double sort is reported.
- **CRASH is itself an anomaly factor** with its own alpha; explaining one anomaly with another long-short return shifts rather than resolves the puzzle, unless CRASH is independently justified as a risk factor (the argument rests on Chabi-Yo et al. 2017).
- **Equal-weighted CRASH vs value-weighted UMD**: mismatch in weighting schemes; the footnoted VW robustness is not tabulated.
- **Tension with crash dynamics.** Daniel and Moskowitz (2016) show momentum crashes occur in market rebounds after bear markets (short leg = high-beta losers rallying), i.e., it is an optionality/beta-timing phenomenon, not simply high unconditional lower-tail dependence. Annual data cannot distinguish these mechanisms.
- **Practical relevance:** for a PM, the result suggests UMD and LTD-sorted portfolios share substantial common variation, so combining them offers less diversification than it appears; it is not a strong reason to consider momentum "fully explained". Monthly-frequency replication with out-of-sample periods (post-2012) would be the natural next check.
