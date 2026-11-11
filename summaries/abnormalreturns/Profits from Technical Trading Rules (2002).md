# Profits from Technical Trading Rules
**Authors:** Mark J. Ready
**Year:** 2002
**Journal/Venue:** Financial Management 31(3), 43-61
**Source file:** Finance/AbnormalReturnsTechnicalAnalysis_Ready_2002.pdf

## Question

Brock, Lakonishok and LeBaron (1992, BLL) found that simple moving-average (MA) rules on the DJIA beat buy-and-hold through 1986. Ready asks a sharper question than "did they work in sample?": could an investor at the end of 1962 have *anticipated*, from price data alone, that these rules would earn after-cost excess returns over 1963-1986? The BLL rules were chosen because they were popular with technical analysts by the late 1980s, and that popularity plausibly reflects their past success, so the BLL evidence is exposed to data snooping. The focus is on profitable (after-cost) predictability, not predictability per se.

## Design

**Rules.** Variable-length MA rules $(s, \ell, b)$: buy (hold the DJIA) when $MA_s > (1+b)MA_\ell$, sell (hold T-bills) when $MA_s < (1-b)MA_\ell$; otherwise keep the previous position. Four of BLL's most profitable rules: (1,150,1%), (5,150,1%), (1,200,1%), (1,150,0%). A market-vs-cash timing strategy, not long-short.

**Ex ante competitor.** Allen and Karjalainen's (1999, AK) genetic algorithm builds rules as trees of Boolean and real-valued functions (and/or/not/if-then-else, comparisons, arithmetic, max/min/average of normalized prices over $n$ days, lags, current position). An initial population of 500 random rules is evolved on a training window (fitness = after-cost excess return), each generation's best rule is scored on a selection window, and the best selection-period rule is kept. The BLL rules lie inside the searchable space (Figure 1 writes (1,150,0%) as a tree), so if the pre-1963 data contained the pattern BLL exploited, AK should find rules at least as good. Main run: 50 rules (different random seeds), training 1957-1960, selection 1961-1962, test 1963-1986. Robustness: longer training 1945-1956 with selection 1957-1962; training with 0.26% one-way cost; a second experiment with training 1981-1984, selection 1985-1986, test 1987-2000.

**Data and costs.** DJIA total returns rebuilt from CRSP (value = price-weighted average of the 30 constituents' total returns) from July 1962; pre-1962 and 2000 from index levels plus summed dividends. Both BLL and AK used price-only series, which biases toward the rules because sell days forgo dividends (Bessembinder and Chan 1998). One-way cost $c = 0.13\%$, from Knez-Ready (1996) effective-spread estimates for DJIA stocks around 1990-91; likely too low for earlier decades, so favorable to the rules. Trades execute at the close on which the signal is observed.

**Excess returns** (log, per year; $I_b, I_s$ buy/sell-day indicators, $f_t$ T-bill rate, $n$ round trips, $T_b, T_s$ buy/sell day counts, $Y$ years):

$$ER_{100\%} = \frac{1}{Y}\Big[\sum_t r_t I_b(t) + \sum_t f_t I_s(t) + n\log\tfrac{1-c}{1+c} - \sum_t r_t\Big]$$

$$ER_{s/b} = \frac{1}{Y}\Big[\sum_t r_t I_b(t) + \sum_t f_t I_s(t) + n\log\tfrac{1-c}{1+c} - \tfrac{T_b}{T}\sum_t r_t - \tfrac{T_s}{T}\sum_t f_t\Big]$$

$ER_{100\%}$ penalizes any rule that is out of the market given a positive equity premium. $ER_{s/b}$ benchmarks against a constant-mix portfolio with the rule's average stock weight, isolating timing skill. Ready notes its flaws: the weights are chosen ex post (look-ahead), and a constant mix is not a feasible strategy; a rational investor prefers constant-mix to a zero-mean dynamic strategy (Dybvig 1988).

## Results

**BLL rules, buy-minus-sell daily return differences (Table II, annualized ×252):**

| Period | (1,150,1%) | (5,150,1%) | (1,200,1%) | (1,150,0%) |
|---|---|---|---|---|
| 1897-1986, no div. (BLL) | 17.6% (t=4.68) | 15.4% (4.05) | 17.6% (4.73) | 15.6% (4.40) |
| 1963-1986, with div. | 10.3% (1.85) | 5.0% (0.89) | 10.9% (1.94) | 14.3% (2.56) |
| 1987-2000, with div. | -16.4% (-1.53) | -12.3% (-1.15) | -20.8% (-1.83) | -10.0% (-0.93) |
| 1988-2000, with div. | -26.6% (-2.76) | -19.1% (-1.98) | -29.5% (-2.86) | -20.2% (-2.06) |

Adding dividends shaves roughly 0.5-1 pp off the 1963-86 spread. After 1986 the sign reverses: sell days beat buy days for all four rules. Cross-period t-stats for the change vs. 1963-86 are 1.55-2.71 (1987-2000) and 2.25-3.59 (1988-2000). The rules did avoid the 1987 crash; excluding 1987 makes the reversal worse.

**Trading performance (Table III).** 1963-1986: 1.0-3.4 trades/yr, ~60% buy days; $ER_{100\%}$ = 0.5% to 2.15%/yr, $ER_{s/b}$ = 1.2% to 2.9%/yr. 1987-2000: $ER_{100\%}$ from -4.95% to -5.9%, $ER_{s/b}$ from -2.6% to -3.9%; 1988-2000 worse still ($ER_{100\%}$ -6.5% to -8.1%).

**Instability within periods (Figure 2, (1,150,0%)).** Over 1939-1962 the rule's $ER_{100\%}$ was -1.9% (vs. +2.15% in 1963-86), and its buy-sell spread was 9.9% vs. 14.3%. Sub-period averages vary a lot: 14.4% annualized excess return from May 1973 to April 1975, against 2.15% for the whole of 1963-86. An investor who had lagged the market with this rule for the 24 years before 1963 would have had little reason to stick with it.

**AK rules vs. BLL (Table IV).**
- *1957-1962 (information available in 1963):* every one of the 50 AK rules beat the BLL (1,150,0%) rule on $ER_{100\%}$ (BLL 1.7%, AK average 3.7%, max 5.5%). 49 of 50 beat it on $ER_{s/b}$. A search on pre-1963 data would not have chosen the BLL rule.
- *1963-1986 test:* AK average $ER_{100\%}$ = 0.1% (range -3.5% to 3.1%) vs. BLL 2.2%; $ER_{s/b}$ AK average 0.8% vs. BLL 2.9%. The AK rules actually have a *larger* average buy-sell spread (22% annualized vs. 14%) but trade far more (average ~12, up to ~38 round trips/yr vs. 3.4), and costs eat the edge. So the out-of-sample failure is about profitable timing, not the absence of any signal.
- Across the 50 AK rules, the correlation between training/selection excess return and test-period excess return is 0.017: the few AK rules that matched BLL in 1963-86 could not have been identified beforehand.
- Longer training window (1945-1956 train, 1957-1962 select): stronger in-sample results, but the BLL rule beat all 50 AK rules in 1963-86. Training with 0.26% costs (to target slower patterns) gives similar results.

**1987-2000 (Table V).** AK rules trained on 1981-1986 did better than the BLL rules after 1987 but were still disappointing. Their ability to identify higher-return days did not persist.

**Implementation lag.** With a one-day execution delay, both the BLL and AK rules earn negative after-cost excess returns in both 1963-1986 and 1987-2000 (Bessembinder-Chan found the same for BLL through 1986). The truth for a real investor lies between the same-close and next-day assumptions.

## Interpretation

Ready's reading is that the evidence is consistent with the BLL 1963-86 profits being spurious, meaning data snooping by the community that popularized the rules. He is explicit that a **nonstationarity** alternative can't be ruled out: the pattern may have been real in 1963-86 only. AK tests persistence from pre-1963 data, so by construction it cannot tell "real but transient" apart from "spurious". Testing the transient hypothesis on 1963-86 data alone runs into the full-search problem that Sullivan, Timmermann and White (1999) handle with the bootstrap, and that universe is itself built from popular rules. A second alternative (footnote 16) is that BLL happens to be the optimal rule. In that case the post-1986 collapse is an even stronger statement about market efficiency, perhaps because statistical arbitrage "traded away" the pattern (Lo-MacKinlay). Low power cuts both ways: failing to reject no-predictability is not evidence against a temporary episode, and the GA's function set and window lengths are arbitrary, so the result covers only the rule population the algorithm can generate.

Relation to STW (1999): STW ask whether there is *any* predictability, net of data-snooping over a rule universe. Ready asks whether there is predictability large enough to trade after costs, using a search that is immune to hindsight by construction.

The paper opens and closes with corporate relevance. Firms timing shelf issues might use short-horizon forecasts even if they are not profitable after costs. Ready warns that the same snooping concern applies to "widely accepted" monthly predictors such as the dividend yield.

## Assessment

- **Convincing:** the out-of-period reversal is large and significant (1988-2000 spreads of -19% to -30% with |t| ~2-2.9). The ex ante GA benchmark is a clean way to test "discoverable in 1962", and the near-zero train/test correlation across 50 GA seeds is persuasive. Total-return data and realistic costs remove two known biases in favor of the rules.
- **Fragile:** it is a single index, and the "test" is a single 24-year window, so inference rests on a handful of regime shifts (e.g., 1973-75 drives much of the 1963-86 excess). GA performance depends on design choices, including training length, function set and early stopping, and the high turnover of the AK rules partly reflects the search overfitting noise, not the absence of a slow signal. The stock/bond benchmark has ex post weights. Costs are flat over 1957-2000, which is unrealistic in both directions.
- **Practical relevance:** a template for evaluating any published timing signal. Ask whether a pre-specified search on the pre-publication information set would have selected it, check the rank correlation between in-sample and out-of-sample performance across search seeds, and add a one-bar implementation lag. Daily MA timing on a large-cap index is shown to be at best a weak, regime-dependent signal whose after-cost value is fragile to small execution frictions.
