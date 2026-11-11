# Predicting Stock Price Movements from Past Returns: The Role of Consistency and Tax-Loss Selling
**Authors:** Mark Grinblatt, Tobias J. Moskowitz
**Year:** 2004
**Journal/Venue:** Journal of Financial Economics 71, 541-579
**Source file:** Finance/AbnormalReturnsTaxLoss_GrinblattMoskowitz_2004.pdf

## Question

Short-term reversal (1 month), intermediate momentum (up to 12 months) and long-term reversal (3-5 years) are usually studied with cumulative past returns, one horizon at a time. The paper asks whether (i) the *path* of past returns (consistency), (ii) the *sign* of past returns (winner/loser asymmetry), and (iii) turn-of-the-year *tax-loss trading* change how past returns forecast the cross-section, and whether the three horizon effects are really linked, as unified behavioral theories (DHS 1998, BSV 1998, Hong-Stein 1999) require.

## Data and design

- CRSP monthly returns, Aug 1963 - Dec 1999 (NYSE/AMEX; NASDAQ-NMS added after 1973). Fama-MacBeth estimation Aug 1966 - Jul 1995; Aug 1995 - Dec 1999 held out for out-of-sample tests (at a referee's suggestion). Turnover from 1976 (NYSE/AMEX) / 1983 (NASDAQ); institutional ownership (S&P) from 1981; maximum short-term capital-gains tax rates from Pechman, Willan and the IRS.
- **Dependent variable: hedged return.** Stock return minus (i) the value-weighted return of its cell in an independent 5x5 size (NYSE breakpoints) x BE/ME sort, minus (ii) the cap-weighted size/BM-hedged return of its industry (20 two-digit-SIC groups, as in Moskowitz-Grinblatt 1999). Expected value zero if size, B/M and industry are the only priced attributes; adding beta, size, past industry returns, BE/ME as regressors barely changes anything, and the resulting strategies have negligible Fama-French loadings.
- **Monthly cross-sectional regression** over three non-overlapping horizons (skip-month / skip-year gaps make the regressors near-orthogonal):

$$
\tilde r_t(j) - \tilde R^B_t(j) = a_t + b_{1t} r_{-1:-1} + b_{2t} r^L_{-1:-1} + b_{3t} DCW_{-1:-1}
+ \sum_{h\in\{-12:-2,\,-36:-13\}} \big(c_{1t} r_h + c_{2t} r^L_h + c_{3t} DCW_h + c_{4t} DCL_h\big) + \varepsilon_t(j)
$$

  with $r^L_h=\min(0,r_h)$ (so $r_h$'s coefficient is the winner slope and $r_h+r^L_h$ the loser slope).
- **Consistency dummies.** One year: $DCW=1$ if at least 8 of the 11 months $t-12..t-2$ are positive ($DCL$: at least 8 negative). Three years: at least 15 of 23 months $t-36..t-13$. Under a fair-coin binomial null each tail has probability of roughly 10%, i.e. the thresholds pick the top decile of consistency. At the one-month horizon $DCW_{-1:-1}$ is simply "last month positive" and $DCL$ is dropped (collinearity).
- Coefficients are averaged over all months and separately over January, Feb-Nov and December. The seasonal averages are then used as scoring weights to form monthly decile portfolios of hedged returns (January coefficients rank in January, etc.).

## Main results

### Fama-MacBeth coefficients (Table 2, all months; t-stats in parentheses)

| Regressor | All | Jan | Feb-Nov | Dec |
|---|---|---|---|---|
| $r_{-1:-1}$ | -0.047 (-11.4) | -0.100 | -0.044 | -0.043 |
| $r^L_{-1:-1}$ | -0.076 (-9.6) | -0.219 | -0.061 | -0.092 |
| $DCW_{-1:-1}$ | 0.0051 (8.8) | 0.0097 | 0.0048 | 0.0060 |
| $r_{-12:-2}$ | 0.0028 (2.5) | -0.0072 (-1.9) | 0.0029 | 0.0075 |
| $r^L_{-12:-2}$ | 0.0113 (3.0) | -0.0725 (-3.6) | 0.0170 (4.6) | 0.0440 (4.7) |
| $DCW_{-12:-2}$ | 0.0046 (5.8) | 0.0126 (2.6) | 0.0042 (5.3) | 0.0017 (0.7) |
| $DCL_{-12:-2}$ | -0.0007 (-0.8) | 0.0044 | -0.0014 | 0.0011 |
| $r_{-36:-13}$ | -0.0015 (-3.5) | -0.0002 (-0.1) | -0.0021 (-4.3) | 0.0023 |
| $r^L_{-36:-13}$ | -0.0052 (-2.0) | -0.0537 (-3.9) | -0.0025 (-1.0) | 0.0159 (2.3) |
| $DCW_{-36:-13}$ | 0.0014 (2.7) | 0.0040 | 0.0011 (2.0) | 0.0010 |
| $DCL_{-36:-13}$ | -0.0007 (-0.8) | 0.0108 (2.1) | -0.0015 | -0.0036 |

Readings:
1. **Sign asymmetry.** Loser interactions have the same sign as the return coefficients: momentum and reversals are steeper for negative past returns.
2. **Winner consistency.** All 12 $DCW$ coefficients are positive, most significant. Holding the one-year return fixed, a consistent winner earns about **46 bp/month** more. $DCL$ is essentially zero. Because consistency is also roughly an inverse-volatility proxy, the lack of a symmetric loser effect is the authors' argument that the winner effect is not just low volatility. Candidate mechanisms: disposition-effect capital-gains overhang (Grinblatt-Han 2002) and sequential learning about discount rates (Watkins 2002); both predict a loser effect too, which the authors suggest tax-loss selling may mask.
3. **Seasonality.** One-year momentum flips sign in January, most visibly for losers (loser slope $r+r^L$: $0.0028+0.0113=0.014$ over all months, $-0.0072-0.0725\approx-0.080$ in January). In December the loser slopes are strongly positive at *both* one- and three-year horizons: **losers keep losing in December and rebound in January.** The January reversal cannot be bid-ask bounce (Keim 1989) because the one-year window skips month $t-1$ and the one-month return is controlled for.
4. **Long-term reversal is a January loser effect.** In January the three-year winner slope is zero and the loser slope is large and negative; in Feb-Nov there is no winner/loser difference and the reversal is small; in December the three-year loser slope is positive (persistence), about eight times the winner slope.
5. **Horizons are largely independent.** Each horizon survives jointly; one-horizon-at-a-time regressions give nearly identical coefficients (unreported); momentum is present all year while long-term reversal is concentrated in January. This undermines theories in which the same overreaction drives both momentum and later reversal.

### Consistency in simple sorts (Table 3, one-year horizon)

Equal-weighted decile 10 (past winners) earns 60 bp/month hedged. Split: non-consistent winners 45 bp, consistent (8 or more of 11) 91 bp, very consistent (9 or more of 11, about 13% of the decile) 99 bp. In Feb-Nov, 73 bp and 86 bp respectively. Value-weighted decile 10 earns 54 bp. So consistency roughly doubles the momentum premium within the top decile. At the three-year horizon, the only Feb-Nov reversal in EW decile 10 comes from non-consistent winners (-24 bp/month; -30 bp VW), 33 bp below the consistent winners in the same decile.

### Ranking strategies (Table 4, in sample, 10-minus-1 hedged spread per month)

| Scoring | EW | VW |
|---|---|---|
| All regressors | 2.80% (t=12.9) | 1.39% (t=6.5) |
| Excluding 1-month regressors | 1.68% (t=7.8) | 1.11% (t=4.9) |
| One-year regressors only | 1.60% (t=8.7) | 0.71% (t=3.6) |
| Three-year regressors only | 0.59% (t=3.5) | 0.17% (t=1.0) |

Decile returns are monotone; the long decile carries most of the spread (EW decile 10: +215 bp vs decile 1: -65 bp) and most of the risk (annualized hedged vol about 10.5-11% vs 3-7% for other deciles). Zeroing the $DCW$ coefficients ("NCW") cuts spreads by only 10-20 bp, but this understates the effect because many stocks overlap. In the one-year VW decile 10, non-consistent winners (about 20% of VW weight) earn -22 bp in Feb-Nov, indistinguishable from decile 1; long consistent winners / short the rest of decile 10 earns **53 bp/month** Feb-Nov, almost the full 10-1 spread.

## Tax-loss trading evidence

- **Cross-sectional (Table 5, VW 10-1 spreads within quintiles).** Profits are larger for high-turnover stocks; for NASDAQ the extra profitability is entirely in January and December, which argues against Lee-Swaminathan's seasonless "momentum life cycle". Among the smallest third of stocks, low institutional ownership raises profits, mainly in December and January (low-IO small-cap January spread about 10% per month for the full strategy). There is no such effect among large caps. Profitability falls sharply with size (201 vs 58 bp/month for the ex-one-month strategy in low-IO smallest vs largest quintile), and much of the gap is at the turn of the year, which is hard to square with Hong-Lim-Stein slow diffusion.
- **Tax regimes (Table 6).** High-tax years: the starting year's maximum short-term capital-gains rate is at least 20% above the average of the adjacent years, and the classification persists until the next 20% move. By this rule 1968-69, 1972-75, 1981, 1985-86 and 1988-99 are high-tax. A time-series regression of the VW ex-one-month 10-1 spread on high-tax, January, December and interaction dummies: only **high-tax January (+3.64%, t=2.39)** and **high-tax December (+4.51%, t=3.30)** are significant. In low-tax regimes, average profit is 37 bp/month (t=1.08), Feb-Nov is insignificant and December is -27 bp; in high-tax years Feb-Nov profits are 75 bp (t=2.63). Past losers (decile 1 in December, decile 10 under January scoring) have more negative December and more positive January hedged returns in high-tax years, and more so for small, low-IO stocks. The one exception is a high-IO category, which should not be tax-sensitive. The authors interpret the Feb-Nov high-tax profits as a steadily growing supply of losers for sale that peaks in December.

## Costs and out-of-sample

- Restricting to stocks priced above $5 barely changes VW spreads (the ex-one-month strategy is about 100 bp/month; the one-year strategy rises from 71 to 77 bp).
- Turnover is high: in 1999, 39% per month on the long side and 64% on the short side. Round-trip costs of about 1% are roughly breakeven, but the VW positions sit around the 86th size percentile and the signal is at least a month old, so trades need not be urgent. The long side alone earns 66 bp/month over benchmark, which survives one-way costs up to about 1.7%.
- Out of sample (Aug 1995 - Dec 1999, fixed in-sample coefficients): VW spreads are comparable or larger. All-regressor spread is 2.03% vs 1.39% in sample, and the one-year strategy is 0.65% vs 0.71%. The ex-one-month strategy falls to 0.75% for all stocks but is 1.29% for stocks above $5.

## Assessment

- **Convincing:** The hedged-return Fama-MacBeth design makes the incremental content of path and sign clean. The consistency effect is large, robust across horizons and seasons, and economically comparable to momentum itself. Documenting a *December* loser continuation, not only a January rebound, is the most useful fact for anyone trading around year-end. The held-out 1995-99 sample is a real, if short, test of the fitted rule.
- **Fragile:**
  - The tax-regime split is coarse and ad hoc (a 20% relative-change rule). "High tax" covers most of the later sample (1988-99), so regime is confounded with era, and the low-tax January inference rests on 12 observations.
  - The consistency thresholds are arbitrary, although motivated by the binomial null.
  - Table 4 scores stocks with full-sample average coefficients (look-ahead). Only Table 7 is genuinely out of sample, and it covers 4.4 years that include the 1999 momentum boom.
  - The DCL null could reflect tax masking, as argued, but that is not tested directly.
  - Equal-weighted results lean on small, illiquid stocks.
- **Practical relevance:** Path smoothness is a cheap, low-correlation refinement of 12-1 momentum. Later work formalizes it as "information discreteness" (frog-in-the-pan), and it is worth testing as a momentum conditioner. The seasonal structure implies momentum and reversal signals should use month-specific weights: stand aside or flip exposure to past losers in January, and lean into loser shorts in December. It also suggests the size of these effects should vary with capital-gains tax incentives and the taxable-investor share of ownership.
